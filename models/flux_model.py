import numpy as np


def flux_model(TMP_cmHg, viscosity, Rt):

    TMP_pa = TMP_cmHg * 1333.22
    flux = TMP_pa / ( viscosity * Rt)

    flux = np.clip(flux, 2e-6, 1.8e-5)

    return flux