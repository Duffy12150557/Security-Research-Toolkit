@echo off
chcp 65001 >nul
title WSUS Security Research Toolkit
cd /d "%~dp0"
if "%~1"=="" (
    python exp.py --help
) else (
    python exp.py %*
)
pause
