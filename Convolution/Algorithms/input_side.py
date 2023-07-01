#!/usr/bin/env python3

"""
Description: Visualise the input side algorithm in the convolution of two randomly generated signal waveforms.
Author: Jensen Benard
Date Created: July 1, 2023
Date Modified: July 1, 2023
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
MAX_INPUT_SIGNAL_VAL = 50

IMPULSE_SIGNAL_LEN = 5
MAX_IMPULSE_SIGNAL_VAL = 10

NUMBER_OF_SIGNALS = 3

STEP_DELAY = 0.2


def get_random_signal(signal_len, max_output):
    """Returns a signal waveform with a uniform length (signal_x)
    with randomly generated output values (signal_y).

    Keyword arguments:
    signal_len -- Length of signal (number of x points).
    max_output -- Maximum possible randomly generated y value.
    """

    signal_x = np.linspace(0, signal_len - 1, signal_len)
    signal_y = np.random.randint(max_output, size=(signal_len))

    return signal_x, signal_y


def get_zero_signal(signal_len): 
    """Returns a signal waveform with a uniform length (signal_x)
    with all outputs set to zero (signal_y).

    Keyword argument:
    signal_len -- Length of signal (number of x points).
    """

    signal_x = np.linspace(0, signal_len - 1, signal_len)
    signal_y = np.zeros(signal_len)

    return signal_x, signal_y


def plot_signal(axis, signal_x, signal_y, title): 
    """Plot a signal waveform.

    Keyword argument:
    axis -- The axis to plot the waveform onto.
    signal_x -- The x values of the waveform.
    signal_y -- The y values of the waveform.
    title -- The title of the plot
    """

    axis.plot(signal_x, signal_y)
    axis.set_title(title)


def plot_index(axis, index, color, label):
    """Plot a vertical line to mark the current index
    in the computation of the algorithm.
    
    Keyword arguments:
    axis -- The axis to plot the waveform onto.
    index -- The x value to place the vertical line.
    color -- Color of the vertical line.
    label -- Text value of the legend, for the line, to place on the plot.
    """

    axis.axvline(x=index, color=color, label=label)


def update_plots(axes, fig, step):
    """Update all axes used to plot the waveforms
    
    Keyword arguments:
    axes -- All axes used to plot the waveforms.
    fig -- Figure corresponding to all axes.
    step -- Current step of the algorithm.
    """

    # Set location of legends for each vertical line in each axis.
    for i in range(0, NUMBER_OF_SIGNALS):
        axes[i].legend(loc="upper right")
    
    # Prevents titles from overlapping x tick marks.
    plt.tight_layout()

    # Print the current step at the top of the plot.
    plt.text(0.02,0.98,f"step: {step}", transform=plt.gcf().transFigure)

    fig.canvas.draw()
    fig.canvas.flush_events()


def clear_plots(axes):
    """Clear each axis completely.

    Keyword argument:
    axes -- All axes to clear.
    """

    for i in range(0, NUMBER_OF_SIGNALS):
        axes[i].clear()


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
    # Create random signals to convolve using the input side algorithm.
    input_signal_x, input_signal_y = get_random_signal(INPUT_SIGNAL_LEN, MAX_INPUT_SIGNAL_VAL)
    impulse_signal_x, impulse_signal_y = get_random_signal(IMPULSE_SIGNAL_LEN, MAX_IMPULSE_SIGNAL_VAL)

    # Initialise an output signal that will contain the result of the convolution.
    output_signal_x, output_signal_y = get_zero_signal(INPUT_SIGNAL_LEN + IMPULSE_SIGNAL_LEN - 1)

    plt.ion()
    fig, axes = plt.subplots(NUMBER_OF_SIGNALS)

    step = 0

    # Process to compute and plot the convolution for each step.
    for input_x in range(0, INPUT_SIGNAL_LEN):
        for impulse_x in range(0, IMPULSE_SIGNAL_LEN):
            clear_plots(axes)

            step += 1
            output_x = input_x + impulse_x

            # Update the output signal with the computation for the current step.
            output_signal_y[output_x] = compute_step(input_signal_y[input_x],
                                                       impulse_signal_y[impulse_x],
                                                       output_signal_y[output_x]) 

            # Plot all signals onto the corresponding axes.
            plot_signal(axes[0], input_signal_x, input_signal_y, "Input signal")
            plot_signal(axes[1], impulse_signal_x, impulse_signal_y, "Impulse signal")
            plot_signal(axes[2], output_signal_x, output_signal_y, "Output signal")

            # Plot veritcal lines to mark the current index for each waveform.
            plot_index(axes[0], input_x, "red", f"Input index: {input_x}")
            plot_index(axes[1], impulse_x, "red", f"Impulse index: {impulse_x}")
            plot_index(axes[2], output_x, "red", f"Output index: {output_x}")

            update_plots(axes, fig, step)
            time.sleep(STEP_DELAY)

    print("Convolution complete.")
    end = input("Press Enter to quit: ")


if __name__ == "__main__":
    main()


