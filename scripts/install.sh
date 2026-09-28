#!/bin/bash
# ==============================================================================
# MD-Laptop-Server-UPS Auto Installer (Systemd Mode)
# ==============================================================================

if [ "$EUID" -ne 0 ]; then
  echo "[-] [ID] Silakan jalankan installer ini sebagai root (gunakan sudo)."
  exit 1
fi

# Dapatkan path dari root project
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
APP_DIR="/opt/md-laptop-server-ups"
SERVICE_FILE="/etc/systemd/system/md-ups.service"

echo "[+] Memulai instalasi MD-Laptop-Server-UPS..."

# 1. Copy seluruh struktur folder ke /opt/
mkdir -p $APP_DIR
cp -r "$PROJECT_ROOT"/* $APP_DIR/

# Siapkan file .env jika belum ada
if [ ! -f "$APP_DIR/config/.env" ]; then
    cp "$APP_DIR/config/.env.example" "$APP_DIR/config/.env"
fi

# 2. Instalasi dependensi
if ! command -v pip3 &> /dev/null; then
    apt-get update && apt-get install -y python3-pip python3-venv
fi

echo "[*] Mengonfigurasi virtual environment..."
python3 -m venv $APP_DIR/venv
$APP_DIR/venv/bin/pip install -r $APP_DIR/requirements.txt

# 3. Pembuatan unit Systemd
echo "[*] Menulis konfigurasi service Systemd..."
cat <<EOF > $SERVICE_FILE
[Unit]
Description=MD Laptop Server UPS (Telegram Power Monitor)
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$APP_DIR
Environment="POWER_MONITOR_ENV=$APP_DIR/config/.env"
ExecStart=$APP_DIR/venv/bin/python $APP_DIR/scripts/md_ups_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable md-ups.service

echo "=================================================================="
echo "✅ INSTALASI SELESAI!"
echo "1. Konfigurasi Bot : nano $APP_DIR/config/.env"
echo "2. Start Layanan   : systemctl start md-ups"
echo "3. Cek Status      : systemctl status md-ups"
echo "=================================================================="