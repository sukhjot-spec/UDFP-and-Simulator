import numpy as np


def agitation_power(rpm, density=1000, impeller_diameter=0.12, power_number=5):

    N = rpm / 60
    P = (power_number*density*(N**3)*(impeller_diameter**5))
    return P