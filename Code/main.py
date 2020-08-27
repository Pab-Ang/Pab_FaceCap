import myFuncs as Fn
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog

userWindow = Tk()
userWindow.title('FaceCap Auto-Label')
# Get the Data (CSV) file location from user
dataFileName = StringVar()
Label(userWindow, text="Select a Data file:").grid(column = 0, row = 0, pady=20)
dataFileBtn = Button(userWindow, text='Browse Data Files', width=18)
dataFileBtn.config(command=lambda: 
   Fn.file_selection(dataFileName,"Select A Data File", [("CSV File", "*.csv")] ) 
   )
dataFileBtn.grid(column = 1, row = 0, pady=20)

# Get the Layout file location from the user
layoutFilePath = StringVar()
Label(userWindow, text="Select a Layout file:").grid(column = 0, row = 2)
layoutFileBtn = Button(userWindow, text='Browse Layout Files', width=18)
layoutFileBtn.config(command=lambda:
   Fn.file_selection(layoutFilePath, "Select A Layout File", [("PNG File", "*.png"),("JPEG File", "*.jpeg"),("JPG File", "*.jpg")] ) 
   )
layoutFileBtn.grid(column = 1, row = 2)

usrMarkerCount = IntVar()
Label(userWindow, text='Enter how many markers you are using:', font=('bold', 10)).grid(column= 0, row= 3)
Entry(userWindow, textvariable=usrMarkerCount).grid(column= 1, row=3)

initialPlotBtn = Button(userWindow, text='Initialize Labels')
initialPlotBtn.config(command =lambda:
   Fn.plotInitialLayout(dataFilePath= dataFileName.get(), layoutPath= layoutFilePath.get())
   )
initialPlotBtn.grid(column = 1, row = 4)

userWindow.mainloop()
preMarkerDict = Fn.PrepareData(Path(dataFileName.get()))
# print('\n Marker Arrays')    
# for key in preMarkerDict:
#    print(key)
#    print(preMarkerDict[key])

preMarkerCount = len(preMarkerDict.keys())
print("User Marker Count",usrMarkerCount.get())

#Eucledian Distance between marker in different frames
point1 = preMarkerDict['marker1'][0,:]
point2 = preMarkerDict['marker1'][1,:]
dist = np.linalg.norm(point1 - point2)

# ------------------------------~CODE TO PLOT DATA~-------------------------------------

# Data in X Dim
xdata = np.array(preMarkerDict['marker1'][:,0])
for i in range(2, preMarkerCount+1):
   xdata = np.concatenate((xdata,preMarkerDict['marker{}'.format(i)][:,0]),axis=0)
# Data in Y Dim
ydata = np.array(preMarkerDict['marker1'][:,1])
for i in range(2, preMarkerCount+1):
   ydata = np.concatenate((ydata,preMarkerDict['marker{}'.format(i)][:,1]),axis=0)
# Data in Z Dim
zdata = np.array(preMarkerDict['marker1'][:,2])
for i in range(2, preMarkerCount+1):
   zdata = np.concatenate((zdata,preMarkerDict['marker{}'.format(i)][:,2]),axis=0)

# ax = plt.axes(projection='3d')
# ax.scatter3D(xfdata, yfdata, zfdata, c=zfdata, cmap='plasma')
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')
# # Z+ pointing into screen | X- pointing to right screen border
# plt.show()