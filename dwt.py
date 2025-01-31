import pywt
import numpy as np
from scipy.signal import lfilter
import matplotlib.pyplot as plt

# Select wavelet
wavelet = pywt.Wavelet('coif4') #('db4')

# Get decomposition filter coefficients
h = wavelet.dec_lo  # Low-pass decomposition filter
g = wavelet.dec_hi  # High-pass decomposition filter

# Initialize buffers for filtering (assuming an FIR structure)
buffer_size = len(h)
buffer = np.zeros(buffer_size)



def dwt_filter(sample):
    global buffer
    buffer = np.roll(buffer, -1)  # Shift buffer
    buffer[-1] = sample  # Add new sample
    
    # Apply filtering
    low_pass_out = np.dot(h, buffer)
    high_pass_out = np.dot(g, buffer)

    return low_pass_out, high_pass_out  # Approximation and Detail coefficients
