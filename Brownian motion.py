import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation
from numba import njit

# Constants
NUM_PARTICLES = 50  # Reduced number for better visualization
BOX_SIZE = 10.0
PARTICLE_RADIUS = 0.1
DT = 0.01
MASS = 1.0  # Assume all particles have the same mass

# Initialize particle positions and velocities
positions = np.random.uniform(PARTICLE_RADIUS, BOX_SIZE - PARTICLE_RADIUS, (NUM_PARTICLES, 2))
velocities = np.random.normal(0, 1, (NUM_PARTICLES, 2))  # Random initial velocities

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
plt.subplots_adjust(left=0.1, bottom=0.25)
scat = ax.scatter(positions[:, 0], positions[:, 1], s=20)
ax.set_xlim(0, BOX_SIZE)
ax.set_ylim(0, BOX_SIZE)

# Add a slider for temperature
ax_temp = plt.axes([0.1, 0.1, 0.8, 0.03])
temp_slider = Slider(ax_temp, 'Temperature (K)', 0, 500, valinit=250)  # Range: 0 K to 500 K

# Global variable to store temperature
current_temperature = temp_slider.val

# Function to update temperature when slider is changed
def update_temperature(val):
    global current_temperature
    current_temperature = temp_slider.val

temp_slider.on_changed(update_temperature)

# Animation function
def animate(frame):
    global positions, velocities
    positions, velocities = update_positions(positions, velocities, current_temperature)
    scat.set_offsets(positions)
    return scat,

# Create animation
ani = FuncAnimation(fig, animate, frames=200, interval=50, blit=True)

plt.show()
