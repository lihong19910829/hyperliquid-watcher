# -*- coding: utf-8 -*-
import requests
import json
import time

# ===== 你需要自定义的参数 =====
TELEGRAM_BOT_TOKEN = "8015236527:AAFXe3h5kaxjeF4QSaX3HWtbLKcpzUzgk2w"
TELEGRAM_CHAT_ID = "6399122975"
MONITORED_ADDRESSES = [
"0x1c95463aec3666f5f766aed360de86b56110d18f",
# 可添加多个地址
]

# ===== 函数：获取指定地址的成交记录 =====
def get_user_fills(address):
url = "https://api.hyperliquid.xyz/info"
headers = {"Content-Type": "application/json"}
data = {
"type": "userFills",
"user": address
}
try:
response = requests.post(url, headers=headers, data=json.dumps(data))
response.raise_for_status()
return response.json()
except Exception as e:
print(f"[请求失败] Address: {address}, 错误: {e}")
return None

# ===== 函数：推送 Telegram 消息 =====
def send_telegram_message(message):
url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
try:
requests.post(url, json=payload)
print("[已发送] Telegram:", message)
except Exception as e:
print(f"[发送失败] Telegram 错误: {e}")

# ===== 主逻辑 =====
def main():
last_fill_ids = {}

while True:
for address in MONITORED_ADDRESSES:
result = get_user_fills(address)
if result and "data" in result and len(result["data"]) > 0:
latest_fill = result["data"][0]
fill_id = latest_fill.get("fillId", str(latest_fill)) # 取唯一标识避免重复

if address not in last_fill_ids or last_fill_ids[address] != fill_id:
last_fill_ids[address] = fill_id
message = f"地址 {address} 有新成交：\n{json.dumps(latest_fill, indent=2)}"
send_telegram_message(message)
else:
print(f"[无新成交] {address}")
else:
print(f"[无数据] {address}")

time.sleep(10) # 每 10 秒轮询一次

if __name__ == "__main__":
main()
