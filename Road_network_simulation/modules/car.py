import numpy as np
from numpy.typing import NDArray
import random

from modules.custom_types import *

class Car:
    """
    Car object with a unique ID, color and max speed.

    Class methods:
        move(position): Moves the car to a new position.
    """
    generation_count = 1

    def __init__(self, position: Node, speed_range: Tuple[float, float] = (0.7, 1.3)) -> None:
        """
        Generates the properties of a car objects, which includes an ID, color, position, and maximum speed.

        Args:
            position (Node): The position of the car.
            speed_range (Tuple[float,float]): Optional to override the range of speeds that the car can travel at.
            Default range is [0.7,1.3].
        """
       
        self.ID = Car.generation_count
        self.color = tuple(random.choices(range(256),k=3))
        self.max_speed =  random.uniform(speed_range[0],speed_range[1])
        self.position = np.array(position)
  
        Car.generation_count += 1

    def move(self, position: NDArray[np.float64]) -> None:
        """
        Moves the car to a new position.
        Args:
            position (NDArray[np.float64]): The new position of the car. 
                Due to the nature of the simulation, the dimension of the position is 2.
        
        Side effects:
            Changes the position of the car to the new position.
        """
        self.position = position
