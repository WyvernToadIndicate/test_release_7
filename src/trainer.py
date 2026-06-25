# trainer.py
import time
import logging
from memory import Memory
from utils import sleep_ms, current_timestamp
import config

class Trainer:
    def __init__(self, process_name):
        self.mem = Memory(process_name)
        self.logger = logging.getLogger(__name__)
        self.running = False
        self.features = {
            "sniper": False,
            "auto_sell": False,
            "mev_protection": False,
            "multi_wallet": False,
            "telegram_alerts": False,
            "price_monitor": False
        }
        self.offsets = config.OFFSETS

    def toggle_feature(self, feature_name):
        if feature_name in self.features:
            self.features[feature_name] = not self.features[feature_name]
            status = "ON" if self.features[feature_name] else "OFF"
            self.logger.info(f"{feature_name} {status}")
            return True
        return False

    def sniper_mode(self):
        self.logger.info("Sniper mode active")
        while self.running and self.features["sniper"]:
            price = self.mem.read_int(self.offsets.get("token_price", 0x34))
            if price < 10:
                self._buy_token(price)
            sleep_ms(500)

    def auto_sell(self):
        self.logger.info("Auto-sell active")
        while self.running and self.features["auto_sell"]:
            balance = self.mem.read_int(self.offsets.get("player_balance", 0x30))
            price = self.mem.read_int(self.offsets.get("token_price", 0x34))
            if price > config.TAKE_PROFIT * 100:
                self._sell_token()
            elif price < config.STOP_LOSS * 100:
                self._sell_token()
            sleep_ms(1000)

    def mev_protection(self):
        self.logger.info("MEV protection active")
        while self.running and self.features["mev_protection"]:
            self.mem.write_int(self.offsets.get("mev_gas", 0x40), config.MEV_GAS_LIMIT)
            sleep_ms(2000)

    def multi_wallet(self):
        self.logger.info("Multi-wallet management active")
        while self.running and self.features["multi_wallet"]:
            self.logger.debug("Switching wallets...")
            sleep_ms(5000)

    def telegram_alerts(self):
        self.logger.info("Telegram alerts active")
        while self.running and self.features["telegram_alerts"]:
            self._send_telegram("Heartbeat")
            sleep_ms(10000)

    def price_monitor(self):
        self.logger.info("Price monitor active")
        while self.running and self.features["price_monitor"]:
            price = self.mem.read_int(self.offsets.get("token_price", 0x34))
            volume = self.mem.read_int(self.offsets.get("token_volume", 0x38))
            self.logger.info(f"Price: {price}, Volume: {volume}")
            sleep_ms(3000)

    def _buy_token(self, price):
        self.logger.info(f"Buying token at price {price}")
        balance = self.mem.read_int(self.offsets.get("player_balance", 0x30))
        self.mem.write_int(self.offsets.get("player_balance", 0x30), balance - 1)

    def _sell_token(self):
        self.logger.info("Selling token")
        balance = self.mem.read_int(self.offsets.get("player_balance", 0x30))
        self.mem.write_int(self.offsets.get("player_balance", 0x30), balance + 1)

    def _send_telegram(self, msg):
        if config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHAT_ID:
            self.logger.info(f"Telegram: {msg}")
        else:
            self.logger.debug("Telegram not configured")

    def start(self):
        self.running = True
        self.logger.info("Trainer started")

    def stop(self):
        self.running = False
        self.mem.close()
        self.logger.info("Trainer stopped")
