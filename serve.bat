@echo off
rem Local preview for Hollow Hill. Double-click to start; close this window (or press Ctrl+C) to stop.
rem Needed because browsers block the sound files when index.html is opened straight from the folder (file://).
rem Add "nobrowser" after the command to skip opening the browser.
cd /d "%~dp0"
if /i not "%~1"=="nobrowser" start "" "http://127.0.0.1:8765/"
echo Serving %cd% at http://127.0.0.1:8765/  (close this window to stop)
python -m http.server 8765 --bind 127.0.0.1
