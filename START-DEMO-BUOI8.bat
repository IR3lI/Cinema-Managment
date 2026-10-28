@echo off
chcp 65001 >nul
title BUOI 8 DEMO - NGINX REVERSE PROXY & UPSTREAM CLUSTER
cls

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║   🎬 CINEMA MANAGEMENT - DEMO BUỔI 8: NGINX REVERSE PROXY       ║
echo ╠══════════════════════════════════════════════════════════════════╣
echo ║  1. NGINX Web Server: Phục vụ file tĩnh SPA (Port 80)           ║
echo ║  2. Reverse Proxy: / ➜ Frontend, /api/ ➜ Backend Cluster        ║
echo ║  3. Upstream Load Balancing: 2 Nodes (Port 5001 ^& Port 5002)    ║
echo ║  4. Container/Docker Ready: docker-compose.buoi8.yml            ║
echo ║  5. client_max_body_size: Thử nghiệm 1MB vs 20MB               ║
echo ║  6. Domain cinemanet.local ^& SSL HTTPS (Port 443)               ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

set ROOT=%~dp0
set NGINX_DIR=%ROOT%nginx\bin\nginx-1.26.2

:: Đồng bộ cấu hình và file tĩnh
echo [1/4] Dong bo cau hinh va file Frontend sang NGINX...
copy /y "%ROOT%nginx\nginx.conf" "%NGINX_DIR%\conf\nginx.conf" >nul
xcopy /s /y /q "%ROOT%nginx\html\*" "%NGINX_DIR%\html\" >nul
if not exist "%NGINX_DIR%\conf\ssl" mkdir "%NGINX_DIR%\conf\ssl"
copy /y "%ROOT%nginx\ssl\*" "%NGINX_DIR%\conf\ssl\" >nul

:: Dừng NGINX cũ nếu đang chạy
taskkill /F /IM nginx.exe >nul 2>&1

:: Khởi động 2 Backend Nodes
echo [2/4] Khoi dong Backend Node 1 (Port 5001)...
start "Backend Node 1 [Port 5001]" cmd /c "cd /d "%ROOT%publish" && set ASPNETCORE_ENVIRONMENT=Production&& set DatabaseProvider=Sqlite&& set NODE_INSTANCE_ID=Node-1-Port-5001&& CineManagement.exe --urls http://127.0.0.1:5001"

timeout /t 2 /nobreak >nul

echo [3/4] Khoi dong Backend Node 2 (Port 5002)...
start "Backend Node 2 [Port 5002]" cmd /c "cd /d "%ROOT%publish" && set ASPNETCORE_ENVIRONMENT=Production&& set DatabaseProvider=Sqlite&& set NODE_INSTANCE_ID=Node-2-Port-5002&& CineManagement.exe --urls http://127.0.0.1:5002"

timeout /t 2 /nobreak >nul

:: Khởi động NGINX
echo [4/4] Khoi dong NGINX Reverse Proxy (Port 80 ^& 443 SSL)...
cd /d "%NGINX_DIR%"
start "" nginx.exe

timeout /t 2 /nobreak >nul

echo.
echo ==================================================================
echo ✅ TOÀN BỘ HỆ THỐNG ĐÃ SẴN SÀNG!
echo • Mở trình duyệt tại: http://localhost
echo • Domain mô phỏng:    http://cinemanet.local (sau khi sua hosts)
echo • HTTPS tự ký:        https://cinemanet.local (Port 443 SSL)
echo ==================================================================
echo.

start "" "http://localhost"

pause
