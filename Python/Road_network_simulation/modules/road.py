import random
import numpy as np
from numpy.typing import NDArray
from modules.custom_types import *
from collections import deque
from modules.car import Car

class Road:
    """
    Object that simulates a road. The road uses a deque to store cars and follows the FIFO principle.
    Cars may only enter from the back of the deque and exit from the front.
    If the road has an entry gate, cars may be generated at the entry gate with a given probability.
    Lastly, it is possible to calculate the distance between a car and the exit of the road.

    Class methods:
        add_car(car) -> None: Adds a car to the end of the deque.
        remove_first_car() -> None: Removes the front most car in the deque.
        generate_car_from_gate() -> None: If the road has an entry gate, generates a car at the end of the deque.
        distance_to_endnode(position) -> float: Calculates the distance between a point and the the endnode.
    """

    def __init__(self, segment: Segment, direction: Unit_Vector, clearance: float, probability: float = 1, entry: bool = False, exit: bool = False,) -> None:
        """
        Initializes the road object.
 
        Args:
            segment (Segment): The start and end node of the road.
            direction (Unit_Vector): The direction of the road.
            probability (float): Optionally, the probability of a car being generated may be overwritten, [0,1]. Default is 1. 
            entry (bool): If the road has an entry gate. Default is False.
            exit (bool): If the road has an exit gate. Default is False.
            clearance (float): The distance from the endnode where cars should stop and the distance between cars on spawn.
        """
        if probability < 0 or probability > 1:
            raise ValueError("Probability must be between 0 and 1.")
        
        if clearance <= 0:
            raise ValueError("Clearance must be positive.")
        
        if np.linalg.norm(np.array(segment[1]) - np.array(segment[0])) <= clearance:
            raise ValueError("Clearance must be less than the length of the road.")
        
        self.startnode = np.array(segment[0])
        self.endnode = np.array(segment[1])

        if np.linalg.norm(self.endnode - self.startnode) == 0:
            raise ValueError("Road must have a length greater than 0.")
        
        self.direction =  np.array(direction)
        self.spawn_probability = probability
        self.has_entry = entry
        self.has_exit = exit
        self.connected_intersection = None
        self.cars = deque()
        self.clearance = clearance
        self.stop_line = self.endnode - (self.clearance * self.direction)

        

    def add_car(self, car: Car) -> None:
        """
        Adds a car to the end of the deque.

        Args:
            car: Car object
        """
        self.cars.append(car)
    
    def remove_first_car(self) -> Car:
        """
        Remove the front most car in the deque.

        Returns:
            Car: The car that was removed.

        Side effects:
            Removes the front most car in the deque.
        """
        return self.cars.popleft()

    def generate_car_from_gate(self) -> None:
        """
        If the road has an entry gate and there is no car occupying the spawn point,
        generate a car with a given probability.

        Side effects:
            Adds a car to the end of the deque.
        """

        #If the road is an entry road, and the car either has no road, or the closest car is far enough from the spawn point
        if self.has_entry and (not self.cars or np.linalg.norm(self.cars[-1].position - self.startnode) >= self.clearance):
            if random.random() <= self.spawn_probability:
                self.cars.append(Car(position=self.startnode))

    def distance_to_endnode(self, position: NDArray[np.float64]) -> float:
        """
        Calculates the Euclidean distance between a point and the endnode.

        Args:
            position (NDArray[np.float64]): The position of a car.
            
        Returns:
            float: The distance between the car and the endnode.
        """
        return np.linalg.norm(position - self.endnode)
                                 
