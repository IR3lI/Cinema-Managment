@echo off
chcp 65001 >nul
set NGINX_BIN=%~dp0..\bin\nginx-1.26.2

echo Kiem tra cu phap cau hinh NGINX...
cd /d "%NGINX_BIN%"
nginx.exe -t
if %ERRORLEVEL% NEQ 0 (
    echo [LOI] Cau hinh co loi, khong reload!
    pause
    exit /b %ERRORLEVEL%
)

echo Dang reload cau hinh NGINX (Zero Downtime)...
nginx.exe -s reload
echo [THANH CONG] NGINX da reload cau hinh moi!
pause
