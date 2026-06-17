import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

class FEMSolver:
    def __init__(self, nelx, nely, KE):
        self.nelx = nelx
        self.nely = nely
        self.KE = KE
        self.ndof = 2 * (nelx + 1) * (nely + 1)
        self._prepare_assembly_indices()

    def _prepare_assembly_indices(self):
        """Precomputes mesh indices to vectorize global matrix assembly."""
        nely, nelx = self.nely, self.nelx
        self.edofMat = np.zeros((nelx * nely, 8), dtype=int)
        
        for elx in range(nelx):
            for ely in range(nely):
                el = ely + elx * nely
                n1 = (nely + 1) * elx + ely
                n2 = (nely + 1) * (elx + 1) + ely
                self.edofMat[el, :] = np.array([
                    2*n1, 2*n1+1, 2*n2, 2*n2+1, 
                    2*n2+2, 2*n2+3, 2*n1+2, 2*n1+3
                ])
                
        self.iK = np.kron(self.edofMat, np.ones((8, 1))).flatten()
        self.jK = np.kron(self.edofMat, np.ones((1, 8))).flatten()

    def solve(self, x, penal, Emin, E0, free_dofs, f):
        """Assembles sparse stiffness matrix and solves KU = F."""
        # SIMP Material Interpolation
        E_penalized = Emin + x**penal * (E0 - Emin)
        
        # Assemble global stiffness matrix
        sK = ((self.KE.flatten()[np.newaxis]).T * E_penalized).flatten(order='F')
        K = coo_matrix((sK, (self.iK, self.jK)), shape=(self.ndof, self.ndof)).tocsc()
        
        # Eliminate fixed DOFs and solve
        K_free = K[free_dofs, :][:, free_dofs]
        u = np.zeros((self.ndof, 1))
        
        # Solve the linear system
        u[free_dofs, 0] = spsolve(K_free, f[free_dofs])
        
        return u
