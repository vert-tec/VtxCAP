import numpy as np


class VtxCAP:
    p_mavg : float = 0.0
    p_mstd : float = 0.0
    p_msum : float = 0.0
    p_win : np.array = []

    def __init__(self, fs : float, Twin_avg : int = 10):
        self._fs = fs
        self._Twin = Twin_avg
        self._Nwin = Twin_avg * fs
        self._alpha = 1.0 / (Twin_avg * fs)

        self.p_win = np.zeros(self._Nwin)

        print(self._Nwin)


    def reset(self) -> None:
        self.p_mavg = 0.0
        self.p_mstd = 0.0

    def process_sample(self, smpl : float) -> None:
        self._put_sample(smpl)

        return [
            self._update_mavg(),
            self._update_mstd(),
            self._updat_msum()
        ]


    def _put_sample(self, smpl : float) -> None:
        self.p_win[:-1] = self.p_win[1:]
        self.p_win[-1] = smpl


    def _update_mavg(self) -> float:
        self.p_mavg = np.mean(self.p_win) #(self._alpha * smpl) + (1 - self._alpha) * self.p_mavg
        return self.p_mavg
    
    def _update_mstd(self) -> float:
        self.p_mstd = np.std(self.p_win)
        return self.p_mstd
    
    def _updat_msum(self) -> float:
        avg = np.mean(self.p_win)
        self.p_msum = np.sum((self.p_win - avg)**2) / self._Nwin
        return self.p_msum