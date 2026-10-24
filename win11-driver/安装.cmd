@echo off
title Nikon 8000 ED / 9000 ED - Install
"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -File "%~dp0Setup.ps1" -Action Install
set "setupExitCode=%errorlevel%"
echo.
pause
exit /b %setupExitCode%
