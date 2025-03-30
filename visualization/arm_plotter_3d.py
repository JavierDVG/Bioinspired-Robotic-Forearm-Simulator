import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ArmPlot3D:
    def __init__(self, parent, l1=1.0, l2=1.0):
        self.l1 = l1
        self.l2 = l2

        self.fig = plt.Figure(figsize=(5, 5))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim([-2, 2])
        self.ax.set_ylim([-2, 2])
        self.ax.set_zlim([-0.5, 0.5])
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")
        self.ax.set_title("3D Robotic Forearm")

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(pady=5)

    def update(self, theta1, theta2, elbow_limit_deg=None):
        self.ax.cla()
        self.ax.set_xlim([-2, 2])
        self.ax.set_ylim([-2, 2])
        self.ax.set_zlim([-0.5, 0.5])
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")
        self.ax.set_title("3D Robotic Forearm")

        # Posiciones
        x0, y0, z0 = 0, 0, 0
        x1 = self.l1 * np.cos(theta1)
        y1 = self.l1 * np.sin(theta1)
        z1 = 0

        x2 = x1 + self.l2 * np.cos(theta1 + theta2)
        y2 = y1 + self.l2 * np.sin(theta1 + theta2)
        z2 = 0

        # Enlaces
        self.ax.plot([x0, x1], [y0, y1], [z0, z1], 'o-', lw=4, label='Link 1')
        self.ax.plot([x1, x2], [y1, y2], [z1, z2], 'o-', lw=4, label='Link 2')

        # Visualización de límite angular en 3D
        if elbow_limit_deg is not None:
            limit_rad = np.deg2rad(elbow_limit_deg)
            arc_angles = np.linspace(-limit_rad, limit_rad, 50)
            arc_x = x1 + self.l2 * np.cos(theta1 + arc_angles)
            arc_y = y1 + self.l2 * np.sin(theta1 + arc_angles)
            arc_z = np.zeros_like(arc_x)

            self.ax.plot(arc_x, arc_y, arc_z, 'r--', lw=1, alpha=0.4, label='Elbow limit')

        self.ax.legend()
        self.canvas.draw()
