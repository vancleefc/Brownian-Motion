import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# Parameters
num_particles = 100  # Number of particles
num_steps = 500      # Number of time steps
initial_step_size = 0.01  # Initial step size for each movement
x_limits = (-1, 1)   # X-axis limits
y_limits = (-1, 1)   # Y-axis limits

# Initialize particle positions
particles = np.random.uniform(low=-1, high=1, size=(num_particles, 2))

# Create the figure and axis
plt.style.use('dark_background')  # Set dark background
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(left=0.1, bottom=0.2)  # Adjust layout for slider
ax.set_xlim(x_limits)
ax.set_ylim(y_limits)
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.5)
ax.set_title("2D Brownian Motion Simulation")

# Scatter plot for particles
scatter = ax.scatter(particles[:, 0], particles[:, 1], c='cyan', s=10)

# Add slider for kinetic energy (step size)
ax_step = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor='lightgray')
step_slider = Slider(ax_step, 'Kinetic Energy', 0.001, 0.1, valinit=initial_step_size, valstep=0.001)

# Function to update particle positions
def update(frame):
    global particles
    # Get current step size from the slider
    step_size = step_slider.val
    
    # Generate random steps for each particle
    steps = np.random.normal(loc=0, scale=step_size, size=(num_particles, 2))
    particles += steps
    
    # Ensure particles stay within the boundaries
    particles = np.clip(particles, x_limits[0], x_limits[1])
    
    # Update scatter plot data
    scatter.set_offsets(particles)
    return scatter,

# Create animation
ani = FuncAnimation(fig, update, frames=num_steps, interval=50, blit=True)

# Function to update step size when slider is changed
def update_step_size(val):
    # The animation will automatically use the new step size in the `update` function
    pass

# Attach the update function to the slider
step_slider.on_changed(update_step_size)

# Show the plot
plt.show()