@echo off
chcp 65001 >nul
echo ========================================================
echo   KHOI DONG 2 BACKEND INSTANCE CHO CINE MANAGEMENT
echo ========================================================

set PROJECT_ROOT=%~dp0..\..
cd /d "%PROJECT_ROOT%\publish"

set ASPNETCORE_ENVIRONMENT=Production
set DatabaseProvider=Sqlite

echo [1/2] Dang khoi dong Backend Node 1 (Port 5001) ...
set NODE_INSTANCE_ID=Node-1-Port-5001
start "Backend Node 1 (Port 5001)" cmd /c "set NODE_INSTANCE_ID=Node-1-Port-5001&& CineManagement.exe --urls http://127.0.0.1:5001"

timeout /t 2 /nobreak >nul

echo [2/2] Dang khoi dong Backend Node 2 (Port 5002) ...
set NODE_INSTANCE_ID=Node-2-Port-5002
start "Backend Node 2 (Port 5002)" cmd /c "set NODE_INSTANCE_ID=Node-2-Port-5002&& CineManagement.exe --urls http://127.0.0.1:5002"

echo.
echo Da khoi dong 2 backend instances tren port 5001 va 5002.
echo Nhan phim bat ky de dong cua so nay (2 backend van tiep tuc chay).
pause >nul
