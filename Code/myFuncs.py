from pathlib import Path
import string
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from tkinter import *
from tkinter import filedialog

#FUNCTIONS AND CLASSES

# Recieves CSV file path for Mocap Data and returns a Dict of the markers as keys and position matrixes as values (FramesxXYZ)
def PrepareData(sessionFilePath):
	# Use pandas to read CSV and save to DataFrame
	# Drop unnecesary rows like Format, HexDecLabel and PositionLabel rows
	path_toData = Path(sessionFilePath)
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
	print('\nInitial Marker Count:', FullMarkerCount, '\n')

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

# Function to plot in 2D the first frame of FaceCap Data with a reference layout image
# markerDict in format ['markerN':((X1,Y1,Z1),(X2,Y2,Z2),...), 'markerN+1':((X1,Y1,Z1),(X2,Y2,Z2),...)]
def PlotInitialLayout(dataFilePath: str, layoutPath: str, usrLabelCount: int):

	preMarkerDict = PrepareData(Path(dataFilePath))
	# print('\n Marker Arrays')    
	# for key in preMarkerDict:
	#    print(key)
	#    print(preMarkerDict[key])

	preMarkerCount = len(preMarkerDict.keys())

	if(preMarkerCount < usrLabelCount):
		NotEnoughMarkerData()
		return None

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

	# 2D plot of the first frame data
	minX = np.amin(xfdata)
	minY = np.amin(yfdata)
	maxX = np.amax(xfdata)
	maxY = np.amax(yfdata)
	print(minX, maxX, minY, maxY)
	# Layout image for reference
	faceimg = plt.imread(Path(layoutPath))

	#creating subplots to use slider widgets on window
	fig, ax = plt.subplots()
	plt.subplots_adjust(left=0.1, bottom=0.35)
	plotFigure = plt.scatter(xfdata, yfdata, cmap='plasma')
	# extent in data units in order imshow(img, zorder=0, extent=[left, right, bottom, top])
	# Default testing values [-0.30, -0.09, 0.18, 0.40]
	layoutFig = plt.imshow(faceimg, zorder=0, extent=[-0.30, -0.09, 0.18, 0.40])
	plt.xlabel('X')
	plt.ylabel('Y')

	minX_Slider = plt.axes([0.25, 0.1, 0.65, 0.03])
	sl_minX = Slider(minX_Slider, 'IMG Left Lim', valmin=1.5*minX, valmax=0.5*minX, valinit=-0.30)

	maxX_Slider = plt.axes([0.25, 0.15, 0.65, 0.03])
	sl_maxX = Slider(maxX_Slider, 'IMG Right Lim', valmin=1.5*maxX, valmax=0.5*maxX, valinit=-0.09)

	minY_Slider = plt.axes([0.25, 0.2, 0.65, 0.03])
	sl_minY = Slider(minY_Slider, 'IMG Bottom Lim', valmin=0.5*minY, valmax=1.5*minY, valinit=0.18)

	maxY_Slider = plt.axes([0.25, 0.25, 0.65, 0.03])
	sl_maxY = Slider(maxY_Slider, 'IMG Top Lim', valmin=0.5*maxY, valmax=1.5*maxY, valinit=0.40)

	def updateLims(val):
		leftLim = sl_minX.val
		rightLim = sl_maxX.val
		bottomLim = sl_minY.val
		topLim = sl_maxY.val

		layoutFig.set_extent([leftLim, rightLim, bottomLim, topLim])
	
	sl_minX.on_changed(updateLims)
	sl_maxX.on_changed(updateLims)
	sl_minY.on_changed(updateLims)
	sl_maxY.on_changed(updateLims)

	plt.show()

# Function to select file on button press, wintitle is a Str and winfiletype is a tuple on format ("Title", "*.extension"),("Title2", "*.extension2")
def File_selection(filenameVar: StringVar, wintitle: str, winfiletype):
	filename =  filedialog.askopenfilename(initialdir=Path(), title=wintitle, filetypes=winfiletype)
	try:
		print("Selected:", filename)
		filenameVar.set(filename)
	except:
		print("No file selected")

def LabelFirstFrame():
	pass

# Function to transform a list of TKinter entries to a StringVar of comma separated strings
def ListToStringVar(listOfEntries: list, passStringVar: StringVar):
	stringList=[]

	for entry in listOfEntries:
		stringList.append(str(entry.get()))
	
	stringComma = ','.join(stringList)
	# to modify external variable in TKinter
	passStringVar.set(stringComma)

# Function to pass comma separated string to a list of strings
def CsStringToStringList(commaSepString: string):
	return commaSepString.split(",")

def StringListToNewLineString(stringList: list):
	nlString = ''

	for x in stringList:
		nlString = nlString + str(x) + '\n'
	
	return nlString

def NotEnoughMarkerData():
	warningWin = Toplevel()
	warningWin.title("WARNING!")

	myLabel = Label(warningWin, text="MARKER COUNT INSUFFICENT \n CHECK DATA FILE AND/OR LABEL COUNT")
	myLabel.pack()
	return None