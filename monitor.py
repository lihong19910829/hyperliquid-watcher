import requests
import time
import os

# ������ַ�б���������չ��
TARGET_ADDRESSES = [
"0x1c95463aec3666f5f766aed360de86b56110d18f"
# ������
]

# Telegram����
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# �ϴγɽ���¼
last_fill_ids = {address: None for address in TARGET_ADDRESSES}

def send_telegram_message(text):
url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
requests.post(url, data=payload)

def check_fills(address):
url = "https://api.hyperliquid.xyz/info/fills"
data = {"user": address}
res = requests.post(url, json=data).json()
fills = res.get("fills", [])

if not fills:
return

latest_fill = fills[0]
fill_id = latest_fill.get("orderId")

if fill_id != last_fill_ids[address]:
last_fill_ids[address] = fill_id
side = latest_fill.get("side")
coin = latest_fill.get("coin")
price = latest_fill.get("price")
sz = latest_fill.get("sz")
message = f"[Hyperliquid �ɽ�����]\n��ַ: {address}\n����: {side}\n����: {coin}\n�۸�: {price}\n����: {sz}"
send_telegram_message(message)

def main():
while True:
try:
for address in TARGET_ADDRESSES:
check_fills(address)
except Exception as e:
print(f"������: {e}")
time.sleep(5)

if __name__ == "__main__":
main()