from kinematics.dh_utils import dh_transform
import numpy as np

class ForearmKinematics:
    def __init__(self, dh_params):
        """
        dh_params: List of tuples (a, alpha, d, theta)
        """
        self.dh_params = dh_params

    def forward_kinematics(self):
        """Compute the final transformation matrix."""
        T = np.eye(4)
        for a, alpha, d, theta in self.dh_params:
            T = T @ dh_transform(a, alpha, d, theta)
        return T
def inverse_kinematics_2d(x, y, l1, l2):
    """Inverse kinematics for a planar 2-link arm."""
    cos_theta2 = (x**2 + y**2 - l1**2 - l2**2) / (2 * l1 * l2)
    if np.abs(cos_theta2) > 1:
        raise ValueError("Target unreachable")
    sin_theta2 = np.sqrt(1 - cos_theta2**2)

    theta2 = np.arctan2(sin_theta2, cos_theta2)
    k1 = l1 + l2 * cos_theta2
    k2 = l2 * sin_theta2
    theta1 = np.arctan2(y, x) - np.arctan2(k2, k1)

    return theta1, theta2