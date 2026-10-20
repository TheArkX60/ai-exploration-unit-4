"""Start screen, layout at three phone sizes plus desktop, Tab order and focus, tap light-up, Play/Pause, credits, reduced-motion read. Run: python tests/test_shell.py   (see tests/README.md)"""
from harness import *

def run(w, h, label, reduced=False, mobile=True):
    p = Page()
    p.cmd("Runtime.enable"); p.cmd("Log.enable"); p.cmd("Page.enable")
    p.cmd("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=1, mobile=mobile)
    p.cmd("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "reduce" if reduced else "no-preference"}])
    p.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html")
    time.sleep(1.2)
    res = {"viewport": label}
    res["start_stage_hidden"] = p.js("document.getElementById('stage').hidden")
    res["start_reducedMotion_attr"] = p.js("document.documentElement.dataset.reducedMotion")
    res["enter_height"] = p.js("document.getElementById('enter').getBoundingClientRect().height")
    p.shot(f"{label}-start")
    p.js("document.getElementById('enter').click()")
    time.sleep(0.5)
    res["phase_after_enter"] = p.js("document.documentElement.dataset.phase")
    res["stage_rect"] = p.js("(()=>{const r=document.getElementById('stage').getBoundingClientRect();return [r.x,r.y,r.width,r.height].map(Math.round)})()")
    res["scrolls"] = p.js("document.documentElement.scrollHeight>innerHeight || document.documentElement.scrollWidth>innerWidth")
    res["hotspots_px_min"] = p.js("""(()=>{let m=1e9;document.querySelectorAll('.hotspot .hit').forEach(h=>{const r=h.getBoundingClientRect();m=Math.min(m,r.width,r.height)});return Math.round(m*10)/10})()""")
    res["toggle_credits_h"] = p.js("[...document.querySelectorAll('.ui .btn')].map(b=>Math.round(b.getBoundingClientRect().height))")
    p.shot(f"{label}-scene")
    res["console_errors"] = [m for m in p.logs if m.get("method") == "Runtime.exceptionThrown" or
                             (m.get("method") == "Log.entryAdded" and m["params"]["entry"]["level"] == "error") or
                             (m.get("method") == "Runtime.consoleAPICalled" and m["params"]["type"] == "error")]
    res["console_errors"] = json.dumps(res["console_errors"])[:600]
    return p, res

results = []
try:
    p, r = run(360, 640, "360x640"); results.append(r)
    # Interaction checks on this page
    r2 = {}
    # Tab order & focus ring: tab through to first hotspot
    seq = []
    for i in range(20):
        p.key("Tab", "Tab", 9)
        seq.append(p.js("document.activeElement.getAttribute('aria-label') || document.activeElement.id"))
    r2["tab_order"] = seq
    # tab until a hotspot is focused, screenshot focus ring, activate with Enter and Space
    p.js("document.getElementById('stage').focus()")
    for i in range(6):
        p.key("Tab", "Tab", 9)
        if p.js("document.activeElement.classList.contains('hotspot')"):
            break
    r2["focused"] = p.js("document.activeElement.getAttribute('aria-label')")
    p.key("Enter", "Enter", 13)
    r2["lit_after_enter"] = p.js("document.activeElement.classList.contains('lit')")
    p.shot("360x640-focus-lit")
    time.sleep(0.7)
    r2["lit_after_wait"] = p.js("document.activeElement.classList.contains('lit')")
    p.key(" ", "Space", 32)
    r2["lit_after_space"] = p.js("document.activeElement.classList.contains('lit')")
    time.sleep(0.6)
    # touch/click activation
    box = p.js("(()=>{const r=document.querySelector('[data-kind=tombstone][data-id=\"2\"] .hit').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()")
    p.click(box[0], box[1])
    r2["lit_after_click"] = p.js("document.querySelector('[data-kind=tombstone][data-id=\"2\"]').classList.contains('lit')")
    time.sleep(0.7)
    # Play/Pause
    p.js("document.getElementById('toggle').click()")
    r2["paused"] = [p.js("document.documentElement.dataset.phase"), p.js("document.getElementById('toggle').getAttribute('aria-pressed')"), p.js("document.getElementById('toggle').textContent")]
    p.click(box[0], box[1])
    r2["lit_while_paused"] = p.js("document.querySelector('[data-kind=tombstone][data-id=\"2\"]').classList.contains('lit')")
    p.shot("360x640-paused")
    p.js("document.getElementById('toggle').click()")
    r2["resumed"] = [p.js("document.documentElement.dataset.phase"), p.js("document.getElementById('toggle').getAttribute('aria-pressed')"), p.js("document.getElementById('toggle').textContent")]
    # Credits
    p.js("document.getElementById('credits-open').click()")
    time.sleep(0.3)
    r2["credits_open"] = p.js("document.getElementById('credits').open")
    p.shot("360x640-credits")
    p.js("document.getElementById('credits-close').click()")
    # Ghost symbol preview (injected, not in the product)
    p.js("""(()=>{const s=document.getElementById('scene');const NS='http://www.w3.org/2000/svg';
      const u=document.createElementNS(NS,'use');u.setAttribute('href','#ghost');u.setAttribute('x',150);u.setAttribute('y',380);u.setAttribute('width',60);u.setAttribute('height',80);u.id='tmp';s.appendChild(u);
      const h=document.createElementNS(NS,'use');h.setAttribute('href','#ghost-hat');h.setAttribute('x',163);h.setAttribute('y',356);h.setAttribute('width',24);h.setAttribute('height',28);s.appendChild(h);})()""")
    p.shot("360x640-ghost-preview")
    results.append(r2)

    for (w, h, l) in [(390, 844, "390x844"), (430, 932, "430x932")]:
        _, r = run(w, h, l); results.append(r)
    _, r = run(1280, 720, "1280x720-desktop", mobile=False); results.append(r)
    _, r = run(360, 640, "360x640-reduced", reduced=True); results.append(r)
finally:
    chrome.terminate(); server.terminate()

print(json.dumps(results, indent=1))


