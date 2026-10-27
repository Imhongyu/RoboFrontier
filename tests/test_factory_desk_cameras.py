import math
import unittest

import numpy as np

from scripts.factory_desk_cameras import fit_view


class DeskCameraFraming(unittest.TestCase):
    def test_fits_small_and_large_asymmetric_station(self):
        orientation = np.eye(3)
        for scale in (.4, 2., 8.):
            points = np.array([[-scale, -scale / 2, -.8], [scale, -scale / 2, -.8],
                               [scale, scale / 2, .9], [-scale, scale / 2, .9]])
            position, target = fit_view(points, orientation, 43.)
            local = (points - position) @ orientation
            depth = -local[:, 2]
            tangent = math.tan(math.radians(43.) / 2)
            normalized = np.column_stack((local[:, 0] / (depth * tangent * 1.6),
                                          local[:, 1] / (depth * tangent)))
            self.assertTrue((depth > 0).all())
            self.assertLessEqual(float(np.max(np.abs(normalized))), .89)
            self.assertGreater(float(np.ptp(normalized, axis=0).max()), 1.4)
            np.testing.assert_allclose((target - position)[:2], [0, 0], atol=1e-10)


if __name__ == '__main__':
    unittest.main()
