from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#FUNCTIONS AND CLASSES

def PrepareData(sessionFilePath):
	# Use pandas to read CSV and save to DataFrame
	# Drop unnecesary rows like Format, HexDecLabel and PositionLabel rows
	path_toData = Path('readCSV.py').parent.parent/ 'Data' / sessionFilePath
	markersDF = pd.read_csv(path_toData.resolve(), skiprows=[0,1,2,4,5,6])

	# Rename Frame and Time header labels as they are read as Unnamed
	markersDF.rename({"Unnamed: 0":"Frame"}, axis="columns", inplace=True)
	markersDF.rename({"Unnamed: 1":"Time"}, axis="columns", inplace=True)
	# Drop Time column | Unnecesary.
	markersDF.drop(["Time"], axis=1, inplace=True)

	# Count number of Rows
	#FullRowCount = len(markersDF.index)

	# Count quantity of markers
	FullColumnCount = len(markersDF.columns)
	# Each marker has x(t), y(t) and z(t) vectors
	FullMarkerCount = (FullColumnCount-1)/3
	FullMarkerCount = int(FullMarkerCount)
	print('\n Marker Count:', FullMarkerCount, '\n')

	# Create Frame numpy Array
	#FrameArray = markersDF.iloc[:, 0].to_numpy(copy=True)

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
	return markerDict

def LabelFirstFrame():
	pass