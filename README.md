**Project Name:** Construction Activity Simulation with Discrete Event Simulation (DES) and Social Force Modeling (SFM)

**Author:** [Mahdi Naeimi Rad- mahdy.naeimyrad@gmail.com]

**Version:** 1.0

**Date:** 2024-01-03

**Description:**

This program simulates the process of building interior walls in a building using a combination of discrete event simulation (DES) and social force modeling (SFM). The goal of this research is to develop a model that can accurately represent the construction process and its impact on productivity. To achieve this, two main approaches are integrated: DES for modeling the work process and SFM for modeling the dynamic movement of workers, with specific emphasis on workspace congestion.

**Key Features:**

* **Work Process Modeling:** DES is utilized to model the sequential steps involved in the wall building process, including task duration, resource requirements, and dependencies.

* **Dynamic Workspace and Worker Movement:** SFM is employed to simulate the real-time movement of workers within the workspace, considering their interactions and the resulting congestion.

* **Crew Size Analysis:** The program allows for analyzing the impact of crew size on productivity, particularly in terms of workspace congestion and worker interactions.

**Installation:**

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
pip install numpy pygame sumpy random sys math config typing time pygame.draw Matplotlib
```

**Usage:**

To run the program, navigate to the project directory and execute the following command in your terminal:

```bash
python simulation1.py
```

This will launch the simulation, visualizing the construction process and worker movements. The simulation will run for a specified number of iterations.

**Examples:**

* **Modifying Workspace Plan:** You can modify the workspace plan by uploading your own jpeg file and defining the location of the walls. The walls can be defined by specifying the start and end points of each wall as lists of coordinates.

* **Data Recording and Modification:** To generate realistic task durations, you'll need to record data from real-world work execution. This data can then be incorporated into the simulation by modifying the probability density functions used in the Random library functions.

* **SFM Parameters:** You can adjust the worker behavior and interactions by modifying the parameters in the SFM module, such as desired speed, mass of the worker, slide friction factor, interaction range, privacy radius, worker current location, and destination.
