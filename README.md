# 🔋 MD-Laptop-Server-UPS

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Deployment](https://img.shields.io/badge/deployment-Systemd%20%7C%20PM2-orange.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20(Ubuntu%20%7C%20Debian%20%7C%20Armbian)-lightgrey.svg)
![Author](https://img.shields.io/badge/developer-Mas%20Dum-blueviolet.svg)
![Infrastructure](https://img.shields.io/badge/infrastructure-PT%20Mdigital%20Dinamika%20Sistem-purple.svg)

A lightweight Linux background daemon that converts spare laptops into robust on-premise servers by utilizing internal battery packs as automated, Telegram-alerted UPS systems.

---

## 🌐 English Documentation

### 📌 Overview & The Problem
Deploying self-hosted, on-premise infrastructure at home or edge offices frequently suffers from sudden mains electricity failure (blackouts). Sudden power cuts cause filesystem corruption, data loss, and severe SLA downtime. Commercial rackmount enterprise UPS hardware is expensive and bulky for lean operations.

`MD-Laptop-Server-UPS` bridges this issue by repurposing spare laptops running Linux into low-power edge nodes. Because laptops already house internal batteries, this daemon monitors the charging status via kernel ACPI sensors in real time. When mains power drops, an immediate priority notification is dispatched to your Telegram bot, allowing time for automated failover routing or graceful shutdowns.

### 🌟 Key Features
* **Zero-Cost Built-In UPS:** Leverages hardware batteries without needing external UPS add-ons.
* **Kernel Glitch Tolerance:** Resilient against transient reading errors when power chargers are physically connected or disconnected.
* **Network Re-attempt Mechanism:** Automated retry routines ensure alerts reach Telegram even if the router restarts during power switching.
* **Scalable Directory Architecture:** Modular layout prepared for future web dashboards (`config/`, `scripts/`, `static/`, `logs/`, `data/`).
* **Multi-Runtime Deployment:** Fully configured for native **Linux Systemd**, **PM2 Process Manager**, or standalone CLI execution.

### 🛠️ System Requirements
* Physical laptop with an active internal battery (Incompatible with Cloud VPS or standard desktop motherboards).
* Operating System: Ubuntu (20.04/22.04/24.04 LTS), Debian (11/12), or Armbian.
* Python 3.8 or newer with `python3-pip` and `python3-venv`.
* Uplink internet connectivity (A mobile 4G router/dongle or fiber modem connected to a mini-UPS).

### 🚀 Installation & Deployment

#### 1. Clone & Configuration
```bash
git clone https://github.com/masdum-md/md-laptop-server-ups.git
cd md-laptop-server-ups
cp config/.env.example config/.env
nano config/.env
```

#### 2. Choose Deployment Mode

* **Option A: Native Linux Service (Systemd)**
  ```bash
  sudo chmod +x scripts/install.sh
  sudo ./scripts/install.sh
  ```
  Commands: `sudo systemctl start md-ups` | `sudo systemctl status md-ups`

* **Option B: PM2 Process Manager**
  ```bash
  pip3 install -r requirements.txt
  pm2 start ecosystem.config.js
  pm2 save
  ```
  Commands: `pm2 status md-ups` | `pm2 logs md-ups`

* **Option C: Manual / Debug Mode**
  ```bash
  chmod +x run.sh
  ./run.sh
  ```

---

# 🇮🇩 Dokumentasi Bahasa Indonesia

## 📌 Latar Belakang & Masalah
Menjalankan server mandiri (*on-premise / edge server*) untuk kebutuhan otomasi dan basis data lokal sering kali terancam oleh pemadaman listrik mendadak dari PLN. Server yang mati tiba-tiba tanpa proses *shutdown* berisiko mengalami kerusakan berkas (*corrupt filesystem*) dan terhentinya SLA operasional. Membeli unit UPS server profesional sering kali membutuhkan biaya investasi yang tinggi.

`MD-Laptop-Server-UPS` hadir sebagai solusi berbiaya nol rupiah dengan memanfaatkan laptop bekas bersistem operasi Linux. Karena laptop telah dibekali baterai internal, skrip ini memantau sensor arus pengisi daya secara *real-time*. Begitu pasokan listrik terputus, bot Telegram akan langsung mengirimkan peringatan darurat ke ponsel Anda, memberikan jeda waktu aman (*grace period*) untuk melakukan pemindahan jalur (*failover*) maupun mematikan sistem secara aman (*graceful shutdown*).

---

## 🌟 Fitur Unggulan
* **UPS Bawaan Tanpa Biaya:** Mengoptimalkan baterai fisik laptop sebagai unit penyimpan daya darurat.
* **Tahan Glitch Sensor Driver:** Kebal terhadap pembacaan keliru sesaat pada driver ACPI kernel Linux ketika soket charger dicabut atau ditancapkan.
* **Auto-Retry Jaringan:** Dilengkapi mekanisme pengiriman notifikasi berulang jika router sempat mengalami *restart* saat listrik padam.
* **Struktur Folder Skala Enterprise:** Arsitektur modular yang rapi dan terisolasi, siap dikembangkan ke arah web dashboard interaktif.
* **Dukungan Multi-Runtime:** Mendukung instalasi sebagai **Systemd Service** (standar Linux), **PM2 Process Manager**, maupun pengeksekusian langsung via skrip `run.sh`.

---

## 🛠️ Persyaratan Sistem
* Unit laptop fisik dengan kondisi baterai yang masih berfungsi menyimpan daya (Tidak berlaku untuk VPS atau PC Desktop).
* Sistem Operasi: Linux Ubuntu (20.04/22.04/24.04 LTS), Debian (11/12), atau Armbian.
* Python versi 3.8 ke atas beserta modul `python3-pip` dan `python3-venv`.
* Cadangan koneksi internet aktif (Modem USB 4G, MiFi, atau router Wi-Fi yang ditenagai mini-UPS DC).

---

## 🚀 Panduan Instalasi & Deployment

### Langkah 1: Klon Repositori & Konfigurasi
```bash
git clone https://github.com/masdum-md/md-laptop-server-ups.git
cd md-laptop-server-ups
cp config/.env.example config/.env
nano config/.env
```
*(Atur `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, dan `POLL_INTERVAL_SEC` di dalam berkas `config/.env`).*

---

### Langkah 2: Pilih Metode Deployment

#### Opsi 1: Mode Layanan Linux (Systemd) — *Disarankan untuk Server Operasional*
```bash
sudo chmod +x scripts/install.sh
sudo ./scripts/install.sh
```
* **Menyalakan Service:** `sudo systemctl start md-ups`
* **Memeriksa Status:** `sudo systemctl status md-ups`
* **Melihat Log Real-time:** `sudo journalctl -u md-ups -f`
* **Mematikan Service:** `sudo systemctl stop md-ups`

#### Opsi 2: Mode PM2 Process Manager — *Disarankan untuk Developer Node.js / Python*
```bash
pip3 install -r requirements.txt
pm2 start ecosystem.config.js
pm2 save
```
* **Cek Status Proses:** `pm2 status md-ups`
* **Melihat Log Aktivitas:** `pm2 logs md-ups`
* **Restart Layanan:** `pm2 restart md-ups`

#### Opsi 3: Mode Eksekusi Manual / Pengujian
```bash
chmod +x run.sh
./run.sh
```

---

## 🔧 Pemecahan Masalah (Troubleshooting)
* **Error "Baterai Tidak Terdeteksi":** Pastikan perangkat keras adalah unit laptop fisik dengan modul baterai yang terpasang dan terbaca oleh sistem operasi Linux.
* **Notifikasi Gagal Terkirim:** Pastikan jalur akses internet (router/modem) tetap memiliki daya saat listrik padam (misalnya menggunakan modem seluler USB yang tertancap langsung di laptop).

---

## 📄 Lisensi
Didistribusikan di bawah lisensi resmi **MIT License**. Bebas dimodifikasi, didistribusikan, dan diterapkan untuk proyek personal maupun komersial.

---

## ✒️ Legalitas & Pengesahan Proyek

| Peran | Entitas | Deskripsi & Tautan |
| :--- | :--- | :--- |
| **Lead Developer & Architect** | **Makhdum Ibrahim (Mas Dum)** | Infrastructure & Automation Engineer<br>GitHub: [@masdum-md](https://github.com/masdum-md) |
| **Corporate Legal Owner** | **PT MDIGITAL DINAMIKA SISTEM** | IT Operations, Network SLA, Web Infra & RPA<br>Website: [www.mdigital.co.id](https://www.mdigital.co.id) |

<br>

<div align="center">
  <sub><b>© 2026 PT Mdigital Dinamika Sistem. All rights reserved.</b></sub><br>
  <sup>Designed with precision for open-source high availability engineering.</sup>
</div>
