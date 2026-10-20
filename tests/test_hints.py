"""hint timing 15/30/45 s (real time), resets, Pause, story, fit at 360 px. Run: python tests/test_hints.py   (see tests/README.md)"""
import base64, json, time
from harness import *
def center(p, sel): return p.js(f"(()=>{{const r=document.querySelector('{sel}').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}})()")
def hint(p): return json.loads(p.js("JSON.stringify({level:hollowHints.level(), hidden:document.getElementById('hint').hidden, text:document.getElementById('hint').textContent, idle:+hollowHints.idle().toFixed(1)})"))
def fresh(w=390, h=844, reduced=False, dsf=1):
    p = Page(); p.cmd("Runtime.enable"); p.cmd("Page.enable"); p.cmd("Log.enable")
    p.cmd("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "reduce" if reduced else "no-preference"}])
    p.cmd("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=dsf, mobile=True)
    p.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html"); time.sleep(1.5)
    p.click(*center(p, "#enter")); return p
def tap_pumpkin(p, i): p.click(*center(p, f'.hotspot[data-kind=pumpkin][data-id="{i}"] .hit')); time.sleep(0.2)
try:
    # ---------- A. real timeline ----------
    p = fresh(); t0 = time.time(); seen = []; last = ""
    while time.time() - t0 < 52:
        h = hint(p)
        if h["text"] != last: seen.append((round(time.time() - t0, 1), h["level"], h["text"])); last = h["text"]
        time.sleep(0.25)
    print("A. hints appeared at:", seen); print("   still showing at 52 s:", hint(p))
    # ---------- B. rules with shortened timers ----------
    p.js("hollowHints.times.splice(0,3,2,4,6)")
    # reset by a tap on empty sky (real click)
    p.click(200, 120); time.sleep(0.3); print("B1. after tapping empty sky:", hint(p))
    time.sleep(2.6); print("    2.6 s later (level 1 again):", hint(p)["level"], "| 4.6 s:", end=" "); time.sleep(2.0); print(hint(p)["level"], "| 7 s:", end=" "); time.sleep(2.4); print(hint(p)["level"])
    # reset by hotspot tap (a tombstone) and by keyboard
    tap_pumpkin(p, 3); print("B2. after tapping a wrong pumpkin (hotspot):", hint(p)["level"], hint(p)["idle"])
    time.sleep(7); print("    reached level", hint(p)["level"])
    p.js("document.getElementById('stage').focus()")
    for n in range(12):
        p.key("Tab", "Tab", 9)
        if (p.js("document.activeElement.getAttribute('aria-label')") or "").startswith("Window 1"): break
    p.key("Enter", "Enter", 13); time.sleep(0.3); print("B3. after keyboard Enter on a window:", hint(p)["level"], hint(p)["idle"])
    # Pause freezes the clock
    time.sleep(2.5); before = hint(p); p.js("document.getElementById('toggle').click()"); time.sleep(8); mid = hint(p)
    print(f"B4. paused: idle {before['idle']} -> {mid['idle']} after 8 s paused (should not advance) | level {before['level']} -> {mid['level']}")
    p.js("document.getElementById('toggle').click()"); time.sleep(1.2); print("    after Play, 1.2 s:", hint(p))
    # Story hides the hint and restarts the clock at 0
    p.js("hollowHints.times.splice(0,3,2,4,6)"); time.sleep(6.5); print("B5. level before story:", hint(p)["level"])
    for i in (1, 2, 3, 4): tap_pumpkin(p, i)
    time.sleep(0.5); print("    during story:", hint(p))
    t1 = time.time()
    while json.loads(p.js("JSON.stringify(hollowApp.state())"))["story"] and time.time() - t1 < 12: time.sleep(0.05)
    time.sleep(0.3); print("    just after story:", hint(p)); time.sleep(2.4); print("    2.4 s after story (level 1 expected):", hint(p)["level"])
    print("exceptions:", len([m for m in p.logs if m.get('method')=='Runtime.exceptionThrown']))
    # ---------- C. reduced motion and fade ----------
    q = fresh(reduced=True); q.js("hollowHints.times.splice(0,3,1,2,3)"); time.sleep(1.8)
    print("C. reduced motion hint animation:", q.js("getComputedStyle(document.getElementById('hint')).animationName"))
    r = fresh(); r.js("hollowHints.times.splice(0,3,1,2,3)"); time.sleep(1.5); print("   normal hint animation:", r.js("getComputedStyle(document.getElementById('hint')).animationName"), "| font:", r.js("getComputedStyle(document.getElementById('hint')).fontSize"))
    # ---------- D. each line fits on one line at 360 px ----------
    s = fresh(360, 640, dsf=2)
    for key in ("pumpkinsOnly", "allStories"):
        for i, txt in enumerate(json.loads(s.js("JSON.stringify(hollowHints.wording)"))[key]):
            s.js(f"(()=>{{const h=document.getElementById('hint');h.hidden=false;h.textContent={json.dumps(txt)};}})()")
            m = json.loads(s.js("JSON.stringify((()=>{const h=document.getElementById('hint');return {scrollW:h.scrollWidth, clientW:h.clientWidth, h:h.getBoundingClientRect().height}})())"))
            print(f"D. {key} level {i+1}: {len(txt)} chars | fits: {m['scrollW'] <= m['clientW']} (text {m['scrollW']} px of {m['clientW']} px) | height {round(m['h'])} px")
            if key == "pumpkinsOnly" and i == 2:
                rr = s.cmd("Page.captureScreenshot", format="png", clip={"x": 0, "y": 0, "width": 360, "height": 150, "scale": 2}); open(os.path.join(OUT, "hint-level3.png"), "wb").write(base64.b64decode(rr["data"]))
finally:
    chrome.terminate(); server.terminate()
