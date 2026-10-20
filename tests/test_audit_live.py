"""requirements audit against the LIVE site: sizes, contrast, credits, effects, Pause, touch, blocked audio. Run: python tests/test_audit_live.py   (see tests/README.md)"""
import base64, json, time, urllib.request
from harness import *
URL = "https://thearkx60.github.io/ai-exploration-unit-4/"
AUDIT_SHOTS = os.path.join(OUT, "audit")
os.makedirs(AUDIT_SHOTS, exist_ok=True)

HELPERS = r"""
window.__lum = c => { const [r,g,b] = c.map(v => { v /= 255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); }); return 0.2126*r + 0.7152*g + 0.0722*b; };
window.__rgb = s => s.match(/[\d.]+/g).map(Number).slice(0, 3);
window.__ratio = (sel, bg) => {
  const cs = getComputedStyle(document.querySelector(sel));
  const a = __lum(__rgb(cs.color)), b = __lum(bg || __rgb(cs.backgroundColor));
  return +((Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05)).toFixed(1);
};
window.__smallFonts = () => { const bad = []; document.querySelectorAll('body *').forEach(e => {
  const has = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
  if (!has) return; const cs = getComputedStyle(e); if (cs.display === 'none' || e.closest('[hidden]')) return;
  if (parseFloat(cs.fontSize) < 16) bad.push(e.tagName + '.' + e.className + ' ' + cs.fontSize); }); return bad; };
"""

def center(p, sel):
    return p.js(f"(()=>{{const r=document.querySelector('{sel}').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}})()")
def js(p, code): return json.loads(p.js("JSON.stringify(" + code + ")"))
def new(w, h, reduced=False, touch=False, blocked=False):
    p = Page(); p.cmd("Runtime.enable"); p.cmd("Page.enable"); p.cmd("Log.enable"); p.cmd("Network.enable")
    if blocked: p.cmd("Network.setBlockedURLs", urls=["*assets/audio/*"])
    p.cmd("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "reduce" if reduced else "no-preference"}])
    p.cmd("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=1, mobile=True)
    if touch: p.cmd("Emulation.setTouchEmulationEnabled", enabled=True, maxTouchPoints=5)
    return p
def go(p):
    p.cmd("Page.navigate", url=URL); time.sleep(2.5); p.js(HELPERS)
def enter(p): p.click(*center(p, "#enter")); time.sleep(1.0)
def errors(p):
    return len([m for m in p.logs if m.get("method") == "Runtime.exceptionThrown" or (m.get("method") == "Log.entryAdded" and m["params"]["entry"]["level"] == "error")])

try:
    print("=== 1. Each phone size (live HTTPS site) ===")
    for (w, h) in [(360, 640), (390, 844), (430, 932)]:
        p = new(w, h); go(p)
        pre = js(p, "{stageHidden:document.getElementById('stage').hidden, animationsRunning:document.getAnimations().filter(a=>a.playState==='running').length, audioStarted:hollowAudio.status().started, enterButtonHeight:Math.round(document.getElementById('enter').getBoundingClientRect().height), secureContext:isSecureContext, protocol:location.protocol}")
        enter(p)
        post = js(p, "{scrollsY:document.documentElement.scrollHeight>innerHeight, scrollsX:document.documentElement.scrollWidth>innerWidth, stage:(()=>{const r=document.getElementById('stage').getBoundingClientRect();return [r.width,r.height].map(Math.round)})(), minHotspotPx:Math.round(Math.min(...[...document.querySelectorAll('.hotspot .hit')].map(e=>{const r=e.getBoundingClientRect();return Math.min(r.width,r.height)}))*10)/10, buttonHeights:[...document.querySelectorAll('.ui .btn')].map(b=>Math.round(b.getBoundingClientRect().height)), textUnder16px:__smallFonts()}")
        print(f"{w}x{h}: before Enter {pre}\n         after Enter {post} | console errors {errors(p)}")
        if (w, h) == (390, 844):
            r = p.cmd("Page.captureScreenshot", format="png"); open(os.path.join(AUDIT_SHOTS, "live-390x844.png"), "wb").write(base64.b64decode(r["data"]))

    print("=== 2. Contrast (WCAG ratio; 4.5 is the minimum for text) ===")
    p = new(390, 844); go(p)
    c = {}
    c["start: title"] = p.js("__ratio('.start-title', [42,17,70])")
    c["start: kicker and notes"] = p.js("__ratio('.start-kicker', [42,17,70])")
    c["start: Enter button"] = p.js("__ratio('#enter')")
    enter(p)
    p.js("document.getElementById('hint').hidden=false;document.getElementById('hint').textContent='test';document.getElementById('story-note').hidden=false;document.getElementById('story-note').textContent='test';document.getElementById('sound-note').hidden=false")
    for label, sel in [("Pause and Credits buttons", "#toggle"), ("hint line", "#hint"), ("story note", "#story-note"), ("sound note", "#sound-note")]:
        c[label] = p.js(f"__ratio('{sel}')")
    p.js("document.getElementById('credits-open').click()"); time.sleep(0.4)
    c["credits dialog text"] = p.js("__ratio('#credits p')")
    print(c)

    print("=== 3. External resources and credits ===")
    hosts = js(p, "[...new Set(performance.getEntriesByType('resource').map(e=>new URL(e.name).host))]")
    print("everything loads from:", hosts)
    print("credits text:", p.js("document.getElementById('credits').innerText").replace("\n", " | "))
    print("credit links:", js(p, "[...document.querySelectorAll('#credits a')].map(a=>a.href)"))
    print("images in page:", p.js("document.images.length"), "| scripts from other hosts:", p.js("[...document.scripts].filter(s=>s.src&&new URL(s.src).host!==location.host).length"))

    print("=== 4. Ambient effects, sound, Play/Pause, timers (390x844) ===")
    p = new(390, 844); go(p); enter(p); time.sleep(20)
    eff = js(p, "{stars:[...document.querySelectorAll('.stars circle')].filter(e=>getComputedStyle(e).animationName!=='none').length, flicker:[...document.querySelectorAll('.flicker')].filter(e=>getComputedStyle(e).animationName!=='none').length, fog:[...document.querySelectorAll('.fog')].filter(e=>getComputedStyle(e).animationName!=='none').length, bats:[...document.querySelectorAll('.bat-fly')].filter(e=>getComputedStyle(e).animationName!=='none').length, leaves:[...document.querySelectorAll('.leaf-fall')].filter(e=>getComputedStyle(e).animationName!=='none').length}")
    print("ambient effects running (elements per effect):", eff)
    print("sound at 20 s:", js(p, "hollowAudio.status()"), "| level", round(p.js("hollowAudio.levelDb()"), 1), "dB")
    p.js("hollowHints.times.splice(0,3,100,200,300)")
    p.js("document.getElementById('toggle').click()"); time.sleep(3)
    s1 = js(p, "{idle:hollowHints.idle(), running:document.getAnimations().filter(a=>a.playState==='running').length, audio:hollowAudio.status().state, time:hollowAudio.status().time}")
    time.sleep(2); s2 = js(p, "{idle:hollowHints.idle(), audio:hollowAudio.status().state, time:hollowAudio.status().time}")
    p.click(*center(p, '.hotspot[data-kind=pumpkin][data-id="1"] .hit')); time.sleep(0.3)
    print(f"PAUSED: animations still running {s1['running']} | audio {s1['audio']}, clock {s1['time']:.2f} -> {s2['time']:.2f} | idle clock {s1['idle']:.2f} -> {s2['idle']:.2f} | tap ignored: progress {p.js('hollowStory.progress()')}")
    p.js("document.getElementById('toggle').click()"); time.sleep(1.5)
    print("RESUMED:", js(p, "{audio:hollowAudio.status().state, animationsRunning:document.getAnimations().filter(a=>a.playState==='running').length}"))

    print("=== 5. Story by touch, three times in a row ===")
    q = new(390, 844, touch=True); go(q); enter(q)
    q.js("window.__t=[];document.addEventListener('hollow:story',e=>window.__t.push([e.detail.story,performance.now()]))")
    def touch_tap(i):
        x, y = center(q, f'.hotspot[data-kind=pumpkin][data-id="{i}"] .hit')
        q.cmd("Input.dispatchTouchEvent", type="touchStart", touchPoints=[{"x": x, "y": y}]); q.cmd("Input.dispatchTouchEvent", type="touchEnd", touchPoints=[]); time.sleep(0.3)
    for run in (1, 2, 3):
        for i in (1, 2, 3, 4): touch_tap(i)
        t0 = time.time()
        while js(q, "hollowApp.state().story") and time.time() - t0 < 15: time.sleep(0.1)
        time.sleep(0.3)
    t = json.loads(q.js("JSON.stringify(window.__t)"))
    print("story durations by touch (s):", [round((t[k+1][1]-t[k][1])/1000, 2) for k in range(0, len(t) - 1, 2)], "| events recorded:", len(t))

    print("=== 6. Audio blocked, hidden tab, reduced motion ===")
    b = new(390, 844, blocked=True); go(b); enter(b); time.sleep(2)
    b.click(*center(b, '.hotspot[data-kind=pumpkin][data-id="1"] .hit')); time.sleep(0.3)
    b.js("document.getElementById('toggle').click()")
    print("audio blocked: note visible:", not b.js("document.getElementById('sound-note').hidden"), "| pumpkin 1 shows progress:", b.js("document.querySelector('.hotspot[data-kind=pumpkin][data-id=\"1\"]').classList.contains('progress')"), "| Pause works:", b.js("document.documentElement.dataset.phase"))
    h = new(390, 844); go(h); enter(h); time.sleep(1)
    first = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9333/json")) if t["type"] == "page"][0]["id"]
    urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:9333/json/new?about:blank", method="PUT")).read(); time.sleep(1)
    print("hidden tab -> phase:", h.js("document.documentElement.dataset.phase"), "| audio:", h.js("hollowAudio.status().state"))
    urllib.request.urlopen("http://127.0.0.1:9333/json/activate/" + first).read(); time.sleep(0.8)
    print("back on the tab -> stays:", h.js("document.documentElement.dataset.phase"))
    r = new(390, 844, reduced=True); go(r)
    print("reduced motion BEFORE Enter -> data-reduced-motion:", r.js("document.documentElement.dataset.reducedMotion"), "| 'Reduced motion is on.' shown:", not r.js("document.getElementById('motion-note').hidden"))
    enter(r); time.sleep(1.5)
    print("reduced motion after Enter -> ambient elements still animating:", r.js("[...document.querySelectorAll('.fx, .fx *')].filter(e=>getComputedStyle(e).animationName!=='none').length"), "| sound state:", r.js("hollowAudio.status().state"))
finally:
    chrome.terminate(); server.terminate()
