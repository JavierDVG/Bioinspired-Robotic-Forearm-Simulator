import numpy as np
import matplotlib.pyplot as plt
from pid_controller import PIDController

def simulate_joint_motion(setpoint, duration=2.0, dt=0.01):
    controller = PIDController(Kp=10.0, Ki=1.0, Kd=0.5, dt=dt)

    time = np.arange(0, duration, dt)
    position = 0.0
    velocity = 0.0
    positions = []

    for t in time:
        control_signal = controller.compute(setpoint, position)
        # Simple second-order system: torque affects acceleration
        acceleration = control_signal - 0.1 * velocity  # damping
        velocity += acceleration * dt
        position += velocity * dt
        positions.append(position)

    plt.plot(time, positions)
    plt.axhline(setpoint, color='r', linestyle='--', label='Setpoint')
    plt.title("Joint Angle Response (PID Controlled)")
    plt.xlabel("Time [s]")
    plt.ylabel("Angle [rad]")
    plt.legend()
    plt.grid()
    plt.show()
