import numpy as np

O2_sat = 1.2 # mg/L dissolved oxygen saturation

def kla_model(agitation, gas_flow):
    """
    van't Riet-style correlation for kLa.
    kLa scales with agitation^1.1 and gas_flow^0.55.
    """
    kla = (0.85*agitation**1.1 * gas_flow**0.55)
    return np.clip(kla, 80, 800)



def update_DO(DO, kla, OUR, DT):
    """
    Oxygen mass balance: accumulation = transfer - uptake
    dDO/dt = kLa * (DO_sat - DO) - OUR
    """
    dDO = (kla* (O2_sat - DO)- OUR) * DT
    DO_new = DO + dDO

    DO_new = np.clip(
        DO_new,
        0,
        O2_sat
    )

    return DO_new


def DO_percent(DO):

    return (DO / O2_sat) * 100