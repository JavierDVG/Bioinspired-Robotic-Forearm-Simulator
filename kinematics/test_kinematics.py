from kinematics import ForearmKinematics
import numpy as np

def test_forward_kinematics_identity():
    fk = ForearmKinematics([
        (0, 0, 0, 0),
        (1, 0, 0, 0)
    ])
    T = fk.forward_kinematics()
    assert np.allclose(T[0:3, 3], [1, 0, 0])

