"""window/lantern flicker: running, Pause, reduced motion. Run: python tests/test_flicker.py   (see tests/README.md)"""
from harness import *
SAMPLE = "(()=>[...document.querySelectorAll('.flicker')].map(e=>+(+getComputedStyle(e).fillOpacity).toFixed(2)))()"
def st(): return p.js("[...document.querySelectorAll('.flicker')].map(e=>getComputedStyle(e).animationName+'/'+getComputedStyle(e).animationPlayState)")
try:
    for reduced in (False, True):
        p = Page(); p.cmd("Runtime.enable"); p.cmd("Page.enable"); p.cmd("Log.enable")
        p.cmd("Emulation.setDeviceMetricsOverride", width=390, height=844, deviceScaleFactor=1, mobile=True)
        p.cmd("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "reduce" if reduced else "no-preference"}])
        p.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html"); time.sleep(1.0)
        p.js("document.getElementById('enter').click()"); time.sleep(0.3)
        print("== reduced:", reduced, st())
        # sample over time to see the range of values (running)
        seen = [min(x) for x in [p.js(SAMPLE) or [1] for _ in range(1)]]
        lows = [1.0]*5
        for _ in range(40):
            v = p.js(SAMPLE); lows = [min(a, b) for a, b in zip(lows, v)]; time.sleep(0.25)
        print("lowest opacity seen in 10s per element:", lows)
        p.js("document.getElementById('toggle').click()"); time.sleep(0.2)
        a = p.js(SAMPLE); time.sleep(1.2); b = p.js(SAMPLE)
        print("paused frozen:", a == b, st())
        p.js("document.getElementById('toggle').click()"); time.sleep(0.2)
        # tap light-up still works while flickering: window 1
        box = p.js("(()=>{const r=document.querySelector('[data-kind=window] .hit').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()")
        p.click(*box)
        print("tap lights window glow:", p.js("getComputedStyle(document.querySelector('[data-kind=window] .glow')).opacity"), "| art still animating:", p.js("getComputedStyle(document.querySelector('[data-kind=window] .art')).animationName"))
        errs=[m for m in p.logs if m.get("method")=="Runtime.exceptionThrown"]
        print("exceptions:", len(errs))
finally:
    chrome.terminate(); server.terminate()
