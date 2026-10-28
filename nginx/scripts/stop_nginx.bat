@echo off
chcp 65001 >nul
set NGINX_BIN=%~dp0..\bin\nginx-1.26.2

echo Dang dung tien trinh NGINX...
cd /d "%NGINX_BIN%"
nginx.exe -s stop 2>nul
taskkill /F /IM nginx.exe 2>nul

echo NGINX da duoc dung hoan toan.
pause
