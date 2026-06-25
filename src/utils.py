# utils.py
import time
import logging
from datetime import datetime

def setup_logging(log_file, level="INFO"):
    logging.basicConfig(
        filename=log_file,
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger()

def sleep_ms(ms):
    time.sleep(ms / 1000.0)

def current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))
