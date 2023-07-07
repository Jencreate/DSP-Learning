#!/usr/bin/env python3

"""
Description: Abstraction to store signal related information.
Author: Jensen Benard
Date Created: July 7, 2023
Date Modified: July 7, 2023
Python Version: 3.11.3
Dependencies: numpy
"""
import numpy as np

class Signal:
    def __init__(self, length, points_count):
        self.len = length
        self.points_count = points_count

        self.x_points = np.linspace(0, self.len - 1, self.points_count)

    def set_custom_output(self, func):
        """ Create an array of output values with a specified function

        Key arguments:
        func -- The function to produce the output values.
        """
        self.y_points = np.array([func(x) for x in self.x_points])

    def set_random_output(self, max_output):
        """ Create an array of random output values.

        Key arguments:
        max_output -- The maximum possible output value allowed.
        """
        self.y_points = np.random.randint(max_output, size=self.len)

    def set_zero_output(self):
        """ Create an array of zero values from a length specified at
        initialisation.
        """
        self.y_points = np.zeros(self.len)





    
