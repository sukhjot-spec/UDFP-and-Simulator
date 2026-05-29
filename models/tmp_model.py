import numpy as np


def TMP_model( filtration_time, Rc, scenario):
    """
    Transmembrane pressure model (constant-flux operation).
    
    TMP rises over time to overcome fouling resistance and maintain
    constant permeate flux.
    
    Parameters:
    filtration_time : Hours since filtration started
    Rc : Current cake resistance (m^-1)
    scenario : Batch scenario
    
    Returns:
    TMP : (float) Transmembrane pressure (cmHg)
    """

    TMP = ( 2 + 0.15 * filtration_time + 5e-14 * Rc)

    if scenario == "shear_stress":
        TMP *= 1.25 # Higher fouling propensity requires more TMP
    elif scenario == "O2_limited":
        # High lysis → high fouling → high TMP needed
        TMP *= 1.35
    return np.clip(TMP, 2, 45) * 100