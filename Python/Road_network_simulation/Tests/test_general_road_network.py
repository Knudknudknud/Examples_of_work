import unittest
from modules.loggers import *
from modules.roadnetworkgenerator import AsymmetricRoadNetwork as dt


#change test to undirected graph
class Test_generate(unittest.TestCase):
    def test_build_correct_network(self):
        segments = [((0, 0), (0, 1)), ((0, 1), (0, 2)), ((0, 2), (0, 3))]
        road_network = dt()
        for segment in segments:
            road_network._add_segment(segment)
        expected = {
            (0, 0): [((0, 1), (0, 1))],
            (0, 1): [((0, 1), (0, 2))],
            (0, 2): [((0, 1), (0, 3))],
            (0, 3): []
        }
        self.assertEqual(road_network.outgoing, expected)
     
    def test_empty_network(self):
        """Empty network, expects empty dictionary."""
        segments = []
        road_network = dt()
        for segment in segments:
            road_network._add_segment(segment)
        self.assertEqual(road_network.outgoing, {})
    
    def test_incorrect_network(self):
        """Contains a diagonal line, expects error."""
        segments = [((0, 0), (0, 1)), ((0, 1), (0, 2)), ((0, 2), (0, 3)), ((3, 3), (3, 3))]
        with self.assertRaises(ValueError):
            road_network = dt()
            for segment in segments:
                road_network._add_segment(segment)
    
class Test_add_segment_to_road_network(unittest.TestCase):
     
    def test_add_segment(self):
        road_network = dt()
        segment = ((0, 0), (0, 1))
        road_network._add_segment(segment)
        expected = {(0, 0): [((0, 1), (0, 1))], (0, 1): []}
        self.assertEqual(road_network.outgoing, expected)

    def test_add_diagonal_line(self):
        road_network = dt()
        segment = ((0, 0), (1, 1))
        with self.assertRaises(ValueError):
            road_network._add_segment(segment)

    def test_add_duplicate(self):
        road_network = dt()
        segment = ((0, 0), (0, 1))
        road_network._add_segment(segment)
        with self.assertRaises(ValueError):
            road_network._add_segment(segment)

class Test_get_unit_vector(unittest.TestCase):

    def test_horizontal_line(self):
        """Horizontal line, expects (0, 1)."""
        segment = ((0, 0), (0, 1))
        road_network = dt()
        result = dt.get_unit_vector(segment)
        self.assertEqual(result, (0, 1))

    def test_vertical_line(self):
        """Vertical line, expects (1, 0)."""
        segment = ((0, 0), (1, 0))
        road_network = dt()
        result = road_network.get_unit_vector(segment)
        self.assertEqual(result, (1, 0))

    def test_diagonal_line(self):
        """Diagonal line, expects ValueError."""
        segment = ((0, 0), (1, 1))
        road_network = dt()
        with self.assertRaises(ValueError):
            road_network.get_unit_vector(segment)
    
    def test_null_vector(self):
        """Null vector, expects ValueError."""
        segment = ((0, 0), (0, 0))
        road_network = dt()
        with self.assertRaises(ValueError):
            road_network.get_unit_vector(segment)

class Test_convert_road_network_to_segments(unittest.TestCase):

    def test_convert_road_network_to_segments(self):
        road_network = dt()
        segments = [((0, 0), (0, 1)), ((0, 1), (0, 2))]
        for segment in segments:
            road_network._add_segment(segment)
        result = road_network.convert_to_segments()
        self.assertEqual(result, segments)

    def test_empty_road_network(self):
        road_network = dt()

        result = road_network.convert_to_segments()
        self.assertEqual(result, [])

class Test_ensure_node_in_network(unittest.TestCase):
    pass
class Test_ensure_not_duplicate_road(unittest.TestCase):
    pass

class Test_segment_in_network(unittest.TestCase):
    pass

class Test_remove_segment(unittest.TestCase):
    pass

class Test_invert_segment(unittest.TestCase):
    pass

class Test_find_exit_gates(unittest.TestCase):

    def test_no_gates(self):
        road_network = dt()
        segments = [((0, 0), (0, 1)), ((0, 1), (1,1)),((1,1),(1,0)),((1,0),(0,0))]

        for segment in segments:
            road_network._add_segment(segment)
        road_network._generate_gates()
        entry_gates = road_network.entry_gates
        exit_gates = road_network.exit_gates
        self.assertEqual(entry_gates, [])
        self.assertEqual(exit_gates, [])


    def test_one_leading_in_zero_out(self):
        segments= [((0, 0), (0,1))]
        road_network = dt()
        for segment in segments:
            road_network._add_segment(segment)
        road_network._generate_gates()
        exit_gates = road_network.exit_gates
        self.assertEqual(exit_gates, [(0, 1)])
        
    def test_two_in_zero_out(self):
        segments= [((0, 0 ), (0, 1)), ((1,1), (0,1))]
        road_network = dt()
        for segment in segments:
            road_network._add_segment(segment)
        road_network._generate_gates()
        exit_gates = road_network.exit_gates
        self.assertEqual(exit_gates, [])

    def test_one_in_one_out(self):
        segments = [((0, 0), (0, 1)), ((0, 1), (1,1))]
        road_network = dt()
        for segment in segments:
            road_network._add_segment(segment)
        road_network._generate_gates()
        exit_gates = road_network.exit_gates

        self.assertEqual(exit_gates, [(1, 1)])

    def test_one_in_two_out(self):
        segments = [((0, 0), (0, 1)), ((0, 1), (1, 1)), ((1, 1), (1, 2))]
        road_network = dt()
        for segment in segments:
            road_network._add_segment(segment)
        road_network._generate_gates()
        exit_gates = road_network.exit_gates

        self.assertEqual(exit_gates, [(1, 2)])

class Test_find_entry_gates(unittest.TestCase):
    def test_none_in_one_out(self):
        segments = [((0, 0), (0, 1))]
        road_network = dt()
        for segment in segments:
            road_network._add_segment(segment)
        road_network._generate_gates()
        entry_gates = road_network.entry_gates
        self.assertEqual(entry_gates, [(0, 0)])

    def test_none_in_two_out(self):
        segments = [((0, 0), (0, 1)), ((0, 0), (1, 0))]
        road_network = dt()
        for segment in segments:
            road_network._add_segment(segment)
        road_network._generate_gates()
        entry_gates = road_network.entry_gates
        self.assertEqual(entry_gates, [])

    def test_one_in_one_out(self):
        segments = [((0, 0), (0, 1)), ((0, 1), (1, 1))]
        road_network = dt()
        for segment in segments:
            road_network._add_segment(segment)
        road_network._generate_gates()
        entry_gates = road_network.entry_gates
        self.assertEqual(entry_gates, [(0, 0)])
    
    def test_two_in_one_out(self):
        segments = [((0, 0), (0, 1)), ((1, 0), (0, 0)), ((-1, 0), (0, 0))]
        road_network = dt()
        for segment in segments:
            road_network._add_segment(segment)
        road_network._generate_gates()
        entry_gates = road_network.entry_gates
     
        self.assertCountEqual(entry_gates, [(-1, 0), (1, 0)])

class Test_ensure_no_illegal_intersection(unittest.TestCase):
    
    def test_only_legal_intersections(self):
        segments = [((0, 0), (0, 1)), ((0, 1), (0, 2)), ((0, 2), (0, 3))]
        road_network = dt()
        for segment in segments:
            road_network._add_segment(segment)
        road_network._generate_gates()
        road_network.search_for_invalid_intersections()
    
    def test_illegal_intersection(self):
        segments = [((0, 0), (0, 1)),((0,2), (0, 1)) ]
        road_network = dt()
        for segment in segments:
            road_network._add_segment(segment)
        road_network._generate_gates()
        with self.assertRaises(ValueError):
            road_network.search_for_invalid_intersections()
            
    def test_two_lines_merge_then_exit(self):
        segments= [((0, 0), (0, 1)), ((1,1), (0,1)), ((0,1), (0,2))]
        road_network = dt()
        road_network.entry_gates = [(0,0), (1,1)]
        road_network.exit_gates = [(0,2)]
        for segment in segments:
            road_network._add_segment(segment)
        road_network.search_for_invalid_intersections()
    
    def test_multiple_entrances_single_exit(self):
        segments = [((0, 0), (1, 0)), ((2, 0), (1, 0)), ((1, 0), (1, 1))]
        road_network = dt()
        road_network.entry_gates = [(0, 0), (2, 0)]
        road_network.exit_gates = [(1, 1)]
        for segment in segments:
            road_network._add_segment(segment)
        road_network.search_for_invalid_intersections()  # Should not raise an error

    def test_entrance_to_dead_end(self):
        segments = [((0, 0), (1, 0))]
        road_network = dt()
        road_network.entry_gates = [(0, 0)]
        road_network.exit_gates = []  # No valid exit
        for segment in segments:
            road_network._add_segment(segment)
        with self.assertRaises(ValueError):
            road_network.search_for_invalid_intersections()
        
  
    def test_three_lanes_into_one_exit(self):
        segments = [((0, 0), (1, 0)), ((1, 1), (1, 0)), ((2, 0), (1, 0)), ((1, 0), (1 , -1))]
        road_network = dt()
        road_network.entry_gates = [(0, 0), (1, 1), (2, 0)]
        road_network.exit_gates = [(1, -1)]
        for segment in segments:
            road_network._add_segment(segment)
        road_network.search_for_invalid_intersections()
    
    def test_no_exit(self):
        segments = [((0, 0), (1, 0)), ((1, 1), (1, 0))]
        road_network = dt()
        for segment in segments:
            road_network._add_segment(segment)
        road_network._generate_gates()
        with self.assertRaises(ValueError):
            road_network.search_for_invalid_intersections()

class Test_intersection_with_no_entrance(unittest.TestCase):
    def test_node_with_only_outgoing_not_gate(self):
        segments = [((0,-20),(0,0)), ((0, -20),(0, -40))]
        a = dt()
        for segment in segments:
            a._add_segment(segment)
        a._generate_gates()
        with self.assertRaises(ValueError):
            a.search_for_invalid_intersections()
    
    def test_node_with_only_incoming_not_gate(self):
        segments = [((0,-20),(0,0)), ((20,0),(0,0))]
        a = dt()
        for segment in segments:
            a._add_segment(segment)
        a._generate_gates()
        with self.assertRaises(ValueError):
            a.search_for_invalid_intersections()
