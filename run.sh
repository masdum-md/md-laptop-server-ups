#!/bin/bash
# Script cepat untuk menjalankan daemon di lingkungan pengembangan (Development)
# Quick script to run the daemon in a development environment

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "[*] Memulai MD-UPS Monitor secara manual..."

# Periksa apakah virtual environment ada
if [ -d "venv" ]; then
    echo "[*] Menggunakan Virtual Environment..."
    source venv/bin/activate
    python3 scripts/md_ups_monitor.py
else
    echo "[!] Virtual Environment tidak ditemukan. Mengeksekusi dengan Python sistem..."
    python3 scripts/md_ups_monitor.py
fi