# -*- coding: utf-8 -*-
# test.py
import os
import requests

# 获取环境变量
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
wallet_addresses = os.getenv("WALLET_ADDRESSES", "").split(",")

def test_telegram():
print(" 正在测试 Telegram 推送功能...")
url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
payload = {
"chat_id": chat_id,
"text": "✅ Telegram 推送测试成功！"
}
try:
res = requests.post(url, json=payload)
res.raise_for_status()
print("✅ Telegram 消息成功发送！")
except Exception as e:
print(" Telegram 推送失败：", e)

def test_hyperliquid():
print(" 正在测试 Hyperliquid API...")
test_address = wallet_addresses[0] if wallet_addresses[0] else "0x0000000000000000000000000000000000000000"
url = "https://api.hyperliquid.xyz/info"
payload = {
"type": "user",
"user": test_address
}
try:
res = requests.post(url, json=payload)
res.raise_for_status()
data = res.json()
if "assetPositions" in data:
print(f"✅ Hyperliquid 地址查询成功：{test_address}")
else:
print("️ Hyperliquid 返回了无效结构，请检查地址是否有效")
except Exception as e:
print(" Hyperliquid 请求失败：", e)

if __name__ == "__main__":
test_telegram()
print()
test_hyperliquid()
