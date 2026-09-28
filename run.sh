#!/bin/bash
# Script cepat untuk menjalankan daemon di lingkungan pengembangan (Development)
# Quick script to run the daemon in a development environment

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