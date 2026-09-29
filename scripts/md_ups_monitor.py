import os
import sys
import time
import signal
from pathlib import Path
from datetime import datetime
import psutil
import requests
from dotenv import load_dotenv

# ==============================================================================
# CONFIG & ENV LOADER / PENGATURAN JALUR KONFIGURASI BARU
# ==============================================================================
# Resolving paths based on new global structure (Menyesuaikan dengan struktur folder baru)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DEFAULT_ENV_PATH = PROJECT_ROOT / "config" / ".env"

ENV_FILE = os.getenv("POWER_MONITOR_ENV", DEFAULT_ENV_PATH)

if Path(ENV_FILE).exists():
    load_dotenv(dotenv_path=ENV_FILE)
else:
    print(f"[!] Warning: Config file not found at {ENV_FILE} / File config tidak ditemukan.")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL_SEC", 5))

# ==============================================================================
# GRACEFUL SHUTDOWN
# ==============================================================================
running = True

def handle_exit(signum, frame):
    """Handle termination signals safely / Tangani sinyal berhenti dengan aman."""
    global running
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n[{now_str}] [EN] Stopping MD-UPS daemon...")
    print(f"[{now_str}] [ID] Menghentikan daemon MD-UPS...")
    running = False

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

def notify_telegram(text: str, retries: int = 3, delay: int = 3) -> bool:
    """Send Telegram alert with auto-retry / Kirim notifikasi dengan percobaan ulang."""
    if not BOT_TOKEN or not CHAT_ID:
        print("[ERR] Token Bot / Chat ID Telegram belum dikonfigurasi.")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}

    for attempt in range(1, retries + 1):
        try:
            res = requests.post(url, json=payload, timeout=8)
            if res.status_code == 200:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] [OK] Notifikasi terkirim.")
                return True
        except requests.exceptions.RequestException as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] [RETRY {attempt}/{retries}] Jaringan fluktuatif: {e}")
            if attempt < retries: time.sleep(delay)
    return False

def read_battery():
    """Read battery status via psutil / Baca status baterai."""
    try:
        battery = psutil.sensors_battery()
        if battery is None: return None, None
        return battery.power_plugged, int(battery.percent)
    except Exception:
        return None, None

def main():
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{start_time}] [ID] Layanan Monitor MD-UPS Resmi Dimulai (Global Structure)...")

    init_state, init_pct = read_battery()
    if init_state is None:
        print("[KRITIS] Baterai tidak terdeteksi! Skrip ini wajib dijalankan pada perangkat berbaterai.")
        sys.exit(1)

    node_name = os.uname().nodename
    notify_telegram(f"🔌 *MD-UPS Monitor Active*\nServer Node: `{node_name}`\nKapasitas Awal: *{init_pct}%*")
    last_state = init_state

    while running:
        current_state, current_pct = read_battery()

        if current_state is None:
            time.sleep(1)
            continue

        if current_state != last_state:
            now_str = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            if not current_state:
                msg = (
                    "⚠️ *URGENT BOSKU: LISTRIK PADAM!*\n"
                    "================================\n"
                    f"⏰ Waktu: `{now_str}`\n"
                    f"🖥️ Server: `{node_name}`\n"
                    "⚡ Status: *PLN OFF (Running Battery & UPS)*\n"
                    f"🔋 Sisa Baterai: *{current_pct}%*\n"
                    "================================"
                )
            else:
                msg = (
                    "✅ *INFO BOSKU: LISTRIK KEMBALI NORMAL*\n"
                    "================================\n"
                    f"⏰ Waktu: `{now_str}`\n"
                    f"🖥️ Server: `{node_name}`\n"
                    "⚡ Status: *PLN ON (AC Power Connected)*\n"
                    f"🔋 Kapasitas Baterai: *{current_pct}%*\n"
                    "☕ Lanjut ngopi bosku."
                )
            success = notify_telegram(msg)
            if success:
                last_state = current_state
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] [WARN] Notifikasi perubahan status gagal terkirim. Akan dicoba ulang pada iterasi berikutnya.")

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()