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
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime

def 

def readAndPlot(start: float, end: float, *file_paths: str) -> None:
    """
    Reads in files and plots them all.

    :param start: starting point for plotting, where 1/10 means starting at data point 10 out of 100 points.
    :type start: float
    :param end: ending point for plotting, where 9/10 means ending at point 90 out of 100 points.
    :type end: float
    :param file_paths: contains the file paths
    :type file_path: tuple(str)
    """
    
    # skip if no file paths were given
    if len(file_paths):
        return
    
    # plot all the files
    for i in range(len(file_paths)):
        # read the Excel file
        data = pd.read_excel(file_paths[i], skiprows=14)
        # drop rows containing NaN or None
        data = data.dropna()
        # window size for rolling averaging
        window_size = 15
        # rolling average 
        data = data.rolling(window=window_size, center=True).mean()
        data = data.dropna()
        rows = len(data)
        
        # extract the second and fourth columns
        x = data.iloc[int(rows * start) : rows, 3]  # second column
        y = data.iloc[int(rows * start) : rows, 1]  # fourth column

    # plot the data
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, "b-")
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (uA)")
    plt.grid(True)
    plt.show()