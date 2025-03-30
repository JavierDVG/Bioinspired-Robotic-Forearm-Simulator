import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches

class ArmPlot2D:
    def __init__(self, parent, l1=1.0, l2=1.0):
        self.l1 = l1
        self.l2 = l2

        self.fig, self.ax = plt.subplots(figsize=(4, 4))
        self.ax.set_xlim(-2, 2)
        self.ax.set_ylim(-2, 2)
        self.ax.set_aspect("equal")
        self.ax.grid(True)
        self.ax.set_title("2D Robotic Forearm")

        self.line1, = self.ax.plot([], [], 'o-', lw=4, label='Link 1')
        self.line2, = self.ax.plot([], [], 'o-', lw=4, label='Link 2')
        self.arc_patch = None
        self.ax.legend()

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(pady=5)

    def update(self, theta1, theta2, elbow_limit_deg=None):
        x0, y0 = 0, 0
        x1 = self.l1 * np.cos(theta1)
        y1 = self.l1 * np.sin(theta1)
        x2 = x1 + self.l2 * np.cos(theta1 + theta2)
        y2 = y1 + self.l2 * np.sin(theta1 + theta2)

        self.line1.set_data([x0, x1], [y0, y1])
        self.line2.set_data([x1, x2], [y1, y2])

        # Restricción visual (arco)
        if elbow_limit_deg is not None:
            if self.arc_patch:
                self.arc_patch.remove()

            self.arc_patch = patches.Arc(
                (x1, y1),
                2 * self.l2, 2 * self.l2,
                angle=np.rad2deg(theta1),
                theta1=-elbow_limit_deg,
                theta2=elbow_limit_deg,
                color='red',
                linestyle='--',
                linewidth=1,
                alpha=0.4,
                zorder=0
            )
            self.ax.add_patch(self.arc_patch)

        self.canvas.draw()
