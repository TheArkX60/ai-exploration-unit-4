"""pumpkin sequence: tones, lights, nope, repeats, other objects, timeout, Pause, keyboard, reduced motion. Run: python tests/test_triggers.py   (see tests/README.md)"""
import json, time
from harness import *
def center(p, sel):
    return p.js(f"(()=>{{const r=document.querySelector('{sel}').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}})()")
def tap(p, kind, i):
    p.click(*center(p, f'.hotspot[data-kind={kind}][data-id="{i}"] .hit')); time.sleep(0.25)
def st(p): return json.loads(p.js("JSON.stringify({story:hollowApp.state().story, phase:hollowApp.state().phase, progress:hollowStory.progress(), lit:[...document.querySelectorAll('.hotspot[data-kind=pumpkin]')].map(e=>e.classList.contains('progress')?1:0).join('')})"))
SPY = """(()=>{window.__cues=[];for(const k of ['tap','nope','tick','story']){const o=hollowCues[k];hollowCues[k]=function(...a){window.__cues.push(k+(a.length?'('+a.join(',')+')':''));return o.apply(this,a)}}})()"""
def cues(p): 
    r = p.js("JSON.stringify(window.__cues)"); p.js("window.__cues=[]"); return json.loads(r)
def fresh(reduced=False):
    p = Page(); p.cmd("Runtime.enable"); p.cmd("Page.enable"); p.cmd("Log.enable")
    p.cmd("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "reduce" if reduced else "no-preference"}])
    p.cmd("Emulation.setDeviceMetricsOverride", width=390, height=844, deviceScaleFactor=1, mobile=True)
    p.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html"); time.sleep(1.5)
    p.click(*center(p, "#enter")); time.sleep(1.0); p.js(SPY); return p
try:
    p = fresh()
    print("1. correct order 1-4:")
    for i in (1, 2, 3):
        tap(p, "pumpkin", i); print(f"   tapped {i}: {st(p)} cues {cues(p)}")
    tap(p, "pumpkin", 4); print(f"   tapped 4: {st(p)} cues {cues(p)}")
    t0 = time.time()
    while st(p)["story"] and time.time() - t0 < 12: time.sleep(0.1)
    print(f"   story lasted ~{round(time.time()-t0+0.25,1)} s, then {st(p)}")
    print("2. wrong order (1, 3):")
    tap(p, "pumpkin", 1); tap(p, "pumpkin", 3); s = st(p)
    print(f"   {s} cues {cues(p)} | tapped pumpkin has 'nope': {p.js('document.querySelector(\".hotspot[data-kind=pumpkin][data-id=\\\"3\\\"]\").classList.contains(\"nope\")')} | anim: {p.js('getComputedStyle(document.querySelector(\".hotspot[data-kind=pumpkin][data-id=\\\"3\\\"] .pumpkin\")).animationName')}")
    time.sleep(0.6); print("   nope class removed after wobble:", not p.js('document.querySelector(\".hotspot[data-kind=pumpkin][data-id=\\\"3\\\"]\").classList.contains(\"nope\")'))
    print("3. repeat the same pumpkin (1, 1):"); tap(p, "pumpkin", 1); tap(p, "pumpkin", 1); print(f"   {st(p)} cues {cues(p)}")
    print("4. other objects mid-sequence (1, tombstone, window, 2):")
    tap(p, "pumpkin", 1); tap(p, "tombstone", 2); tap(p, "window", 1); tap(p, "pumpkin", 2); print(f"   {st(p)} cues {cues(p)}")
    tap(p, "pumpkin", 4); cues(p)    # wrong (expects 3) -> reset
    print("5. timeout: tap 1,2 then wait 8.6 s")
    tap(p, "pumpkin", 1); tap(p, "pumpkin", 2); print("   before:", st(p)); time.sleep(7.0); print("   at 7 s:", st(p)); time.sleep(1.8); print("   at 8.8 s:", st(p))
    print("6. timeout freezes during Pause: tap 1,2, Pause 10 s, resume")
    tap(p, "pumpkin", 1); tap(p, "pumpkin", 2); time.sleep(3)
    p.js("document.getElementById('toggle').click()"); time.sleep(10); print("   after 10 s paused:", st(p))
    tap(p, "pumpkin", 3); print("   tap while paused ignored:", st(p)["progress"] == 2)
    p.js("document.getElementById('toggle').click()"); time.sleep(3); print("   3 s after resume (should still be alive):", st(p)); time.sleep(3.5); print("   6.5 s after resume (3+3.5 idle... ~8 reached):", st(p))
    print("7. keyboard: Tab/Enter/Space through 1-4")
    p.js("document.getElementById('stage').focus()")
    order = []
    for n in range(12):
        p.key("Tab", "Tab", 9); lab = p.js("document.activeElement.getAttribute('aria-label')")
        if lab and lab.startswith("Pumpkin 1"): break
    print("   focused:", lab)
    for i in range(1, 5):
        p.key("Enter" if i % 2 else " ", "Enter" if i % 2 else "Space", 13 if i % 2 else 32); time.sleep(0.25); print(f"   key on pumpkin {i}: progress {st(p)['progress']} story {st(p)['story']} cues {cues(p)}")
        if i < 4: p.key("Tab", "Tab", 9); time.sleep(0.1)
    t0 = time.time()
    while st(p)["story"] and time.time() - t0 < 12: time.sleep(0.1)
    print("   story done:", st(p))
    print("exceptions:", len([m for m in p.logs if m.get('method')=='Runtime.exceptionThrown']))
    # reduced motion
    q = fresh(reduced=True)
    tap(q, "pumpkin", 1); tap(q, "pumpkin", 3)
    print("8. reduced motion, wrong tap: animation =", q.js('getComputedStyle(document.querySelector(".hotspot[data-kind=pumpkin][data-id=\\"3\\"] .pumpkin")).animationName'), "| cues", cues(q))
finally:
    chrome.terminate(); server.terminate()
