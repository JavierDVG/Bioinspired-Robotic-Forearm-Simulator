# gui.py (Interfaz profesional completa y funcional)

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from visualization.arm_plotter import ArmPlot2D
from visualization.arm_plotter_3d import ArmPlot3D
from kinematics.kinematics import inverse_kinematics_2d
import numpy as np
import time
import csv
import matplotlib.pyplot as plt

class ArmGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bioinspired Robotic Forearm Simulator")
        self.root.geometry("900x850")
        self.root.resizable(False, False)

        self.l1 = 1.0
        self.l2 = 1.0
        self.motion_profile = []
        self.loaded_profile = []
        self.current_step = 0
        self.plot_mode = tk.StringVar(value="2D")
        self.max_elbow_angle = tk.DoubleVar(value=150.0)

        self.plot_area = None
        self.setup_styles()
        self.setup_widgets()
        self.render_plot()

    def setup_styles(self):
        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=5)
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TCombobox", font=("Segoe UI", 10))
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabelframe", font=("Segoe UI", 11, "bold"), background="#f8f8f8")

    def switch_mode(self, event=None):
        self.render_plot()

    def setup_widgets(self):
        title = ttk.Label(self.root, text="Forearm Joint & Position Control", font=("Segoe UI", 18, "bold"))
        title.pack(pady=15)

        mode_frame = ttk.Frame(self.root)
        mode_frame.pack(pady=10)
        ttk.Label(mode_frame, text="Visualization Mode:").pack(side="left")
        mode_selector = ttk.Combobox(mode_frame, textvariable=self.plot_mode, values=["2D", "3D"], state="readonly", width=5)
        mode_selector.pack(side="left", padx=5)
        mode_selector.bind("<<ComboboxSelected>>", self.switch_mode)

        slider_frame = ttk.LabelFrame(self.root, text="Manual Joint Control (Angles)", padding=15)
        slider_frame.pack(padx=15, pady=10, fill="x")

        self.theta1_var = tk.DoubleVar(value=45)
        ttk.Label(slider_frame, text="Shoulder Joint (θ₁) [°]:").grid(row=0, column=0, sticky="w")
        self.theta1_slider = ttk.Scale(slider_frame, from_=-180, to=180, orient="horizontal", variable=self.theta1_var, command=self.update_labels)
        self.theta1_slider.grid(row=0, column=1, padx=10, sticky="ew")
        self.theta1_val = ttk.Label(slider_frame, text="45.0°")
        self.theta1_val.grid(row=0, column=2)

        self.theta2_var = tk.DoubleVar(value=45)
        ttk.Label(slider_frame, text="Elbow Joint (θ₂) [°]:").grid(row=1, column=0, sticky="w")
        self.theta2_slider = ttk.Scale(slider_frame, from_=-180, to=180, orient="horizontal", variable=self.theta2_var, command=self.update_labels)
        self.theta2_slider.grid(row=1, column=1, padx=10, sticky="ew")
        self.theta2_val = ttk.Label(slider_frame, text="45.0°")
        self.theta2_val.grid(row=1, column=2)

        ttk.Label(slider_frame, text="Max Elbow Angle (°):").grid(row=2, column=0, sticky="w")
        self.elbow_limit_entry = ttk.Entry(slider_frame, textvariable=self.max_elbow_angle, width=10)
        self.elbow_limit_entry.grid(row=2, column=1, padx=5, sticky="w")

        position_frame = ttk.LabelFrame(self.root, text="Inverse Kinematics (Target Position)", padding=15)
        position_frame.pack(padx=15, pady=10, fill="x")

        ttk.Label(position_frame, text="X [m]:").grid(row=0, column=0, sticky="w")
        self.x_entry = ttk.Entry(position_frame, width=10)
        self.x_entry.grid(row=0, column=1, padx=5)

        ttk.Label(position_frame, text="Y [m]:").grid(row=1, column=0, sticky="w")
        self.y_entry = ttk.Entry(position_frame, width=10)
        self.y_entry.grid(row=1, column=1, padx=5)

        ttk.Button(position_frame, text="Calculate IK", command=self.compute_inverse_kinematics).grid(row=0, column=2, rowspan=2, padx=10)

        action_frame = ttk.Frame(self.root)
        action_frame.pack(pady=10)

        buttons = [
            ("Visualize Arm", self.plot_arm),
            ("Animate Move", self.animate_move),
            ("Export Profile", self.export_profile),
            ("Load Profile", self.load_profile),
            ("Edit Profile", self.edit_profile)
        ]
        for i, (label, cmd) in enumerate(buttons):
            ttk.Button(action_frame, text=label, command=cmd).grid(row=0, column=i, padx=5, pady=5)

        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=5)

        self.footer = ttk.Label(self.root, text=f"Link lengths: L1 = {self.l1}, L2 = {self.l2}", font=("Segoe UI", 9, "italic"))
        self.footer.pack(pady=5)

    def update_labels(self, event=None):
        self.theta1_val.config(text=f"{self.theta1_var.get():.1f}°")
        self.theta2_val.config(text=f"{self.theta2_var.get():.1f}°")

    def validate_elbow_angle(self, theta2_rad):
        max_angle_rad = np.deg2rad(self.max_elbow_angle.get())
        return abs(theta2_rad) <= max_angle_rad

    def plot_arm(self):
        theta1 = np.deg2rad(self.theta1_var.get())
        theta2 = np.deg2rad(self.theta2_var.get())
        if not self.validate_elbow_angle(theta2):
            messagebox.showwarning("Angle Limit", "Elbow angle exceeds allowed limit.")
            return
        elbow_limit_deg = self.max_elbow_angle.get()
        self.plot_area.update(theta1, theta2, elbow_limit_deg=elbow_limit_deg)
        self.motion_profile.append((theta1, theta2))

    def animate_move(self):
        self.plot_arm()

    def compute_inverse_kinematics(self):
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            theta1, theta2 = inverse_kinematics_2d(x, y, self.l1, self.l2)
            if not self.validate_elbow_angle(theta2):
                messagebox.showwarning("Angle Limit", "Elbow angle exceeds limit.")
                return
            self.animate_to(theta1, theta2)
        except Exception:
            messagebox.showerror("Invalid Input", "Please enter valid X and Y values.")

    def animate_to(self, theta1, theta2, steps=30):
        t1_init = np.deg2rad(self.theta1_var.get())
        t2_init = np.deg2rad(self.theta2_var.get())
        for t1, t2 in zip(np.linspace(t1_init, theta1, steps), np.linspace(t2_init, theta2, steps)):
            self.theta1_var.set(np.rad2deg(t1))
            self.theta2_var.set(np.rad2deg(t2))
            self.update_labels()
            self.plot_area.update(t1, t2, elbow_limit_deg=self.max_elbow_angle.get())
            self.root.update()
            time.sleep(0.02)

    def export_profile(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not filepath:
            return
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Theta1 (rad)", "Theta2 (rad)"])
            for t1, t2 in self.motion_profile:
                writer.writerow([t1, t2])

    def load_profile(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not filepath:
            return
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()[1:]
                self.loaded_profile = []
                for line in lines:
                    parts = line.strip().split(',')
                    t1, t2 = float(parts[0]), float(parts[1])
                    self.loaded_profile.append((t1, t2))
            messagebox.showinfo("Loaded", f"Loaded {len(self.loaded_profile)} steps.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def edit_profile(self):
        if not self.loaded_profile:
            messagebox.showwarning("No Profile", "Load a profile first.")
            return
        editor = tk.Toplevel(self.root)
        editor.title("Edit Motion Profile")
        editor.geometry("400x300")

        index_label = ttk.Label(editor, text="Step 0")
        index_label.pack(pady=5)

        t1_var = tk.DoubleVar()
        t2_var = tk.DoubleVar()

        t1_entry = ttk.Entry(editor, textvariable=t1_var)
        t2_entry = ttk.Entry(editor, textvariable=t2_var)
        ttk.Label(editor, text="Theta1 (rad)").pack()
        t1_entry.pack()
        ttk.Label(editor, text="Theta2 (rad)").pack()
        t2_entry.pack()

        def show_step(i):
            if 0 <= i < len(self.loaded_profile):
                self.current_step = i
                t1, t2 = self.loaded_profile[i]
                t1_var.set(t1)
                t2_var.set(t2)
                index_label.config(text=f"Step {i}")
                self.plot_area.update(t1, t2, elbow_limit_deg=self.max_elbow_angle.get())

        def save_step():
            try:
                t1 = float(t1_var.get())
                t2 = float(t2_var.get())
                self.loaded_profile[self.current_step] = (t1, t2)
                show_step(self.current_step)
            except:
                messagebox.showerror("Error", "Invalid values")

        def delete_step():
            if self.loaded_profile:
                self.loaded_profile.pop(self.current_step)
                if self.current_step >= len(self.loaded_profile):
                    self.current_step = len(self.loaded_profile) - 1
                show_step(self.current_step)

        def save_to_file():
            path = filedialog.asksaveasfilename(defaultextension=".csv")
            if not path:
                return
            with open(path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Theta1 (rad)", "Theta2 (rad)"])
                for t1, t2 in self.loaded_profile:
                    writer.writerow([t1, t2])
            messagebox.showinfo("Saved", "Profile saved.")

        ttk.Button(editor, text="◀ Prev", command=lambda: show_step(self.current_step - 1)).pack(side="left", padx=5)
        ttk.Button(editor, text="Next ▶", command=lambda: show_step(self.current_step + 1)).pack(side="left", padx=5)
        ttk.Button(editor, text="✏ Save Step", command=save_step).pack(side="left", padx=5)
        ttk.Button(editor, text="❌ Delete", command=delete_step).pack(side="left", padx=5)
        ttk.Button(editor, text="💾 Save File", command=save_to_file).pack(side="bottom", pady=10)

        show_step(0)

    def render_plot(self):
        if self.plot_area:
            self.plot_area.canvas_widget.destroy()
        if self.plot_mode.get() == "2D":
            self.plot_area = ArmPlot2D(self.root, self.l1, self.l2)
        else:
            self.plot_area = ArmPlot3D(self.root, self.l1, self.l2)
        self.plot_arm()

    def on_close(self):
        try:
            plt.close('all')
        except:
            pass
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ArmGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()