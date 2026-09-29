import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from pathlib import Path

# Add project root and scripts dir to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import md_ups_monitor


class TestMDUPSMonitor(unittest.TestCase):

    @patch("requests.post")
    def test_notify_telegram_success(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_post.return_value = mock_resp

        with patch.object(md_ups_monitor, "BOT_TOKEN", "fake_token"), \
             patch.object(md_ups_monitor, "CHAT_ID", "12345"):
            result = md_ups_monitor.notify_telegram("Test message")
            self.assertTrue(result)
            mock_post.assert_called_once()

    @patch("requests.post")
    def test_notify_telegram_retry_then_fail(self, mock_post):
        import requests
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")

        with patch.object(md_ups_monitor, "BOT_TOKEN", "fake_token"), \
             patch.object(md_ups_monitor, "CHAT_ID", "12345"):
            result = md_ups_monitor.notify_telegram("Test message", retries=2, delay=0.1)
            self.assertFalse(result)
            self.assertEqual(mock_post.call_count, 2)

    def test_notify_telegram_missing_credentials(self):
        with patch.object(md_ups_monitor, "BOT_TOKEN", None), \
             patch.object(md_ups_monitor, "CHAT_ID", None):
            result = md_ups_monitor.notify_telegram("Test message")
            self.assertFalse(result)

    @patch("psutil.sensors_battery")
    def test_read_battery_laptop(self, mock_battery):
        mock_bat = MagicMock()
        mock_bat.power_plugged = True
        mock_bat.percent = 85
        mock_battery.return_value = mock_bat

        plugged, pct = md_ups_monitor.read_battery()
        self.assertTrue(plugged)
        self.assertEqual(pct, 85)

    @patch("psutil.sensors_battery")
    def test_read_battery_none(self, mock_battery):
        mock_battery.return_value = None
        plugged, pct = md_ups_monitor.read_battery()
        self.assertIsNone(plugged)
        self.assertIsNone(pct)


if __name__ == "__main__":
    unittest.main()
