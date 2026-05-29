import biosteam as bst
from membrane.membrane_unit import foulMembrane
from config.reactor_config import working_vol

def create_system(Biomass, Nitrate, Rc, Rp):
    V = working_vol/1000

    biomass_flow = Biomass*V
    NH3_flow = Nitrate*V

    broth = bst.Stream(
        'Broth',
        Water=3000,
        Biomass = biomass_flow,
        NH3 = NH3_flow
    )

    membrane = foulMembrane(
        'M1',
        ins=broth,
        outs = ('permeate', 'retentate'),
        Rc=Rc,
        Rp=Rp
    )
    return bst.System('sys', path=(membrane,))