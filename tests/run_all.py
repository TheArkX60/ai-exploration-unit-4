"""Run the tests one after another and print each one's output. Usage:
    python tests/run_all.py --quick     the fast set
    python tests/run_all.py             everything except the live-site audit
    python tests/run_all.py --live      everything, including the live-site audit
A test "fails" here only if it crashes or times out; read the printed values against tests/README.md."""
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
QUICK = ["test_shell.py", "test_triggers.py", "test_story.py", "test_enter_focus.py", "test_story_note.py",
         "test_story_note_pause.py", "test_autopause.py", "test_flicker.py", "test_fog.py", "test_leaves.py",
         "test_face_shake.py", "test_graveyard.py", "test_house.py"]
SLOW = ["test_hints.py", "test_audio.py", "test_bats.py", "test_bat_gaps.py", "test_story_frames.py"]
LIVE = ["test_audit_live.py"]

args = sys.argv[1:]
tests = QUICK + ([] if "--quick" in args else SLOW) + (LIVE if "--live" in args else [])

summary = []
for name in tests:
    print(f"\n{'=' * 8} {name} {'=' * 8}", flush=True)
    start = time.time()
    try:
        done = subprocess.run([sys.executable, os.path.join(HERE, name)], timeout=900)
        status = "finished" if done.returncode == 0 else f"CRASHED (exit code {done.returncode})"
    except subprocess.TimeoutExpired:
        status = "TIMED OUT"
    summary.append((name, status, round(time.time() - start)))
    time.sleep(1)                                     # let the ports free up

print("\n" + "=" * 8 + " summary " + "=" * 8)
for name, status, secs in summary:
    print(f"{name:32} {status:28} {secs:>4} s")
