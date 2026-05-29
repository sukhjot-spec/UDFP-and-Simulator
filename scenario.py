import numpy as np

def generate_scenario():
    scenario = np.random.choice([
        'healthy', 'O2_limited', 'shear_stress', 'late_harvest'
    ])

    param = {
        'mu_max': np.random.uniform(0.75, 1.10),
        'Ks': 0.5,
        'Yxs': 0.55,
        'qO2': np.random.uniform(0.5, 1.2),
        'So': np.random.uniform(120, 180),
        'initial_viability': np.random.uniform(0.85, 0.99)
    }

    if scenario =='O2_limited':
        param['gas_flow'] = np.random.uniform(0.02, 0.08)
        param['agitation'] = np.random.uniform(50, 120)

    elif scenario == 'shear_stress':
        param['gas_flow'] = np.random.uniform(0.8, 1.4)
        param['agitation'] = np.random.uniform(700, 1000)

    else:
        param['gas_flow'] = np.random.uniform(0.5, 1)
        param['agitation'] = np.random.uniform(350, 600)

    param['scenario'] = scenario
    return param