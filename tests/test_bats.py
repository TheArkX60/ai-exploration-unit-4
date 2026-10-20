"""bats: flight range, 75 s coverage, reduced motion. Run: python tests/test_bats.py   (see tests/README.md)"""
import base64
from harness import *
ONSCREEN = "(()=>{const W=innerWidth;return ['a','b','c'].map(c=>{const b=document.querySelector('.bat-'+c).getBoundingClientRect();return b.right>0&&b.left<W})})()"
def shot(name, clip):
    r = p.cmd("Page.captureScreenshot", format="png", clip=clip); open(os.path.join(OUT, name + ".png"), "wb").write(base64.b64decode(r["data"]))
try:
    # ---- timing on a phone-sized screen, real time ----
    p = Page(); p.cmd("Runtime.enable"); p.cmd("Page.enable")
    p.cmd("Emulation.setDeviceMetricsOverride", width=390, height=844, deviceScaleFactor=1, mobile=True)
    p.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html"); time.sleep(1.0)
    p.js("document.getElementById('enter').click()"); t0 = time.time()
    print("range vars:", p.js("[getComputedStyle(document.documentElement).getPropertyValue('--bat-left'), getComputedStyle(document.documentElement).getPropertyValue('--bat-right')]"))
    samples = []
    while time.time() - t0 < 75:
        samples.append((round(time.time() - t0, 1), p.js(ONSCREEN))); time.sleep(0.5)
    first = next(t for t, s in samples if any(s))
    none_run = longest = 0
    for t, s in samples:
        if any(s): none_run = 0
        else: none_run += 0.5; longest = max(longest, none_run)
    print(f"phone 75 s: first bat on screen at {first}s | time with >=1 bat: {100*sum(any(s) for _, s in samples)//len(samples)}% | with >=2: {100*sum(sum(s)>=2 for _, s in samples)//len(samples)}% | longest empty stretch: {longest}s")
    print("on-screen timeline (a b c) every 5s:", [(t, ''.join('X' if x else '.' for x in s)) for t, s in samples[::10]])
    # ---- wing flap frames ----
    p.js("document.getElementById('toggle').click()")
    p.js("document.getAnimations().forEach(a=>{const n=a.animationName; if(n==='fly-a') {a.currentTime=6250; } })")
    for i, ct in enumerate((0, 210, 420)):
        p.js(f"document.getAnimations().forEach(a=>{{ if(a.animationName==='bat-flap'||a.animationName==='bat-bob'){{ a.pause(); a.currentTime={ct}; }} }})")
        time.sleep(0.15)
        r = p.js("(()=>{const b=document.querySelector('.bat-a .bat-bob').getBoundingClientRect();return [b.x,b.y,b.width,b.height]})()")
        shot(f"bat-flap-{i}", {"x": r[0]-14, "y": r[1]-14, "width": r[2]+28, "height": r[3]+28, "scale": 8})
    # ---- desktop range ----
    p2 = Page(); p2.cmd("Runtime.enable"); p2.cmd("Page.enable")
    p2.cmd("Emulation.setDeviceMetricsOverride", width=1280, height=720, deviceScaleFactor=1, mobile=False)
    p2.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html"); time.sleep(1.0)
    p2.js("document.getElementById('enter').click()"); time.sleep(0.3)
    print("desktop range vars:", p2.js("[getComputedStyle(document.documentElement).getPropertyValue('--bat-left'), getComputedStyle(document.documentElement).getPropertyValue('--bat-right')]"))
    # reduced motion: bats offscreen
    p3 = Page(); p3.cmd("Runtime.enable"); p3.cmd("Page.enable")
    p3.cmd("Emulation.setDeviceMetricsOverride", width=390, height=844, deviceScaleFactor=1, mobile=True)
    p3.cmd("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "reduce"}])
    p3.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html"); time.sleep(1.0)
    p3.js("document.getElementById('enter').click()"); time.sleep(0.3)
    print("reduced motion, bats on screen:", p3.js(ONSCREEN), "| animations:", p3.js("[...document.querySelectorAll('.bat-fly,.bat-bob,.bat-wing')].map(e=>getComputedStyle(e).animationName).filter(n=>n!=='none').length"))
finally:
    chrome.terminate(); server.terminate()
