import modules.roadnetworkgenerator as rng
from modules.map_manager import MapManager
from modules.roadnetworkgenerator import * 
from modules.validators import Validators
from SimWindow import SimWindow as ms
import sys


class Main:
    """
    Main interface for the user to configure and generate road networks.
    Allows users to choose between random and custom road generation,
    set simulation parameters, and handle traffic setup.
    """
    def __init__(self):
        """
        Initializes the user interface and handles the initial configuration
        process, including road generation and map manager setup.
        """
        self.road_network = None
        self.map_manager = None
        self.spawn_probability = None
        self.clearance = 6

        options = ['random', 'custom']
        generation_type = Validators.prompt(
            validator=Validators.validate_options,
            prompt=f'Please select the generation type of the roads. \n available options are: {options}.',
            options=options
        )

        options = ['yes', 'no']
        disallow_unreachable_roads = Validators.prompt(
            validator=Validators.validate_options,
            prompt='Would you like to disallow unreachable roads? \n Available options are: yes, no.',
            options=['yes', 'no']
        )
        
        if disallow_unreachable_roads == 'yes':
            disallow_unreachable_roads = True
        else:
            disallow_unreachable_roads = False

        if generation_type == 'random':
            self.handle_random_generation(disallow_unreachable_roads)
    
        elif generation_type == 'custom':
            self.handle_custom_generation(disallow_unreachable_roads)

        self.spawn_probability = Validators.prompt(
            Validators.validate_float,
            prompt='Please enter the spawn probability of cars on the roads.\n'
               'Probability must be between 0 and 1.',
            lower_bound=0,
            upper_bound=1
        )
        
        self.map_manager = MapManager(
            self.road_network.outgoing,
            clearance=self.clearance,
            entry_gates=self.road_network.entry_gates,
            exit_gates=self.road_network.exit_gates,
            probability=self.spawn_probability
        )
        
        self.setup_simulation()
        

    def handle_random_generation(self, strict_generation:bool)->None:
        """
        Handles the process for generating a random road network.

        Args:
            strict_generation (bool): Whether to disallow unreachable roads.

        Prompts:
            - Number of roads to generate (at least 1).
            - Scaling factor for road length (at least 2x clearance).
        
        Side effects:
            -Modifies self.road_network
        """
        lower_bound = 1
        total_segments = Validators.prompt(
            Validators.validate_integer,
            prompt = f'How many roads would you like to generate? \n' \
                    f'At least {lower_bound} roads are required.',
            lower_bound=1
        )

        min_road_scalar = max(self.clearance * 2, 20)
        scaling_factor = Validators.prompt(
            Validators.validate_integer,
            prompt = 'Please choose a scaling factor for the road generation (integer), \n' \
                    f'Lower bound is {min_road_scalar}',
            lower_bound=min_road_scalar
        )

        self.road_network = rng.RandomRoadNetwork(total_segments, scaling_factor, strict_generation)

    
    def handle_custom_generation(self, strict_generation:bool)->None:
        """
        Handles the process for generating a custom road network based on
        a user-provided file.

        Args:
            strict_generation (bool): Whether to disallow unreachable roads.

        Prompts:
            - File path containing road segments.
        
        Side effects:
            -Modifies self.road_network
        """
        while True:
            try:
                path = Validators.prompt(
                    Validators.validate_path,
                    prompt='Please enter the path to the file containing the road segments.'
                )
                segments = Validators.extract_file_data(path)
                self.road_network = rng.CustomRoadNetwork(segments, strict_generation)
                break
            except Exception as e:
                print(e)
                retry = Validators.prompt(
                    Validators.validate_options,
                    prompt='Would you like to retry custom generation?',
                    options=['yes', 'no']
                )
                if retry == 'yes':
                    self.handle_custom_generation(strict_generation)
                else:
                    print('Exiting program.')
                    sys.exit()


    def setup_simulation(self):
        """
        Sets up and launches the simulation window using the generated road network and map manager.
        """
        window = ms()
        window.set_roads(self.road_network.convert_to_segments())
        window.set_in_gates(self.road_network.entry_gates)
        window.set_out_gates(self.road_network.exit_gates)
        window.show(updatecar=self.map_manager.update_car)

if __name__ == '__main__':
    Main()





