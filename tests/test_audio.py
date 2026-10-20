"""ambient sound: starts at Enter, continuous, Pause/Play, blocked files, reduced motion. Run: python tests/test_audio.py   (see tests/README.md)"""
import json, time
from harness import *
ST = "JSON.stringify(hollowAudio.status())"
def enter(p):
    box = p.js("(()=>{const r=document.getElementById('enter').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()")
    p.click(*box)
try:
    # ---------- 1. normal run ----------
    p = Page(); p.cmd("Runtime.enable"); p.cmd("Page.enable"); p.cmd("Log.enable")
    p.cmd("Emulation.setDeviceMetricsOverride", width=390, height=844, deviceScaleFactor=1, mobile=True)
    p.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html"); time.sleep(1.5)
    print("before Enter:", p.js(ST), "| sound note hidden:", p.js("document.getElementById('sound-note').hidden"))
    enter(p); time.sleep(1.5)
    print("after Enter :", p.js(ST))
    t0 = time.time(); levels = []
    while time.time() - t0 < 40:
        levels.append((round(time.time() - t0, 1), round(p.js("hollowAudio.levelDb()"), 1))); time.sleep(0.5)
    print("final:", p.js(ST))
    vals = [l for _, l in levels]
    quiet = [t for t, l in levels if l < -70]
    print(f"level over 40 s: min {min(vals)} dB, median {sorted(vals)[len(vals)//2]} dB, max {max(vals)} dB | samples below -70 dB (silence): {len(quiet)} of {len(vals)}")
    print("level every ~4 s:", [l for _, l in levels[::8]])
    # ---------- 2. pause / resume ----------
    s1 = json.loads(p.js(ST)); p.js("document.getElementById('toggle').click()"); time.sleep(0.4)
    s2 = json.loads(p.js(ST)); time.sleep(2.0); s3 = json.loads(p.js(ST))
    print(f"paused: state={s3['state']} | clock frozen: {s2['time']==s3['time']} | no new gusts/hoots: {(s2['gusts'],s2['hoots'])==(s3['gusts'],s3['hoots'])}")
    p.js("document.getElementById('toggle').click()"); time.sleep(2.0); s4 = json.loads(p.js(ST))
    print(f"resumed: state={s4['state']} | clock advancing: {s4['time']>s3['time']}")
    print("exceptions:", len([m for m in p.logs if m.get('method')=='Runtime.exceptionThrown']))

    # ---------- 3. audio files blocked (F4) ----------
    p2 = Page(); p2.cmd("Runtime.enable"); p2.cmd("Page.enable"); p2.cmd("Network.enable")
    p2.cmd("Network.setBlockedURLs", urls=["*assets/audio/*"])
    p2.cmd("Emulation.setDeviceMetricsOverride", width=390, height=844, deviceScaleFactor=1, mobile=True)
    p2.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html"); time.sleep(1.5)
    enter(p2); time.sleep(1.5)
    print("BLOCKED files -> note visible:", not p2.js("document.getElementById('sound-note').hidden"), "| phase:", p2.js("document.documentElement.dataset.phase"))
    box = p2.js("(()=>{const r=document.querySelector('[data-kind=\"pumpkin\"][data-id=\"1\"] .hit').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()")
    p2.click(*box); time.sleep(0.2)
    print("scene still works (pumpkin 1 shows progress):", p2.js("document.querySelector('[data-kind=\"pumpkin\"][data-id=\"1\"]').classList.contains('progress')"))
    p2.js("document.getElementById('toggle').click()"); time.sleep(0.3)
    print("Pause still works with no audio:", p2.js("document.documentElement.dataset.phase"))
    p2.shot("audio-blocked-note")
    # ---------- 4. reduced motion does not silence audio ----------
    p3 = Page(); p3.cmd("Runtime.enable"); p3.cmd("Page.enable")
    p3.cmd("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "reduce"}])
    p3.cmd("Emulation.setDeviceMetricsOverride", width=390, height=844, deviceScaleFactor=1, mobile=True)
    p3.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html"); time.sleep(1.5)
    enter(p3); time.sleep(3)
    print("reduced motion ->", p3.js(ST), "| level dB:", round(p3.js("hollowAudio.levelDb()"), 1))
finally:
    chrome.terminate(); server.terminate()
