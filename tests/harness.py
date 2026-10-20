"""Shared test harness for Hollow Hill. Importing this module starts what the tests need:

  - a small web server for a temporary COPY of the project (so OneDrive file locks cannot stall it, and the
    real project folder is never touched), on port 8777;
  - a headless Chrome with remote debugging on port 9333.

Each test script does `from harness import *`, drives the page through the `Page` class (real mouse clicks,
real key events, JavaScript evaluation, screenshots), prints what it measured, and in its `finally:` block calls
chrome.terminate() and server.terminate(). See README.md.
"""
import atexit, base64, json, os, shutil, subprocess, sys, tempfile, time, urllib.request

try:
    import websocket
except ImportError:
    sys.exit("This needs the websocket-client package:  python -m pip install websocket-client")

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "output")                  # screenshots and other files tests write (git-ignored)
os.makedirs(OUT, exist_ok=True)
PORT = 8777                                         # the page; serve.bat uses 8765, so both can run together
DEBUG_PORT = 9333                                   # Chrome's remote-debugging port
BASE = f"http://127.0.0.1:{PORT}/"


def find_chrome():
    candidates = [
        os.environ.get("HOLLOW_CHROME", ""),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        "/usr/bin/google-chrome", "/usr/bin/chromium", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    for c in candidates:
        if c and os.path.exists(c):
            return c
    for name in ("chrome", "google-chrome", "chromium", "msedge"):
        found = shutil.which(name)
        if found:
            return found
    sys.exit("Chrome or Edge was not found. Set the HOLLOW_CHROME environment variable to its full path.")


# ---- Serve a temporary copy of the project ----
_site = tempfile.mkdtemp(prefix="hollowhill-site-")
_profile = tempfile.mkdtemp(prefix="hollowhill-chrome-")
shutil.copytree(PROJECT_ROOT, os.path.join(_site, "site"),
                ignore=shutil.ignore_patterns(".git", "tests", "screenshots", "transcripts", "reference", "__pycache__"))
SITE = os.path.join(_site, "site")

server = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                          cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
chrome = subprocess.Popen([find_chrome(), "--headless=new", f"--remote-debugging-port={DEBUG_PORT}",
                           f"--user-data-dir={_profile}", "--no-first-run", "--hide-scrollbars", "about:blank"],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _cleanup():
    for proc in (chrome, server):
        try:
            proc.terminate()
        except Exception:
            pass
    time.sleep(0.5)
    shutil.rmtree(_site, ignore_errors=True)
    shutil.rmtree(_profile, ignore_errors=True)


atexit.register(_cleanup)

# Wait until Chrome answers instead of sleeping a fixed time
for _ in range(60):
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{DEBUG_PORT}/json", timeout=1).read()
        break
    except Exception:
        time.sleep(0.25)
else:
    sys.exit("Chrome did not start (is another test or browser using port 9333?).")


class Page:
    """One connection to Chrome's first tab. Several Page objects share that tab (each new one starts fresh)."""

    def __init__(self):
        tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{DEBUG_PORT}/json"))
        tab = [t for t in tabs if t["type"] == "page"][0]
        self.ws = websocket.create_connection(tab["webSocketDebuggerUrl"], max_size=None, suppress_origin=True)
        self.n = 0
        self.logs = []                               # console messages, exceptions and log entries seen so far
        self.cmd("Network.enable")
        self.cmd("Network.setCacheDisabled", cacheDisabled=True)   # a cached old file once fooled us

    def cmd(self, method, **params):
        self.n += 1
        self.ws.send(json.dumps({"id": self.n, "method": method, "params": params}))
        while True:
            m = json.loads(self.ws.recv())
            if m.get("id") == self.n:
                return m.get("result", m)
            if m.get("method") in ("Runtime.consoleAPICalled", "Runtime.exceptionThrown", "Log.entryAdded"):
                self.logs.append(m)

    def js(self, expr):
        r = self.cmd("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=True)
        return r.get("result", {}).get("value")

    def shot(self, name):
        r = self.cmd("Page.captureScreenshot", format="png")
        with open(os.path.join(OUT, name + ".png"), "wb") as f:
            f.write(base64.b64decode(r["data"]))

    def key(self, key, code, vk):
        """A real key press (down and up). Space is key ' '; Enter is 'Enter'."""
        for t in ("keyDown", "keyUp"):
            self.cmd("Input.dispatchKeyEvent", type=t, key=key, code=code, windowsVirtualKeyCode=vk,
                     text=" " if key == " " and t == "keyDown" else ("\r" if key == "Enter" and t == "keyDown" else ""))

    def click(self, x, y):
        """A real mouse click at page coordinates (browsers only allow sound after a genuine gesture)."""
        for t in ("mousePressed", "mouseReleased"):
            self.cmd("Input.dispatchMouseEvent", type=t, x=x, y=y, button="left", clickCount=1)
