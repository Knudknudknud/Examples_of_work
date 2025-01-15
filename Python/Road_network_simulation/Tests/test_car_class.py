import unittest
from modules.car import Car
import numpy as np

class TestCar(unittest.TestCase):
    def test_init(self):
        position = [0, 0]
        car = Car(position=position)
        self.assertEqual(car.ID, 1)
        self.assertEqual(len(car.color), 3)

        self.assertTrue((car.position == np.array(position)).all())

    
    def test_update_id(self):
        # Reset the generation count
        Car.generation_count = 1

        car = Car(position=[0, 0])
        self.assertEqual(car.ID, 1)
        car2 = Car(position=[0, 0])
        self.assertEqual(car2.ID, 2)
    
    def test_move(self):
        car = Car(position=[0, 0])
        car.move(np.array((1, 1)))
        self.assertTrue((car.position == np.array([1, 1])).all())