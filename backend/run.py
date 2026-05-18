#!/usr/bin/env python3
"""
CropSense One-Command Runner
Installs deps, trains model if missing, starts Flask dev server.
"""

import os
import sys
import subprocess
import venv
import joblib
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
VENV_DIR = BASE_DIR / "venv"
MODEL_PATH = BASE_DIR / "crop_model.pkl"
DATASET_PATH = BASE_DIR / "dataset" / "crop_data.csv"

def print_step(msg):
    print(f"🌱 {msg}")

def run_command(cmd, cwd=None, check=True):
    """Run shell command."""
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=check, shell=True if os.name == 'nt' else False)

# 1. Create venv if missing
if not VENV_DIR.exists():
    print_step("Creating virtual environment...")
    venv.create(VENV_DIR, with_pip=True)

# 2. Activate venv & upgrade pip
python_exe = VENV_DIR / "Scripts" / "python.exe" if os.name == 'nt' else VENV_DIR / "bin" / "python"
pip_exe = VENV_DIR / "Scripts" / "pip.exe" if os.name == 'nt' else VENV_DIR / "bin" / "pip"

run_command([str(pip_exe), "install", "--upgrade", "pip"], check=True)

# 3. Install requirements
print_step("Installing dependencies...")
run_command([str(pip_exe), "install", "python-dotenv", "-r", str(BASE_DIR / "requirements.txt")])


# 4. Check/train model
if not MODEL_PATH.exists():
    print_step("Training ML model (crop_model.pkl)...")
    run_command([str(python_exe), "model.py"], cwd=BASE_DIR)
else:
    print_step("Model already exists ✓")

# 5. Copy .env if missing
env_path = BASE_DIR / ".env"
if not env_path.exists():
    print_step("Creating .env from example...")
    (BASE_DIR / ".env.example").write_text(env_path.read_text())
    print("ℹ️  Edit backend/.env with your Gmail credentials for contact form.")

print_step("🚀 Starting Flask dev server on http://localhost:5000")
print("Press Ctrl+C to stop.")

# 6. Start app
run_command([str(python_exe), "app.py"], cwd=BASE_DIR)

