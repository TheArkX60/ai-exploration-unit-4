"""House story: right/left/upper-middle trigger, feedback, replay, Pause, and reduced motion."""
import json, time
from harness import *

def center(p, selector):
    return p.js(f"(()=>{{const r=document.querySelector('{selector}').getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}})()")

def tap(p, window):
    p.click(*center(p, f'.hotspot[data-kind=window][data-id="{window}"] .hit'))
    time.sleep(0.25)

def state(p):
    return json.loads(p.js("""JSON.stringify({story:hollowApp.state().story, phase:hollowApp.state().phase,
      progress:hollowStory.houseProgress(), lit:[...document.querySelectorAll('.hotspot[data-kind=window]')]
        .map(e=>e.classList.contains('progress')?1:0).join('')})"""))

SPY = """(()=>{window.__houseCues=[];for(const k of ['houseTap','nope','story']){const o=hollowCues[k];
  hollowCues[k]=function(...a){window.__houseCues.push(k+(a.length?'('+a.join(',')+')':''));return o.apply(this,a)}}})()"""

def cues(p):
    result = json.loads(p.js("JSON.stringify(window.__houseCues)"))
    p.js("window.__houseCues=[]")
    return result

def fresh(reduced=False):
    p = Page(); p.cmd("Runtime.enable"); p.cmd("Page.enable"); p.cmd("Log.enable")
    p.cmd("Emulation.setEmulatedMedia", features=[{"name": "prefers-reduced-motion", "value": "reduce" if reduced else "no-preference"}])
    p.cmd("Emulation.setDeviceMetricsOverride", width=390, height=844, deviceScaleFactor=1, mobile=True)
    p.cmd("Page.navigate", url="http://127.0.0.1:8777/index.html"); time.sleep(1.5)
    p.click(*center(p, "#enter")); time.sleep(1)
    p.js(SPY)
    return p

try:
    p = fresh()
    print("1. correct right -> left -> upper-middle order (3, 1, 2):")
    for window in (3, 1):
        tap(p, window); print(f"   tapped {window}: {state(p)} cues {cues(p)}")
    tap(p, 2); print(f"   tapped 2: {state(p)} cues {cues(p)}")
    started = time.time()
    while state(p)["story"] and time.time() - started < 12: time.sleep(0.05)
    print(f"   story lasted ~{round(time.time()-started+0.25, 2)} s; after: {state(p)}")

    print("2. wrong order (right, upper-middle):")
    tap(p, 3); tap(p, 2)
    print("  ", state(p), "cues", cues(p), "wrong window has nope:",
          p.js("document.querySelector('[data-kind=window][data-id=\"2\"]').classList.contains('nope')"))

    print("3. replay and Pause mid-story:")
    print("   started:", p.js("hollowStory.play('house')"))
    time.sleep(4.5); p.js("document.getElementById('toggle').click()")
    p.js("new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))")
    frozen_a = p.js("document.querySelector('.h-party-middle').getAnimations()[0].currentTime")
    time.sleep(1)
    frozen_b = p.js("document.querySelector('.h-party-middle').getAnimations()[0].currentTime")
    print("   animation clock frozen under Pause:", frozen_a == frozen_b, "|", state(p))
    p.js("document.getElementById('toggle').click()")
    while state(p)["story"] and time.time() - started < 25: time.sleep(0.05)
    print("   replay finished:", state(p))
    print("   exceptions:", len([m for m in p.logs if m.get('method') == 'Runtime.exceptionThrown']))

    q = fresh(reduced=True)
    q.js("hollowStory.play('house')"); time.sleep(0.2)
    print("4. reduced motion:", q.js("[getComputedStyle(document.querySelector('#house-building')).animationName, getComputedStyle(document.querySelector('.h-party-middle')).animationName, getComputedStyle(document.querySelector('[data-kind=window] .art')).animationName]"))
finally:
    chrome.terminate(); server.terminate()
