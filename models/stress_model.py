def viability_map(viability, DO, A, agitation, DT):
    """
    Compute viability decay based on metabolic and physical stress.
    
    Stress factors:
    - Low DO (< 25%): oxygen limitation stress
    - High acetate: metabolic toxicity
    - High agitation: shear stress
    Returns updated viability (0-1).
    """

    # Oxygen stress (increases sharply below 25% DO)
    DO_stress = max(0, (25 - DO) / 25)
    
    # Acetate toxicity (Monod-like inhibition)
    acetate_stress = A / (1 + A)
    
    # Shear stress (normalized to typical bioreactor range)
    shear_stress = agitation / 450
    
    # Combined stress (weighted sum)
    stress = DO_stress + acetate_stress + shear_stress
    
    # Viability decay rate (exponential decay with stress)
    # Increased decay coefficient from 0.003 to 0.005 for stronger effect
    decay_rate = 0.005 * stress * DT
    
    # Update viability (ensure it stays in [0, 1])
    viability *= max(0, (1 - decay_rate))
    
    return viability