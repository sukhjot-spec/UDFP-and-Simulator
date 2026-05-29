def ionic_strength_model(S, A, nitrate):
    ionic_strength = 0.05+0.002*nitrate+0.003*A+0.0005*S
    return max(ionic_strength, 0.01)