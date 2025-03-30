import argparse
import numpy as np
from visualization.arm_plotter import plot_2d_arm
from kinematics.kinematics import inverse_kinematics_2d

def main():
    parser = argparse.ArgumentParser(description="Robotic Forearm CLI")
    parser.add_argument("--x", type=float, help="Target X position", required=True)
    parser.add_argument("--y", type=float, help="Target Y position", required=True)
    parser.add_argument("--l1", type=float, default=1.0, help="Link 1 length")
    parser.add_argument("--l2", type=float, default=1.0, help="Link 2 length")

    args = parser.parse_args()

    try:
        theta1, theta2 = inverse_kinematics_2d(args.x, args.y, args.l1, args.l2)
        print(f"Joint Angles (rad): θ1={theta1:.2f}, θ2={theta2:.2f}")
        plot_2d_arm(theta1, theta2, args.l1, args.l2)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
