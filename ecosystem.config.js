module.exports = {
  apps: [{
    name: "md-ups",
    script: "./scripts/md_ups_monitor.py",
    interpreter: "python3",
    autorestart: true,
    watch: false,
    max_memory_restart: "100M",
    env: {
      POWER_MONITOR_ENV: "./config/.env"
    }
  }]
};