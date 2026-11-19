import matplotlib.pyplot as plt

# ThonnyのShellからコピーした数値を貼り付け
wavelengths = [310.0, 312.68, ...]  # ← Wavelength_nm の行の数値を入れる
intensities = [1200, 1250, ...]  # ← Intensity の行の数値を入れる

plt.figure(figsize=(10, 5))
plt.plot(wavelengths, intensities, color="royalblue", linewidth=1.5)
plt.title("C12880MA Spectral Profile")
plt.xlabel("Wavelength [nm]")
plt.ylabel("Intensity [16-bit ADC]")
plt.xlim(340, 850)  # C12880MAの有効波長範囲 (340nm〜850nm)
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()