
import machine
import time

# GP26をアナログ入力に設定
ph_pin = machine.ADC(26)

while True:
    # ADC値を取得
    value = ph_pin.read_u16()

    # 電圧に変換
    voltage = value * 3.3 / 65535

    print("ADC:", value)
    print("電圧:", round(voltage, 3), "V")

    time.sleep(1)
