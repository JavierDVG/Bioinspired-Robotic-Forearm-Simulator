def circular_trajectory(radius=1.0, steps=100):
    import numpy as np
    for angle in np.linspace(0, 2 * np.pi, steps):
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        yield x, y
