from arm_plotter import plot_2d_arm
import numpy as np

def test_plot_arm():
    theta1 = np.pi / 4
    theta2 = np.pi / 4
    plot_2d_arm(theta1, theta2)
test_plot_arm()