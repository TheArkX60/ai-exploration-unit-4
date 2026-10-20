"""pumpkin faces shake together with the pumpkins. Run: python tests/test_face_shake.py   (see tests/README.md)"""
import base64, json, time
from harness import *
BOX = """(()=>{const out=[];const faces=[...document.querySelectorAll('.s-face')];const pumps=[...document.querySelectorAll('.pumpkin ellipse')];
  faces.forEach((f,i)=>{const a=f.getBoundingClientRect(), b=pumps[i].getBoundingClientRect(); out.push([+(a.x+a.width/2).toFixed(2), +(b.x+b.width/2).toFixed(2), +(a.y+a.height).toFixed(2), +(b.y+b.height).toFixed(2)]);});return JSON.stringify(out)})()"""
try:
    for reduced in (False, True):
        p = Page(); p.cmd("Runtime.enable"); p.cmd("Page.enable")
        p.cmd("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "reduce" if reduced else "no-preference"}])
        p.cmd("Emulation.setDeviceMetricsOverride", width=390, height=844, deviceScaleFactor=2, mobile=True)
        p.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html"); time.sleep(1.5)
        box = p.js("(()=>{const r=document.getElementById('enter').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()"); p.click(*box); time.sleep(1.0)
        p.js("hollowStory.play('pumpkins')")
        p.js("document.querySelectorAll('#layer-particles, #layer-fog').forEach(e=>e.style.display='none')")
        def at(T): 
            p.js(f"document.getAnimations().forEach(a=>{{ a.pause(); if((a.animationName||'').startsWith('s-')) a.currentTime={int(T*1000)}; }})"); time.sleep(0.12)
        at(2.0)   # idle-ish reference: faces fully shown, mid-shake offsets are visible vs 1.0
        ref = json.loads(p.js(BOX)); at(1.0); rest = json.loads(p.js(BOX))
        print(f"== reduced={reduced}")
        # a shake moment: 1.2 s delay + 0.045 s = quarter cycle (translateX -1.6 px, rotate -2.5deg)
        at(1.245); moving = json.loads(p.js(BOX))
        for i, (f, b) in enumerate(zip(moving, rest)):
            fx_shift = f[0] - b[0]; 
            print(f" pumpkin {i+1}: face center x {moving[i][0]} vs pumpkin center x {moving[i][1]} -> offset between them {round(moving[i][0]-moving[i][1],2)} px (at rest {round(rest[i][0]-rest[i][1],2)} px); bottoms {moving[i][2]} vs {moving[i][3]}")
        if not reduced:
            r = p.cmd("Page.captureScreenshot", format="png", clip={"x": 120, "y": 620, "width": 270, "height": 160, "scale": 3}); open(os.path.join(OUT, "face-shake.png"), "wb").write(base64.b64decode(r["data"]))
finally:
    chrome.terminate(); server.terminate()
