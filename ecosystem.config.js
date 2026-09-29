const path = require("path");
const fs = require("fs");

const projectRoot = __dirname;
const venvPython = path.join(projectRoot, "venv", "bin", "python3");
const interpreterPath = fs.existsSync(venvPython) ? venvPython : "python3";

module.exports = {
  apps: [{
    name: "md-ups",
    script: path.join(projectRoot, "scripts", "md_ups_monitor.py"),
    cwd: projectRoot,
    interpreter: interpreterPath,
    autorestart: true,
    watch: false,
    max_memory_restart: "100M",
    env: {
      POWER_MONITOR_ENV: path.join(projectRoot, "config", ".env")
    }
  }]
};