#!/usr/bin/env python3

"""
Description: Visualise the input side algorithm in the convolution of two generated signal waveforms.
Author: Jensen Benard
Date Created: July 1, 2023
Date Modified: July 3, 2023
Python Version: 3.11.3
Dependencies: matplotlib, numpy, time

Reference:
    'The Scientist and Engineer's Guide to Digital Signal Processing' by Steven W.Smith,
    July 7, 2023,
    https://www.dspguide.com/ch6/3.htm
"""

import time
import matplotlib.pyplot as plt
import numpy as np

INPUT_SIGNAL_LEN = 20
INPUT_SIGNAL_RES = 20
MAX_INPUT_SIGNAL_VAL = 50

IMPULSE_SIGNAL_LEN = 5
IMPULSE_SIGNAL_RES = 5
MAX_IMPULSE_SIGNAL_VAL = 10

NUMBER_OF_SIGNALS = 3

STEP_DELAY = 0.2


def get_signal_x(signal_len, signal_res):
    """Returns x coordinates of signal waveform with a uniform length.

    Keyword arguments:
    signal_len -- Length of signal (number of x points).
    signal_res -- Number of x data points.
    """

    signal_x = np.linspace(0, signal_len - 1, signal_res)

    return signal_x

def get_custom_signal_y(signal_x, func):
    """Returns a signal waveform with a uniform length (signal_x)
    with a specified custom output function

    Keyword arguments:
    signal_x -- x coordinates of signal.
    func -- Custom function to generate output values (signal_y).
    """

    signal_y = np.array([func(x) for x in signal_x])

    return signal_y

def get_random_signal_y(signal_x, max_output):
    """Returns a signal waveform with a uniform length (signal_x)
    with randomly generated output values (signal_y).

    Keyword arguments:
    signal_x -- x coordinates of signal.
    max_output -- Maximum possible randomly generated y value.
    """

    signal_y = np.random.randint(max_output, size=len(signal_x))

    return signal_y


def get_zero_signal_y(signal_x): 
    """Returns a signal waveform with a uniform length (signal_x)
    with all outputs set to zero (signal_y).

    Keyword argument:
    signal_x -- x coordinates of signal.
    """

    signal_y = np.zeros(len(signal_x))

    return signal_y

def update_plot(axes, fig):
    """Update all axes used to plot the waveforms

    Keyword arguments:
    axes -- All axes used to plot the waveforms.
    fig -- Figure corresponding to all axes.
    step -- Current step of the algorithm.
    """

    # Set location of legends for each vertical line in each axis.
    for i in range(0, NUMBER_OF_SIGNALS):
        axes[i].legend(loc="upper right")

    fig.canvas.draw()
    fig.canvas.flush_events()

def compute_step(input_y, impulse_y, prev_output_y):
    """Return the input side computation algorithm for
    a single step.

    Keyword argument:
    input_y -- y output of input signal for the current index (x value).
    impulse_y -- y output of the impulse signal for the current index (x value).
    prev_output_y -- The previous y output of the resulting output signal.
    """

    return prev_output_y + input_y * impulse_y


def init_axis(axis, title, min_x=None, max_x=None, min_y=None, max_y=None):
    """Initialise the axis with the specified arguments.

    Keyword argument:
    axis -- The axis to initialise.
    title -- The title of the axis, displayed at the top.
    min_x -- The minimum x value to display.
    max_x -- The maximum x value to display.
    min_y -- The minimum y value to display.
    max_y -- The maximum y value to display.
    """

    if min_x != None:
        axis.set_xlim([min_x, max_x])

    if min_y != None:
        axis.set_ylim([min_y, max_y])

    axis.set_title(title)


def get_lines(axis, color):
    """Return Line2D objects for the signal wavefrom and index line.

    Keyword argument:
    axis -- The axis to plot the signal waveform and index line.
    color -- The color of the index line.
    """

    signal_line, = axis.plot([], [])
    index_line = axis.axvline(x=0, color=color)

    return signal_line, index_line

def update_line(line, data_x, label):
    """Return the input side computation algorithm for
    a single step.

    Keyword argument:
    input_y -- y output of input signal for the current index (x value).
    impulse_y -- y output of the impulse signal for the current index (x value).
    prev_output_y -- The previous y output of the resulting output signal.
    """
    line.set_xdata([data_x])
    line.set_label(label)


def main():
    # Create signals to convolve using the input side algorithm.
    input_signal_x = get_signal_x(INPUT_SIGNAL_LEN, INPUT_SIGNAL_RES)
    input_signal_y = get_custom_signal_y(input_signal_x, np.sin)

    impulse_signal_x = get_signal_x(IMPULSE_SIGNAL_LEN, IMPULSE_SIGNAL_RES)
    impulse_signal_y = get_random_signal_y(impulse_signal_x, MAX_IMPULSE_SIGNAL_VAL)

    # Initialise an output signal that will contain the result of the convolution.
    output_signal_len = len(input_signal_x) + len(impulse_signal_x) - 1
    output_signal_x = get_signal_x(output_signal_len, output_signal_len) 
    output_signal_y = get_zero_signal_y(output_signal_x)

    # Create and initialise axes.
    plt.ion()
    fig, axes = plt.subplots(NUMBER_OF_SIGNALS)
    init_axis(axes[0], "Input signal", 0, max(input_signal_x), min(input_signal_y), max(input_signal_y))
    init_axis(axes[1], "Impulse signal", -0.1, max(impulse_signal_x), min(impulse_signal_y), max(impulse_signal_y))
    init_axis(axes[2], "Output signal", 0, max(output_signal_x))

    # Create the Line2D objects for the index lines.
    input_signal_line, input_index_line = get_lines(axes[0], "red")
    impulse_signal_line, impulse_index_line = get_lines(axes[1], "red")
    output_signal_line, output_index_line = get_lines(axes[2], "red")

    # Prevent axis titles from intersecting x values of above axes.
    plt.tight_layout()

    # Initialise to print the current step at the top of the plot.
    step = 0
    step_text = plt.text(0.02,0.98,f"step: {step}", transform=plt.gcf().transFigure)

    # Process to compute and plot the convolution for each step.
    for input_index, input_x in enumerate(input_signal_x):
        for impulse_index, impulse_x in enumerate(impulse_signal_x):

            step += 1
            output_index = input_index + impulse_index
            output_x = output_signal_x[output_index]

            # Update the output signal with the computation for the current step.
            output_signal_y[output_index] = compute_step(input_signal_y[input_index],
                                                         impulse_signal_y[impulse_index],
                                                         output_signal_y[output_index]) 

            # Plot all signals onto the corresponding axes.
            input_signal_line.set_data(input_signal_x, input_signal_y)
            impulse_signal_line.set_data(impulse_signal_x, impulse_signal_y)
            output_signal_line.set_data(output_signal_x, output_signal_y)

            # Plot vertical lines to mark the current index for each waveform.
            update_line(input_index_line, input_x, f"Input index: {input_index}")
            update_line(impulse_index_line, impulse_x, f"Impulse index: {impulse_index}")
            update_line(output_index_line, output_x, f"Output index: {output_index}")

            # Update the y limits of the output signal axis.
            axes[2].set_ylim([min(output_signal_y), max(output_signal_y)])

            # Update the current step count shown on the plot.
            step_text.set_text(f"step: {step}")

            update_plot(axes, fig)
            time.sleep(STEP_DELAY)

    print("Convolution complete.")
    end = input("Press Enter to quit: ")


if __name__ == "__main__":
    main()


