

from stdfilters.algo_sos import VtxSosStage

import matplotlib.pyplot as plt
import numpy as np


def run():

    coef = [0.02008337, 0.04016673, 0.02008337, 1., -1.56101808, 0.64135154]
    filt = VtxSosStage(coeffs=coef)


    # sos = sp.signal.butter(2, Wn=0.1, analog=False, output='sos')
    # print(sos)
    # sos_int = (np.round(sos * 2**16).astype(np.uint16))
    # print(sos_int)
    # fil = FilterTapSOS(sos, bits=16)


    f1 = 11.0
    f2 = 200.0

    fs = 1000

    t = np.linspace(0, 1, int(fs))

    sig = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)
    sig = sig / 2.0


    sig_fil = [filt.apply(x) for x in sig]


    fig = plt.plot(figsize=(20, 10))
    plt.plot(t, sig, alpha=.6, color="teal")
    plt.plot(t, sig_fil, alpha=.6, color="magenta")
    plt.show()


if __name__ == "__main__":
    run()