@echo off
chcp 65001 >nul 2>&1
title MySQL Server (Cinema DB)
echo.
echo ======================================================
echo    Dang khoi dong MySQL / MariaDB Server (Port 3306)...
echo    CSDL: cinema_db
echo    User: root (khong mat khau)
echo ======================================================
echo.
"%~dp0mariadb-10.11.8-winx64\bin\mariadbd.exe" --datadir="%~dp0mariadb-10.11.8-winx64\data" --port=3306 --console
pause
