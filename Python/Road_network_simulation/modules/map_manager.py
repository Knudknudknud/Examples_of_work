import random
import numpy as np
from modules.road import Road
from modules.intersection import Intersection
from modules.car import Car
from modules.custom_types import *
from typing import List

class MapManager:
    """
    Map manager object that simulates the traffic in the simulation. 
    The simulator handles the interplay between roads, intersections and cars.
    The simulator generates cars from entry gates, and moves them along the roads.
    The simulator also handles special constraints at intersections, to avoid collisions.
    The simulator is called by the SimWindow object, which is responsible for the visualization of the simulation.

    Class methods:
        move_cars(): Moves the cars along the roads.
        handle_exit(car, road, intersection): Handles specific car movement at the end of roads.
        max_speed(car, car_in_front, road): Returns the maximum speed the car may move during the given iteration. 
        generate_cars(): Attempts to generate cars from the roads with entry gates.
        update_car(car_positions, car_colors): Updates car positions and car colors and returns these values.

    Requirements:
        - Road_network must be a graph with nodes and directed non overlapping edges (This is not validated).
            - Cycles are allowed in the road network.
            - Every segment should either have an exit gate or be connected to another segment or the simulation will halt. (This is not validated)
            - Every segment must have a minimum length of 2x the minimum clearance.
            - Every segment must be either horizontal or vertical.
        -Gates are not strictly a requirement, but:
            - if there is no entry gate, no cars will spawn
            - if no exit gate exists, the road network will fill up with cars and the simulation will halt.
            - Each entry/exit gate must be a node in the road network (or it will be ignored).
            - Duplicate entry/exit gates are ignored.
        - The probability of a car being generated at an entry gate must be between 0 and 1.
        - The minimum clearance must be at least 6 to avoid collisions (Assuming SimWindow remains unchanged).

    Requirements handled by the class:
        - The sum of the minimum clearance between two cars and the minimum clearance between a car
          and the intersection must be strictly less than the distance in "Intersection.find available road".
    """

    def __init__(self, road_network: Graph, entry_gates: List[Node], exit_gates: List[Node], probability: float = 0.05, clearance: float = 6) -> None:
        """
        Initializes the map manager object.
    
        Args:
            road_network (Graph): The road network that the simulation is based on.
            entry_gates (List[Node]): The entry gates of the simulation.
            exit_gates (List[Node]): The exit gates of the simulation.
            probability (float): The probability of a car being generated at an entry gate. Default is 0.05.
            clearance (float): The minimum distance between two cars and distance from any outgoing car and the intersection.
                               Setting clearance to less than 6 will cause car collisions.

        Raises:
            ValueError: If the probability is not between 0 and 1.
            ValueError: If the clearance is less than 6.
            ValueError: If the roads are not 2x clearance in length or are not horizontal or vertical.

        Side effects:
            Generates the necessary roads and intersections for the simulation and links these with one another.
            Roads with entry gates are added to the entry roads.
        """
        self.roads = []
        self.entry_roads = []
        self.intersections = []
        self.min_clearance = clearance

        if probability < 0 or probability > 1:
            raise ValueError("Probability must be between 0 and 1.")
        
        if clearance < 6:
            raise ValueError("Clearance must be at least 6 to avoid collision.")
        
        self._generate_roads(road_network, entry_gates, exit_gates, probability)

        #Must be placed after _generate_roads.
        if not self._validate_roads():
            raise ValueError("Roads must be 2x clearance in length and must be horizontal or vertical.")
        
        self._generate_intersections(road_network)

    def _validate_roads(self) -> bool:
        """
        Validates that the shortest road in the simulation is at least 2x the minimum clearance.
        Validates that every road is horizontal or vertical.

        Returns:
            bool: True if the shortest road is at least 2x the minimum clearance and no segment is diagonal, otherwise False.
        """
        min_length = 2 * self.min_clearance
        for road in self.roads:
            if np.linalg.norm(road.endnode - road.startnode) < min_length:
                return False
            elif not (road.direction[0] == 0 or road.direction[1] == 0):
                return False
        return True
    
    def _generate_roads(self, road_network: Graph, entry_gates: List[Node], exit_gates: List[Node], probability: float) -> None:
        """
        Generates the necessary roads for the simulation. 
        If any road has an entry gate, the road is added to the entry roads.

        Args:
            road_network (Graph): The road network that the simulation is based on.
            entry_gates (List[Node]): The entry gates of the simulation.
            exit_gates (List[Node]): The exit gates of the simulation.
            probability (float): The probability of a car being generated at an entry gate, [0,1].
        
        Side effects:
            Creates multiple Road objects and appends them to the roads list.
            If a road has an entry gate, the road is appended to the entry roads list.
        
        Raises:
            ValueError: If the probability is not between 0 and 1.
        """
        if probability < 0 or probability > 1:
            raise ValueError("Probability must be between 0 and 1.")
        
        
        for startnode in road_network:
           for direction, endnode in road_network[startnode]:
                entry = startnode in entry_gates
                exit = endnode in exit_gates
                road = Road((startnode, endnode),direction,self.min_clearance, probability, entry, exit)
                
                self.roads.append(road)

                if entry == True:
                    self.entry_roads.append(road)
    
 
    def _generate_intersections(self, road_network: Graph) -> None:
        """
        Generates the necessary intersections for the simulation.
        Secondly roads are given a reference to their respective outgoing intersection.

        Args:
            road_network (Graph): The road network that the simulation is based on.
        
        Raises:
            ValueError: If a road does not have an exit or a connected segment.

        Side effects:
            Creates multiple Intersection objects and appends them to the intersections list.
            Roads are given a reference to their respective outgoing intersection.
        """
    
        for node in road_network:
                intersection = Intersection(node, clearance=self.min_clearance) 
                self.intersections.append(intersection)
        
        #This line runs in O(n*m) time, but the number of intersections is expected to be small.
        #Could be optimized but since it's only run once, it's not a priority.
        for road in self.roads:
            for intersection in self.intersections:

                if np.array_equal(road.endnode, intersection.position):
                    intersection.add_incoming_road(road)
                    road.connected_intersection = intersection

                if np.array_equal(road.startnode, intersection.position):
                    intersection.add_outgoing_road(road)

    def move_cars(self) -> None:
        """
        Handles the movement of cars along the roads. 
        Roads are shuffled to give different roads priority over intersections between cycles.

        Side effects:
            Deletes cars from the road deque, if they are at an exit gate or move to a new road.
            Appends the car to a new road, if the car moves to a new road.
            Mutates the positions of the cars on the roads.
        """

        #Shuffle the roads, so that priority in intersections is randomized between iterations.
        road_copy = self.roads.copy()
        random.shuffle(road_copy)

        for road in road_copy:
            intersection = road.connected_intersection
            #While this copies the cars, the list still references to the same objects.
            cars = road.cars.copy()
            for i, car in enumerate(cars):
                car_in_front = cars[i - 1] if i > 0 else None

                #Calculate the maximum speed the car may move at and the position it would move to.
                max_speed = self._max_speed(car, car_in_front,road)
                max_position = car.position + (road.direction * max_speed)
                
                #If the car would cross the stopping line, ensure that it may approach the intersection otherwise stop at the stopping line.
                if road.distance_to_endnode(max_position) <= self.min_clearance and not intersection.can_approach(car):
                        car.move(road.stop_line)
                else:
                    car.move(max_position)

                    #This can only occur if the car is the first car in the deque.
                    if np.array_equal(car.position, road.endnode):
                        self._handle_exit(road, intersection)

                
    def _handle_exit(self, road: Road, intersection: Intersection) -> None:
        """
        Handles the movement of a car at the end of a road.
        If a car is at an exit gate, then the car is removed from the road.
        Otherwise, if there exists a road that the car has sufficient clearance to move to, then the car is moved to that road.

        Args:
            road (Road): The road of the current cycle.
            intersection (Intersection): The intersection that the car is at.

        Side effects:
            If the car is at an exit gate, the car is deleted from the road.
            If the car can move to another road, the car is moved to that road and removed from the current road.
        """
        if road.has_exit:
            road.remove_first_car()
        else:
            if new_road := intersection.find_available_road():
                car = road.remove_first_car()
                new_road.add_car(car)


    def _max_speed(self, car: Car, car_in_front: Car, road: Road) -> float:
        """
        Returns  the maximum speed a car may move at.
        If there is a car in front, the car may only move as far as the distance to the car in front minus the minimum clearance.
        If there is no car in front, the car may move as far as the distance to the end of the road.

        Args:
            car (Car): The car of the current cycle.
            car_in_front (Car): The car in front of the current car.
            road (Road): The road of the current cycle.

        Returns:
            float: The maximum speed the car may move at.
        """
        dist_to_end = np.linalg.norm(road.endnode - car.position)

        if car_in_front:
            dist_to_car_infront = np.linalg.norm(car_in_front.position - car.position)
            max_movement = min(dist_to_car_infront - self.min_clearance, car.max_speed)
            
            #safety check to ensure that the car does not move backwards.
            max_movement = max(0, max_movement)
            return min(dist_to_end, max_movement)
        else:
            return min(dist_to_end, car.max_speed)

    def generate_cars(self) -> None:
        """
        Generates cars from entry gates.

        Side effects:
            Adds a car to the end of a road deque, if a spawn is valid.
        """
        for road in self.entry_roads:
                road.generate_car_from_gate()
    
    def update_car(self, car_positions: Position, car_colors: RGB) -> Tuple[List[Position], List[RGB]]:
        """
        Clears the lists of car positions and colors, and updates them with the current positions and colors of the cars in the simulation.

        Args:
            car_positions (List[Position]): The positions of the cars in the simulation.
            car_colors (List[RGB]): The colors of the cars in the simulation.

        Returns:
            Tuple[List[Position], List[RGB]]: The updated positions and colors of the cars in the simulation.
        """
        
        car_positions.clear()
        car_colors.clear()
        self.move_cars()
        self.generate_cars()

        for road in self.roads:
            for car in road.cars:
                car_positions.append(tuple(car.position))
                car_colors.append(car.color)
    
        return car_positions, car_colors
