# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'journey planner'
copyright = '2023, group4'
author = 'group4'

# The full version, including alpha/beta/rc tags
release = '0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',  # Support automatic documentation
    'sphinx.ext.coverage', # Automatically check if functions are documented
    'sphinx.ext.mathjax',  # Allow support for algebra
    'sphinx.ext.viewcode', # Include the source code in documentation
    'numpydoc'             # Support NumPy style docstrings
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

"""
London Underground Journey Planner Package
==========================================

This Python package provides tools for planning journeys on the London Underground network. It is designed to 
utilize real-time data to calculate the most efficient routes between stations, considering current network 
conditions and disruptions.

Components:
-----------
1. journey_planner.py: 
   - Contains the main functionality to plan journeys. 
   - It takes a start and destination station, along with a date, and returns the optimal journey path and duration.

2. Network.py:
   - Defines the Network class, used to represent the network of the London Underground.
   - It includes functionality to manipulate and query network data, such as merging networks and retrieving network attributes.

3. query.py:
   - Handles communication with external web services to fetch real-time data about the London Underground network.
   - Provides functions to query specific aspects of the network, like line connections, and integrates this data into the Network class.

Usage:
------
The package can be used to plan journeys across the London Underground. It can handle queries for specific dates 
and times, taking into account real-time network conditions and disruptions. This makes it an invaluable tool for 
both daily commuters and tourists seeking to navigate the city efficiently.

Developed as part of the UCL-COMP0233 course, this package demonstrates the application of network analysis, 
data fetching from web services, and object-oriented programming in Python to solve real-world problems.

Example:
--------
To plan a journey from 'Waterloo' to 'Baker Street' on a specific date:

    from journey_planner import plan_journey
    journey, duration = plan_journey("Waterloo", "Baker Street", "2023-01-01")
    print(f"Journey: {journey}, Duration: {duration} mins")

This package is a prototype and is intended for educational purposes in network analysis and Python programming.
"""

"""
London Underground Journey Planner: User Guide
==============================================

Installation
------------
To install the London Underground Journey Planner package, follow these steps:

1. Ensure you have Python installed on your system. Python 3.6 or later is recommended.
2. Download the package files from the provided source (e.g., GitHub repository, website).
3. Navigate to the directory containing the package files in your terminal or command prompt.
4. Run the installation command:

    pip install .

   This will install the package along with its dependencies.

Alternatively, if the package is hosted on a package repository like PyPI, you can install it directly using pip:

    pip install london-journey-planner

Example Workflow
----------------
After installation, you can use the package to plan journeys on the London Underground. Here's a step-by-step example:

1. Import the `plan_journey` function from the `journey_planner` module:

    from journey_planner import plan_journey

2. Define your start and destination stations along with the date of the journey. For example, to plan a journey from 'Waterloo' to 'Baker Street' on January 1, 2023:

    start_station = "Waterloo"
    destination_station = "Baker Street"
    journey_date = "2023-01-01"

3. Call the `plan_journey` function with these parameters:

    journey, duration = plan_journey(start_station, destination_station, journey_date)

4. The function will return the journey route and duration. You can print these details:

    print(f"Journey: {journey}, Duration: {duration} mins")

This will output the sequence of stations on the journey path and the total journey duration in minutes.

Note: This guide assumes a basic understanding of Python and command-line operations. For more detailed information and troubleshooting, please refer to the package documentation.
"""
"""
London Underground Journey Planner: Developer Guide
===================================================

Contributing to the Repository
------------------------------
We welcome contributions from the community. To contribute to this project, please follow these steps:

1. Fork the Repository:
   - Navigate to the GitHub page of the repository and use the 'Fork' button to create your own copy.

2. Clone the Forked Repository:
   - Clone your forked repository to your local machine:
     git clone https://github.com/your-username/london-journey-planner.git

3. Create a New Branch:
   - Navigate into the cloned directory and create a new branch for your feature or bug fix:
     git checkout -b your-feature-branch

4. Make Your Changes:
   - Implement your feature or bug fix.

5. Write Tests:
   - Add or update tests to cover your changes.

6. Follow the Coding Style:
   - Ensure your code adheres to the project's coding standards (PEP 8 for Python).

7. Commit Your Changes:
   - Commit your changes with a clear and descriptive commit message.

8. Push to GitHub:
   - Push your changes to your fork on GitHub.

9. Submit a Pull Request:
   - Open a pull request from your feature branch to the main repository.

Your pull request will be reviewed by the maintainers and merged into the main codebase after review and approval.

Testing the Code
----------------
To ensure the reliability of the package, please follow these guidelines for testing:

1. Write Unit Tests:
   - Add unit tests for every new feature or bug fix in the `tests` directory.
   - Use Python's built-in `unittest` framework or a framework like `pytest`.

2. Run Tests Locally:
   - Run the test suite locally to ensure that all tests pass before submitting a pull request.
   - You can use commands like `python -m unittest discover` or `pytest`.

3. Continuous Integration:
   - The project uses continuous integration (CI) tools (e.g., GitHub Actions, Travis CI). Ensure that your code passes all CI checks.

Coding Style
------------
This project adheres to the PEP 8 style guide for Python code. Please ensure your code follows these guidelines:

- Use 4 spaces for indentation.
- Limit lines to 79 characters.
- Use descriptive variable and function names.
- Document your code with docstrings.

Additional Resources
--------------------
For more information on contributing, testing, and coding styles, please refer to the following resources:

- PEP 8 Style Guide: https://www.python.org/dev/peps/pep-0008/
- Git and GitHub Guide: https://guides.github.com/
- Python Testing: https://docs.python.org/3/library/unittest.html

We appreciate your interest in contributing to the London Underground Journey Planner package and look forward to your valuable contributions!
"""


#journey_planner 
import argparse
import query
from Network import Network
import matplotlib.pyplot as plt
from datetime import date

def plan_journey(start, dest, date):
    """
    This function calculates the optimal journey path and duration from a start station to a destination station on a specified date.

    It utilizes the London Tube network data to compute the journey, considering real-time network conditions.

    Args:
        start (int, str): The ID or name of the start station.
        dest (int, str): The ID or name of the destination station.
        date (str): The date of the journey in the format 'YYYY-MM-DD'.

    Returns:
        journey (list): A list containing the IDs of stations along the journey path, in the order of travel.
        duration (float): The total time spent for the journey, in minutes.

    The function converts station names to IDs if necessary and employs Dijkstra's algorithm (through the 'query' module)
    to find the shortest path and duration. It handles both numeric and string inputs for station identifiers.

    Example:
        >>> plan_journey("Waterloo", "Baker Street", "2023-01-01")
        ([10, 23, 45], 35.0)
    """
    # Function implementation...

#Network
import numpy as np
import argparse
from datetime import datetime
import matplotlib.pyplot as plt

class Network:
    """
    A class to represent a network, characterized by its number of nodes and adjacency matrix.

    Attributes:
        n_nodes (int): The number of nodes in the network.
        adjacency_matrix (numpy.ndarray): A 2D array representing the adjacency matrix of the network.

    Methods:
        __add__(self, other): Enables the addition of two Network objects to merge their networks.
    """

    def __init__(self, n_nodes, adjacency_matrix):
        """
        Initializes a new Network object with a given number of nodes and an adjacency matrix.

        Args:
            n_nodes (int): The number of nodes in the network.
            adjacency_matrix (numpy.ndarray): A 2D numpy array representing the network's adjacency matrix,
                                              where each element represents the connection weight between nodes.

        Example:
            >>> n_nodes = 5
            >>> adjacency_matrix = np.zeros((n_nodes, n_nodes))
            >>> network = Network(n_nodes, adjacency_matrix)
        """
        self.n_nodes = n_nodes
        self.adjacency_matrix = adjacency_matrix

    def __add__(self, other):
        """
        Overloads the + operator to allow the addition of two Network objects.

        This method merges two networks by adding their adjacency matrices. It assumes both networks have the same number of nodes.

        Args:
            other (Network): Another Network object to add.

        Returns:
            Network: A new Network object representing the merged network.

        Raises:
            ValueError: If the two networks have different numbers of nodes.

        Example:
            >>> network1 = Network(5, np.zeros((5, 5)))
            >>> network2 = Network(5, np.ones((5, 5)))
            >>> combined_network = network1 + network2
        """
        # Method implementation...

#query
import requests
from datetime import date
import csv
from io import StringIO
import numpy as np
from Network import Network

def query_line_connections(line_identifier):
    """
    Queries information about the connectivity of a specific line in the London tube network and returns a Network object representing that line.

    This function communicates with a web service to obtain the line's connectivity data and constructs a network representation from it.

    Args:
        line_identifier (int): The identifier for a specific line in the London tube network.

    Returns:
        Network: A Network object representing the connectivity of the queried line. The Network object contains an adjacency matrix representing the line's stations and connections.

    Raises:
        HTTPError: If the request to the web service fails.

    Example:
        >>> query_line_connections(1)  # Querying for a specific line
        Network object representing the connectivity of line 1

    The function initializes an adjacency matrix for the London tube network, makes a request to the web service, 
    and parses the response to populate the matrix. It handles exceptions for failed requests.
    """
    # Function implementation...
