@echo off
chcp 65001 >nul
echo Dang tao chung chi SSL tu ky (Self-signed Certificate) cho cinemanet.local ...

set OPENSSL_EXE=C:\Program Files\Git\usr\bin\openssl.exe
if not exist "%OPENSSL_EXE%" (
    set OPENSSL_EXE=openssl
)

"%OPENSSL_EXE%" req -x509 -nodes -days 365 -newkey rsa:2048 -keyout "%~dp0cinemanet.key" -out "%~dp0cinemanet.crt" -subj "/C=VN/ST=Hanoi/L=Hanoi/O=CinemaManagement/OU=IT/CN=cinemanet.local"

if %ERRORLEVEL% EQU 0 (
    echo [THANH CONG] Da tao cinemanet.crt va cinemanet.key!
) else (
    echo [THAT BAI] Khong the tao SSL cert. Vui long kiem tra OpenSSL.
)
pause
