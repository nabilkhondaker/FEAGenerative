import numpy as np

class OptimizationConfig:
    def __init__(self):
        # Grid Resolution
        self.nelx = 120           # Number of elements in X (Length)
        self.nely = 40            # Number of elements in Y (Height)
        
        # SIMP Parameters
        self.volfrac = 0.4        # Target volume fraction (40% of material kept)
        self.penal = 3.0          # Penalization power to force 0 or 1 densities
        self.rmin = 1.5           # Filter radius (prevents checkerboard patterns)
        
        # Material Properties
        self.E0 = 1.0             # Young's Modulus of solid material
        self.Emin = 1e-9          # Void material stiffness (prevents singular matrix)
        self.nu = 0.3             # Poisson's ratio
        
        # Optimizer Settings
        self.max_loop = 100       # Maximum iterations
        self.tol = 0.01           # Convergence tolerance
