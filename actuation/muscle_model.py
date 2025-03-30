import numpy as np

class McKibbenMuscle:
    def __init__(self, max_force, rest_length):
        self.max_force = max_force
        self.rest_length = rest_length

    def force(self, pressure, contraction_ratio):
        """
        Simplified force model: F = P * A_eff * efficiency
        """
        efficiency = 1 - contraction_ratio  # simplistic
        area_eff = 0.785  # example: effective area in cm²
        return pressure * area_eff * efficiency
