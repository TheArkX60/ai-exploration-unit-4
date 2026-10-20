"""stray Enter after a click, key auto-repeat, keyboard still works. Run: python tests/test_enter_focus.py   (see tests/README.md)"""
import json, time
from harness import *
def center(p, sel): return p.js(f"(()=>{{const r=document.querySelector('{sel}').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}})()")
def tap(p, kind, i): p.click(*center(p, f'.hotspot[data-kind={kind}][data-id="{i}"] .hit')); time.sleep(0.25)
def st(p): return json.loads(p.js("JSON.stringify({story:hollowApp.state().story, progress:hollowStory.progress(), focus:(document.activeElement&&(document.activeElement.getAttribute('aria-label')||document.activeElement.id))||'body'})"))
SPY = """(()=>{window.__cues=[];for(const k of ['tap','nope','tick','story']){const o=hollowCues[k];hollowCues[k]=function(...a){window.__cues.push(k+(a.length?'('+a.join(',')+')':''));return o.apply(this,a)}}})()"""
def cues(p): r = p.js("JSON.stringify(window.__cues)"); p.js("window.__cues=[]"); return json.loads(r)
def key(p, k, code, vk, repeat=False):
    for t in ("keyDown", "keyUp"):
        p.cmd("Input.dispatchKeyEvent", type=t, key=k, code=code, windowsVirtualKeyCode=vk, autoRepeat=(repeat and t == "keyDown"), text=("\r" if k == "Enter" and t == "keyDown" else ""))
try:
    p = Page(); p.cmd("Runtime.enable"); p.cmd("Page.enable")
    p.cmd("Emulation.setDeviceMetricsOverride", width=390, height=844, deviceScaleFactor=1, mobile=True)
    p.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html"); time.sleep(1.5)
    p.click(*center(p, "#enter")); time.sleep(1.0); p.js(SPY)
    print("A. click pumpkin 1 with the mouse, then press Enter:")
    tap(p, "pumpkin", 1); print("   after click :", st(p), cues(p))
    key(p, "Enter", "Enter", 13); time.sleep(0.25); print("   after Enter :", st(p), cues(p), "(was a wrong tap before the fix)")
    print("B. finish with the mouse (2,3,4), press Enter during and after the story:")
    for i in (2, 3, 4): tap(p, "pumpkin", i)
    print("   after 4th   :", st(p), cues(p))
    key(p, "Enter", "Enter", 13); time.sleep(0.25); print("   Enter during story:", st(p), cues(p))
    t0 = time.time()
    while st(p)["story"] and time.time() - t0 < 12: time.sleep(0.1)
    key(p, "Enter", "Enter", 13); time.sleep(0.25); print("   Enter after story :", st(p), cues(p))
    print("C. keyboard still works, and holding Enter counts once:")
    p.js("document.getElementById('stage').focus()")
    for n in range(12):
        key(p, "Tab", "Tab", 9)
        if (p.js("document.activeElement.getAttribute('aria-label')") or "").startswith("Pumpkin 1"): break
    key(p, "Enter", "Enter", 13); key(p, "Enter", "Enter", 13, repeat=True); key(p, "Enter", "Enter", 13, repeat=True); time.sleep(0.25)
    print("   Enter + two auto-repeats on pumpkin 1:", st(p), cues(p))
    for i in (2, 3, 4):
        key(p, "Tab", "Tab", 9); key(p, "Enter" if i % 2 else " ", "Enter" if i % 2 else "Space", 13 if i % 2 else 32); time.sleep(0.25)
    print("   after keys on 2,3,4:", st(p), cues(p))
    print("D. Space also ignores auto-repeat; Tab key position kept after a keyboard tap:", )
finally:
    chrome.terminate(); server.terminate()
