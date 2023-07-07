#!/usr/bin/env python3

"""
Description: Abstraction to plot a given signal on a given axis with an optional index line.
Author: Jensen Benard
Date Created: July 7, 2023
Date Modified: July 7, 2023
Python Version: 3.11.3
Dependencies: matplotlib, signal (local)
"""
import signal as sig
import matplotlib.pyplot as plt

class SignalAxis:
    def __init__(self, signal, axis, title):
        self.signal = signal
        self.axis = axis
        self.signal_line, = self.axis.plot([], [])
        self.axis.set_title = title

    def add_index_line(self, color, label, index_value=0):
        """ Create a new vertical line to show the current index value

        Key arguments:
        color -- The color of the line
        label -- The label of the line to show on the axis.
        index_value -- The x position of the line.
        """

        self.index_line = self.axis.axvline(x=0, color=color)
        self.index_line.set_label(label)
        self.index_line.set_xdata([index_value])


    def update_axis_limits(self, min_x=None, max_x=None, min_y=None, max_y=None, use_signal_for_x=False, use_signal_for_y=False):
        """ Set the axis limits based on hard values to the signal minimum and maximum values for each axis. 

        Key arguments:
        min_x -- The minimum value for the x axis.
        max_x -- The maximum value for the x axis.
        min_y -- The minimum value for the y axis.
        max_y -- The maximum value for the y axis.
        use_signal_for_x -- Flag to use the signal minimum and maximum values for the x axis.
        use_signal_for_y -- Flag to use the signal minimum and maximum values for the y axis.
        """

        if use_signal_for_x == True:
            self.axis.set_xlim([min(self.signal.x_points), 
                                max(self.signal.x_points)])
        elif min_x != None:
            self.axis.set_xlim([min_x, max_x])

        if use_signal_for_y == True:
            self.axis.set_ylim([min(self.signal.y_points),
                                max(self.signal.y_points)])
        elif min_y != None:
            self.axis.set_ylim([min_y, max_y])


    def update_index_line(self, label, index_value):
        """ Set the label and x position of the veritcal line.

        Key arguments:
        label -- A string to set the label
        index_value -- The new x position of the vertical line.
        """

        self.index_line.set_label(label)
        self.index_line.set_xdata(index_value)

    def update_signal_line(self):
        """ Update the signal curve to plot with new signal values.
        """

        self.signal_line.set_data(self.signal.x_points, self.signal.y_points)
