from thermosteam import Chemical, Chemicals
import biosteam as bst


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