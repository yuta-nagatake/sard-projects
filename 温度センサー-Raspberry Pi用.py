import glob
import time

# DS18B20のデバイスを検索
devices = glob.glob('/sys/bus/w1/devices/28-*')

if not devices:
    print("DS18B20が見つかりません")
else:
    device_file = devices[0] + '/w1_slave'

    while True:
        with open(device_file, 'r') as f:
            lines = f.readlines()

        if lines[0].strip()[-3:] == 'YES':
            pos = lines[1].find('t=')

            if pos != -1:
                temperature = float(lines[1][pos+2:]) / 1000
                print(f"温度: {temperature:.2f} ℃")

        else:
            print("温度データの読み取りに失敗")

        time.sleep(2)