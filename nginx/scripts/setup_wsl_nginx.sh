#!/bin/bash
# Script cài đặt & cấu hình NGINX tự động cho Ubuntu / WSL
# Sử dụng: chmod +x setup_wsl_nginx.sh && ./setup_wsl_nginx.sh

echo "=== [WSL / Ubuntu] Cài đặt NGINX và thiết lập môi trường Buổi 8 ==="

# 1. Cài đặt NGINX
sudo apt update
sudo apt install -y nginx openssl

# 2. Tạo thư mục chứa web và ssl
sudo mkdir -p /var/www/cinemanet/html
sudo mkdir -p /etc/nginx/ssl

# 3. Copy frontend demo vào thư mục web server
sudo cp -r ../html/* /var/www/cinemanet/html/

# 4. Sinh chứng chỉ SSL tự ký
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/cinemanet.key \
  -out /etc/nginx/ssl/cinemanet.crt \
  -subj "/C=VN/ST=Hanoi/L=Hanoi/O=CinemaManagement/OU=IT/CN=cinemanet.local"

# 5. Đặt cấu hình NGINX
sudo cp ../nginx-wsl.conf /etc/nginx/sites-available/cinemanet.conf
sudo ln -sf /etc/nginx/sites-available/cinemanet.conf /etc/nginx/sites-enabled/cinemanet.conf
sudo rm -f /etc/nginx/sites-enabled/default

# 6. Kiểm tra cú pháp và khởi động service
sudo nginx -t
if [ $? -eq 0 ]; then
    sudo systemctl restart nginx || sudo service nginx restart
    echo "=== [THANH CONG] NGINX da khoi dong tren WSL! ==="
    echo "Truy cap tu trinh duyet Windows: http://localhost hoac https://cinemanet.local"
else
    echo "=== [LOI] Kiem tra cu phap NGINX that bai! ==="
fi
