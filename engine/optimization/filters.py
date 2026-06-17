import numpy as np
from scipy.sparse import coo_matrix

class MeshFilter:
    def __init__(self, nelx, nely, rmin):
        self.nelx = nelx
        self.nely = nely
        self.rmin = rmin
        self.H, self.Hs = self._build_filter()

    def _build_filter(self):
        """Constructs the spatial filter matrix based on search radius."""
        iH = np.ones(self.nelx * self.nely * (2 * int(np.ceil(self.rmin)) - 1)**2)
        jH = np.ones(iH.shape)
        sH = np.zeros(iH.shape)
        k = 0
        for i1 in range(self.nelx):
            for j1 in range(self.nely):
                e1 = i1 * self.nely + j1
                for i2 in range(max(i1 - int(np.ceil(self.rmin)) + 1, 0), 
                                min(i1 + int(np.ceil(self.rmin)), self.nelx)):
                    for j2 in range(max(j1 - int(np.ceil(self.rmin)) + 1, 0), 
                                    min(j1 + int(np.ceil(self.rmin)), self.nely)):
                        e2 = i2 * self.nely + j2
                        iH[k] = e1
                        jH[k] = e2
                        sH[k] = max(0, self.rmin - np.sqrt((i1 - i2)**2 + (j1 - j2)**2))
                        k += 1
        H = coo_matrix((sH[:k], (iH[:k], jH[:k])))
        Hs = np.array(H.sum(1))[:, 0]
        return H, Hs

    def apply(self, x, dc):
        """Applies density filter to the sensitivity derivatives."""
        return np.asarray(self.H.dot(x * dc)) / self.Hs / np.maximum(0.001, x)
