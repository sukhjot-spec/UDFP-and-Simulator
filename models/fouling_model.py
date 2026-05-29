import numpy as np

class FoulingModel:
    """
    Tracks cumulative fouling resistance based on lysis history.
    
    Rc and Rp depend on accumulated eDNA and HCP from lysis,
    not on instantaneous biomass. This ensures O2_limited batches (high lysis
    due to DO stress) produce high fouling, not low fouling.
    """

    def __init__(self):

        self.Rc = 0
        self.Rp = 0
        self.cumulative_eDNA = 0  
        self.cumulative_HCP = 0   
        self.cumulative_volume = 0

    def update(self, biomass, viability, viability_prev, flux, filtration_time, DT, scenario):

        """
        fouling resistances based on lysis-driven foulant accumulation.
        
        Parameters:
        biomass : float Current biomass concentration (g/L)
        viability : float Current viability fraction (0-1)
        viability_prev : float Viability at previous time step (0-1)
        flux : float Current permeate flux (m/s)
        filtration_time : float Time since filtration started (hr)
        DT : float Time step (hr)
        scenario : str Batch scenario identifier
        
        Returns:
        Rc, Rp : float Updated cake and pore resistances (m^-1)
        """

        # Lysis event this time step (g/L biomass lysed)
        # using viability drop as proxy for cell death
        viability_drop = max(0, viability_prev - viability)
        lysis_mass = viability_drop * biomass
        
        # DNA and protein release from lysed cells
        # Real E. coli composition: 3% DNA, 50% protein by dry mass
        k_dna = 0.030   # g DNA / g lysed biomass
        k_hcp = 0.500   # g protein / g lysed biomass
        

        # Converting to mg/L and accumulate
        deDNA = lysis_mass * k_dna * 1000 
        dHCP = lysis_mass * k_hcp * 1000   
        
        # Scenario-specific modifiers
        if scenario == "shear_stress":
            # Shear causes extra DNA release
            deDNA *= 2.0
            dHCP *= 1.5
        
        elif scenario == "O2_limited":
            # Oxygen stress causes protein denaturation → more HCP fouling
            dHCP *= 1.3
        
        # Accumulation over time 
        self.cumulative_eDNA += deDNA
        self.cumulative_HCP += dHCP
        
        # Tracking permeate volume for cake compaction
        self.cumulative_volume += flux * DT * 3600  # m³
        
        
        # SECTION 2: Resistance calculation
        
        # Pore resistance (HCP-driven, blocks membrane pores)
        # Hermia standard blocking model: Rp prop. [HCP]*sqrt(time)
        alpha_hcp = 5e12  # m^-1 per (mg/L HCP)
        time_factor = np.sqrt(filtration_time + 0.1)  # sqrt(hr)
        dRp = alpha_hcp * self.cumulative_HCP * time_factor * DT
        

        # Cake resistance (DNA-driven, gel layer on membrane surface)
        # Compressible cake: Rc prop. [DNA]*permeate_volume
        # DNA forms high-viscosity gel that compacts under pressure
        alpha_dna = 1.2e13  # m^-1 per (mg/L DNA × m³)
        volume_factor = max(self.cumulative_volume, 1e-9)
        dRc = alpha_dna * self.cumulative_eDNA * volume_factor * DT
        
        # Scenario-specific resistance multipliers
        if scenario == "late_harvest":
            # Extended fermentation → autolysis → more debris
            dRc *= 1.4
            dRp *= 1.2
        
        # Update resistances
        self.Rc += dRc
        self.Rp += dRp
        
        # Physical constraints (so that resistance can't decrease)
        self.Rc = max(self.Rc, 0)
        self.Rp = max(self.Rp, 0)
        
        return self.Rc, self.Rp