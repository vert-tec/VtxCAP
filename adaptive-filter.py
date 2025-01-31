import numpy as np
import matplotlib.pyplot as plt

from stdfilters.filters import VtxDCOffsetFilter

# Generate a test signal: slow-varying DC + sinusoid
fs = 20  # Sampling rate

data = np.loadtxt("./data/warmup.txt")
t = np.arange(0, len(data)/fs, step=1.0/fs)

# t = np.arange(0, 100, 1/fs)  # 100 seconds
dc_offset = 0.5 * np.sin(2 * np.pi * 0.01 * t)  # Slow varying DC offset (0.01 Hz)
#signal = np.sin(2 * np.pi * 0.5 * t)  # Desired signal (0.5 Hz)
#x = signal + dc_offset  # Noisy signal

x = data

# Adaptive LMS filter setup
mu = 0.05  # Step size
w = 0  # Initial weight (estimate of DC offset)
y = np.zeros_like(x)  # Filtered signal
yc = np.zeros_like(x)
fil = VtxDCOffsetFilter(fs)
print(fil.mu)

for n in range(1, len(x)):
    e = x[n] - w  # Error (desired signal)
    w = w + mu * e  # LMS update equation
    y[n] = e  # DC-free signal

yc = fil.filterVector(x)


# Plot results
plt.figure(figsize=(10, 5))
plt.plot(t, x, label="Signal with DC Offset", alpha=.3, color='red')
#plt.plot(t, y, label="Filtered Signal (DC Removed)", alpha=.5)
plt.plot(t, y, label="Filtered Signal (DC Removed)", alpha=.5)
plt.legend()
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Adaptive LMS Filter for DC Offset Removal")
plt.grid()
plt.show()