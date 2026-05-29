def disturbance(t, scenario):
    if scenario == 'O2_limited' and 8 < t < 12:
        return -80
    if scenario == 'shear_stress' and 5 < t < 10:
        return +70

    return 0