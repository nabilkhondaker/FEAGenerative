# run_optimization.py
# full program engineered by nabil khondaker ahmad
import numpy as np
import matplotlib.pyplot as plt

# Import from the complex engine architecture
from config.parameters import OptimizationConfig
from engine.mesh.elements import QuadElement
from engine.fem.boundary_conditions import apply_cantilever_bcs
from engine.fem.solver import FEMSolver
from engine.optimization.filters import MeshFilter
from engine.optimization.simp_oc import OptimalityCriteria

def main():
    print("INITIALIZING TOPOLOGY OPTIMIZATION ENGINE...")
    
    # 1. Load Configurations
    cfg = OptimizationConfig()
    
    # 2. Initialize Core Mechanics Components
    element = QuadElement(cfg.E0, cfg.nu)
    fem_solver = FEMSolver(cfg.nelx, cfg.nely, element.KE)
    fixed_dofs, free_dofs, f = apply_cantilever_bcs(cfg.nelx, cfg.nely)
    
    # 3. Initialize Optimization Components
    mesh_filter = MeshFilter(cfg.nelx, cfg.nely, cfg.rmin)
    optimizer = OptimalityCriteria(cfg.volfrac)
    
    # 4. Initial State Setup
    x = np.ones(cfg.nelx * cfg.nely) * cfg.volfrac
    loop = 0
    change = 1.0
    
    # 5. Visualization Setup
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 4))
    im = ax.imshow(-x.reshape((cfg.nelx, cfg.nely)).T, cmap='gray', 
                   interpolation='none', vmin=-1, vmax=0)
    ax.set_title("Generative Design Engine: Iteration 0")
    plt.axis('off')
    
    print("BEGINNING ITERATIVE SOLVER...")
    
    # 6. Main Optimization Loop
    while change > cfg.tol and loop < cfg.max_loop:
        loop += 1
        x_old = x.copy()
        
        # A. Finite Element Analysis (Displacements)
        u = fem_solver.solve(x, cfg.penal, cfg.Emin, cfg.E0, free_dofs, f)
        
        # B. Objective Function & Sensitivity Analysis (Compliance Calculation)
        ce = np.zeros(cfg.nelx * cfg.nely)
        for el in range(cfg.nelx * cfg.nely):
            ue = u[fem_solver.edofMat[el, :]]
            ce[el] = np.dot(ue.T, np.dot(element.KE, ue)).item()
            
        c = np.sum((cfg.Emin + x**cfg.penal * (cfg.E0 - cfg.Emin)) * ce)
        dc = -cfg.penal * x**(cfg.penal - 1) * (cfg.E0 - cfg.Emin) * ce
        
        # C. Mesh-Independency Filter
        dc = mesh_filter.apply(x, dc)
        
        # D. Optimality Criteria Update
        x = optimizer.update(x, dc)
        
        # E. Calculate Change
        change = np.linalg.norm(x.reshape(cfg.nelx * cfg.nely, 1) - 
                                x_old.reshape(cfg.nelx * cfg.nely, 1), np.inf)
        
        # F. Update Animation
        print(f"  Iteration: {loop:03d} | Compliance: {c:.4f} | Volume: {np.mean(x):.3f} | Change: {change:.4f}")
        im.set_array(-x.reshape((cfg.nelx, cfg.nely)).T)
        ax.set_title(f"Generative Design Engine: Iteration {loop} | Compliance: {c:.2f}")
        plt.draw()
        plt.pause(0.01)
        
    print("\nOPTIMIZATION CONVERGED SUCCESSFULLY.")
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    main()
