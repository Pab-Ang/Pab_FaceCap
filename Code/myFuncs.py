from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from tkinter import *
from tkinter import filedialog
from hungarian_algorithm import algorithm

#FUNCTIONS AND CLASSES

# Recieves CSV file path for Mocap Data and returns a Dict of the markers as keys and position matrixes as values (FramesxXYZ)
def PrepareData(sessionFilePath):
	# Use pandas to read CSV and save to DataFrame
	# Drop unnecesary rows like Format, HexDecLabel and PositionLabel rows
	path_toData = Path(sessionFilePath)
	markersDF = pd.read_csv(path_toData.resolve(), skiprows=[0,1,2,4,5,6])
	# print(markersDF)

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

	# Create a Dict to store marker arrays
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

#Label input pop-up window
def InputLabelsWindow(usrLabelCount: int, StringVarToPass: StringVar):
   entryList = []
   popWin = Toplevel()
   popWin.title("Naming Labels")
   

   if(usrLabelCount <4):
      notEnoughLabels = Label(popWin, text= "More than 4 labels are needed\n Close Window and resume")
      notEnoughLabels.pack(pady=15,padx=10)
   #dimensions for the window change if even or odd number of labels
   elif (usrLabelCount % 2 == 0):
      entryCounter=0
      winColumnCount = int(4)
      winRowCount = int(np.ceil(usrLabelCount/winColumnCount))
      #Row Entry creation loop
      for y in range(winRowCount):
         #Column Entry creation loop
         for x in range(1,2*winColumnCount,2):
            if(entryCounter >= usrLabelCount):
               break
            Label(popWin, text="{}.".format(entryCounter+1)).grid(row=y, column=x-1, pady=0, padx=0)
            myEntry = Entry(popWin)
            myEntry.grid(row=y, column=x, pady=5, padx=5)
            entryList.append(myEntry)

            entryCounter+=1
      
      passListBtn = Button(popWin, text='Set Labels and Continue', command=lambda: 
         ListToStringVar(listOfEntries= entryList, passStringVar= StringVarToPass)
         )
      passListBtn.grid(row= winRowCount +1, column= 0, pady=10)


   else:
      entryCounter=0
      winColumnCount = int(3)
      winRowCount = int(np.ceil(usrLabelCount/winColumnCount))
      #Row Entry creation loop
      for y in range(winRowCount):
         #Column Entry creation loop
         for x in range(1,2*winColumnCount,2):
            if(entryCounter >= usrLabelCount):
               break
            Label(popWin, text="{}.".format(entryCounter+1)).grid(row=y, column=x-1, pady=0, padx=0)
            myEntry = Entry(popWin)
            myEntry.grid(row=y, column=x, pady=5, padx=5)
            entryList.append(myEntry)

            entryCounter+=1
      
      passListBtn = Button(popWin, text='Set Labels and Continue', command=lambda: 
         ListToStringVar(listOfEntries= entryList, passStringVar= StringVarToPass)
         )
      passListBtn.grid(row= winRowCount +1, column= 0, pady=10)

# Function to plot in 2D the first frame of FaceCap Data with a reference layout image
# markerDict in format ['markerN':((X1,Y1,Z1),(X2,Y2,Z2),...), 'markerN+1':((X1,Y1,Z1),(X2,Y2,Z2),...)]
def PlotInitialLayout(dataFilePath: str, layoutPath: str, usrLabelCount: int, listOfLabels: list = None, listForCoords: list =None, mainWindowRoot: Tk = None):

	DisplayLabelsWindow(labelsList= listOfLabels, labelCount=usrLabelCount)

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
	for i in range(3, usrLabelCount+1):
   		xfdata = np.concatenate(( xfdata,[preMarkerDict['marker{}'.format(i)][0,0]]),axis=0)
	#First frame Data in Y Dim
	yfdata = np.array((preMarkerDict['marker1'][0,1], preMarkerDict['marker2'][0,1]))
	for i in range(3, usrLabelCount+1):
		yfdata = np.concatenate(( yfdata,[preMarkerDict['marker{}'.format(i)][0,1]]),axis=0)
	#First Frame Data in Z Dim
	zfdata = np.array((preMarkerDict['marker1'][0,2], preMarkerDict['marker2'][0,2]))
	for i in range(3, usrLabelCount+1):
	   zfdata = np.concatenate(( zfdata,[preMarkerDict['marker{}'.format(i)][0,2]]),axis=0)

	# print("First X Data: \n", xfdata, "\n \n", "First Y Data: \n", yfdata)
	# 2D plot of the first frame data
	minX = np.amin(xfdata)
	minY = np.amin(yfdata)
	maxX = np.amax(xfdata)
	maxY = np.amax(yfdata)
	print("Min X | Max X | Min Y | Max Y \n" , minX, maxX, minY, maxY)
	# Layout image for reference
	faceimg = plt.imread(Path(layoutPath))

	#Creating subplots to use slider widgets on window
	fig, ax = plt.subplots()
	plt.subplots_adjust(left=0.1, bottom=0.35)
	plotFigure = plt.scatter(xfdata, yfdata, cmap = 'plasma', picker = usrLabelCount)
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

	# Picker for picking initial points
	coordList = plt.ginput(n=usrLabelCount, show_clicks =True)
	# fig.canvas.mpl_connect('pick_event', lambda event:
	#  onpick(event, xArray= xfdata, yArray= yfdata, zArray= zfdata)
	#  )

	plt.show()
	resultList = []
	for elem in coordList:
		resultList.append(list(elem))
	# listForCoords.extend(resultList)
	listForCoords = resultList[:]
	return resultList

# Function to plot Dict data in 3D
def PlotDict3D(markerDict: dict = None):
	markerCount = len(markerDict.keys())

	# Data in X Dim
	xdata = np.array(markerDict['marker1'][:,0])
	for i in range(2, markerCount+1):
		xdata = np.concatenate((xdata,markerDict['marker{}'.format(i)][:,0]),axis=0)
	# Data in Y Dim
	ydata = np.array(markerDict['marker1'][:,1])
	for i in range(2, markerCount+1):
		ydata = np.concatenate((ydata,markerDict['marker{}'.format(i)][:,1]),axis=0)
	# Data in Z Dim
	zdata = np.array(markerDict['marker1'][:,2])
	for i in range(2, markerCount+1):
		zdata = np.concatenate((zdata,markerDict['marker{}'.format(i)][:,2]),axis=0)

	ax = plt.axes(projection='3d')
	ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='plasma')
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_zlabel('z')
	# Z+ pointing into screen | X- pointing to right screen border
	plt.show()

# def onpick(event, xArray, yArray, zArray, label: string, storageDict: dict):
#         ind = event.ind
#         print('Picked point at coordinates:', ind, xArray[ind], yArray[ind], zArray[ind])

# Function to display a pop-up window with labels ordered for reference
def DisplayLabelsWindow(labelsList: list = None, labelCount: int = None):
	if labelsList is None:
		Exception("No label list to display")
	else:
		lblWin = Toplevel()
		lblWin.title("Labels for reference")

		for i in range(labelCount):
			textToDisplay = str("{}".format(i+1) + ". " + labelsList[i])
			lblLabel = Label(lblWin, text=textToDisplay)
			lblLabel.pack(padx=150)

# Function to select file on button press, wintitle is a Str and winfiletype is a tuple on format ("Title", "*.extension"),("Title2", "*.extension2")
def File_selection(filenameVar: StringVar, wintitle: str, winfiletype):
	filename =  filedialog.askopenfilename(initialdir=Path(), title=wintitle, filetypes=winfiletype)
	try:
		print("Selected:", filename)
		filenameVar.set(filename)
	except:
		print("No file selected")

# Function to transform a list of TKinter entries to a StringVar of comma separated strings
def ListToStringVar(listOfEntries: list, passStringVar: StringVar):
	stringList=[]
	entryCounter = 1
	print("List of Labels")

	for entry in listOfEntries:
		stringList.append(str(entry.get()))

		print(str(entryCounter) + ". " + str(entry.get()) +"\n")
		entryCounter+=1
	
	stringComma = ','.join(stringList)
	# to modify external variable in TKinter
	passStringVar.set(stringComma)

# Function to pass comma separated string to a list of strings
def CsStringToStringList(commaSepString: str):
	return commaSepString.split(",")

# Function to transform a list of strings to a single string separating each original object with a newline
def StringListToNewLineString(stringList: list):
	nlString = ''

	for x in stringList:
		nlString = nlString + str(x) + '\n'
	
	return nlString

# Function to display warning message | Warning there are less markers in the data than there are labels
def NotEnoughMarkerData():
	warningWin = Toplevel()
	warningWin.title("WARNING!")

	myLabel = Label(warningWin, text="MARKER COUNT INSUFFICENT \n CHECK DATA FILE AND/OR LABEL COUNT")
	myLabel.pack()
	return None


# Function to compare XY points to XYZ points proyected to XY in distance:
def From2DTo3D(xyPoints: list, xyzPoints: list):
	# 2d Array needs to have just as many elements as the 3D Array
	labelCount = len(xyPoints)
	markerCount = len(xyzPoints)
	if (labelCount > markerCount):
		print("More Labels than markers in data")
		return None
	
	resultList = []
	
	for i in range(labelCount):
		minDist = int(sys.maxsize)
		resInd = int()
		for j in range(markerCount):
			activeDist = EucDist(point1= [ xyPoints[i][0], xyPoints[i][1] ] ,point2= [ xyzPoints[j][0], xyzPoints[j][1] ])
			if(minDist > activeDist):
				minDist = activeDist
				resInd = j
		
		resultList.append(xyzPoints[resInd])

	# print(resultList)
	return resultList

# Function to calculate distance in 2D points
def EucDist(point1=None, point2=None):
	point1 = np.array(point1)
	point2 = np.array(point2)

	dist = np.linalg.norm(point1 - point2)

	return dist

# Function to transform the Dictionary way of storing initial marker position into a 2 dimensional np.array (matrix)
# with row= marker and column= x/y/z
def DictToInitPosList(dictOfMarkers: dict = None):

	markerCount = len(dictOfMarkers.keys())
	keylist = list(dictOfMarkers.keys())
	
	# Pass the marker lists into a list of their initial positions
	# as of Python 3.7 and newer Dicts are order-perserving
	completeList = []
	for key in dictOfMarkers:
		activeMarkerInitList = dictOfMarkers[key][0,:].tolist()
		completeList.append(activeMarkerInitList)
	
	# Remove zero-ed and nan elements
	initialPosList = [s for s in completeList if np.isnan(np.sum(s)) == False]

	return initialPosList

# Function that takes two lists of coordinates each representing a frame, and matches them with labels using Hungarian Algorithm
# (WARNING: this func adapts the coordinates' format and matches it to the last frame, 
# last frame list MUST be in the same order as the label list/vertexs)
def FrameHungarianMatching(lastFrameList: list = None, activeFrameList: list = None, labelVertex: list = None):
	markerCount = len(activeFrameList)
	labelCount = len(labelVertex)

	markerVertex = activeFrameList
	# dict to store the final matched coords
	matchedCoords = {}
	# cleaned marker list without NaNs
	markerListClean = [list(s) for s in markerVertex if np.isnan(np.sum(s)) == False]
	cleanMarkerCount = len(markerListClean)
	# if there are less markers than labels, copy last frame coords
	if cleanMarkerCount < labelCount:
		for k in range(labelCount):
				matchedCoords[labelVertex[k]] = lastFrameList[k]

	else:
		hungEntryDict = {}
		# Making the new dict to be used with the hungarian algorithm matching func
		# the Last Frame Coordinate list HAS to be matched and ordered already
		for i in range(markerCount):
			# Create dict key for label vertex
			if i < labelCount:
				hungEntryDict[str(labelVertex[i])] = {}
			# Create dummies for extra marker spaces
			elif labelCount <= i <= markerCount:
				hungEntryDict['dummy{}'.format(i)] = {}
			# Loop to fill with a dict of the marker vertex and the weight function of 
			for j in range(markerCount):
				# Dummy labels are non important
				if i >= labelCount:
					hungEntryDict['dummy{}'.format(i)]['{}'.format(j)] = int(100*np.sum(max(lastFrameList)))
				# NaN values mean these coordinates aren't for this frame
				elif np.isnan(np.sum(activeFrameList[j])):
					hungEntryDict[str(labelVertex[i])]['{}'.format(j)] = int(100*np.sum(max(lastFrameList)))
				# The weigth of the match is the eucledian distance between the last frame's point and the new frame's one
				else:
					hungEntryDict[str(labelVertex[i])]['{}'.format(j)] = EucDist(
						point1= lastFrameList[i],
						point2= [markerVertex[j][0], markerVertex[j][1], markerVertex[j][2]]
					)
		
		# print('Algorithm Entry \n',hungEntryDict)
		hungMatchedList = algorithm.find_matching(hungEntryDict, matching_type='min', return_type='list')
		# print('Matched List: \n', hungMatchedList)

		# If matching fails then assign with costly direct eucledian distance comparisson
		if type(hungMatchedList) == type(bool()):
			# If there are equal number of markers and labels use min Euc Dist comparisson
			if cleanMarkerCount == labelCount:
				for k in range(labelCount):
					minDist = int(sys.maxsize)
					resInd = int()
					for l in range(labelCount):
						currentDist = EucDist(
							point1= lastFrameList[k],
							point2= [markerVertex[l][0], markerVertex[l][1], markerVertex[l][2]]
						)
						if(minDist > currentDist):
							minDist = currentDist
							resInd = l
					matchedCoords[labelVertex[k]] = list(markerVertex[resInd])

			# if there are more or less markers than labels repeat last frame
			else:
				for k in labelCount:
					matchedCoords[labelVertex[k]] = lastFrameList[k]

		# Matching succesful then do this
		else:
			for item in hungMatchedList:
				matchedCoords[item[0][0]] = list(markerVertex[ int(item[0][1]) ])
	
	# print('Matched Coords: \n', matchedCoords)
	return matchedCoords

# Function to run the matching algorithm to the marker dict frame by frame
def MarkerDictHungMatch(dataFilePath: str  = None, labelList: list = None, usrCoords: list = None, dictToPass: dict = None):

	dictMarkersFull = PrepareData(Path(dataFilePath))

	firstCoords = DictToInitPosList(dictOfMarkers = dictMarkersFull)
	initialCoords = From2DTo3D(xyPoints= usrCoords, xyzPoints= firstCoords)
	# print('InitialCoordCount: ', len(initialCoords), '\n')

	frameCount = len(dictMarkersFull['marker1'])
	labelCount = len(labelList)
	# print('Labelcount: ', labelCount, '\n')
	markerCount = len(dictMarkersFull.keys())

	# initialize the result dict with the initial coords with the labels as keys
	resultMatchedDict = {}
	for k in range(labelCount):
		resultMatchedDict[str(labelList[k]) + 'X'] = list()
		resultMatchedDict[str(labelList[k]) + 'Y'] = list()
		resultMatchedDict[str(labelList[k]) + 'Z'] = list()

		resultMatchedDict[str(labelList[k]) + 'X'].append(initialCoords[k][0])
		resultMatchedDict[str(labelList[k]) + 'Y'].append(initialCoords[k][1])
		resultMatchedDict[str(labelList[k]) + 'Z'].append(initialCoords[k][2])



	lastFrameData = initialCoords
	for i in range(1,frameCount):
		# making list with current frame coordinates for each marker
		myFrameList = list()
		for key in dictMarkersFull:
   			myFrameList.append(list(dictMarkersFull[key][i,:]))
		
		# frame matching function
		# print("Frame number: ", i, '\n')
		matchedFrame = FrameHungarianMatching(lastFrameList= lastFrameData, activeFrameList= myFrameList, labelVertex= labelList)
		
		# adding the matched values to corresponding label in result dictionary
		for k in range(labelCount):
			resultMatchedDict[str(labelList[k]) + 'X'].append(matchedFrame[labelList[k]][0])
			resultMatchedDict[str(labelList[k]) + 'Y'].append(matchedFrame[labelList[k]][1])
			resultMatchedDict[str(labelList[k]) + 'Z'].append(matchedFrame[labelList[k]][2])
		
		# updating last frame data
		tempList = list()
		for labelKey in labelList:
			tempList.append(matchedFrame[labelKey])
		lastFrameData = tempList
	
	dictToPass = resultMatchedDict
	return resultMatchedDict