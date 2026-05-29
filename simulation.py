import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scenario import generate_scenario
from membrane.membrane_system import create_system
from models.growth_model import growth_step
from models.DO_model import kla_model, O2_sat, update_DO, DO_percent
from models.ionic_model import ionic_strength_model
from models.stress_model import viability_map
from models.disturbance_model import disturbance
from config.reactor_config import total_vol, working_vol, headspace_vol, temperature
from config.membrane_config import membrane_area, pore_size, base_viscosity, Rm
from models.power_model import agitation_power
from models.fouling_model import FoulingModel
from models.tmp_model import TMP_model

def simulate_batch(batchID, DT=0.1, time=30):
    param = generate_scenario()
    t_span = np.arange(0, time, DT)

    X = 0.1
    S = param['So']
    P = 0
    A = 0.05
    DO = 0.95*O2_sat

    viability = param['initial_viability']
    viability_prev = viability

    filtration_start = 20

    rows = []
    fouling = FoulingModel()
    for t in t_span:
        agitation = (param['agitation']+ disturbance(t,param['scenario']))
        DO_pct = DO_percent(DO)

        if DO_pct < 30:
            agitation += 25

        agitation = np.clip(agitation, 80, 1000)
        gas_flow = param['gas_flow']
        kLa = kla_model(agitation,gas_flow)

        if param['scenario'] == 'O2_limited': 
            kLa *= 0.02

        X, S, P, A, _, OUR = growth_step(X, S, P, A, DO_pct, DT, param, kLa)



        if t < filtration_start:
            OTR_max = (kLa* (O2_sat- DO))
            oxygen_deficit = OUR - OTR_max
            if oxygen_deficit > 0:
                DO -= (0.25* oxygen_deficit* DT)
            else:
                DO = update_DO(
                    DO,
                    kLa,
                    OUR,
                    DT
                )

            DO = np.clip( DO, 0, O2_sat)
            DO_pct = DO_percent(DO)

            if (param['scenario']== 'O2_limited'):

                DO_pct = min(DO_pct, np.random.uniform(0, 5))
                DO = ( DO_pct / 100) * O2_sat
        else:
            DO_pct = 20



        nitrate = (10+ 4 * np.sin(t / 5)+ np.random.normal(0, 0.3))

        ionic_strength = ionic_strength_model(S, A, nitrate)
        viability_prev = viability
        viability = viability_map(viability, DO, A, agitation, DT)
        fermentation_power = agitation_power(agitation)


        if t < filtration_start:
            TMP = 0
            flux = 0
            filtration_power = 0
            phase = 0
            filtration_t = 0
            total_power = fermentation_power
            Rt = 0

        else:
            phase = 1
            filtration_t = (t - filtration_start)

            TMP = TMP_model(
                filtration_t,
                fouling.Rc,
                param['scenario']
            )

            viscosity = (base_viscosity * (1 + 0.015 * X))
            Rt = Rm + fouling.Rc + fouling.Rp

            TMP_pa = TMP * 1333.22
            flux = TMP_pa / ( viscosity * Rt)
            flux = np.clip(
                flux,
                2e-6,
                1.8e-5
            )

            Rc, Rp = fouling.update(biomass=X, viability=viability, viability_prev=viability_prev, flux=flux, filtration_time=filtration_t, DT=DT, scenario=param['scenario'])
            sys = create_system(
                X,
                nitrate,
                Rc,
                Rp
            )
            sys.simulate()
            membrane = sys.units[0]

            filtration_power = membrane.power
            total_power = (fermentation_power+ filtration_power)
        
        rows.append({
            "batchID": batchID,
            "time(hr)": t,
            "process_phase": phase,
            "scenario": param["scenario"],

            "pH": 7 - 0.4 * np.log1p(A),
            "biomass_conc(g/L)": X,
            "substrate_conc(g/L)": S,
            "product_conc(g/L)": P,
            "acetate_conc(g/L)": A,
            "viability": viability,

            "DO(%)": DO_pct,
            "kLa(hr1)": kLa,
            "gas_flow_rate(vvm)": gas_flow,
            "O2_uptake_rate(mmol/L/hr)": OUR,

            "agitation(rpm)": agitation,
            "ionic_strength(mol/L)": ionic_strength,

            "TMP(cmHg)": TMP,
            "membrane_resistance(m1)": Rt,
            "flux(m/s)": flux,
            "flux(LMH)": flux*3600*1000,
            "power(W)": total_power,
            "filtration_time(hr)": filtration_t,

            "cumulative_eDNA(mg/L)": fouling.cumulative_eDNA if t >= filtration_start else 0,
            "cumulative_HCP(mg/L)": fouling.cumulative_HCP if t >= filtration_start else 0,
            
            # "reactor_volume(L)": total_vol,
            # "working_volume(L)": working_vol,
            # "headspace_volume(L)": headspace_vol,
            # "feed_rate(L/hr)": 0,
            # "temperature(C)": temperature,
            # "DO_saturation(%)": 100,
            # "O2_in_fraction": 1.0,
            # "pore_size(um)": pore_size,
            # "membrane_area(m2)": membrane_area,
            # "base_viscosity(Pa.s)": base_viscosity,
            # "density(kg/m3)": 1000,
        })

    return pd.DataFrame(rows)