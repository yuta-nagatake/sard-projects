import time
from machine import ADC, Pin

# ==========================================
# 1. ピン設定
# ==========================================
PIN_CLK = 18    # C12880MA 3番ピン (CLK)
PIN_ST = 19     # C12880MA 4番ピン (ST)
PIN_VIDEO = 26  # C12880MA 6番ピン (VIDEO -> 分圧回路経由 -> GP26)

clk = Pin(PIN_CLK, Pin.OUT, value=0)
st = Pin(PIN_ST, Pin.OUT, value=0)
video = ADC(Pin(PIN_VIDEO))

CHANNELS = 288

# ==========================================
# 2. 波長校正係数（検査成績書の値に書き換える）
# ==========================================
# ※下記はC12880MAの一般的な標準例です。
#   袋に入っている検査成績書の A0, B1, B2, B3, B4, B5 を転記してください。
A0 = 310.0
B1 = 2.68
B2 = -1.10e-3
B3 = -7.50e-6
B4 = 1.60e-8
B5 = -1.20e-11


def calc_wavelengths():
    """288ピクセルそれぞれの対応波長(nm)を事前計算する"""
    wl = []
    for x in range(CHANNELS):
        val = (
            A0
            + B1 * x
            + B2 * (x**2)
            + B3 * (x**3)
            + B4 * (x**4)
            + B5 * (x**5)
        )
        wl.append(round(val, 2))
    return wl


# 起動時に波長配列を作成
WAVELENGTHS = calc_wavelengths()


# ==========================================
# 3. 分光器 読み取り関数
# ==========================================
def read_spectrometer(integration_time_us=5000):
    """C12880MAから288画素分の強度(0-65535)を取得

    integration_time_us: 露光時間(us)。光が弱い場合は増やす(例: 50000)
    """
    data = [0] * CHANNELS

    # 1. スタートパルスと露光開始
    clk.value(1)
    time.sleep_us(1)
    clk.value(0)
    st.value(1)
    time.sleep_us(1)

    # 露光開始クロック (3クロック分)
    for _ in range(3):
        clk.value(1)
        time.sleep_us(1)
        clk.value(0)
        time.sleep_us(1)

    # 指定した露光時間だけ電荷を蓄積
    time.sleep_us(integration_time_us)

    # 2. STをLowにして読み出し開始
    st.value(0)

    # 仕様書規定のダミークロック (87クロック分スキップ)
    for _ in range(87):
        clk.value(1)
        time.sleep_us(1)
        clk.value(0)
        time.sleep_us(1)

    # 3. 288ピクセルのVIDEO出力を順次ADCサンプリング
    for i in range(CHANNELS):
        clk.value(1)
        time.sleep_us(1)
        data[i] = video.read_u16()
        clk.value(0)
        time.sleep_us(1)

    # 終了処理用ダミークロック
    for _ in range(10):
        clk.value(1)
        time.sleep_us(1)
        clk.value(0)
        time.sleep_us(1)

    return data


# ==========================================
# 4. メイン実行ループ
# ==========================================
print("--- C12880MA 分光測定開始 ---")
# 1行目に波長(nm)のヘッダをCSV形式で出力
print("Wavelength_nm," + ",".join(map(str, WAVELENGTHS)))

while True:
    # 露光時間 10000us (10ms) で取得
    spectrum = read_spectrometer(integration_time_us=10000)

    # 2行目以降に各波長の強度値をCSV形式で出力
    print("Intensity," + ",".join(map(str, spectrum)))

    time.sleep(1.0)