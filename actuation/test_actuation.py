import numpy as np
from actuation_optimizer import optimize_actuation

def test_optimization_output():
    (pressure, contraction), cost = optimize_actuation(np.pi / 2, (1.0, 0.5))
    assert 0.1 <= pressure <= 5
    assert 0.0 <= contraction <= 1.0
