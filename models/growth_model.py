import numpy as np

from config.biological_config import (
    Kd,
    Ms,
    Ko,
    KI_acetate
)

def growth_step(X, S, P, A, DO, DT, param, kla):
    X = max(X, 0)
    S = max(S, 0)
    A = max(A, 0)
    DO = np.clip(DO, 0, 100)

    mu_max = param['mu_max']
    Ks = param['Ks']
    Yxs = param['Yxs']
    qO2 = param['qO2']

    mu_s = S / (Ks + S) if S > 0 else 0
    mu_o = DO / (Ko + DO)
    mu_i = 1 / (1 + A / KI_acetate)
    mu = mu_max * mu_s * mu_o * mu_i
    dX = ((mu * X) - (Kd * X)) * DT

    dS = (-((1 / Yxs) * mu * X)- (Ms * X)) * DT
    dP = (0.08 * mu * X) * DT
    acetate_prod = 0.08 * mu * X if mu > 0.35 else 0.002

    dA = acetate_prod-(0.03 * A) * DT
    OUR = qO2 * X


    dDO = (kla * (100 - DO) - OUR)* DT
    X += dX
    S += dS
    P += dP
    A += dA
    DO += dDO

    X = max(X, 0)
    S = max(S, 0.2)
    P = max(P, 0)
    A = max(A, 0.02)
    DO = np.clip(DO, 0, 100)

    return X, S, P, A, DO, OUR