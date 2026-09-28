# 🔋 MD-Laptop-Server-UPS

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Deployment](https://img.shields.io/badge/deployment-Systemd%20%7C%20PM2-orange.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20(Ubuntu%20%7C%20Debian%20%7C%20Armbian)-lightgrey.svg)
![Author](https://img.shields.io/badge/developer-Mas%20Dum-blueviolet.svg)
![Infrastructure](https://img.shields.io/badge/infrastructure-PT%20Mdigital%20Dinamika%20Sistem-purple.svg)

> **[EN]** A resilient Linux background daemon that converts spare laptops into robust on-premise servers by utilizing internal battery packs as automated, Telegram-alerted UPS systems.  
> **[ID]** Daemon Linux latar belakang tangguh yang menyulap laptop bekas menjadi server lokal handal dengan memanfaatkan baterai bawaan sebagai UPS darurat otomatis berbasis notifikasi Telegram.

---

## 📑 Table of Contents / Daftar Isi
1. [English Documentation](#-english-documentation)
   * [Overview & The Problem](#overview--the-problem)
   * [Key Features](#key-features)
   * [System Requirements](#system-requirements)
   * [Directory Structure](#directory-structure)
   * [Installation & Deployment](#installation--deployment)
   * [Troubleshooting](#troubleshooting)
2. [Dokumentasi Bahasa Indonesia](#-dokumentasi-bahasa-indonesia)
   * [Latar Belakang & Masalah](#latar-belakang--masalah)
   * [Fitur Unggulan](#fitur-unggulan)
   * [Persyaratan Sistem](#persyaratan-sistem)
   * [Panduan Instalasi & Deployment](#panduan-instalasi--deployment)
   * [Pemecahan Masalah (Troubleshooting)](#pemecahan-masalah-troubleshooting)
3. [Developer & Company Sign-Off / Pengesahan Resmi](#-developer--company-sign-off)

---

# 🌐 English Documentation

## Overview & The Problem
Deploying self-hosted, on-premise infrastructure (APIs, microservices, databases, or automation bots) at home or edge offices frequently suffers from sudden **mains electricity failure (blackouts)**. Without notice, sudden power cuts cause filesystem corruption, data loss, and severe SLA downtime. Commercial rackmount enterprise UPS hardware is expensive and bulky for lean operations.

`MD-Laptop-Server-UPS` bridges this issue by repurposing spare laptops running Linux (Ubuntu, Debian, or Armbian) into low-power edge nodes. Because laptops already house internal batteries, this daemon monitors the charging status via kernel ACPI sensors in real time. When mains power drops, an immediate priority notification is dispatched to your Telegram bot, allowing time for automated failover routing or graceful shutdowns.

## Key Features
* **Zero-Cost Built-In UPS:** Leverages hardware batteries without needing external UPS add-ons.
* **Kernel Glitch Tolerance:** Resilient against transient reading errors when power chargers are physically connected or disconnected.
* **Network Re-attempt Mechanism:** Features automated retry routines if the uplink router momentarily restarts during a power transfer.
* **Scalable Directory Architecture:** Organized following enterprise layout conventions (`config/`, `scripts/`, `static/`, `logs/`, `data/`).
* **Multi-Runtime Deployment:** Fully configured for native **Linux Systemd**, **PM2 Process Manager**, or standalone CLI execution.

## System Requirements
* Physical laptop with an active internal battery (Incompatible with Cloud VPS or standard desktop motherboards).
* Operating System: Ubuntu 20.04/22.04/24.04 LTS, Debian 11/12, or Armbian.
* Python 3.8 or newer with `python3-pip` and `python3-venv`.
* Uplink internet connectivity (A mobile 4G router/dongle or fiber modem connected to a 12V DC mini-UPS).

## Directory Structure
```text
md-laptop-server-ups/
├── config/
│   └── .env.example        # Configuration template
├── data/                   # Data storage for persistent metrics
├── logs/                   # Log output directory
├── output/                 # Script operational exports
├── scripts/
│   ├── install.sh          # Native Systemd auto-installer
│   └── md_ups_monitor.py   # Core monitoring engine
├── static/                 # Static web dashboard assets (assets, css, js)
├── ecosystem.config.js     # PM2 application runtime descriptor
├── README.md               # Bilingual documentation
├── requirements.txt        # Python dependency manifest
└── run.sh                  # Development execution entrypoint

Installation & Deployment
Step 1: Clone Repository
Bash

git clone [https://github.com/masdum-md/md-laptop-server-ups.git](https://github.com/masdum-md/md-laptop-server-ups.git)
cd md-laptop-server-ups

Step 2: Configure Environment

Copy the example environment file:
Bash

cp config/.env.example config/.env
nano config/.env

Provide your credentials inside config/.env:
Cuplikan kode

TELEGRAM_BOT_TOKEN="123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TELEGRAM_CHAT_ID="123456789"
POLL_INTERVAL_SEC=5

Step 3: Choose Your Deployment Method
Option A: Native Linux Service (Systemd) — Recommended for Production

Execute the automated installer with root privileges:
Bash

sudo chmod +x scripts/install.sh
sudo ./scripts/install.sh

    Start Service: sudo systemctl start md-ups

    Check Status: sudo systemctl status md-ups

    View Live Logs: sudo journalctl -u md-ups -f

    Stop Service: sudo systemctl stop md-ups

Option B: PM2 Process Manager — Recommended for Node.js / Python Devs
Bash

pip3 install -r requirements.txt
pm2 start ecosystem.config.js
pm2 save

    Check Status: pm2 status md-ups

    View Logs: pm2 logs md-ups

    Restart: pm2 restart md-ups

Option C: Manual Debugging / Development Mode
Bash

chmod +x run.sh
./run.sh

Troubleshooting

    Sensor Returns None: Ensure you are running on real laptop hardware. Virtual Machines and standard PC towers do not expose battery states via ACPI.

    Telegram Connection Timeout: Verify that the modem or access point routing traffic from the server remains powered by a mini-UPS during local outages.

🇮🇩 Dokumentasi Bahasa Indonesia
Latar Belakang & Masalah

Menjalankan infrastruktur server mandiri (on-premise / edge server) untuk kebutuhan otomasi, database, maupun web application sering kali terancam oleh satu masalah utama: pemadaman listrik mendadak oleh PLN.

Ketika aliran listrik padam seketika, server yang mati tanpa proses shutdown berisiko mengalami kerusakan berkas (corrupt filesystem), hilangnya basis data, serta putusnya SLA layanan bisnis. Membeli unit UPS komersial untuk kebutuhan server kecil sering kali membutuhkan biaya investasi yang mahal.

MD-Laptop-Server-UPS hadir sebagai solusi cerdas berbiaya nol rupiah (zero-cost solution) dengan memanfaatkan laptop bekas bersistem operasi Linux (Ubuntu, Debian, atau Armbian). Mengingat laptop secara fisik telah memiliki baterai internal, skrip ini memantau sensor daya secara real-time. Begitu charger kehilangan arus listrik, bot Telegram akan langsung mengirimkan peringatan darurat ke ponsel Anda sehingga penanganan sistem atau graceful shutdown dapat segera dilakukan.
Fitur Unggulan

    UPS Bawaan Tanpa Biaya Tambahan: Menyulap baterai internal laptop menjadi pengganti unit UPS cadangan.

    Kebal Terhadap Bug Sensor Driver: Memiliki penanganan khusus terhadap galat pembacaan sensor Linux ACPI sesaat ketika colokan charger dicabut atau dipasang.

    Percobaan Ulang Jaringan Otomatis: Dilengkapi proteksi pengiriman notifikasi berulang apabila router mengalami jeda restart saat peralihan daya.

    Struktur Folder Berskala Global: Arsitektur modular yang rapi (config/, scripts/, static/, dll.) yang siap dikembangkan ke arah web dashboard interaktif.

    Tiga Pilihan Operasional Fleksibel: Mendukung pemasangan via Systemd Service (standar Sysadmin Linux), PM2 Ecosystem (standar Developer Backend), dan Skrip Eksekusi Manual (run.sh).

Persyaratan Sistem

    Perangkat laptop fisik dengan kondisi baterai yang masih dapat menyimpan daya (Tidak berlaku untuk VPS atau PC Desktop).

    Sistem Operasi: Linux Ubuntu 20.04/22.04/24.04 LTS, Debian 11/12, atau Armbian Linux.

    Python versi 3.8 ke atas beserta modul python3-pip dan python3-venv.

    Cadangan koneksi internet aktif (Modem USB 4G, MiFi, atau router Wi-Fi yang ditenagai mini-UPS DC).

Panduan Instalasi & Deployment
Langkah 1: Klon Repositori
Bash

git clone [https://github.com/masdum-md/md-laptop-server-ups.git](https://github.com/masdum-md/md-laptop-server-ups.git)
cd md-laptop-server-ups

Langkah 2: Pengaturan Berkas Konfigurasi

Salin berkas contoh konfigurasi ke dalam folder config/:
Bash

cp config/.env.example config/.env
nano config/.env

Masukkan token bot dan chat ID Telegram Anda:
Cuplikan kode

TELEGRAM_BOT_TOKEN="123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TELEGRAM_CHAT_ID="123456789"
POLL_INTERVAL_SEC=5

Langkah 3: Pilih Metode Menjalankan Layanan
Opsi 1: Mode Layanan Linux (Systemd) — Rekomendasi Utama untuk Server Operasional

Jalankan skrip instalasi otomatis dengan akses root:
Bash

sudo chmod +x scripts/install.sh
sudo ./scripts/install.sh

    Menyalakan Service: sudo systemctl start md-ups

    Memeriksa Status: sudo systemctl status md-ups

    Melihat Log Real-time: sudo journalctl -u md-ups -f

    Mematikan Service: sudo systemctl stop md-ups

Opsi 2: Mode PM2 Process Manager — Rekomendasi Developer Backend / Node.js
Bash

pip3 install -r requirements.txt
pm2 start ecosystem.config.js
pm2 save

    Cek Status Proses: pm2 status md-ups

    Melihat Log Aktivitas: pm2 logs md-ups

    Restart Layanan: pm2 restart md-ups

Opsi 3: Mode Eksekusi Manual / Uji Coba Pengembang
Bash

chmod +x run.sh
./run.sh

Pemecahan Masalah (Troubleshooting)

    Pesan "Baterai Tidak Terdeteksi": Pastikan perangkat keras yang digunakan adalah unit laptop fisik dengan modul baterai yang terpasang dan dikenali oleh kernel Linux.

    Notifikasi Gagal Terkirim ke Telegram: Pastikan perangkat perantara internet (router, switch, atau modem) tidak mati saat listrik padam, atau gunakan modem seluler USB mini yang langsung tertancap pada port USB laptop server.

📄 Lisensi (License)

Didistribusikan di bawah lisensi resmi MIT License. Bebas digunakan, dipelajari, dimodifikasi, dan diterapkan untuk kepentingan personal maupun infrastruktur komersial.
✒️ Developer & Company Sign-Off

© 2026 PT MDIGITAL DINAMIKA SISTEM. All rights reserved.

Designed with precision for open-source high availability engineering.