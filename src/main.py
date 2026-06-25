# main.py
import sys
import time
import logging
import ctypes
from ctypes import wintypes
import config
from utils import setup_logging
from trainer import Trainer

logger = setup_logging(config.LOG_FILE, config.LOG_LEVEL)

PROCESS_NAME = "game.exe"

def register_hotkeys(trainer):
    user32 = ctypes.windll.user32
    for i, key in enumerate(config.HOTKEYS, start=1):
        vk = 0x70 + (i-1)
        mod = 0
        if not user32.RegisterHotKey(None, i, mod, vk):
            logger.error(f"Не удалось зарегистрировать {key}")
        else:
            logger.info(f"Горячая клавиша {key} зарегистрирована")

    msg = wintypes.MSG()
    while True:
        if user32.GetMessageA(ctypes.byref(msg), None, 0, 0):
            if msg.message == 0x0312:
                hotkey_id = msg.wParam
                feature_names = list(trainer.features.keys())
                if 1 <= hotkey_id <= len(feature_names):
                    trainer.toggle_feature(feature_names[hotkey_id-1])
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageA(ctypes.byref(msg))
        else:
            break

def main():
    try:
        trainer = Trainer(PROCESS_NAME)
        trainer.start()
        logger.info("Трейнер запущен. Используйте F1-F6 для включения/выключения функций.")
        print("Trainer is running. Press F1-F6 to toggle features. Close the window to stop.")
        register_hotkeys(trainer)
    except Exception as e:
        logger.exception("Ошибка в main")
        print(f"Error: {e}")
    finally:
        trainer.stop()

if __name__ == "__main__":
    main()
