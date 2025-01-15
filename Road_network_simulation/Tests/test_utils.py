import unittest
from modules.utils import Utils as utils

class Test_pick_direction(unittest.TestCase):
    def test_pick_direction(self):
        """Test pick direction, expects a valid direction."""
        available_directions = [(0, 1)]
        result = utils.pick_item(available_directions)
        self.assertEqual(result, (0, 1))

    def test_pick_direction_no_directions(self):
        """Test pick direction with no available directions, expects None."""
        available_directions = []
        result = utils.pick_item(available_directions)
        self.assertEqual(result, None)

    def test_pick_with_weight(self):
        """Test pick direction with weight, expects a valid direction.
            Done by selecting a very high weight and examining if a very unlikely result occurs.
        """
        available_directions = [(0, 1),(1, 0)]
        weighted_direction = (1, 0)
        weight = 2**63
        results = {direction: 0 for direction in available_directions}

        for _ in range(1000):
            result = utils.pick_item(available_directions,weighted_direction,weight)
            results[result] += 1

        if results[(1, 0)] < 996:
            self.fail("Weighted direction was not picked enough times.")
