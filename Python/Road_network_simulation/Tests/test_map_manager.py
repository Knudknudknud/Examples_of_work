import unittest
from modules.map_manager import MapManager
from modules.road import Road
import numpy as np
from modules import roadnetworkgenerator as rng


class Test_validate_road_length(unittest.TestCase):

    def setUp(self):
        segs =  [((0,0),(100,0)), ((100,0), (100,100)), ((100,100),(0, 100)), ((0,100),(0,0)),
        ((0,0),(0,-100)), ((200,100),(100,100))]
        entry_nodes = [(200,100)]
        exit_gates = [(0,-100)]
        customnetwork = rng.CustomRoadNetwork(segs)
        self.dt = MapManager(customnetwork.outgoing,clearance=6, entry_gates=entry_nodes,exit_gates=exit_gates,probability=1)
    
    def tearDown(self):
        return super().tearDown()
    
    def test_road_too_short_for_clearence(self):
        self.dt.min_clearance = 10000
        self.assertFalse(self.dt._validate_roads())
    
    def test_road_length_barely_ok(self):
        self.dt.min_clearance = 50 
        self.assertTrue(self.dt._validate_roads())

    def test_barely_nok_ok(self):
        self.dt.min_clearance = 51
        self.assertFalse(self.dt._validate_roads())

    def test_generate_diagonal_roads(self):
        road = Road(((0,0), (100,100)),(1,1),6)
        self.dt.roads = [road]
        self.assertFalse(self.dt._validate_roads())


class Test_generate_roads(unittest.TestCase):
    def setUp(self):
        segs=  [((0,0),(100,0)),]
        entry_nodes = [(0,0)]
        exit_gates = [(100,0)]
        customnetwork = rng.CustomRoadNetwork(segs)
        self.dt = MapManager(customnetwork.outgoing,clearance=6, entry_gates=entry_nodes,exit_gates=exit_gates,probability=1)
    
    def tearDown(self):
        return super().tearDown()

    def test_generate_roads(self):
        self.assertTrue(len(self.dt.roads) == 1)
        self.assertTrue(np.array_equal(self.dt.roads[0].endnode, (100,0)))
        self.assertTrue(np.array_equal(self.dt.roads[0].startnode, (0,0)))
        self.assertTrue(self.dt.roads[0].has_entry == True)

    def test_probability_bound(self):

        segs=  [((0,0),(100,0)),]
        entry_nodes = [(0,0)]
        exit_gates = [(100,0)]
        customnetwork = rng.CustomRoadNetwork(segs)
        
        self.dt._generate_roads(customnetwork.outgoing, entry_gates=entry_nodes, exit_gates=exit_gates, probability=0.5)

        with self.assertRaises(ValueError):
            self.dt._generate_roads(customnetwork.outgoing, entry_gates=entry_nodes, exit_gates=exit_gates, probability=1.1)
        
        with self.assertRaises(ValueError):
            self.dt._generate_roads(customnetwork.outgoing, entry_gates=entry_nodes, exit_gates=exit_gates, probability=-0.1)

   
class Test_generate_intersections(unittest.TestCase):
    #sequentially this also tests the _generate_intersections method successfully.
    def setUp(self):
        segs =  [((0,0),(100,0)), ((100,0), (100,100)), ((100,100),(0, 100)), ((0,100),(0,0)),
        ((0,0),(0,-100)), ((200,100),(100,100))]
        entry_nodes = [(200,100)]
        exit_gates = [(0,-100)]
        customnetwork = rng.CustomRoadNetwork(segs)
        self.dt = MapManager(customnetwork.outgoing,clearance=6, entry_gates=entry_nodes,exit_gates=exit_gates,probability=1)
    
    def tearDown(self):
        return super().tearDown()

    def test_all_intersections_present(self):
        visited = {road: False for road in self.dt.roads}
        for road in self.dt.roads:
            for intersection in self.dt.intersections:
                if np.array_equal(road.startnode, intersection.position):
                    visited[road] = True

        visited_end = {road: False for road in self.dt.roads}
        for road in self.dt.roads:
            for intersection in self.dt.intersections:
                if np.array_equal(road.endnode, intersection.position):
                    visited_end[road] = True
        self.assertTrue(all(visited.values()))
        self.assertTrue(all(visited_end.values()))


class Test_max_speed(unittest.TestCase):
    def setUp(self):
        segs =  [((0,0),(100,0))]
        entry_nodes = [(0,0)]
        exit_gates = [(0,100)]
        customnetwork = rng.CustomRoadNetwork(segs)
        self.dt = MapManager(customnetwork.outgoing,clearance=6, entry_gates=entry_nodes,exit_gates=exit_gates,probability=1)
    

    def test_car_infront(self):
        self.dt.generate_cars()
        self.dt.roads[0].cars[0].position = np.array((50,0))
        self.dt.generate_cars()
        self.dt.roads[0].cars[1].position = np.array((43.5,0))
        self.dt.roads[0].cars[1].max_speed = 1

        speed = self.dt._max_speed(car= self.dt.roads[0].cars[1],car_in_front=self.dt.roads[0].cars[0],
                                               road=self.dt.roads[0])
        #as the clearence would restrict further movement
        self.assertTrue(speed == 0.5)
    
    def test_car_infront_outside_of_clearence(self):
        self.dt.generate_cars()
        self.dt.roads[0].cars[0].position = np.array((50,0))
        self.dt.generate_cars()
        self.dt.roads[0].cars[1].position = np.array((42,0))
        self.dt.roads[0].cars[1].max_speed = 1

        speed = self.dt._max_speed(car= self.dt.roads[0].cars[1],car_in_front=self.dt.roads[0].cars[0],
                                               road=self.dt.roads[0])

        self.assertTrue(speed == 1)

    def test_no_car_infront(self):
        self.dt.generate_cars()
        self.dt.roads[0].cars[0].position = np.array((50,0))
        self.dt.roads[0].cars[0].max_speed = 10

        speed = self.dt._max_speed(car= self.dt.roads[0].cars[0],car_in_front=None,
                                               road=self.dt.roads[0])

        self.assertTrue(speed == 10)
    def test_dist_to_end_restrict(self):
        self.dt.generate_cars()
        self.dt.roads[0].cars[0].position = np.array((95,0))
        self.dt.roads[0].cars[0].max_speed = 10

        speed = self.dt._max_speed(car= self.dt.roads[0].cars[0],car_in_front=None,
                                               road=self.dt.roads[0])

        self.assertTrue(speed == 5)


class Test_move_car(unittest.TestCase):

    pass

class Test_handle_exit(unittest.TestCase):

    def setUp(self):
        
        segs =  [((0,0),(100,0))]
        entry_nodes = [(0,0)]
        exit_gates = [(100,0)]
        customnetwork = rng.CustomRoadNetwork(segs)
        self.dt = MapManager(customnetwork.outgoing,clearance=6, entry_gates=entry_nodes,exit_gates=exit_gates,probability=1)
    
    

    def tearDown(self):
        return super().tearDown()
    

    def test_exit(self):
        self.dt.generate_cars()
        self.dt._handle_exit(self.dt.roads[0], self.dt.roads[0].connected_intersection)
        self.assertEqual(len(self.dt.roads[0].cars), 0)
    

class Test_move_cars(unittest.TestCase):

    def setUp(self):
        segs = [((0,0),(100,0))]
        entry_nodes = [(0,0)]
        exit_gates = [(100,0)]
        customnetwork = rng.CustomRoadNetwork(segs)
        self.dt = MapManager(customnetwork.outgoing, clearance=6, entry_gates=entry_nodes, exit_gates=exit_gates, probability=1)    
        self.dt.generate_cars()
    

    def tearDown(self):
        return super().tearDown()

    def test_move_cars_no_obstacles(self):
        car = self.dt.roads[0].cars[0]
        car.position = np.array((0,0))
        car.max_speed = 10
        self.dt.move_cars()
        self.assertTrue(np.array_equal(car.position, np.array((10,0))))

    def test_move_cars_with_obstacle(self):
        car1 = self.dt.roads[0].cars[0]
        car1.position = np.array((10,0))
        car1.max_speed = 10

        self.dt.generate_cars()
        car2 = self.dt.roads[0].cars[1]
        car2.position = np.array((4,0))
        car2.max_speed = 20

        self.dt.move_cars()
        self.assertTrue(np.array_equal(car1.position, np.array((20,0))))
        self.assertTrue(np.array_equal(car2.position, np.array((14,0))))

    def test_move_to_stop_line(self):
        car = self.dt.roads[0].cars[0]
        car.position = np.array((90,0))
        car.max_speed = 10
        with unittest.mock.patch('modules.intersection.Intersection.can_approach', return_value=False):
            self.dt.move_cars()
            self.assertTrue(np.array_equal(car.position, np.array((94,0))))
    
    def test_move_to_exit_and_remove(self):
        car1 = self.dt.roads[0].cars[0]
        car1.position = np.array((95,0))
        car1.max_speed = 10

        self.dt.move_cars()
        self.assertTrue(np.array_equal(car1.position, np.array((100,0))))
        self.assertEqual(len(self.dt.roads[0].cars), 0)
