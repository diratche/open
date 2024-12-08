import numpy as np
import matplotlib.pyplot as plt

def generate_samples(target_distribution={'mean': np.array([2.0, 2.0]), 'cov': np.array([[1.0, 0.8], [0.8, 1.0]])},
                     methods=['ULA', 'MALA', 'SGLD'],
                     n_samples=2000,
                     step_size=0.1,
                     burn_in=100,
                     start_point=np.array([0.0, 0.0]),
                    ):
    """
    Inputs:
    - target_distribution: dictionary with keys 'mean': np.array() and 'cov': np.array(), the covariance matrix.
    - methods: list of methods in 'ULA', 'MALA' and 'SGLD'.
    - n_samples: number of samples to be generated for each method.
    - step_size: Step size.
    - burn_in: Number of initial samples to discard.
    - start_point: The starting point as a np.array() of same dimension as target_distribution['mean'].
    Output:
    - samples: dictionary with methods as keys and np.array() of samples as values.
    """
    
    # Define the target distribution as a 2D Gaussian
    def log_potential(x, target_distribution=target_distribution):
        """Log potential function for the target distribution."""
        mean = target_distribution['mean']
        cov_inv = np.linalg.inv(target_distribution['cov'])  # Inverse of covariance matrix
        diff = x - mean
        g = -0.5 * diff.T @ cov_inv @ diff
        return g + np.cos(x[0]) + np.sin(x[1])
    
    def grad_log_potential(x, target_distribution=target_distribution):
        """Gradient of the log potential function."""
        mean = target_distribution['mean']
        cov_inv = np.linalg.inv(target_distribution['cov'])  # Inverse of covariance matrix
        diff = x - mean
        grad_gaussian = -cov_inv @ diff
        grad_cos_sin = np.array([-np.sin(x[0]), np.cos(x[1])])  # Gradient of cos(x[0]) + sin(x[1])
        return grad_gaussian + grad_cos_sin
    
    # Langevin Monte Carlo sampling
    samples = {}
    for method in methods:
        samples[method] = [start_point]
        current = start_point
        for i in range(n_samples + burn_in):
            # Calculate gradient of the log potential
            grad = grad_log_potential(current, target_distribution)
            if method == 'SGLD':
                noise_gradient = np.random.normal(0, 0.1, size=current.shape)  # Simulate subsampling noise
                grad = grad + noise_gradient
            # Propose a new position using Langevin dynamics
            noise = np.sqrt(2 * step_size) * np.random.normal(size=current.shape)
            proposed = current + step_size * grad + noise
            # Accept the new position (Langevin Monte Carlo has an implicit acceptance rate of 1)
            if method == 'MALA':
                grad_proposed = grad_log_potential(proposed, target_distribution)
                log_q_forward = -np.sum((proposed - current - step_size * grad) ** 2) / (4 * step_size)
                log_q_backward = -np.sum((current - proposed - step_size * grad_proposed) ** 2) / (4 * step_size)
                log_acceptance_ratio = log_potential(proposed, target_distribution) - log_potential(current, target_distribution) + log_q_backward - log_q_forward
                if np.log(np.random.uniform(0, 1)) < log_acceptance_ratio:
                    current = proposed  # Accept the proposal
            else:
                current = proposed
            samples[method].append(current)
        # Convert list of samples to a NumPy array if necessary and discard burn-in samples
        samples[method] = np.array(samples[method][burn_in:])
        
    return samples

def display_langevin(samples,
                     target_distribution={'mean': np.array([2.0, 2.0]), 'cov': np.array([[1.0, 0.8], [0.8, 1.0]])},
                     start_point=np.array([0.0, 0.0]),
                    ):

    def log_potential(x, target_distribution=target_distribution):
        """Log potential function for the target distribution."""
        mean = target_distribution['mean']
        cov_inv = np.linalg.inv(target_distribution['cov'])  # Inverse of covariance matrix
        diff = x - mean
        g = -0.5 * diff.T @ cov_inv @ diff
        return g + np.cos(x[0]) + np.sin(x[1])

    def display_one_method(method, method_samples, target_distribution):   
        # Plot the samples and the target distribution contour
        x, y = np.meshgrid(np.linspace(-3, 6, 100), np.linspace(-6, 3, 100))
        z = np.exp(np.vectorize(lambda x, y: log_potential(np.array([x, y])))(x, y))
        plt.figure(figsize=(8, 6))
        plt.contourf(x, y, z, levels=30, cmap="viridis", alpha=0.7)
        plt.plot(method_samples[:, 0], method_samples[:, 1], 'o', markersize=2, color="red", alpha=0.6, label="LMC samples")
        plt.scatter(*start_point, color="blue", label="Start point")
        plt.title(f"Langevin Monte Carlo Sampling ({method})")
        plt.xlabel("X1")
        plt.ylabel("X2")
        plt.legend()
        plt.grid()
        plt.show()

    methods = list(samples.keys())
    for method in methods:
        display_one_method(method, samples[method], target_distribution)
