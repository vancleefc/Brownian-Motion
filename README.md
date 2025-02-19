Brownian Motion Simulation
This Python script simulates the Brownian motion of particles in a 2D box, with a slider to adjust the temperature dynamically. The simulation includes elastic collisions between particles and the walls of the box, as well as between the particles themselves.

Description
The script models the random motion of particles in a 2D box, where the temperature controls the magnitude of the particles' random motion. At higher temperatures, particles move faster and collide more frequently, while at lower temperatures, particles move slower. At absolute zero (0 K), all particle motion stops. The simulation uses the finite difference method to update particle positions and velocities over time, and it includes realistic elastic collisions between particles and walls.

Dependencies:
Python 3
NumPy
Matplotlib
Numba (for performance optimization)

How It Works
Define the spatial domain: The box is a 2D square of size BOX_SIZE x BOX_SIZE.
Set up initial conditions: Particles are randomly placed within the box, and their initial velocities are set to zero.
Temperature control: A slider allows you to adjust the temperature, which scales the random motion of the particles.
Time evolution: The positions and velocities of the particles are updated at each time step using a finite difference method.
Collision handling: Particles collide elastically with the walls and with each other.
Visualization: The positions of the particles are plotted and animated to show their motion over time.

How to Run
Ensure you have the required dependencies installed. You can install them using pip:
bash
Copy
pip install numpy matplotlib numba
Run the script:
bash
Copy
python brownian_motion.py

Expected Behavior
At 0 K: Particles stop moving entirely (frozen state).
At moderate temperatures (e.g., 250 K): Particles move at a moderate speed, with occasional collisions.
At high temperatures (e.g., 500 K): Particles move rapidly, colliding frequently and bouncing off each other.
Collisions: Particles bounce off the walls and each other realistically, conserving momentum and energy.
