"""gaps between bat passes over 110 s. Run: python tests/test_bat_gaps.py   (see tests/README.md)"""
from harness import *
ONSCREEN = "(()=>{const W=innerWidth;return ['a','b','c'].map(c=>{const b=document.querySelector('.bat-'+c).getBoundingClientRect();return b.right>0&&b.left<W})})()"
try:
    p = Page(); p.cmd("Runtime.enable"); p.cmd("Page.enable")
    p.cmd("Emulation.setDeviceMetricsOverride", width=390, height=844, deviceScaleFactor=1, mobile=True)
    p.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html"); time.sleep(1.0)
    p.js("document.getElementById('enter').click()"); t0 = time.time()
    samples = []
    while time.time() - t0 < 110:
        samples.append((time.time() - t0, any(p.js(ONSCREEN)))); time.sleep(0.25)
    gaps, start = [], None
    for t, on in samples:
        if not on and start is None: start = t
        if on and start is not None: gaps.append((round(start, 1), round(t - start, 1))); start = None
    print("gaps (start s, length s):", gaps)
    lens = [g[1] for g in gaps if g[0] > 0.5]
    print("gap lengths: min", min(lens), "max", max(lens), "| on screen:", f"{100*sum(on for _, on in samples)//len(samples)}%")
    first_on = next(t for t, on in samples if on); print("first bat visible at", round(first_on, 1), "s")
finally:
    chrome.terminate(); server.terminate()
