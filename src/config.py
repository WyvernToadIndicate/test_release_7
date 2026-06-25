# config.py
import os
import json

APP_NAME = "PumpFun"
VERSION = "1.0"
AUTHOR = "Anonymous"

HOTKEYS = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6']

OFFSETS_FILE = os.path.join(os.path.dirname(__file__), "offsets.json")

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "trainer.log")
LOG_LEVEL = "INFO"

SNIPE_AMOUNT = 0.1
TAKE_PROFIT = 0.2
STOP_LOSS = 0.05
MEV_GAS_LIMIT = 200000

TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""

with open(OFFSETS_FILE, 'r') as f:
    OFFSETS = json.load(f)
