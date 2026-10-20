"""fog drifts, Pause, reduced motion, taps pass through. Run: python tests/test_fog.py   (see tests/README.md)"""
import base64
from harness import *
TX = "(()=>[...document.querySelectorAll('.fog')].map(e=>getComputedStyle(e).transform))()"
def st(): return p.js("[...document.querySelectorAll('.fog')].map(e=>getComputedStyle(e).animationName+'/'+getComputedStyle(e).animationPlayState)")
try:
    for reduced in (False, True):
        p = Page(); p.cmd("Runtime.enable"); p.cmd("Page.enable"); p.cmd("Log.enable")
        p.cmd("Emulation.setDeviceMetricsOverride", width=390, height=844, deviceScaleFactor=2, mobile=True)
        p.cmd("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "reduce" if reduced else "no-preference"}])
        p.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html"); time.sleep(1.0)
        p.js("document.getElementById('enter').click()"); time.sleep(0.3)
        print("== reduced:", reduced, st())
        a = p.js(TX); time.sleep(3); b = p.js(TX)
        print("moves over 3s:", a != b, "\n  t0:", a, "\n  t1:", b)
        p.js("document.getElementById('toggle').click()"); time.sleep(0.2)
        c = p.js(TX); time.sleep(1.5); d = p.js(TX)
        print("paused frozen:", c == d)
        p.js("document.getElementById('toggle').click()")
        # taps still reach pumpkins/tombstones/windows beneath fog (fog must not block)
        for kind, i in (("pumpkin", 1), ("pumpkin", 4), ("tombstone", 2), ("window", 1)):
            box = p.js(f"(()=>{{const r=document.querySelector('[data-kind=\"{kind}\"][data-id=\"{i}\"] .hit').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}})()")
            p.click(*box); time.sleep(0.15)
            print(f"tap {kind} {i}: lit =", p.js(f"document.querySelector('[data-kind=\"{kind}\"][data-id=\"{i}\"]').classList.contains('lit')"))
        print("exceptions:", len([m for m in p.logs if m.get('method')=='Runtime.exceptionThrown']))
        if not reduced:
            r = p.cmd("Page.captureScreenshot", format="png"); open(os.path.join(OUT, "fog-390x844.png"), "wb").write(base64.b64decode(r["data"]))
            p.js("document.documentElement.style.cssText=''")
finally:
    chrome.terminate(); server.terminate()
