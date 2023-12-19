.. automodule:: my_package.my_module
   :members:

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