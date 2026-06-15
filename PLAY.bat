@echo off
title JV Pirates
cd /d "%~dp0"
echo Installing dependencies (first run only)...
py -3.12 -m pip install -r requirements.txt -q
echo Starting JV Pirates...
py -3.12 code\main.py
pause
