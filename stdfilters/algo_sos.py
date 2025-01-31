

class VtxSosStage:
    """
        ### SOS Filter Stage in Transposed Direct-Form-II


    """

    a1 = 0.0
    a2 = 0.0
    b0 = 0.0
    b1 = 0.0
    b2 = 0.0

    T1 = 0.0
    T2 = 0.0


    def __init__(self, coeffs : list = None) -> None:
        self.set_coeffs(coeffs)


    def set_coeffs(self, coeffs) -> None:
        """
            Set Filter Coefficients

        Parameters:
            coeffs - list = [ b0, b1, b2, a0, a1, a2]
        """
        if coeffs is not None:
            C = coeffs
            if len(C) != 6:
                raise Exception("Expected Array with 6 Coefficients! [b0, b1, b2, a0, a1, a2]")

            self.b0 = C[0]
            self.b1 = C[1]
            self.b2 = C[2]
            self.a1 = C[4]
            self.a2 = C[5]


    def reset(self):
        self.T1 = 0.0
        self.T2 = 0.0


    def apply(self, val):
        res = (self.b0 * val) + self.T1
        self.T1 = (self.b1 * val - res * self.a1) + self.T2
        self.T2 = (self.b2 * val - res * self.a2)

        return res




class VtxSosStage_Integer:
    """
        ### SOS Filter Stage in Transposed Direct-Form-II in Integer Arithmetik


    """

    a1 = 0.0
    a2 = 0.0
    b0 = 0.0
    b1 = 0.0
    b2 = 0.0

    T1 = 0.0
    T2 = 0.0

    scale = 0

    def __init__(self, coeffs : list = None, bits : int = 0) -> None:
        self.set_coeffs(coeffs, bits=bits)


    def set_coeffs(self, coeffs, bits : int = 0) -> None:
        """
            Set Filter Coefficients

        Parameters:
            coeffs - list = [ b0, b1, b2, a0, a1, a2]
        """
        if coeffs is not None:
            C = coeffs
            if len(C) != 6:
                raise Exception("Expected Array with 6 Coefficients! [b0, b1, b2, a0, a1, a2]")

            if bits == 0:
                self.scale = 1

            else:
                self.scale = 2**(bits)

            self.b0 = C[0] * self.scale
            self.b1 = C[1] * self.scale
            self.b2 = C[2] * self.scale
            self.a1 = C[4] * self.scale
            self.a2 = C[5] * self.scale


    def reset(self):
        self.T1 = 0.0
        self.T2 = 0.0


    def apply(self, val):
        val = val * self.scale

        res = (self.b0 * val) / self.scale + self.T1
        self.T1 = (self.b1 * val - res * self.a1) / self.scale + self.T2
        self.T2 = (self.b2 * val - res * self.a2) / self.scale

        return (res) / self.scale