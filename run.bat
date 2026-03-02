@echo off
chcp 65001 >nul
title Security Research Toolkit
cd /d "%~dp0"
python main.py
pause
