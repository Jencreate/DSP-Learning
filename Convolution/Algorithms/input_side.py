#!/usr/bin/env python3

"""
Description: Visualise the input side algorithm in the convolution of two generated signal waveforms.
Author: Jensen Benard
Date Created: July 1, 2023
Date Modified: July 7, 2023
Python Version: 3.11.3
Dependencies: matplotlib, numpy, time

Reference:
    'The Scientist and Engineer's Guide to Digital Signal Processing' by Steven W.Smith,
    July 1, 2023,
    https://www.dspguide.com/ch6/3.htm
"""

import time
import matplotlib.pyplot as plt
import numpy as np
from common.signals.signal import Signal
from common.signals.signal_axis import SignalAxis

INPUT_SIGNAL_LEN = 20
INPUT_SIGNAL_RES = 20
MAX_INPUT_SIGNAL_VAL = 50

IMPULSE_SIGNAL_LEN = 5
IMPULSE_SIGNAL_RES = 5
MAX_IMPULSE_SIGNAL_VAL = 10

NUMBER_OF_SIGNALS = 3

STEP_DELAY = 0.2


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


def main():
    # Create signals to convolve using the input side algorithm.
    input_signal = Signal(INPUT_SIGNAL_LEN, INPUT_SIGNAL_RES)
    input_signal.set_custom_output(np.sin)

    impulse_signal = Signal(IMPULSE_SIGNAL_LEN, IMPULSE_SIGNAL_RES)
    impulse_signal.set_random_output(MAX_IMPULSE_SIGNAL_VAL)

    # Initialise an output signal that will contain the result of the convolution.
    output_signal_len = input_signal.len + impulse_signal.len - 1
    output_signal = Signal(output_signal_len, output_signal_len) 
    output_signal.set_zero_output()

    # Create and initialise axes.
    plt.ion()
    fig, axes = plt.subplots(NUMBER_OF_SIGNALS)
 
    input_signal_axis = SignalAxis(input_signal, axes[0], "Input signal") 
    impulse_signal_axis = SignalAxis(impulse_signal, axes[1], "Impulse signal") 
    output_signal_axis = SignalAxis(output_signal, axes[2], "Output signal") 

    # Set axis limits and add index lines.
    input_signal_axis.update_axis_limits(use_signal_for_x=True, use_signal_for_y=True)
    input_signal_axis.add_index_line("red", f"Input index: {0}")

    impulse_signal_axis.update_axis_limits(use_signal_for_x=True,use_signal_for_y=True)
    impulse_signal_axis.add_index_line("red", f"Impulse index: {0}")

    output_signal_axis.update_axis_limits(use_signal_for_x=True)
    output_signal_axis.add_index_line("red", f"Output index: {0}")

    # Plot the input and impulse signals.
    input_signal_axis.update_signal_line()
    impulse_signal_axis.update_signal_line()

    # Prevent axis titles from intersecting x values of above axes.
    plt.tight_layout()

    # Initialise to print the current step at the top of the plot.
    step = 0
    step_text = plt.text(0.02,0.98,f"step: {step}", transform=plt.gcf().transFigure)

    # Process to compute and plot the convolution for each step.
    for input_index, input_x in enumerate(input_signal.x_points):
        for impulse_index, impulse_x in enumerate(impulse_signal.x_points):

            step += 1
            output_index = input_index + impulse_index
            output_x = output_signal.x_points[output_index]

            # Update the output signal with the computation for the current step.
            output_signal.y_points[output_index] = compute_step(input_signal.y_points[input_index],
                                                         impulse_signal.y_points[impulse_index],
                                                         output_signal.y_points[output_index]) 
            
            # Update index line positions and labels for each signal plot.
            input_signal_axis.update_index_line(f"Input index: {input_index}", input_index) 
            impulse_signal_axis.update_index_line(f"Impulse index: {impulse_index}", impulse_index)
            output_signal_axis.update_index_line(f"Output index: {output_index}", output_index)

            # Update the output signal curve.
            output_signal_axis.update_signal_line(

            # Update the y limits of the output signal axis.
            output_signal_axis.update_axis_limits(use_signal_for_y=True)

            # Update the current step count shown on the plot.
            step_text.set_text(f"step: {step}")

            update_plot(axes, fig)
            time.sleep(STEP_DELAY)

    print("Convolution complete.")
    end = input("Press Enter to quit: ")


if __name__ == "__main__":
    main()


