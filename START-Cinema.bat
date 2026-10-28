@echo off
chcp 65001 >nul 2>&1
title He Thong Quan Ly Rap Chieu Phim - CineManagement Demo
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║       🎬 CINEMA MANAGEMENT SYSTEM - BAN DEMO             ║
echo ╠══════════════════════════════════════════════════════════╣
echo ║  🌐 He thong san sang cho Giang vien & Hoi dong         ║
echo ║  💾 Co so du lieu: SQLite (app.db) - Khong can cai MySQL ║
echo ╠══════════════════════════════════════════════════════════╣
echo ║  🔑 TAI KHOAN DEMO:                                      ║
echo ║  • Admin:    admin@cinema.com    / Admin@123            ║
echo ║  • Staff:    staff@cinema.com    / Staff@123            ║
echo ║  • Khach:    customer@cinema.com / Customer@123         ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo Dang khoi dong he thong... Trinh duyet se tu dong mo http://localhost:5050!
echo (Nhan Ctrl+C tai cua so nay neu muon tat he thong)
echo.

if exist "%~dp0publish\CineManagement.exe" (
    cd /d "%~dp0publish"
    set ASPNETCORE_ENVIRONMENT=Production
    set ASPNETCORE_URLS=http://localhost:5050
    start "" cmd /c "timeout /t 3 /nobreak >nul & start http://localhost:5050"
    CineManagement.exe --urls "http://localhost:5050"
) else (
    cd /d "%~dp0CineManagement"
    start "" cmd /c "timeout /t 5 /nobreak >nul & start http://localhost:5006"
    dotnet run
)

pause
