
import numpy as np


class VtxDCOffsetFilter:
    """
        ### Adaptive Digital Filter to remove DC Offset

        Adjust mu to make it converge faster or slower
        
        Good approximation for mu = 1/fs
    """


    def __init__(self, fs : int):
        """
            fs - Sample Rate in Hz
        """
        self._e = 0
        self._w = 0
        self._mu = (1.0 / fs)


    @property
    def mu(self) -> float:
        return self._mu
    

    @mu.setter
    def mu(self, value : float) -> None:
        self._mu = value


    def filterSample(self, smpl : float) -> float:
        e = smpl - self._w
        self._w = self._w + self._mu * e
        
        return e
    

    def filterVector(self, vector : np.array) -> np.array:
        if len(vector) == 0: 
            return [0]
        
        res = np.zeros_like(vector)

        for n, x in enumerate(vector):
            res[n] = self.filterSample(x)

        return res