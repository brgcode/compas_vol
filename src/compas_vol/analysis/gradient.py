from compas.geometry import Point
from compas.geometry import Vector


class Gradient(object):
    """
    A Gradient object calculates the ∇ (Nabla), or the direction vector of
    the gradient of a distance function. It is perpendicular to the 0-level
    iso-surface for points on the boundary.

    Parameters
    ----------
    o : :class:`compas_vol` distance object.
        The object with the signed distance function to calculate the gradient from.
    e : float
        Epsilon, the offset (+/-) for the central distance calculation.
    """

    def __init__(self, o, e=0.01):
        self.o = o
        self.e = e
        self.ex = Point(e, 0, 0)
        self.ey = Point(0, e, 0)
        self.ez = Point(0, 0, e)

    def get_gradient_regular(self, point):
        """
        central difference gradient method
        """
        import warnings
        warnings.warn("get_gradient_regular is deprecated and might/will be removed in the future", DeprecationWarning, 2)

        dx = self.o.get_distance(point + self.ex) - self.o.get_distance(
            point + self.ex * -1
        )
        dy = self.o.get_distance(point + self.ey) - self.o.get_distance(
            point + self.ey * -1
        )
        dz = self.o.get_distance(point + self.ez) - self.o.get_distance(
            point + self.ez * -1
        )
        v = Vector(dx, dy, dz)
        v.unitize()
        return v

    def get_gradient(self, point):
        """
        central differences, with tetrahedron technique. 30-40% faster regular `get_gradient_regular`.
        """
        d0 = self.o.get_distance(Point(point.x + self.e, point.y - self.e, point.z - self.e))
        d1 = self.o.get_distance(Point(point.x - self.e, point.y - self.e, point.z + self.e))
        d2 = self.o.get_distance(Point(point.x - self.e, point.y + self.e, point.z - self.e))
        d3 = self.o.get_distance(Point(point.x + self.e, point.y + self.e, point.z + self.e))
        v = Vector(d0 - d1 - d2 + d3, -d0 - d1 + d2 + d3, -d0 + d1 - d2 + d3)
        v.unitize()
        return v

    def get_gradient_numpy_regular(self, x, y, z):
        import warnings
        warnings.warn("get_gradient_numpy_regular is deprecated and might/will be removed in the future", DeprecationWarning, 2)

        import numpy as np
        dx = self.o.get_distance_numpy(x + self.e, y, z) - self.o.get_distance_numpy(
            x - self.e, y, z
        )
        dy = self.o.get_distance_numpy(x, y + self.e, z) - self.o.get_distance_numpy(
            x, y - self.e, z
        )
        dz = self.o.get_distance_numpy(x, y, z + self.e) - self.o.get_distance_numpy(
            x, y, z - self.e
        )
        return np.array([dx, dy, dz]).T

    def get_gradient_numpy(self, x, y, z):
        """
        vectorized tetrahedron difference method for gradient
        """
        import numpy as np
        d0 = self.o.get_distance_numpy(x + self.e, y - self.e, z - self.e)
        d1 = self.o.get_distance_numpy(x - self.e, y - self.e, z + self.e)
        d2 = self.o.get_distance_numpy(x - self.e, y + self.e, z - self.e)
        d3 = self.o.get_distance_numpy(x + self.e, y + self.e, z + self.e)
        dx, dy, dz = (d0 - d1 - d2 + d3, -d0 - d1 + d2 + d3, -d0 + d1 - d2 + d3)
        return np.array([dx, dy, dz]).T
