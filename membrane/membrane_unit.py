import biosteam as bst
import numpy as np
from config.membrane_config import Rm, membrane_area, base_viscosity, TMP_operation

class foulMembrane(bst.Unit):
    _N_ins = 1
    _N_outs = 2

    def __init__(self, ID, ins, outs, Rc, Rp):
        super().__init__(ID, ins, outs)
        self.area = membrane_area
        self.Rm = Rm
        self.Rc = Rc
        self.Rp = Rp
    
    def _run(self):

        feed = self.ins[0]
        permeate, retentate = self.outs
        permeate.copy_like(feed)
        retentate.copy_like(feed)

        total_mass = max(feed.F_mass, 1e-6)
        biomass_mass = feed.imass['Biomass']
        biomass = (biomass_mass / total_mass) * 1000

        Rt = (
            self.Rm
            + self.Rp
            + self.Rc
        )

        viscosity = (base_viscosity* (1 + 0.15 * biomass))

        TMP_pa = TMP_operation * 100000

        flux = TMP_pa / (viscosity * Rt)
        flux = np.clip(
            flux,
            5e-6,
            1.7e-5
        )

        J_vol = flux * self.area
        J_vol_hr = J_vol * 3600
        rho = 1000
        max_perm = J_vol_hr * rho

        permeate.F_mass = min(
            max_perm,
            feed.F_mass
        )

        retentate.F_mass = (
            feed.F_mass
            - permeate.F_mass
        )

        self.flux = flux
        self.TMP = TMP_operation*75
        self.Rt = Rt
        self.deltaP = TMP_pa

    def _design(self):
        rho = 1000
        Q = (self.outs[0].F_mass/ rho) / 3600
        self.power = Q * self.deltaP

    def _cost(self):
        self.power_utility(self.power)