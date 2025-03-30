import numpy as np
from scipy.optimize import minimize
from muscle_model import McKibbenMuscle

def optimize_actuation(target_angle, initial_guess):
    muscle = McKibbenMuscle(max_force=100, rest_length=1.0)

    def cost_function(x):
        pressure, contraction = x
        force = muscle.force(pressure, contraction)
        error = np.abs(target_angle - contraction * np.pi)  # Simplified mapping
        energy = pressure**2 + contraction**2
        return 10 * error + energy

    bounds = [(0.1, 5), (0.0, 1.0)]
    result = minimize(cost_function, initial_guess, bounds=bounds)
    return result.x, result.fun
