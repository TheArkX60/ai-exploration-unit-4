"""falling leaves: count, motion, Pause, reduced motion. Run: python tests/test_leaves.py   (see tests/README.md)"""
import base64
from harness import *
POS = "(()=>[...document.querySelectorAll('.leaf-fall')].map(e=>{const b=e.getBoundingClientRect();return [Math.round(b.x),Math.round(b.y)]}))()"
VIS = "(()=>{const W=innerWidth,H=innerHeight;return [...document.querySelectorAll('.leaf-fall')].filter(e=>{const b=e.getBoundingClientRect();return b.bottom>0&&b.top<H&&b.right>0&&b.left<W}).length})()"
try:
    for (w, h, label, reduced) in [(390, 844, "phone", False), (1280, 720, "desktop", False), (390, 844, "phone-reduced", True)]:
        p = Page(); p.cmd("Runtime.enable"); p.cmd("Page.enable"); p.cmd("Log.enable")
        p.cmd("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=1, mobile=(w < 1000))
        p.cmd("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "reduce" if reduced else "no-preference"}])
        p.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html"); time.sleep(1.0)
        p.js("document.getElementById('enter').click()"); time.sleep(0.3)
        print(f"== {label}: leaves built: {p.js('document.querySelectorAll(\".leaf-fall\").length')} | range vars:", p.js("['--fall-top','--fall-bottom'].map(v=>getComputedStyle(document.documentElement).getPropertyValue(v))"))
        print("visible leaves now:", p.js(VIS))
        if reduced:
            print("animations running:", p.js("[...document.querySelectorAll('.leaf-fall,.leaf-sway,.leaf-spin')].map(e=>getComputedStyle(e).animationName).filter(n=>n!=='none').length")); continue
        a = p.js(POS); time.sleep(2); b = p.js(POS)
        moved = sum(1 for x, y in zip(a, b) if x != y); print("leaves that moved in 2 s:", moved, "of", len(a), "| mean fall px/s:", round(sum(y2[1]-y1[1] for y1, y2 in zip(a, b))/len(a)/2, 1))
        p.js("document.getElementById('toggle').click()"); time.sleep(0.2)
        c = p.js(POS); time.sleep(1.2); d = p.js(POS); print("paused frozen:", c == d)
        p.js("document.getElementById('toggle').click()")
        # a leaf wraps: sample 40s of "visible count" to see leaves keep coming
        counts = []
        t0 = time.time()
        while time.time() - t0 < 30: counts.append(p.js(VIS)); time.sleep(1)
        print("visible leaves over 30 s (min/max):", min(counts), max(counts))
        # taps still work through leaves
        box = p.js("(()=>{const r=document.querySelector('[data-kind=\"tombstone\"][data-id=\"2\"] .hit').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()")
        p.click(*box); time.sleep(0.15); print("tap tombstone 2 lit:", p.js("document.querySelector('[data-kind=\"tombstone\"][data-id=\"2\"]').classList.contains('lit')"))
        print("exceptions:", len([m for m in p.logs if m.get('method')=='Runtime.exceptionThrown']))
        if label == "phone":
            p.js("document.getAnimations().forEach(x=>x.pause())")
            r = p.cmd("Page.captureScreenshot", format="png"); open(os.path.join(OUT, "leaves-phone.png"), "wb").write(base64.b64decode(r["data"]))
finally:
    chrome.terminate(); server.terminate()
