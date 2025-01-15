import unittest
import numpy as np
from collections import deque
from modules.road import Road


class Test_road(unittest.TestCase):
    def test_init(self):
        segment = [(0, 0), (0, 5)]
        direction = (0, 1)
        road = Road(segment, direction, 1,probability=0.1)
        self.assertTrue((road.startnode == np.array(segment[0])).all())
        self.assertTrue((road.endnode == np.array(segment[1])).all())
        self.assertTrue((road.direction == np.array(direction)).all())
        self.assertEqual(road.connected_intersection, None)
        self.assertEqual(road.cars, deque())
        self.assertFalse(road.has_entry)
        self.assertFalse(road.has_exit)
        self.assertEqual(road.spawn_probability, 0.1)
        
class Test_generate_car_from_gate(unittest.TestCase):

    def test_generate_car_two_cars_if_one_moved_away(self):
        segment = [(0, 0), (0, 7)]
        road = Road(segment,(0,1), clearance=1,entry=True)
        self.assertEqual(len(road.cars), 0)
        road.generate_car_from_gate()
        self.assertEqual(len(road.cars), 1)
        
        road.cars[-1].move(np.array([0, 1000]))
        road.generate_car_from_gate()
        self.assertEqual(len(road.cars), 2)
    
    def test_generate_car_no_car_if_no_entry(self):
        segment = [(0, 0), (0, 5)]
        road = Road(segment,(0,1), clearance=1,entry=False)
        self.assertEqual(len(road.cars), 0)
        road.generate_car_from_gate()
        self.assertEqual(len(road.cars), 0)
    
    def test_generate_2nd_car_but_car_too_close(self):
        segment = [(0, 0), (0,5)]
        road = Road(segment,(0,1), entry=True,clearance=1,probability=1)
        self.assertEqual(len(road.cars), 0)
        road.generate_car_from_gate()
        self.assertEqual(len(road.cars), 1)
        
        road.generate_car_from_gate()
        self.assertEqual(len(road.cars), 1)

class Test_add_car(unittest.TestCase):
    def test_add_car(self):
        segment = [(0, 0), (0, 5)]

        road2 = Road(segment,(0,1), clearance=1,entry=True,probability=1)
        road2.generate_car_from_gate()

        road = Road(segment,(0,1), 1)

        for car in road2.cars:
            road.add_car(car)
        self.assertEqual(road.cars[-1], road2.cars[0])
        
class Test_remove_first_car(unittest.TestCase):
    def test_remove_first_car(self):
        segment = [(0, 0), (0, 5)]

        road = Road(segment,(0,1), 1)
        road.cars.append(1)
        road.cars.append(2)
        road.remove_first_car()
        self.assertEqual(road.cars[0], 2)

class Test_limitations(unittest.TestCase):
    def test_min_clearance(self):
        segment = [(0, 0), (0, 5)]

        with self.assertRaises(ValueError):
            road = Road(segment,(0,1), 0,probability=0.1)

    def test_clearance_larger_than_road_length(self):
        segment = [(0, 0), (0, 5)]

        with self.assertRaises(ValueError):
            road = Road(segment,(0,1), 6,probability=0.1)
    
    def test_probability_out_of_range(self):
        segment = [(0, 0), (0, 5)]

        with self.assertRaises(ValueError):
            road = Road(segment,(0,1), 1,probability=1.1)
            
        with self.assertRaises(ValueError):
            road = Road(segment,(0,1), 1,probability=-0.1)