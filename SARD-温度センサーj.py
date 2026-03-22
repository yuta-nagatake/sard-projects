import machine
import time
import os

# I2Cの設定（今の成功している設定です）
i2c = machine.I2C(0, sda=machine.Pin(8), scl=machine.Pin(9), freq=100000)

def get_temp(reg):
    try:
        data = i2c.readfrom_mem(0x5a, reg, 2)
        temp = (data[1] << 8) | data[0]
        return temp * 0.02 - 273.15
    except:
        return None

# --- ファイル名の連番を決める処理 ---
file_index = 1
while True:
    filename = "data_{}.txt".format(file_index)
    try:
        os.stat(filename)
        file_index += 1
    except OSError:
        break

print("保存開始: {} (停止ボタンで安全に終了します)".format(filename))

# --- メインの測定ループ ---
try:
    with open(filename, "w") as f:
        f.write("count, object_temp, ambient_temp\n") # 見出し
        count = 1
        while True:
            obj_temp = get_temp(0x07)
            amb_temp = get_temp(0x06)
            
            if obj_temp is not None:
                # 画面とファイルの両方に書き出す
                data_line = "{}, {:.2f}, {:.2f}".format(count, obj_temp, amb_temp)
                print(data_line)
                f.write(data_line + "\n")
                
                # 重要：これを入れると止めた瞬間のデータも保存されやすくなります
                f.flush() 
                
                count += 1
            time.sleep(1) # 1秒ごとに計測
            
except KeyboardInterrupt:
    # 停止ボタン（■）を押した時にここが動きます
    print("\n停止ボタンが押されました。プログラムを終了します。")