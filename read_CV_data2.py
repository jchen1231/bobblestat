"""
read_CV_data2.py

This module provides utility functions for data processing.

Features:
- Plots data from Bobblestat result files
- Animates data from Bobblestat result files

Example: ---

Author: Jason Chen
License: ---
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime


def readAndPlot(start: float, end: float, *files: str) -> None:
    """
    Reads in files and plots them all.

    :param start: starting point for plotting, where 1/10 means starting at data point 10 out of 100 points.
    :type start: float
    :param end: ending point for plotting, where 9/10 means ending at point 90 out of 100 points.
    :type end: float
    :param files: contains the file paths
    :type files: (str, str)
    """

    # skip everything if no file paths were given
    if len(files) == 0:
        return

    fig, ax = plt.subplots()

    # plot all the files
    for i in range(len(files)):
        # read the Excel file
        data = pd.read_excel(files[i][1], skiprows=14)
        # drop rows containing NaN or None
        data.dropna(inplace=True)
        # window size for rolling averaging
        window_size = 15
        # rolling average, returns a df window object
        rolled_data = data.rolling(window=window_size, center=True).mean()
        # drop rows containing NaN or None generated by rolling()
        rolled_data.dropna(inplace=True)

        rows = len(rolled_data)
        row_start = int(rows * start)
        row_end = int(rows * end)
        # extract the second and fourth columns
        x = rolled_data.iloc[row_start:row_end, 3].values  # second column
        y = rolled_data.iloc[row_start:row_end, 1].values  # fourth column
        # plot the data
        ax.plot(x, y)

    # add plot features
    ax.set_title("Combined CV Plots")
    ax.set_xlabel("Voltage (V)")
    ax.set_ylabel("Current (uA)")
    # ax.set_xlim(min(x) - 0.1, max(x) + 0.1)  # x-axis range
    # ax.set_ylim(min(y) - 1, max(y) + 1)  # y-axis range
    names = [name[0] for name in files]
    ax.legend(names)
    ax.grid(True)
    plt.show()


def readAndAnimate(start: float, end: float, *files: str) -> None:
    # Initialize the plot (empty data)
    def init():
        for line in lines:
            line.set_data([], [])

    # Update function for each frame
    def update(frame):
        for i in range(len(lines)):
            lines[i].set_data(datas[i][0][0:frame], datas[i][1][0:frame])

    # skip everything if no file paths were given
    if len(files) == 0:
        return

    fig, ax = plt.subplots()
    lines = list()
    datas = list()

    # For setting up animation
    fewest_rows = float("inf")
    min_x = float("inf")
    max_x = -float("inf")
    min_y = float("inf")
    max_y = -float("inf")

    for i in range(len(files)):
        # create line object for animation and add to a list
        (line,) = ax.plot([], [], lw=2)  # empty line object
        lines.append(line)

        ##################################################
        # ADJUST ROWS TO SKIP
        ROWS_TO_SKIP = 14
        ##################################################

        # read the Excel file and store in dictionary
        data = pd.read_excel(files[i][1], skiprows=ROWS_TO_SKIP)
        # drop rows containing NaN or None
        data.dropna(inplace=True)

        ##################################################
        # ADJUST WINDOW SIZE FOR AVERAGING
        WINDOW_SIZE = 15
        ##################################################

        rolled_data = data.rolling(window=WINDOW_SIZE, center=True).mean()
        # drop rows containing NaN or None generated by rolling()
        rolled_data.dropna(inplace=True)
        rows = len(rolled_data)

        row_start = int(rows * start)
        row_end = int(rows * end)
        # extract the second and fourth columns, convert from df to array
        x = rolled_data.iloc[row_start:row_end, 3].to_numpy()  # fourth column
        y = rolled_data.iloc[row_start:row_end, 1].to_numpy()  # second column
        datas.append([x, y])

        # keep track of the fewest number of rows to calculate number of frames to use
        rows_plotted = row_end - row_start
        if rows_plotted < fewest_rows:
            fewest_rows = rows_plotted

        # Find absolute mins and maxes for setting axis limits
        if min(x) < min_x:
            min_x = min(x)
        if max(x) > max_x:
            max_x = max(x)
        if min(y) < min_y:
            min_y = min(y)
        if max(y) > max_y:
            max_y = max(y)

    # Add plot/animation features
    ax.set_xlim([min_x * 1.1, max_x * 1.1])  # x-axis range
    ax.set_ylim([min_y * 1.1, max_y * 1.1])  # y-axis range
    ax.set_title("Combined CV Plot")
    ax.set_xlabel("Voltage (V)")
    ax.set_ylabel("Current (uA)")
    names = [name[0] for name in files]
    ax.legend(names)
    ax.grid(True)

    ani = FuncAnimation(
        fig,
        update,
        frames=fewest_rows,
        init_func=init,
        blit=False,
    )
    # get current date
    tnow = datetime.now()
    # format date as yyyymmdd
    yyyymmdd = tnow.strftime("%Y%m%d")
    ani.save(f"{yyyymmdd}_{title}.gif", writer="pillow", fps=30)
    plt.show()


if __name__ == "__main__":
    title = ""
    name1 = "1X PBS"
    path1 = r"/home/jchen777/bobblestat_data/BobbleSTAT_data_20240222-I10-3.xlsx"
    name2 = "0.5mM ruthenium"
    path2 = r"/home/jchen777/bobblestat_data/BobbleSTAT_data_20240222-I10-5.xlsx"
    name3 = "deionized water"
    path3 = r"/home/jchen777/bobblestat_data/BobbleSTAT_data_20240222-I10-6.xlsx"
    # readAndPlot(3/7,6/7,(name1,path1),(name2,path2),(name3,path3))
    readAndAnimate(3 / 7, 6 / 7, (name1, path1), (name2, path2), (name3, path3))
