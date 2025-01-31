import numpy as np
import matplotlib.pyplot as plt

from stdfilters.algo import VtxCAP

DATA_DIR = "./data/"

def moving_avg(data : np.array, fs : float, Twin : float = 10) -> np.array:
    '''
        
        Return the Moving Average for Data
    
    #### Parameters:    

        data    - Input Signal

        fs      - Sample Rate

        Twin    - Moving Avg. Window Length in Seconds
    '''

    N = int(Twin * fs)
    win = np.ones(N) / N

    return np.convolve(data, win, mode='same')


def moving_std(data : np.array, fs : float, Twin : float = 10) -> np.array:
    N = int(Twin * fs)

    [ data[n:n+N] for n in range(len(data)) ]



def run():

    fs = 10
    data = np.loadtxt(DATA_DIR + "warmup.txt")
    secs = np.arange(0, len(data)/fs, step=1.0/fs)

    # len(secs)

    c_avg = moving_avg(data, fs)

    alg = VtxCAP(fs)

    avg = []
    std = []
    eta = []

    for smpl in data:
        savg, sstd, seta = alg.process_sample(smpl)
        avg.append(savg)
        std.append(sstd)
        eta.append(seta)


    std = np.array(std)

    poor = np.where(np.logical_or(std < 200, std > 1000), 5000, 0)

    #mse = (data - avg)**2

    spec = 2.0 * np.abs(np.fft.fft(data[200:1400] - np.mean(data[200:1400])))
    freq = np.fft.fftfreq(len(data[200:1400]), 1.0 / fs)

    print(data.std())

    fig, axs = plt.subplots(2, 1, figsize=(15, 9), sharex=False)

    axs[0].plot(secs, data - avg, alpha=.4, color='blue')
    axs[0].plot(secs, avg, alpha=.8, color='red')
    axs[0].fill_between(secs, poor, alpha=.3, color='purple')

    axs[1].plot(freq[2:200], spec[2:200])
    
    #axs[1].plot(secs / 60.0, std, color='magenta')
    #plt.plot(secs, mse, alpha=.8, color='magenta')

    fig.tight_layout()
    plt.show()


def run_dwt():
    from dwt import dwt_filter, wavelet

    fs = 10
    data = np.loadtxt(DATA_DIR + "warmup.txt")
    secs = np.arange(0, len(data)/fs, step=1.0/fs)

    # len(secs)

    fil = []


    for smpl in data:
        sfil = dwt_filter(smpl)
        fil.append(sfil)

        # savg, sstd, seta = alg.process_sample(smpl)
        # avg.append(savg)
        # std.append(sstd)
        # eta.append(seta)


    fil = np.array(fil)

    fig = plt.figure(figsize=(12, 8))
    [phi, psi, x] = wavelet.wavefun(level=10)
    plt.plot(x, phi)
    [phi, psi, x] = wavelet.wavefun(level=2)
    plt.plot(x, phi)


    fig = plt.figure()
    plt.plot(secs, data, alpha=.5, color='red')
    plt.plot(secs, fil, label=["high", "low"], alpha=.5)
    fig.legend()
    fig.tight_layout()
    plt.show()



if __name__ == "__main__":
    run_dwt()