import biosteam as bst
import numpy as np 
from thermosteam import Chemical, Chemicals


# DT = 0.1 #6 mins
# time = np.arange(0, 30, DT)
delP_Base = 1e5
Rm = 1e11
R_vol = 5

chems = Chemicals([
    Chemical('Water'),
    Chemical('Glucose'),
    Chemical('O2'),
    Chemical('CO2'),
    Chemical('NH3'),
    Chemical('Acetate'),
    Chemical('Protein', phase='s', MW=50000, search_db=False),
    Chemical('Biomass', phase='s', MW=24.6, search_db=False)
])
chems.compile(skip_checks=True)
bst.settings.set_thermo(chems)