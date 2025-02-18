import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime

def readAndPlot(start, file_path):
    # read the Excel file
    data = pd.read_excel(file_path, skiprows=14)
    # extract the second and fourth columns
    data = data.dropna()
    # adjust window size
    window_size = 15
    data = data.rolling(window=window_size, center=True).mean()
    data = data.dropna()
    rows = len(data)
    x = data.iloc[int(rows*start):rows, 3] # second column
    y = data.iloc[int(rows*start):rows, 1] # fourth column

    # plot the data
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, 'b-')
    plt.xlabel('Voltage (V)')
    plt.ylabel('Current (uA)')
    plt.grid(True)
    plt.show()

# Initialize the plot (empty data)
def init():
    line.set_data([], [])
    return line

# Update function for each frame
def update(frame):
    x = data.iloc[startrow:frame+startrow, 3].to_numpy() # second column
    y = data.iloc[startrow:frame+startrow, 1].to_numpy() # fourth column
    # print(f"x: {x}, y: {y}")
    line.set_data(x, y)
    return line

def readAndAnimate(start, file_path):
    global data, line, startrow
    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2) # empty line object
    # read the Excel file
    data = pd.read_excel(file_path, skiprows=14)
    # extract the second and fourth columns
    data = data.dropna()
    # adjust window size
    window_size = 15
    data = data.rolling(window=window_size, center=True).mean()
    data = data.dropna()
    rows = len(data)
    x = data.iloc[int(rows*start):rows, 3] # second column
    y = data.iloc[int(rows*start):rows, 1] # fourth column
    ax.set_xlim(min(x)-.1,max(x)+.1) # x-axis range
    ax.set_ylim(min(y)-1,max(y)+1) # y-axis range
    ax.set_title('CV Plot')
    ax.set_xlabel('Voltage (V)')
    ax.set_ylabel('Current (uA)')
    ax.grid(True)

    startrow = int(len(data)*start)
    ani = FuncAnimation(fig, update, frames=int(rows*(1-start)), init_func=init, blit=False)
    plt.show()

    # get current date
    tnow = datetime.now()
    # format date as yyyymmdd
    yyyymmdd = tnow.strftime("%Y%m%d")
    ani.save(f'{yyyymmdd}{file_path[-20:-5]}.gif', writer='pillow', fps=30)

# Initialize the plot (empty data)
def init2():
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    return line1, line2

# Update function for each frame
def update2(frame):
    if(frame < len(data1)):
        x = data1.iloc[startrow1:frame+startrow1, 3].to_numpy() # second column
        y = data1.iloc[startrow1:frame+startrow1, 1].to_numpy() # fourth column
        # print(f"x: {x}, y: {y}")
        line1.set_data(x, y)
    if(frame < len(data2)):
        x = data2.iloc[startrow2:frame+startrow2, 3].to_numpy() # second column
        y = data2.iloc[startrow2:frame+startrow2, 1].to_numpy() # fourth column
        # print(f"x: {x}, y: {y}")
        line2.set_data(x, y)    
    if(frame < len(data3)):
        x = data3.iloc[startrow3:frame+startrow3, 3].to_numpy() # second column
        y = data3.iloc[startrow3:frame+startrow3, 1].to_numpy() # fourth column
        # print(f"x: {x}, y: {y}")
        line3.set_data(x, y)    
    return line1, line2

def readAndAnimate2(start, end, file_path1, file_path2, file_path3, title, sample1, sample2, sample3):
    global data1, data2, data3, line1, line2, line3, startrow1, startrow2, startrow3
    window_size = 15
    fig, ax = plt.subplots()
    line1, = ax.plot([], [], lw=2) # empty line object
    line2, = ax.plot([], [], lw=2)
    line3, = ax.plot([], [], lw=2)

    # read the first Excel file 
    data1 = pd.read_excel(file_path1, skiprows=14)
    # extract the second and fourth columns
    data1 = data1.dropna()
    # adjust window size
    data1 = data1.rolling(window=window_size, center=True).mean()
    data1 = data1.dropna()
    rows = len(data1)
    startrow1 = int(rows*start)
    x1 = data1.iloc[int(rows*start):int(rows*(1-end)), 3] # second column
    y1 = data1.iloc[int(rows*start):int(rows*(1-end)), 1] # fourth column

    # read the Excel file 
    data2 = pd.read_excel(file_path2, skiprows=14)
    # extract the second and fourth columns
    data2 = data2.dropna()
    # adjust window size
    data2 = data2.rolling(window=window_size, center=True).mean()
    data2 = data2.dropna()
    rows = len(data2)
    startrow2 = int(rows*start)
    x2 = data2.iloc[int(rows*start):int(rows*(1-end)), 3] # second column
    y2 = data2.iloc[int(rows*start):int(rows*(1-end)), 1] # fourth column
    
    # read the Excel file 
    data3 = pd.read_excel(file_path3, skiprows=14)
    # extract the second and fourth columns
    data3 = data3.dropna()
    # adjust window size
    data3 = data3.rolling(window=window_size, center=True).mean()
    data3 = data3.dropna()
    rows = len(data3)
    startrow3 = int(rows*start)
    x3 = data3.iloc[int(rows*start):int(rows*(1-end)), 3] # second column
    y3 = data3.iloc[int(rows*start):int(rows*(1-end)), 1] # fourth column

    ax.set_xlim(np.min(pd.concat([x1,x2,x3]))-.1,np.max(pd.concat([x1,x2,x3]))+.1) # x-axis range
    ax.set_ylim(np.min(pd.concat([y1,y2,y3]))-1,np.max(pd.concat([y1,y2,y3]))+1) # y-axis range
    ax.set_title('Combined CV Plot')
    ax.set_xlabel('Voltage (V)')
    ax.set_ylabel('Current (uA)')
    ax.legend([sample1,sample2, sample3])
    ax.grid(True)
    ani = FuncAnimation(fig, update2, frames=int(max([len(data1),len(data2)])*(1-start-end)), init_func=init2, blit=False)
    # get current date
    tnow = datetime.now()
    # format date as yyyymmdd
    yyyymmdd = tnow.strftime("%Y%m%d")
    ani.save(f'{yyyymmdd}_{title}.gif', writer='pillow', fps=30)
    plt.show()

if __name__ == "__main__":
    title = '_____'
    pathname1 = r"C:\Users\jason\OneDrive - University of Maryland\MPower\Smart Marble\BobbleSTAT_data_20240222-I10-5.xlsx"
    pathname2 = r"C:\Users\jason\OneDrive - University of Maryland\MPower\Smart Marble\BobbleSTAT_data_20240222-I10-3.xlsx"
    pathname3 = r"C:\Users\jason\OneDrive - University of Maryland\MPower\Smart Marble\BobbleSTAT_data_20240222-I10-6.xlsx"
    # readAndPlot(1/2,pathname1)
    # readAndAnimate(3/7,pathname3)

    readAndAnimate2(3/7,1/7,pathname1,pathname2,pathname3,title,'0.5mM ruthenium','1X PBS (pH=7.4)','di-water')