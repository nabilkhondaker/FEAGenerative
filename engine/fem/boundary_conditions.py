import numpy as np

def apply_cantilever_bcs(nelx, nely):
    """
    Defines the Fixed Degrees of Freedom and Load Vector for a cantilever beam.
    Returns: fixed_dofs, free_dofs, forces
    """
    ndof = 2 * (nelx + 1) * (nely + 1)
    
    # Force Vector: Apply downward load at bottom right corner
    f = np.zeros((ndof, 1))
    f[2 * (nelx + 1) * (nely + 1) - 1, 0] = -1.0  
    
    # Fixed DOFs: Left edge is rigidly attached to a wall
    fixed_dofs = np.union1d(
        np.arange(0, 2 * (nely + 1), 2), 
        np.arange(1, 2 * (nely + 1), 2)
    )
    
    all_dofs = np.arange(0, ndof)
    free_dofs = np.setdiff1d(all_dofs, fixed_dofs)
    
    return fixed_dofs, free_dofs, f
