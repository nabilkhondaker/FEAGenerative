"""
Finite Element Method (FEM) Package.
Handles sparse global matrix assembly, degree of freedom management, 
and linear system solving.
"""

from .solver import FEMSolver
from .boundary_conditions import apply_cantilever_bcs

__all__ = ['FEMSolver', 'apply_cantilever_bcs']
