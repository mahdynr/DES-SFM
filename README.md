# DES-SFM
## Author
[Mahdi Naeimi Rad- mahdy.naeimyrad@gmail.com]

## Version
1.0

## Date
2024-01-03

## Description
This program simulates the process of building interior walls in a building using a combination of discrete event simulation (DES) and social force modeling (SFM). The goal of this research is to develop a model that can accurately represent the construction process and its impact on productivity. To achieve this, two main approaches are integrated: DES for modeling the work process and SFM for modeling the dynamic movement of workers, with specific emphasis on workspace congestion.

## Key Features

* **Work Process Modeling:** DES is utilized to model the sequential steps involved in the wall-building process, including task duration, resource requirements, and dependencies.

* **Dynamic Workspace and Worker Movement:** SFM is employed to simulate the real-time movement of workers within the workspace, considering their interactions and the resulting congestion.

* **Crew Size Analysis:** The program allows for analyzing the impact of crew size on productivity, particularly in terms of workspace congestion and worker interactions.

## Installation

The only requirement is a working installation of Python 3.x. Additionally, you'll need to install the following libraries:

* Numpy
* pygame
* sumpy
* random
* sys
* math
* config
* typing
* time
* pygame.draw
* Matplotlib

To install these dependencies, use the following command in your terminal:

```bash
pip install numpy matplotlib


## Usage

To run the program, navigate to the project directory and execute the following command in your terminal:

bash
python simulation1.py


This will launch the simulation, visualizing the construction process and worker movements. The simulation will run for a specified number of iterations.

## Examples

* **Modifying Workspace Plan:** You can modify the workspace plan by uploading your own jpeg file and defining the location of the walls. The walls can be defined by specifying the start and end points of each wall as lists of coordinates.

* **Data Recording and Modification:** To generate realistic task durations, you'll need to record data from real-world work execution. This data can then be incorporated into the simulation by modifying the probability density functions used in the Random library functions.

* **SFM Parameters:** You can adjust the worker behavior and interactions by modifying the parameters in the SFM module, such as desired speed, mass of the worker, slide friction factor, interaction range, privacy radius, worker current location, and destination.

## Contribution Guidelines

To contribute to this project, please follow these guidelines:

1. **Code Style:** Adhere to Python coding conventions, such as PEP8.

2. **Licensing:** Maintain the same open-source license (MIT License) for your contributions.

3. **Issue Reporting:** Submit bug reports or feature requests using the issue tracker on GitHub.

## Conclusion

This program provides a valuable tool for analyzing the impact of crew size and workspace congestion on construction activity productivity. The integration of DES and SFM enables a more realistic representation of the construction process, aiding project managers in making informed decisions.

## Code Comments

### tools1.py

This module contains functions for loading the workspace plan, modeling the workspace geometry, and generating worker paths using the Dijkstra algorithm.

python
def load_workspace_plan(plan_path):
    # Load the workspace plan from the specified path
    # ...

    return workspace_data

def model_workspace_geometry(workspace_data):
    # Create a representation of the workspace geometry
    # ...

    return workspace_geometry

def generate_worker_paths(workspace_geometry, worker_locations):
    # Use Dijkstra's algorithm to find the shortest path for each worker from their current location to their destination
    # ...

    return worker_paths


### agent1.py

This module contains the agent class, which represents a worker in the simulation. The agent class manages the worker's movement, interactions with other workers, and task execution.

python
class Agent:
    def __init__(self, id, initial_position, destination, desired_speed, mass, slide_friction_factor, interaction_range, privacy_radius):
        # Initialize the agent's state
        # ...

    def update_position(self, current_time, workspace_geometry):
        # Update the agent's position based on its movement and interactions with other workers
        # ...
