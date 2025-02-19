import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation
from numba import njit

# Constants
NUM_PARTICLES = 200
BOX_SIZE = 10.0
PARTICLE_RADIUS = 0.1
DT = 0.01
MASS = 1.0  # Assume all particles have the same mass

# Initialize particle positions and velocities
positions = np.random.uniform(PARTICLE_RADIUS, BOX_SIZE - PARTICLE_RADIUS, (NUM_PARTICLES, 2))
velocities = np.random.normal(0, 1, (NUM_PARTICLES, 2))  # Random initial velocities

# Initialize path for the red particle
red_particle_path = []

@njit
def update_positions(positions, velocities, temperature):
    # Add random motion scaled by temperature
    if temperature > 0:
        velocities += np.sqrt(temperature) * np.random.normal(0, 1, velocities.shape) * DT
    else:
        # At 0 K, particles stop moving
        velocities = np.zeros_like(velocities)
    
    # Update positions
    positions += velocities * DT
    
    # Handle collisions with walls
    for i in range(NUM_PARTICLES):
        for j in range(2):
            if positions[i, j] < PARTICLE_RADIUS:
                positions[i, j] = PARTICLE_RADIUS
                velocities[i, j] *= -1  # Reverse velocity on wall collision
            elif positions[i, j] > BOX_SIZE - PARTICLE_RADIUS:
                positions[i, j] = BOX_SIZE - PARTICLE_RADIUS
                velocities[i, j] *= -1  # Reverse velocity on wall collision
    
    # Handle collisions between particles (elastic collisions)
    for i in range(NUM_PARTICLES):
        for j in range(i + 1, NUM_PARTICLES):
            # Calculate distance between particles
            delta_pos = positions[i] - positions[j]
            dist = np.linalg.norm(delta_pos)
            
            # Check if particles are colliding
            if dist < 2 * PARTICLE_RADIUS:
                # Normalize the distance vector
                normal = delta_pos / dist
                
                # Relative velocity
                relative_velocity = velocities[i] - velocities[j]
                
                # Calculate the velocity along the normal (dot product)
                velocity_along_normal = np.dot(relative_velocity, normal)
                
                # Only proceed if particles are moving towards each other
                if velocity_along_normal < 0:
                    # Calculate impulse (elastic collision with equal masses)
                    impulse = (2 * MASS * velocity_along_normal) / (2 * MASS)
                    
                    # Update velocities
                    velocities[i] -= impulse * normal
                    velocities[j] += impulse * normal
    
    return positions, velocities

# Set up the plot
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.3)
scat = ax.scatter(positions[:, 0], positions[:, 1], s=20, c='blue')
red_particle, = ax.plot([], [], 'r-', lw=2)  # Red particle's path
ax.set_xlim(0, BOX_SIZE)
ax.set_ylim(0, BOX_SIZE)

# Add a slider for temperature
ax_temp = plt.axes([0.1, 0.15, 0.8, 0.03])
temp_slider = Slider(ax_temp, 'Temperature (K)', 0, 500, valinit=250)  # Range: 0 K to 500 K

# Add a reset button
ax_reset = plt.axes([0.8, 0.05, 0.1, 0.04])
reset_button = Button(ax_reset, 'Reset')

# Global variable to store temperature
current_temperature = temp_slider.val

# Function to update temperature when slider is changed
def update_temperature(val):
    global current_temperature
    current_temperature = temp_slider.val

temp_slider.on_changed(update_temperature)

# Function to reset the simulation
def reset(event):
    global positions, velocities, red_particle_path
    positions = np.random.uniform(PARTICLE_RADIUS, BOX_SIZE - PARTICLE_RADIUS, (NUM_PARTICLES, 2))
    velocities = np.random.normal(0, 1, (NUM_PARTICLES, 2))  # Random initial velocities
    red_particle_path = []
    scat.set_offsets(positions)
    red_particle.set_data([], [])
    plt.draw()

reset_button.on_clicked(reset)

# Animation function
def animate(frame):
    global positions, velocities, red_particle_path
    
    # Update particle positions and velocities
    positions, velocities = update_positions(positions, velocities, current_temperature)
    
    # Update the red particle's path
    red_particle_path.append(positions[0].copy())  # Track the first particle
    if len(red_particle_path) > 1000:  # Limit the path length
        red_particle_path.pop(0)
    
    # Update the scatter plot
    scat.set_offsets(positions)
    
    # Update the red particle's path plot
    red_particle.set_data([p[0] for p in red_particle_path], [p[1] for p in red_particle_path])
    
    return scat, red_particle

# Create animation
ani = FuncAnimation(fig, animate, frames=200, interval=50, blit=True)

plt.show()
