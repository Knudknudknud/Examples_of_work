import unittest
from unittest.mock import patch
from modules.roadnetworkgenerator import CustomRoadNetwork as dt
import logging 
logging.disable(logging.CRITICAL)


class Test_adjacent_overlap(unittest.TestCase):

    def test_duplicate_lines_vertical(self):
        segments = [((0,1),(0,5)),((3,3),(3,9)),((4,0),(4,9)),((0,1),(0,5))]
        segments.sort(key=lambda line: line[0][1])
        with self.assertRaises(ValueError):
            dt._check_adjacent_overlap(segments,'vertical')

    def test_correct_handle_of_vertical(self):
        segments = [((0,1),(0,5)),((3,3),(3,9)),((4,0),(4,9))]
        segments.sort(key=lambda line: line[0][1])
        result = dt._check_adjacent_overlap(segments,'vertical')
        self.assertEqual(result, None)
    
    def test_duplicate_lines_horizontal(self):
        segments = [((1,0),(5,0)),((3,3),(9,3)),((0,4),(9,4)),((1,0),(5,0))]
        segments.sort(key= lambda line: line[0][0])
        with self.assertRaises(ValueError):
            dt._check_adjacent_overlap(segments,'horizontal')

    def test_correct_horizontal_lines(self):
        segments = [((1,0),(5,0)),((3,3),(9,3)),((0,4),(9,4))]
        segments.sort(key= lambda line: line[0][0])
        result = dt._check_adjacent_overlap(segments,'horizontal')
        self.assertEqual(result,None)

    def test_correct_test_only_if_sorted(self):
        segments = [((1,0),(5,0)),((-1,0),(0,0)),((3,0),(3,6))]
        with self.assertRaises(ValueError):
            dt._check_adjacent_overlap(segments,'horizontal')
    
class Test_sort_by_direction(unittest.TestCase):
    def test_vertical_and_horizontal_no_diag(self):
        segments = [((0,0),(0,5)),((5,0),(10,0))]
        vertical, horizontal = dt._sort_by_direction(segments)
        self.assertEqual(vertical,[((0, 0), (0, 5))])
        self.assertEqual(horizontal, [((5, 0), (10, 0))])

    def test_no_lines(self):
        segments = []
        vertical, horizontal = dt._sort_by_direction(segments)
        self.assertEqual(vertical, [])
        self.assertEqual(horizontal,[])


    def test_vertical_and_horizontal_diag(self):
        segments = [((0,0),(0,5)),((5,0),(10,0)),((5,3),(7,4))]
        with self.assertRaises(ValueError):
            dt._sort_by_direction(segments)

class Test_intersections(unittest.TestCase):
    def test_intersection_between_lines(self):    
        horizontal = [((0,0),(5,0))]
        vertical = [((2,-3),(2,5))]
        with self.assertRaises(ValueError):
            dt._check_intersections(horizontal,vertical)

    def test_intersection_at_endpoints(self):
        horizontal = [((0,0),(5,0))]
        vertical = [((0,-3),(0,5))]
        with self.assertRaises(ValueError):
            dt._check_intersections(horizontal,vertical)
    
    def test_line_start_at_end_point(self):
        horizontal = [((0,0),(5,0))]
        vertical = [((0,0),(0,5))]
        result = dt._check_intersections(horizontal,vertical)
        self.assertEqual(result,None)

    def test_line_end_at_end_point(self):
        horizontal = [((0,0),(5,0))]
        vertical = [((0,-5),(0,0))]
        result = dt._check_intersections(horizontal,vertical)
        self.assertEqual(result,None)

    def test_line_starts_middle_of_line(self):
        horizontal = [((0,0),(5,0))]
        vertical = [((2,0),(2,5))]
        with self.assertRaises(ValueError):
            dt._check_intersections(horizontal,vertical)

    def test_no_intersection(self):
        horizontal = [((0,0),(5,0))]
        vertical = [((2,2),(2,5))]
        result = dt._check_intersections(horizontal,vertical)
        self.assertEqual(result,None)

class Test_connected_network(unittest.TestCase):

    def test_is_connected_network_directed(self):

        def patched_init(self,segments):
            self.outgoing = {}
            self.incoming = {}
            self._generate_roads(segments)

        segments =[ 
            ((0, 0), (1, 0)),
            ((1, 0), (1, 1)),  
            ((1, 1), (2, 1)),  
            ((2, 1), (10, 1))]
        with patch.object(dt, '__init__', patched_init):
            road_network = dt(segments)
            result = road_network._check_is_connected_network()
            self.assertEqual(result, None)
        
    def test_is_not_connected_network(self):
        segments =[
            ((0, 0), (1, 0)),
            ((1, 0), (1, 1)),
            ((1, 1), (2, 1)),
            ((50, 50), (50, 60))]
        
        def patched_init(self,segments):
            self.outgoing = {}
            self.incoming = {}
            self._generate_roads(segments)
        with patch.object(dt, '__init__', patched_init):
            with self.assertRaises(ValueError):
                a = dt(segments)
                a._check_is_connected_network()

    def test_is_connnected_only_if_undirected(self):
        segments =[
            ((0, 0), (1, 0)),
            ((1, 0), (1, 1)),
            ((1, 1), (2, 1)),
            ((2, 1), (2, 2)),
            ((2, 4), (2, 2))]
        
        def patched_init(self,segments):
            self.outgoing = {}
            self.incoming = {}
            self._generate_roads(segments)
        
        with patch.object(dt, '__init__', patched_init):
            a = dt(segments)
            a._check_is_connected_network()
    
    def test_start_at_isolated_node(self):
        """Code always starts at first node."""
        segments =[
            ((50, 50), (50, 60)),
            ((0, 0), (1, 0)),
            ((1, 0), (1, 1)),
            ((1, 1), (2, 1))]
        def patched_init(self,segments):
            self.outgoing = {}
            self.incoming = {}
            self._generate_roads(segments)
        with patch.object(dt, '__init__', patched_init):
            with self.assertRaises(ValueError):
                a = dt(segments)
                a._check_is_connected_network()
    def test_empty_road_network(self):
        segments =[]
        def patched_init(self,segments):
            self.outgoing = {}
            self.incoming = {}
            self._generate_roads(segments)
        with patch.object(dt, '__init__', patched_init):
            a = dt(segments)
            a._check_is_connected_network()
