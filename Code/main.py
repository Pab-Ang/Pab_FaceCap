import myFuncs as Fn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Get the file location from user starting from Data directory
dataFilePath = input("Path to file from /Data:")
preMarkerDict = Fn.PrepareData(dataFilePath)
# print('\n Marker Arrays')    
# for key in preMarkerDict:
#    print(key)
#    print(preMarkerDict[key])

preMarkerCount = len(preMarkerDict.keys())

#Eucledian Distance between marker in different frames
point1 = preMarkerDict['marker1'][0,:]
point2 = preMarkerDict['marker1'][1,:]
dist = np.linalg.norm(point1 - point2)

# ------------------------------~CODE TO PLOT DATA~-------------------------------------
ax = plt.axes(projection='3d')

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

# First frame Data in X Dim
xfdata = np.array((preMarkerDict['marker1'][0,0], preMarkerDict['marker2'][0,0]))
for i in range(3, preMarkerCount+1):
   xfdata = np.concatenate(( xfdata,[preMarkerDict['marker{}'.format(i)][0,0]]),axis=0)
#First frame Data in Y Dim
yfdata = np.array((preMarkerDict['marker1'][0,1], preMarkerDict['marker2'][0,1]))
for i in range(3, preMarkerCount+1):
   yfdata = np.concatenate(( yfdata,[preMarkerDict['marker{}'.format(i)][0,1]]),axis=0)
#First Frame Data in Z Dim
zfdata = np.array((preMarkerDict['marker1'][0,2], preMarkerDict['marker2'][0,2]))
for i in range(3, preMarkerCount+1):
   zfdata = np.concatenate(( zfdata,[preMarkerDict['marker{}'.format(i)][0,2]]),axis=0)

ax.scatter3D(xfdata, yfdata, zfdata, c=zfdata, cmap='plasma')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
# Z+ pointing into screen | X- pointing to right screen border
plt.show()

# 2D plot of the first frame data
minX = np.amin(xfdata)
minY = np.amin(yfdata)
maxX = np.amax(xfdata)
maxY = np.amax(yfdata)
faceimg = plt.imread("./Code/Layout14.png")

plt.scatter(xfdata, yfdata, cmap='plasma')
plt.imshow(faceimg, zorder=0, extent=[-0.30, -0.09, 0.18, 0.40])
plt.xlabel('X')
plt.ylabel('Y')
plt.show()