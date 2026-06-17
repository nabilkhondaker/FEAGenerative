"""
Numerical Optimization Package.
Implements Solid Isotropic Material with Penalization (SIMP) methodology,
Optimality Criteria (OC) updaters, and mesh-independency filters.
"""

from .filters import MeshFilter
from .simp_oc import OptimalityCriteria

__all__ = ['MeshFilter', 'OptimalityCriteria']
