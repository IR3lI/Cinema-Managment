@echo off
chcp 65001 >nul
set NGINX_BIN=%~dp0..\bin\nginx-1.26.2

echo Dang khoi dong NGINX (Port 80 va Port 443 SSL) ...
cd /d "%NGINX_BIN%"
start "" nginx.exe

timeout /t 2 /nobreak >nul
tasklist | findstr nginx.exe >nul
if %ERRORLEVEL% EQU 0 (
    echo [THANH CONG] NGINX dang chay!
    echo Web Server & Proxy: http://localhost hoac https://cinemanet.local
) else (
    echo [LOI] Khong the chay NGINX. Vui long kiem tra logs\error.log
)
pause
