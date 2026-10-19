@echo off
rem Local preview for Hollow Hill. Double-click to start; close this window (or press Ctrl+C) to stop.
rem Needed because browsers block the sound files when index.html is opened straight from the folder (file://).
rem Add "nobrowser" after the command to skip opening the browser.
cd /d "%~dp0"
rem TEMPORARY (story review): the #play-pumpkins part makes the pumpkin story play about a second after you press Enter.
rem Remove it, and the matching hook in story.js, when the real tap triggers are built.
if /i not "%~1"=="nobrowser" start "" "http://127.0.0.1:8765/#play-pumpkins"
echo Serving %cd% at http://127.0.0.1:8765/  (close this window to stop)
python -m http.server 8765 --bind 127.0.0.1
