@echo off
rem Local preview for Hollow Hill. Double-click to start; close this window (or press Ctrl+C) to stop.
rem Needed because browsers block the sound files when index.html is opened straight from the folder (file://).
rem Add "nobrowser" after the command to skip opening the browser.
cd /d "%~dp0"
set PORT=8765
set PY=
where py >nul 2>nul && set PY=py
if not defined PY where python >nul 2>nul && set PY=python
if not defined PY (
  echo Python was not found on this computer.
  echo Install it from https://www.python.org/downloads/ and tick "Add python.exe to PATH", then try again.
  echo.
  pause
  exit /b 1
)
echo Using: %PY%
echo Serving this folder at http://127.0.0.1:%PORT%/
echo Leave this window open while you use the page. Close it to stop.
echo.
if /i not "%~1"=="nobrowser" start "" "http://127.0.0.1:%PORT%/"
%PY% -m http.server %PORT% --bind 127.0.0.1
echo.
echo The server stopped. If you did not close it on purpose, the message above says why.
pause