from modules.intersection import Intersection
from modules.car import Car
from modules.road import Road
import numpy as np
import unittest


class Test_intersection(unittest.TestCase):
    def test_init(self):
        position = (0, 0)
        intersection1 = Intersection(position,6)
        self.assertTrue((intersection1.position == position).all())
        self.assertEqual(intersection1.incoming_roads, [])
        self.assertEqual(intersection1.outgoing_roads, [])
    
    def test_add_roads(self):
        position = (0, 0)
        intersection1 = Intersection(position,6)
        road = Road(((-20, 0), (0, 0)),(1,0),clearance=6, entry = True)
        intersection1.add_incoming_road(road)
        self.assertEqual(intersection1.incoming_roads,[road])
        road2 = Road(((20, 0), (0, 0)),(-1,0),clearance=6, entry = True)
        intersection1.add_outgoing_road(road2)
        self.assertEqual(intersection1.outgoing_roads, [road2])
    
    def test_add_roads_wrong_type(self):
        position = (0, 0)
        intersection1 = Intersection(position,6)
        with self.assertRaises(TypeError):
            intersection1.add_incoming_road(1)
        with self.assertRaises(TypeError):
            intersection1.add_outgoing_road(1)
        
class Test_distance_to_car(unittest.TestCase):

    def test_not_car(self):
        position = (0, 0)
        intersection1 = Intersection(position,6)
        with self.assertRaises(TypeError):
            intersection1.distance_to_car(1)

    def test_distance_to_car_positive(self):
        position = (0, 0)
        intersection1 = Intersection(position, 6)
        car = Car((3, 4), (0, 0))
        self.assertEqual(intersection1.distance_to_car(car), 5)
    
    def test_negative_distance_to_car(self):
        position = (0, 0)
        intersection1 = Intersection(position, 6)
        car = Car((-3, -4), (0, 0))
        self.assertEqual(intersection1.distance_to_car(car), 5)

class Test_closest_incoming_car(unittest.TestCase):

    def test_not_car_type(self):
        position = (0, 0)
        intersection1 = Intersection(position,6)
        with self.assertRaises(TypeError):
            intersection1.closest_incoming_car(1)

    def test_closest_incoming_car(self):
        position = (0, 0)
        intersection1 = Intersection(position, 6)

        road = Road(((-20, 0), (0, 0)),(1,0),clearance = 6, entry = True)
        road2 = Road(((20, 0), (0, 0)),(-1,0),clearance = 6, entry = True)

        intersection1.add_incoming_road(road)
        intersection1.add_incoming_road(road2)
        road.generate_car_from_gate()
        road2.generate_car_from_gate()
        road.cars[0].move(np.array((-3,0)))
        road2.cars[0].move(np.array((1,0)))

        self.assertEqual(intersection1.closest_incoming_car(road.cars[0]), road2.cars[0])

    def test_closest_incoming_car_both_same_distance(self):
        position = (0, 0)
        intersection1 = Intersection(position,6)

        road = Road(((-20, 0), (0, 0)),(1,0),clearance = 6, entry = True)
        road2 = Road(((20, 0), (0, 0)),(-1,0),clearance = 6, entry = True)

        intersection1.add_incoming_road(road)
        intersection1.add_incoming_road(road2)
        road.generate_car_from_gate()
        road2.generate_car_from_gate()
        road.cars[0].move(np.array((-3,0)))
        road2.cars[0].move(np.array((3,0)))

        #expects the called car to be priority
        self.assertEqual(intersection1.closest_incoming_car(road.cars[0]), road.cars[0])
    
class Test_closest_outgoing_car(unittest.TestCase):
    def test_closest_outgoing_car(self):
        position = (0, 0)
        intersection1 = Intersection(position,6)

        road = Road(((0, 0), (-20, 0)),(-1,0),clearance=6, entry = False)
        road2 = Road(((0, 0), (20, 0)),(1,0),clearance=6, entry = False)

        car1 = Car((-4, 0), (0, 0))
        road.add_car(car1)
        car2 = Car((5, 0), (0, 0))
        road2.add_car(car2)

        intersection1.add_outgoing_road(road)
        intersection1.add_outgoing_road(road2)

        self.assertEqual(intersection1.closest_outgoing_car(), road.cars[0])

    def test_closest_outgoing_car_no_cars(self):
        position = (0, 0)
        intersection1 = Intersection(position,6)

        road = Road(((-20, 0), (0, 0)),(1,0),clearance=6, entry = False)
        road2 = Road(((20, 0), (0, 0)),(-1,0),clearance=6, entry = False)

        intersection1.add_outgoing_road(road)
        intersection1.add_outgoing_road(road2)

        self.assertEqual(intersection1.closest_outgoing_car(), None)

class Test_can_approach(unittest.TestCase):
    def test_not_car_type(self):
        position = (0, 0)
        intersection1 = Intersection(position,6)
        with self.assertRaises(TypeError):
            intersection1.can_approach(1)
    
    def test_cant_approach_not_closest(self):
        position = (0, 0)
        intersection1 = Intersection(position,6)

        road = Road(((-20, 0), (0, 0)),(1,0),clearance = 6, entry = True)
        road2 = Road(((20, 0), (0, 0)),(-1,0),clearance = 6, entry = True)

        intersection1.add_incoming_road(road)
        intersection1.add_incoming_road(road2)
        road.generate_car_from_gate()
        road2.generate_car_from_gate()
        road.cars[0].move(np.array((-3,0)))
        road2.cars[0].move(np.array((1,0)))

        self.assertFalse(intersection1.can_approach(road.cars[0]))

    def test_can_approach_closest_incoming(self):
        position = (0, 0)
        intersection1 = Intersection(position,6)

        road = Road(((-20, 0), (0, 0)),(1,0),clearance = 6, entry = True)
        road2 = Road(((20, 0), (0, 0)),(-1,0),clearance = 6, entry = True)

        intersection1.add_incoming_road(road)
        intersection1.add_incoming_road(road2)
        road.generate_car_from_gate()
        road2.generate_car_from_gate()
        road.cars[0].move(np.array((-3,0)))
        road2.cars[0].move(np.array((3,0)))

        self.assertTrue(intersection1.can_approach(road.cars[0]))

    def test_can_approach_no_cars(self):
        position = (0, 0)
        intersection1 = Intersection(position,6)

        road = Road(((-20, 0), (0, 0)),(1,0),clearance = 6, entry = True)
        road2 = Road(((0, 0), (20,0)),(1,0), clearance = 6, entry = True)

        intersection1.add_incoming_road(road)
        road.generate_car_from_gate()
        intersection1.add_outgoing_road(road2)

        self.assertTrue(intersection1.can_approach(road.cars[0]))
    
    def test_cant_outgoing_too_close(self):
        position = (0, 0)
        intersection1 = Intersection(position,6)

        road = Road(((-20, 0), (0, 0)),(1,0),clearance = 6, entry = True)
        #Not actually a valid, road but lets you generate easily
        road2 = Road(((0, 0), (20,0)),(-1,0), clearance = 6, entry = True)

        intersection1.add_incoming_road(road)
        intersection1.add_outgoing_road(road2)
        road.generate_car_from_gate()
        road2.generate_car_from_gate()

        self.assertFalse(intersection1.can_approach(road.cars[0]))
    
    def test_cant_outgoing_too_close_edge(self):
        position = (0, 0)
        intersection1 = Intersection(position,6)

        road = Road(((-20, 0), (0, 0)),(1,0),clearance = 6, entry = True)
        #Not actually a valid, road but lets you generate easily
        road2 = Road(((0, 0), (20,0)),(-1,0), clearance = 6, entry = True)

        intersection1.add_incoming_road(road)
        intersection1.add_outgoing_road(road2)
        road.generate_car_from_gate()
        road2.generate_car_from_gate()

        road2.cars[0].move(np.array((5.9999,0)))

        self.assertFalse(intersection1.can_approach(road.cars[0]))

    def test_cant_outgoing_not_too_close_edge(self):
        position = (0, 0)
        intersection1 = Intersection(position,6)

        road = Road(((-20, 0), (0, 0)),(1,0),clearance = 6, entry = True)
        #Not actually a valid, road but lets you generate easily
        road2 = Road(((0, 0), (20,0)),(-1,0), clearance = 6, entry = True)

        intersection1.add_incoming_road(road)
        intersection1.add_outgoing_road(road2)
        road.generate_car_from_gate()
        road2.generate_car_from_gate()

        road2.cars[0].move(np.array((6,0)))

        self.assertTrue(intersection1.can_approach(road.cars[0]))

class Test_find_available_road(unittest.TestCase):
    def test_no_cars_on_road(self):
        position = (0, 0)
        intersection1 = Intersection(position,6)
        road2 = Road(((20, 0), (0, 0)),(0,1), 6)

        intersection1.add_outgoing_road(road2)

        self.assertEqual(intersection1.find_available_road(), road2)
    
    def test_car_within_invalid_range(self):
        position = (0, 0)
        intersection1 = Intersection(position,6)

        road2 = Road(((0, 0), (20, 0)),(0,1),clearance = 6, entry = True)

        intersection1.add_outgoing_road(road2)
        road2.generate_car_from_gate()
        road2.cars[0].move(np.array((11.999,0)))

        self.assertEqual(intersection1.find_available_road(), None)
    
        
    def test_car_not_within_range(self):
        position = (0, 0)
        intersection1 = Intersection(position,6)

        road2 = Road(((0, 0), (20, 0)),(0,1),clearance = 6, entry = True)

        intersection1.add_outgoing_road(road2)
        road2.generate_car_from_gate()
        road2.cars[0].move(np.array((12,0)))

        self.assertEqual(intersection1.find_available_road(), road2)