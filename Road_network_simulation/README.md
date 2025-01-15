# DS830-Intro-to-Programming (Group B13)
# Road Network Simulation with Car Placement

This program simulates road network generation and car placement using both random and custom configurations. It incorporates modular functionality for validation, error handling, and visualization.

---

## Structure

The program consists of the following main components:

1. **Main Module (highway-sim.py)(SimWindow.py)**:
- "The main"- file acts as the interface for the user to configure and generate road networks, allowing users to choose 
  between random/custom road generation, setting simulation parametres and handle traffic setup.
  
The 'modules' directory contains essential components for the simulation, and enables dynamic road generation, traffic management, and performance analysis:

 -   customtypes.py: Defines data structures like Node, Segment, and Graph.
 -   road.py: Manages road segments and their properties.
 -   intersection.py: Handles logic for traffic at intersections.
 -   roadnetworkgenerator.py: Generates random or custom road networks.
 -   map_manager.py: Oversees traffic flow, car placement, and movement.
 -   car.py: Define and manage individual car behavior.
 -   loggers.py: Provides logging for debugging and execution tracking.
 -   utils.py: Contains helper functions for common operations.
 -   validators.py: Offers utility functions to validate user inputs, ensuring they meet 
     requirements such as valid options.
 -   intersection.py: Represents an intersection in the simulation with properties to 
     simulate traffic flow and vehicle movements.
 
2. **Plotting(flux_plotting.py, flux_roadnetwork.txt, flux_roadnetwork_as_csv.txt)**:
   - flux_plotting. py: Plots the average flux of incoming and outgoing cars. Includes 
     error bars representing the standard deviation 
     for each data point. The data is sourced from an Excel file, which contains results 
     from running the simulation 10 times for each injection probability. 
     
3. **Test Module (`test_file.py`)**:
   - Contains unittests to validate the functionality of core components, such as map and car generation:
   - **Test Modules**:
   - test_car_class.py: Car class functionality.
   - test_custom_road_network.py: Custom road network generation.
   - test_general_road_network.py: General road network operations.
   - test_handle_generation.py: User interaction for map generation.
   - test_intersection.py: Road intersection logic.
   - test_random_road_network.py: Random road network generation.
   - test_road.py: Road segment functionality.
   - test_traffic_handler.py: Traffic handling.
   - test_utils.py: Utility functions.
---

## Features

- **Map Generation**:
  - **Random**: Users can define the number of road segments and their lengths.
  - **Custom**: Users provide a file with road segment coordinates, validated for connectivity, non-diagonal structure, and absence of 
      overlaps or intersections.
    
- **Error Handling**:
  - **Input Validation**: Ensures input integrity for integers, options, paths, and file contents.
    
- **Visualization**:
  - **Dynamic Rendering**: Displays road networks and dynamically moving cars using the SimWindow module for real-time simulation.

- **Simulation**:
   - **Dynamic Car Movement**: Cars update their paths and directions based on road connections, simulating realistic traffic behavior.
   - **Scalable Configurations**: Accommodates user-defined parameters for road networks and car placements.

---

## Installation Requirements

- Python 3.12.4
  
**Standard Python Libraries**: 
- logging: https://docs.python.org/3/library/logging.html
- sys: https://docs.python.org/3/library/sys.html
- unittest: https://docs.python.org/3/library/unittest.html
- re: https://docs.python.org/3/library/re.html
- os: https://docs.python.org/3/library/os.html
- random: https://docs.python.org/3/library/random.html
- typing: https://docs.python.org/3/library/typing.html
- numpy: https://numpy.org/doc/2.2/
- matplotlib: https://matplotlib.org/stable/index.html


## Usage

1. Download the entire directory.

2. Run the program using Python:
   ```bash
   python highway-sim.py

Follow on-screen prompts to:

- Generate maps (random or custom).
- Choose injection probability for placement of cars

## Input Formats

-**Map Segments**: Each line defines a road segment with coordinates in the format:
_"x1, y1, x2, y2"_

_Example_:\
_"0, 0, 10, 0\
10, 0, 10, 10"_
