@echo off
title Nikon 8000 ED / 9000 ED - Uninstall
"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -File "%~dp0Setup.ps1" -Action Uninstall
set "setupExitCode=%errorlevel%"
echo.
pause
exit /b %setupExitCode%
