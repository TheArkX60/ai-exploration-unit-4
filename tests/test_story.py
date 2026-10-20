"""story length, replay x3, tap lock, Pause mid-story, sound level, reduced motion. Run: python tests/test_story.py   (see tests/README.md)"""
import json, time
from harness import *
def click_sel(p, sel):
    box = p.js(f"(()=>{{const r=document.querySelector('{sel}').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}})()"); p.click(*box)
def app(p): return json.loads(p.js("JSON.stringify(hollowApp.state())"))
SNAP = """(()=>{const g=e=>getComputedStyle(document.querySelector(e));
  return JSON.stringify({ghost:g('.s-ghost-rise').transform, lid:g('.s-lid').opacity, glow:g('.s-glow').opacity, face:g('.s-face').opacity, open:g('.s-opening').opacity, puff:g('.s-puff').opacity});})()"""
def freeze_at(p, T):
    p.js(f"document.getAnimations().forEach(a=>{{ if((a.animationName||'').startsWith('s-')) {{ a.pause(); a.currentTime={int(T*1000)}; }} }})")
try:
    # ---------- normal motion ----------
    p = Page(); p.cmd("Runtime.enable"); p.cmd("Page.enable"); p.cmd("Log.enable")
    p.cmd("Emulation.setDeviceMetricsOverride", width=390, height=844, deviceScaleFactor=1, mobile=True)
    p.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html"); time.sleep(1.5)
    print("before Enter: play() returns", p.js("hollowStory.play('pumpkins')"), "(should be False)")
    click_sel(p, "#enter"); time.sleep(1.0)
    base = p.js(SNAP); print("idle look:", base)
    # --- duration, tap lock, replay x3 ---
    for n in (1, 2, 3):
        t0 = time.time(); ok = p.js("hollowStory.play('pumpkins')"); time.sleep(0.5)
        # taps during the story must be ignored
        click_sel(p, '[data-kind=pumpkin][data-id="2"] .hit'); time.sleep(0.1)
        lit_during = p.js("document.querySelector('[data-kind=\"pumpkin\"][data-id=\"2\"]').classList.contains('lit')")
        second = p.js("hollowStory.play('pumpkins')")
        while app(p)["story"] and time.time() - t0 < 12: time.sleep(0.05)
        dur = round(time.time() - t0, 2)
        time.sleep(0.2)
        print(f"run {n}: started={ok} | lasted {dur}s | tap during story lit pumpkin: {lit_during} | second play() while playing: {second} | after: story={app(p)['story']}, look restored: {p.js(SNAP) == base}")
    # --- pause mid-story ---
    p.js("hollowStory.play('pumpkins')"); time.sleep(3.2)
    p.js("document.getElementById('toggle').click()"); time.sleep(0.3)
    a = p.js(SNAP); au = json.loads(p.js("JSON.stringify(hollowAudio.status())")); time.sleep(1.5); b = p.js(SNAP); au2 = json.loads(p.js("JSON.stringify(hollowAudio.status())"))
    print("paused mid-story: frozen:", a == b, "| audio:", au2["state"], "clock frozen:", au["time"] == au2["time"], "| story still set:", app(p)["story"], "| phase:", app(p)["phase"])
    click_sel(p, '[data-kind=pumpkin][data-id="3"] .hit'); time.sleep(0.1)
    print("  tap while paused ignored:", not p.js("document.querySelector('[data-kind=\"pumpkin\"][data-id=\"3\"]').classList.contains('lit')"))
    t1 = time.time(); p.js("document.getElementById('toggle').click()")
    while app(p)["story"] and time.time() - t1 < 12: time.sleep(0.05)
    print(f"  resumed: finished after {round(time.time()-t1,2)} s more (expected about 4.8) | story={app(p)['story']}, phase={app(p)['phase']}")
    # --- audio during the story: level above the ambient floor around the pop ---
    p.js("hollowStory.play('pumpkins')"); lv = []; t0 = time.time()
    while time.time() - t0 < 8.5: lv.append((round(time.time()-t0,1), round(p.js("hollowAudio.levelDb()"),1))); time.sleep(0.1)
    peak = max(lv, key=lambda x: x[1]); print("audio level during story: peak", peak[1], "dB at", peak[0], "s | at pop (2.8-3.0 s):", max(l for t,l in lv if 2.8 <= t <= 3.1), "dB")
    print("exceptions:", len([m for m in p.logs if m.get('method')=='Runtime.exceptionThrown']))

    # ---------- reduced motion ----------
    p2 = Page(); p2.cmd("Runtime.enable"); p2.cmd("Page.enable")
    p2.cmd("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "reduce"}])
    p2.cmd("Emulation.setDeviceMetricsOverride", width=390, height=844, deviceScaleFactor=1, mobile=True)
    p2.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html"); time.sleep(1.5)
    click_sel(p2, "#enter"); time.sleep(1.0)
    p2.js("hollowStory.play('pumpkins')"); time.sleep(0.2)
    anims = p2.js("[...new Set(document.getAnimations().map(a=>a.animationName).filter(n=>n&&(n.startsWith('s-'))))]")
    movers = p2.js("(()=>{const bad=[];for(const sel of ['.pumpkin','.s-lid','.s-ghost-wobble']){const n=getComputedStyle(document.querySelector(sel)).animationName;if(n!=='none')bad.push(sel+':'+n)}return bad})()")
    print("reduced motion: animations", anims, "| movement animations still on:", movers)
    ghost_t = []
    for T in (1.0, 3.0, 3.9, 4.5, 6.5):
        freeze_at(p2, T); time.sleep(0.1); ghost_t.append((T, p2.js("getComputedStyle(document.querySelector('.s-ghost-rise')).opacity"), p2.js("getComputedStyle(document.querySelector('.s-ghost-rise')).transform")))
    print("  ghost (time, opacity, transform):", ghost_t)
    p2.js("document.getAnimations().forEach(a=>a.play())")
    t0 = time.time()
    while app(p2)["story"] and time.time() - t0 < 12: time.sleep(0.05)
    print(f"  reduced-motion story ended after {round(time.time()-t0,2)} s more | story={app(p2)['story']}")
finally:
    chrome.terminate(); server.terminate()

