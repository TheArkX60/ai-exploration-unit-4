"""screenshots of the story at 12 moments (look at tests/output/story-t*.png). Run: python tests/test_story_frames.py   (see tests/README.md)"""
import base64, json, time
from harness import *
def real_click(p, sel):
    box = p.js(f"(()=>{{const r=document.querySelector('{sel}').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}})()"); p.click(*box)
try:
    p = Page(); p.cmd("Runtime.enable"); p.cmd("Page.enable"); p.cmd("Log.enable")
    p.cmd("Emulation.setDeviceMetricsOverride", width=390, height=844, deviceScaleFactor=2, mobile=True)
    p.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html"); time.sleep(1.5)
    real_click(p, "#enter"); time.sleep(1.0)
    print("play started:", p.js("hollowStory.play('pumpkins')"), "| data-story:", p.js("document.documentElement.dataset.story"))
    # freeze everything and step the story timeline to chosen moments
    p.js("document.getAnimations().forEach(a=>a.pause())")
    # hide ambient clutter so the story is easy to judge
    p.js("document.querySelectorAll('#layer-particles, #layer-fog').forEach(e=>e.style.display='none')")
    names = p.js("[...new Set(document.getAnimations().map(a=>a.animationName).filter(n=>n&&n.startsWith('s-')))]")
    print("story animations running:", names)
    for T in (0.0, 0.5, 1.9, 2.7, 2.95, 3.3, 3.8, 4.5, 5.6, 6.3, 7.4, 8.0):
        p.js(f"document.getAnimations().forEach(a=>{{ if((a.animationName||'').startsWith('s-')) a.currentTime={int(T*1000)}; }})"); time.sleep(0.15)
        r = p.cmd("Page.captureScreenshot", format="png", clip={"x": 120, "y": 620, "width": 270, "height": 160, "scale": 3})
        open(os.path.join(OUT, f"story-t{int(T*100):03d}.png"), "wb").write(base64.b64decode(r["data"]))
    print("exceptions:", len([m for m in p.logs if m.get('method')=='Runtime.exceptionThrown']))
finally:
    chrome.terminate(); server.terminate()
