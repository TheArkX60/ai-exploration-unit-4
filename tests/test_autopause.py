"""switching tabs auto-pauses; stays paused until Play. Run: python tests/test_autopause.py   (see tests/README.md)"""
import json, time, urllib.request
from harness import *
ST = "JSON.stringify(hollowAudio.status())"
def phase(p): return p.js("document.documentElement.dataset.phase")
try:
    p = Page(); p.cmd("Runtime.enable"); p.cmd("Page.enable")
    tabs = json.load(urllib.request.urlopen("http://127.0.0.1:9333/json")); first_id = [t for t in tabs if t["type"] == "page"][0]["id"]
    p.cmd("Emulation.setDeviceMetricsOverride", width=390, height=844, deviceScaleFactor=1, mobile=True)
    p.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html"); time.sleep(1.5)
    box = p.js("(()=>{const r=document.getElementById('enter').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()"); p.click(*box); time.sleep(3)
    print("running:", phase(p), json.loads(p.js(ST))["state"], "| hidden:", p.js("document.hidden"))
    # open a second tab and bring it to the front: the first tab becomes hidden
    urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:9333/json/new?about:blank", method="PUT")).read(); time.sleep(1.0)
    print("after switching tabs -> hidden:", p.js("document.hidden"), "| phase:", phase(p), "| audio:", json.loads(p.js(ST))["state"], "| Pause button reads:", p.js("document.getElementById('toggle').textContent"))
    time.sleep(2); a = json.loads(p.js(ST)); time.sleep(1.5); b = json.loads(p.js(ST)); print("  audio clock frozen while hidden:", a["time"] == b["time"])
    urllib.request.urlopen("http://127.0.0.1:9333/json/activate/" + first_id).read(); time.sleep(1.0)
    print("back on the tab -> hidden:", p.js("document.hidden"), "| phase (should STAY paused):", phase(p), "| audio:", json.loads(p.js(ST))["state"])
    box = p.js("(()=>{const r=document.getElementById('toggle').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()"); p.click(*box); time.sleep(2)
    s = json.loads(p.js(ST)); print("after tapping Play -> phase:", phase(p), "| audio:", s["state"], "| clock advancing:", s["time"] > b["time"])
finally:
    chrome.terminate(); server.terminate()
