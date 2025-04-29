# -*- coding: utf-8 -*-
import requests
import time
import os

# 从环境变量中获取配置
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
WALLET_ADDRESSES = os.environ.get("WALLET_ADDRESSES", "").split(",")

# 发送 Telegram 消息
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
    "chat_id": TELEGRAM_CHAT_ID,
    "text": message
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
    except Exception as e:
        print(f"Telegram error: {e}")

# 获取成交数据
def get_trade_data(wallet):
    try:
        url = f"https://api.hyperliquid.xyz/info/userFills?user={wallet.strip()}"
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.json()
        else:
            print(f"请求失败: {resp.status_code}")
            return None
    except Exception as e:
        print(f"获取数据失败: {e}")
        return None

# 记录每个地址的最后成交 ID
last_trade_ids = {}

def monitor_wallets():
    print(f"Started monitoring addresses: {WALLET_ADDRESSES}")
    while True:
        for wallet in WALLET_ADDRESSES:
            trade_data = get_trade_data(wallet)
            if not trade_data:
                continue

            if len(trade_data) == 0:
                continue

            latest_trade = trade_data[0]
            latest_id = latest_trade.get("fillId")

            if wallet not in last_trade_ids:
                last_trade_ids[wallet] = latest_id
                continue

            if latest_id != last_trade_ids[wallet]:
                last_trade_ids[wallet] = latest_id
                price = latest_trade.get("price")
                qty = latest_trade.get("base")
                side = latest_trade.get("side")
                coin = latest_trade.get("coin")
                time_ms = latest_trade.get("time")
                ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time_ms) / 1000))

                message = (
                f"【成交推送】\n"
                f"地址：{wallet}\n"
                f"时间：{ts}\n"
                f"交易对：{coin}\n"
                f"方向：{'买入' if side == 'buy' else '卖出'}\n"
                f"价格：{price}\n"
                f"数量：{qty}"
                )
                print(f"New trade for {wallet}: {message}")
                send_telegram_message(message)

        time.sleep(3)

if __name__ == "__main__":
    monitor_wallets()
