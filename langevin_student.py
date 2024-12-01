import numpy as np
import matplotlib.pyplot as plt

# Define the target distribution as a 2D Gaussian
def log_potential(x):
    """Log potential function for the target distribution."""
    mean = np.array([2.0, -2.0])
    cov_inv = np.linalg.inv(np.array([[1.0, 0.8], [0.8, 1.0]]))  # Inverse of covariance matrix
    diff = x - mean
    g = -0.5 * diff.T @ cov_inv @ diff
    return g + np.cos(x[0]) + np.sin(x[1])

def grad_log_potential(x):
    """Gradient of the log potential function."""
    #fill 
    return 

# Langevin Monte Carlo parameters
n_samples = 2000    # Number of samples
step_size = 0.1     # Step size
burn_in = 100       # Number of initial samples to discard
start_point = np.array([0.0, 0.0])  # Starting point

# Langevin Monte Carlo sampling
samples = [start_point]
current = start_point

for i in range(n_samples + burn_in):
    # Calculate gradient of the log potential
    # fill

    # Propose a new position using Langevin dynamics
    # fill

    # Accept the new position (Langevin Monte Carlo has an implicit acceptance rate of 1)
    # fill
        
# Convert list of samples to a NumPy array if necessary and discard burn-in samples
samples = # fill


# Plot the samples and the target distribution contour
x, y = np.meshgrid(np.linspace(-3, 6, 100), np.linspace(-6, 3, 100))
z = np.exp(np.vectorize(lambda x, y: log_potential(np.array([x, y])))(x, y))

plt.figure(figsize=(8, 6))
plt.contourf(x, y, z, levels=30, cmap="viridis", alpha=0.7)
plt.plot(samples[:, 0], samples[:, 1], 'o', markersize=2, color="red", alpha=0.6, label="LMC samples")
plt.scatter(*start_point, color="blue", label="Start point")
plt.title("Langevin Monte Carlo Sampling")
plt.xlabel("X1")
plt.ylabel("X2")
plt.legend()
plt.grid()
plt.show()
