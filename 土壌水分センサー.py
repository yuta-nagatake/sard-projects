import time
from machine import ADC, Pin

# GP26 (ADC0) を読み取り
sensor = ADC(Pin(26))

print("--- 測定開始 ---")
while True:
    raw = sensor.read_u16()          # 0 〜 65535
    voltage = raw * (3.3 / 65535)   # 電圧(V)
    print(f"RAW値: {raw:5d} | 電圧: {voltage:.2f}V")
    time.sleep(0.5)