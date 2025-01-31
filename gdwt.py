import pywt
import numpy as np
import matplotlib.pyplot as plt

def dwt_with_sampling(signal, fs, base_fs=1000):
    """
    Perform Discrete Wavelet Transform (DWT) and adjust decomposition level based on sampling rate.
    
    Args:
        signal (array): Input time series.
        fs (float): Current sampling rate.
        base_fs (float): Reference sampling rate (default 1000 Hz).
    
    Returns:
        coeffs (list): Wavelet decomposition coefficients.
        level (int): Number of decomposition levels used.
    """
    wavelet = pywt.Wavelet('coif4')  # Select Daubechies-4 wavelet
    max_level = pywt.dwt_max_level(len(signal), wavelet.dec_len)  
    level = 2 # min(max_level, int(np.log2(base_fs / fs)))  # Adjust levels dynamically

    coeffs = pywt.wavedec(signal, wavelet, level=level)  # Perform DWT
    return coeffs, wavelet, level


# Generate Example Signal
fs = 20  # Sampling rate (Hz)
#signal = np.sin(2 * np.pi * 0.5 * t) + 0.5 * np.sin(2 * np.pi * 0.19 * t)  # Mixed sine wave
signal = np.loadtxt("./data/warmup.txt")
t = np.arange(0, len(signal)/fs, step=1.0/fs)  # Time vector


# Apply DWT
coeffs, wavelet, level = dwt_with_sampling(signal, fs)

# Plot Original Signal and Wavelet Coefficients
plt.figure(figsize=(10, 6))
plt.subplot(level + 3, 1, 1)
plt.plot(t, signal, label="Original Signal", color='black')
plt.legend()
plt.title("Wavelet Decomposition using DWT")

rcoeffs = []

# Plot Approximation and Detail Coefficients
for i, coef in enumerate(coeffs):
    print(i, len(coef))
    plt.subplot(level + 3, 1, i + 2)
    plt.plot(coef, label=f"Level {i} {'Approx' if i == 0 else 'Detail'}")
    plt.legend()

    if i == 0:
        rcoeffs.append(np.ones(len(coef)))
    else:
        rcoeffs.append(coef)

# print(coeffs)
# print(rcoeffs)

reconstructed_signal = pywt.waverec(rcoeffs, wavelet)

# Ensure the reconstructed signal matches the original length
plt.subplot(level + 3, 1, i + 3)
plt.plot(t, reconstructed_signal[1:], label="Original Signal", color='teal')



plt.tight_layout()
plt.show()
