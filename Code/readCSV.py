from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Get the file location from user starting from Data directory
sessionFilePath = input("Path to file from /Data:")

# Use pandas to read CSV and save to DataFrame
# Drop unnecesary rows like Format, HexDecLabel and PositionLabel rows
path_toData = Path('readCSV.py').parent.parent/ 'Data' / sessionFilePath
markersDF = pd.read_csv(path_toData.resolve(), skiprows=[0,1,2,4,5,6])

# Rename Frame and Time header labels as they are read as Unnamed
markersDF.rename({"Unnamed: 0":"Frame"}, axis="columns", inplace=True)
markersDF.rename({"Unnamed: 1":"Time"}, axis="columns", inplace=True)
# Drop Frame column | Unnecesary.
markersDF.drop(["Frame"], axis=1, inplace=True)

# Count number of Rows
FullRowCount = len(markersDF.index)
# Count quantity of markers
FullColumnCount = len(markersDF.columns)
# Each marker has x(t), y(t) and z(t) vectors
FullMarkerCount = (FullColumnCount-1)/3
FullMarkerCount = int(FullMarkerCount)
print('\n Marker Count:', FullMarkerCount, '\n')

# Create Time numpy Array
TimeArray = markersDF.iloc[:, 0].to_numpy(copy=True)

# Create a dict to store marker arrays
markerDict ={}
for i in range (1,FullMarkerCount+1):
    markerDict['marker{}'.format(i)] = np.empty


# Copying each markers XYZ to a different NumPy matrix
for i in range(1, FullColumnCount, 3):
    # Select only the columns of interest for the marker and copy them to activeMarker
    activeMarker = markersDF.iloc[:, i:i+3].to_numpy(copy=True)

    # The number of marker active in each loop
    currentMarkerIndex = (i-1)/3 +1
    currentMarkerIndex = int(currentMarkerIndex)

    # add the active marker matrix to the corresponding marker dictionary key
    markerDict['marker{}'.format(currentMarkerIndex)] = activeMarker

# print('\n Marker Arrays')    
# for key in markerDict:
#     print(key)
#     print(markerDict[key])

# ------------------------------~CODE TO PLOT DATA~-------------------------------------
ax = plt.axes(projection='3d')
# Data in X Dim
xdata = markerDict['marker1'][:,0]
for i in range(2, FullMarkerCount+1):
        xdata = np.concatenate((xdata,markerDict['marker{}'.format(i)][:,0]),axis=0)
# Data in Y Dim
ydata = markerDict['marker1'][:,1]
for i in range(2, FullMarkerCount+1):
        ydata = np.concatenate((ydata,markerDict['marker{}'.format(i)][:,1]),axis=0)
# Data in z Dim
zdata = markerDict['marker1'][:,2]
for i in range(2, FullMarkerCount+1):
        zdata = np.concatenate((zdata,markerDict['marker{}'.format(i)][:,2]),axis=0)

ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='plasma')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
# Z+ pointing into screen | X- pointing to right screen border
plt.show()