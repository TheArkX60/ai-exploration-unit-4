"""the closing fade of that note freezes on Pause. Run: python tests/test_story_note_pause.py   (see tests/README.md)"""
import json, time
from harness import *
def center(p, sel): return p.js(f"(()=>{{const r=document.querySelector('{sel}').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}})()")
def app(p): return json.loads(p.js("JSON.stringify(hollowApp.state())"))
OP = "[getComputedStyle(document.getElementById('story-note')).opacity, document.getElementById('story-note').hidden, getComputedStyle(document.getElementById('story-note')).animationPlayState]"
try:
    for reduced in (False, True):
        p = Page(); p.cmd("Runtime.enable"); p.cmd("Page.enable")
        p.cmd("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "reduce" if reduced else "no-preference"}])
        p.cmd("Emulation.setDeviceMetricsOverride", width=390, height=844, deviceScaleFactor=1, mobile=True)
        p.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html"); time.sleep(1.5)
        p.click(*center(p, "#enter")); time.sleep(1.0)
        p.js("hollowStory.play('pumpkins')")
        t0 = time.time()
        while app(p)["story"] and time.time() - t0 < 12: time.sleep(0.05)
        time.sleep(1.9)                                  # into the closing fade (fade starts at 1.6 s)
        p.js("document.getElementById('toggle').click()"); time.sleep(0.2)
        a = p.js(OP); time.sleep(2.5); b = p.js(OP)
        print(f"reduced={reduced}: paused during the closing fade -> {a} then 2.5 s later {b} | frozen: {a == b}")
        p.js("document.getElementById('toggle').click()"); time.sleep(1.5); print("   after Play, 1.5 s later:", p.js(OP))
finally:
    chrome.terminate(); server.terminate()
