"""'A story is playing' / 'Your turn' note. Run: python tests/test_story_note.py   (see tests/README.md)"""
import base64, json, time
from harness import *
def center(p, sel): return p.js(f"(()=>{{const r=document.querySelector('{sel}').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}})()")
def tap(p, kind, i): p.click(*center(p, f'.hotspot[data-kind={kind}][data-id="{i}"] .hit')); time.sleep(0.25)
NOTE = "JSON.stringify({hidden:document.getElementById('story-note').hidden, text:document.getElementById('story-note').textContent, state:document.getElementById('story-note').dataset.state, opacity:getComputedStyle(document.getElementById('story-note')).opacity, size:getComputedStyle(document.getElementById('story-note')).fontSize})"
def note(p): return json.loads(p.js(NOTE))
def app(p): return json.loads(p.js("JSON.stringify(hollowApp.state())"))
def shot(p, name):
    r = p.cmd("Page.captureScreenshot", format="png", clip={"x": 0, "y": 0, "width": 390, "height": 200, "scale": 2}); open(os.path.join(OUT, name + ".png"), "wb").write(base64.b64decode(r["data"]))
try:
    p = Page(); p.cmd("Runtime.enable"); p.cmd("Page.enable"); p.cmd("Log.enable")
    p.cmd("Emulation.setDeviceMetricsOverride", width=390, height=844, deviceScaleFactor=2, mobile=True)
    p.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html"); time.sleep(1.5)
    p.click(*center(p, "#enter")); time.sleep(1.0)
    print("idle:", note(p))
    for i in (1, 2, 3, 4): tap(p, "pumpkin", i)
    time.sleep(0.5); print("during story (0.7 s):", note(p)); shot(p, "story-note-playing")
    # Pause mid-story: the note stays
    time.sleep(2); p.js("document.getElementById('toggle').click()"); time.sleep(0.5); print("paused mid-story:", note(p), "| story still set:", app(p)["story"])
    p.js("document.getElementById('toggle').click()")
    t0 = time.time()
    while app(p)["story"] and time.time() - t0 < 12: time.sleep(0.05)
    time.sleep(0.4); print("just after story ends:", note(p), "| story:", app(p)["story"]); shot(p, "story-note-done")
    # control is back immediately: a tap works while the "done" note still shows
    tap(p, "pumpkin", 1); print("tap right after the story works:", app(p)["story"] is None and json.loads(p.js("JSON.stringify(hollowStory.progress())")) == 1)
    time.sleep(2.6); print("2.6 s later:", note(p))
    # replay while the done-note is showing: playing state must take over cleanly
    for i in (2, 3, 4): tap(p, "pumpkin", i)   # progress was 1 (from the tap above) -> wrong, resets; so do a full sequence
    p.js("hollowStory.progress()")
    for i in (1, 2, 3, 4): tap(p, "pumpkin", i)
    time.sleep(0.5); print("second run, during story:", note(p))
    print("exceptions:", len([m for m in p.logs if m.get('method')=='Runtime.exceptionThrown']))
finally:
    chrome.terminate(); server.terminate()
