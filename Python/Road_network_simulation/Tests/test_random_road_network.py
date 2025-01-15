import unittest
from unittest.mock import patch
from modules.roadnetworkgenerator import RandomRoadNetwork as dt

class Test_generate(unittest.TestCase):
    def test_generate_amount(self):
        """Tests generation of a road network with 20 segments"""
        object = dt(20,1)
        result = object.outgoing
        count = 0
        for start_node in result:
            for _,__ in result[start_node]:
                count += 1
        self.assertEqual(count, 20)

    def test_generate_negative(self):
        with self.assertRaises(ValueError):
            result = dt(-1,1)
            
    def test_generate_zero(self):
        with self.assertRaises(ValueError):
            result = dt(0,1)
    

class Test_find_endnode(unittest.TestCase):

    def test_longer_endnode(self):
        """Tests generation of a longer road, where same direction is picked twice"""
        start_node = (0, 0)
        direction = (0, 1)
        nw = dt(1,1)
        nw.outgoing = {}
        nw.incoming = {}
        with patch('modules.utils.Utils.pick_item', side_effect=[(0, 1), (0, 1), (1, 0)]):
            result = nw._find_endnode(start_node, direction)
            self.assertEqual(result, (0, 3))

    def test_normal_length(self):
        """Tests generation of a normal length road"""
        start_node = (0, 0)
        direction = (0, 1)

        with patch('modules.utils.Utils.pick_item', return_value=(1, 0)):
            nw = dt(1,1)
            nw.outgoing = {}
            nw.incoming = {}
            nw._add_segment(((0, 0), (0, 1)))
            result = nw._find_endnode(start_node, direction)
            self.assertEqual(result, (0, 1))

class Test_check_is_obstacle(unittest.TestCase):
    def test_not_obstacle(self):
        temp = dt(1,1)  # Create an instance of the class
        temp.blocked_nodes.add((0, 0))
        temp.blocked_nodes.add((1, 2))
        result = temp._node_is_obstacle((0, 1))  # Pass both arguments
        self.assertEqual(result, False)

        
    def test_check_is_obstacle(self):
        node = (0, 1)
        temp = dt(1,1)
        temp.blocked_nodes.add((0, 1))
        result = temp._node_is_obstacle(node)
        self.assertEqual(result,True)

class Test_check_available_directions(unittest.TestCase):
    def test_no_directions_due_to_full_node(self):
        """Node is fully connected, expects empty list"""
        start_node = (0, 0)
        road_network = {(0, 0): [((0, 1), (0, 1)),((0, -1), (0, -1)),((1, 0), (1, 0)),((-1, 0), (-1, 0))],
                        (0, 1): [((0, -1), (0, 0))],
                        (0, -1): [((0, 1), (0, 0))],
                        (1, 0): [((0, 0), (1, 0))]}
        nw = dt(1,1)
        nw.outgoing = road_network
        result = nw._get_available_directions(start_node)
        self.assertEqual(result, [])

    def test_no_directions_due_to_obstacle(self):
        """Node is blocked by an obstacle, expects empty list"""
        node = (0, 0)
        dt_instance = dt(1,1)
        for element in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dt_instance.blocked_nodes.add(element)

        result = dt_instance._get_available_directions(node)
        self.assertEqual(result, [])


class Test_upscale_road_network(unittest.TestCase):
    def test_upscale_road_network(self):
        initial_segments = [((0, 0), (0, 1)), ((0, 1), (0, 2))]
        road_network = dt(1,1)
        road_network.outgoing = {}
        road_network.incoming = {}
        for segment in initial_segments:
            road_network._add_segment(segment)

        road_network._upscale_road_network(3)   
        expected = {(0, 0): [((0, 1), (0, 3))], (0, 3): [((0, 1), (0, 6))], (0, 6): []}
        self.assertEqual(road_network.outgoing, expected)

    def test_upscales_incoming(self):
        initial_segments = [((0, 0), (0, 1)), ((0, 1), (0, 2))]
        road_network = dt(1,3)
        road_network.outgoing = {}
        road_network.incoming = {}
        for segment in initial_segments:
            road_network._add_segment(segment)

        road_network._upscale_road_network(3)   
        expected = {(0,0): [],(0, 3): [(0, 0)], (0, 6): [(0, 3)]}
        self.assertEqual(road_network.incoming, expected)
    

    def test_float_upscale(self):
        road_network = dt(1,1)
        road_network.outgoing = {}
        road_network.incoming = {}

        initial_segments = [((0, 0), (0, 1)), ((0, 1), (0, 2))]
        for segment in initial_segments:
            road_network._add_segment(segment)
        with self.assertRaises(ValueError):
            road_network._upscale_road_network(3.5)
    
    def test_negative_upscale(self):
        road_network = dt(1,1)
        road_network.outgoing = {}
        road_network.incoming = {}
        initial_segments = [((0, 0), (0, 1)), ((0, 1), (0, 2))]
        for segment in initial_segments:
            road_network._add_segment(segment)
        with self.assertRaises(ValueError):
            road_network._upscale_road_network(-3)

    def test_zero_upscale(self):
        #Generate a road network and overwrite it
        road_network = dt(total_segments=1,scalar=1)
        with self.assertRaises(ValueError):
            road_network._upscale_road_network(0)

    def test_string_upscale(self):
        road_network = dt(1,1)
        road_network.outgoing = {}
        road_network.incoming = {}
        initial_segments = [((0, 0), (0, 1)), ((0, 1), (0, 2))]
        for segment in initial_segments:
            road_network._add_segment(segment)
        with self.assertRaises(TypeError):
            road_network._upscale_road_network("3")
