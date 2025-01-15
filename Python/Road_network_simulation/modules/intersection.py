import numpy as np
import random
from modules.car import Car
from modules.road import Road
from typing import Optional, Tuple


class Intersection:
    """
    Object that represents the intersection in the simulation.
    Each intersection has a position and a list of incoming roads and outgoing roads.
    Likewise a clearence distance, which sets the minimum distance a car must be from the intersection for another to move into the intersection.


    Class methods:
        add_incoming_road(road): Adds a road to the incoming roads.
        add_outgoing_road(road): Adds a road to the outgoing roads.
        distance_to_car(car) -> float: Calculates the distance between the intersection and a car.
        closest_incoming_car(priority_car) -> Car: Finds the closest car in the incoming roads to the intersection.
        closest_outgoing_car() -> Optional[Car]: Finds the closest car in the outgoing roads to the intersection.
        can_approach(car) -> bool: Determines if a car can approach the intersection.
        find_available_road() -> Optional[Road]: Finds the next road that a car can move to.
    """
    def __init__(self, position: Tuple[float, float], clearance: float)->None:
        """
        Initializes the intersection with a position and empty lists of incoming and outgoing roads.
        
        Args:
            position: Tuple[float,float] - The position of the intersection.
            clearance: float - The minimum distance a car must be from the intersection for another to move into the intersection.
        """
        self.position = np.array(position)
        self.incoming_roads = []
        self.outgoing_roads = []
        self.min_clearance = clearance
    
    def add_incoming_road(self, road: Road)->None:
        """
        Adds a road to the incoming roads.

        Args:
            road: Road - The road to be added to the incoming roads.

        Side effects:
            The road is added to the incoming roads.

        Raises:
            TypeError: If the road is not of type Road.
        """
        if not isinstance(road, Road):
            raise TypeError("Road must be of type Road.")
        
        self.incoming_roads.append(road)
  

    def add_outgoing_road(self, road: Road)->None:
        """
        Adds a road to the outgoing roads.
    
        Args:
            road: Road - The road to be added to the outgoing roads.
        
        Side effects:
            The road is added to the outgoing roads.

        Raises:
            TypeError: If the road is not of type Road.
        """
        if not isinstance(road, Road):
            raise TypeError("Road must be of type Road.")
        
        self.outgoing_roads.append(road)

    def distance_to_car(self, car: Car) -> float:
        """
        Calculates the Euclidean distance between the intersection and a car in its connected roads.

        Args:
            car: Car object

        Returns:
            float: The distance between the intersection and the car.

        Raises:
            TypeError: If the car is not of type Car.
        """
        if not isinstance(car, Car):
            raise TypeError("Car must be of type Car.")
        
        return np.linalg.norm(car.position - self.position)
    
    def closest_incoming_car(self, priority_car: Car) -> Car:
        """
        Finds the closest car in the incoming roads to the intersection. 
        Priority car is the car, to be preferred if two cars are equally close.

        Args:
            priority_car: Car object

        Returns:
            Car: The closest car to the intersection.

        Raises:
            TypeError: If the priority car is not of type Car.
        """
        if not isinstance(priority_car, Car):
            raise TypeError("Car must be of type Car.")
        
        closest_car = priority_car
        min_distance = self.distance_to_car(priority_car)

        for road in self.incoming_roads:
            if road.cars:
                #car[0] is the first car in the deque
                distance = self.distance_to_car(road.cars[0])
                if distance < min_distance:
                    closest_car = road.cars[0]
                    min_distance = distance

        return closest_car
    
    def closest_outgoing_car(self) -> Optional[Car]:
        """
        Calculates the distance to the closest car in the outgoing roads.

        Returns:
            Car: The closest car to the intersection.
            None: If there are no cars in the outgoing roads.
        """
        closest_car = None
        min_distance = float('inf')

        for road in self.outgoing_roads:
            if road.cars:
                #Car that is the last on the road
                distance = self.distance_to_car(road.cars[-1])
                if not closest_car or distance < min_distance:
                    closest_car = road.cars[-1]
                    min_distance = distance
                    
        return closest_car

    def can_approach(self, car: Car) -> bool:
        """
        Determines if a car can approach the intersection. A car can approach the intersection if:
            - There is no car within the clearance distance on an outgoing road.
            - The car is the closest car in the incoming road to the intersection.
            
        Args:
            car: Car object
            
        Returns:
            bool: True if the car can approach the intersection, False otherwise.
            
        Raises:
            TypeError: If the car is not of type Car.
        """

        if not isinstance(car, Car):
            raise TypeError("Car must be of type Car.")

        closest_car = self.closest_outgoing_car()

        #If there is a car on an outgoing road, and it has not left the intersection, disallow the car from approaching.
        if closest_car and self.distance_to_car(closest_car) < self.min_clearance:
            return False
        
        #If another car is already approaching the intersection disallow the car from moving.
        elif car != self.closest_incoming_car(car):
            return False
        
        return True

    def find_available_road(self) -> Optional[Road]:
        """
        Examines all outgoing roads from the intersection. 
        If there exists at least one road that a car can move to, then a random road one is selected.
        A road is available if:
            - There are no cars on the road.
            - The car may move far enough onto the road, such that
              it does not block the intersection (dist > (min dist between two cars + min dist from car to intersection)).
              
        Returns:
            Road: A random road that the car can move to.
            None: If there are no available roads.
        """
        available_roads = []

        for road in self.outgoing_roads:
            if not road.cars:
                available_roads.append(road)
            else:
                #Multiplied by two, as it needs to be able to itself move the clearence distance from the intersection
                if np.linalg.norm(road.cars[-1].position - self.position) >= (self.min_clearance * 2):
                    available_roads.append(road)

        return random.choice(available_roads) if available_roads else None
