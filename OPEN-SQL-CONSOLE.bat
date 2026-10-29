@echo off
chcp 65001 >nul 2>&1
title MariaDB SQL Console - cinema_db (Port 3307)
echo ==============================================================
echo    KET NOI TRUC TIEP VAO CO SO DU LIEU: cinema_db (Port 3307)
echo    User: root (khong mat khau)
echo ==============================================================
echo.
echo Goi y cac cau lenh SQL thu nghiem:
echo   SHOW TABLES;
echo   SELECT * FROM cinemas;
echo   SELECT MovieId, Title, Duration, Rating FROM movies LIMIT 5;
echo   SELECT COUNT(*) AS TongSoGhe FROM showtimeseats;
echo   EXIT;
echo.
echo Dang mo terminal SQL...
echo ==============================================================
echo.
"%~dp0mariadb-10.11.8-winx64\bin\mysql.exe" -u root -P 3307 cinema_db
pause
