import numpy as np

class OptimalityCriteria:
    def __init__(self, volfrac):
        self.volfrac = volfrac

    def update(self, x, dc):
        """
        Optimality criteria update scheme using a bisection algorithm
        to find the Lagrange multiplier that satisfies the volume constraint.
        """
        l1, l2, move = 0.0, 1e9, 0.2
        xnew = np.zeros_like(x)
        
        # Bisection loop
        while (l2 - l1) > 1e-4:
            lmid = 0.5 * (l2 + l1)
            
            # Update density rule
            xnew = np.maximum(0.0, np.maximum(x - move, 
                   np.minimum(1.0, np.minimum(x + move, x * np.sqrt(-dc / lmid)))))
            
            if np.mean(xnew) - self.volfrac > 0:
                l1 = lmid
            else:
                l2 = lmid
                
        return xnew
