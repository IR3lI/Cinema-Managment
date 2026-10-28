@echo off
chcp 65001 >nul 2>&1
title MariaDB Server (cinema_db - Port 3307)
echo.
echo ======================================================
echo    Dang khoi dong MariaDB Server tren Port 3307...
echo    (Chay song song, khong can quyen Admin, khong xung dot MySQL80)
echo.
echo    Host: localhost (hoac 127.0.0.1)
echo    Port: 3307
echo    User: root (khong mat khau)
echo    CSDL: cinema_db
echo ======================================================
echo.
"%~dp0mariadb-10.11.8-winx64\bin\mariadbd.exe" --datadir="%~dp0mariadb-10.11.8-winx64\data" --port=3307 --console
pause
