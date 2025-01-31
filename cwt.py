import numpy as np
from scipy.signal import cwt, ricker
from scipy.signal import convolve

class CWTFilter:
    def __init__(self, wavelet, widths, window_size, exclude_scales):
        """
        Initialize the CWT filter.
        
        :param wavelet: Wavelet function (e.g., scipy.signal.ricker).
        :param widths: Array of widths (scales) to analyze the signal.
        :param window_size: Size of the sliding window.
        :param exclude_scales: Scales to exclude (list of indices from widths array).
        """
        self.wavelet = wavelet
        self.widths = widths
        self.window_size = window_size
        self.exclude_scales = exclude_scales
        self.buffer = []
        self.last_reconstructed = np.zeros(window_size)  # Initialize reconstructed buffer
    
    def add_sample(self, sample):
        """
        Add a new sample to the buffer, filter it, and return the filtered signal.
        
        :param sample: New data sample.
        :return: Filtered signal (current sliding window) or None if the buffer isn't full.
        """
        self.buffer.append(sample)
        
        # Ensure the buffer size doesn't exceed the window size
        if len(self.buffer) > self.window_size:
            self.buffer.pop(0)
        
        # Process if the buffer is full
        if len(self.buffer) == self.window_size:
            signal = np.array(self.buffer)
            cwt_matrix = cwt(signal, self.wavelet, self.widths)
            
            # Exclude certain frequency components
            for scale in self.exclude_scales:
                cwt_matrix[scale, :] = 0  # Zero out unwanted scales
            
            # Reconstruct the signal from the modified CWT coefficients
            reconstructed_signal = self.inverse_cwt(cwt_matrix)
            self.last_reconstructed = reconstructed_signal
            return reconstructed_signal
        
        return None  # Not enough data to process yet

    def inverse_cwt(self, cwt_matrix):
        """
        Reconstruct the signal from the modified CWT coefficients.
        
        :param cwt_matrix: Modified CWT coefficient matrix.
        :return: Reconstructed signal.
        """
        # Approximation of inverse CWT by summing the coefficients
        reconstructed_signal = np.sum(cwt_matrix, axis=0)
        return reconstructed_signal

# Example Usage
window_size = 128  # Sliding window size
widths = np.arange(1, 31)  # Scales for wavelet analysis
exclude_scales = [0]  # Exclude low-frequency components (corresponding to smallest scales)
wavelet = ricker  # Ricker wavelet (Mexican hat)

cwt_filter = CWTFilter(wavelet, widths, window_size, exclude_scales)

# Simulated data stream
# np.random.seed(0)
# data_stream = np.sin(np.linspace(0, 10 * np.pi, 300)) + np.random.normal(0, 0.1, 300)

data_stream = np.loadtxt("./data/warmup.txt")

# Process data sample-by-sample
filtered_data = []
for i, sample in enumerate(data_stream):
    filtered_sample = cwt_filter.add_sample(sample)
    if filtered_sample is not None:
        filtered_data.append(filtered_sample[-1])  # Use the last value of the sliding window

# Visualize original and filtered signal
import matplotlib.pyplot as plt


plt.plot(data_stream / np.max(data_stream), label="Original Signal", alpha=0.7)
plt.plot(range(len(filtered_data)), filtered_data / np.max(filtered_data), label="Filtered Signal", alpha=0.7)
plt.legend()
plt.title("CWT Filter: Removing Selected Frequency Components")
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.show()
