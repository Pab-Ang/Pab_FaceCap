import myFuncs as Fn
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog

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
         for x in range(winColumnCount):
            if(entryCounter >= usrLabelCount):
               break
            myEntry = Entry(popWin)
            myEntry.grid(row=y, column=x, pady=20, padx=5)
            entryList.append(myEntry)

            entryCounter+=1
      
      passListBtn = Button(popWin, text='Set Labels and Continue', command=lambda: 
         Fn.ListToStringVar(listOfEntries= entryList, passStringVar= StringVarToPass)
         )
      passListBtn.grid(row= winRowCount +1, column= 0, pady=20)


   else:
      entryCounter=0
      winColumnCount = int(3)
      winRowCount = int(np.ceil(usrLabelCount/winColumnCount))
      #Row Entry creation loop
      for y in range(winRowCount):
         #Column Entry creation loop
         for x in range(winColumnCount):
            if(entryCounter >= usrLabelCount):
               break
            myEntry = Entry(popWin)
            myEntry.grid(row=y, column=x, pady=20, padx=5)
            entryList.append(myEntry)

            entryCounter+=1
      
      passListBtn = Button(popWin, text='Set Labels and Continue', command=lambda: 
         Fn.ListToStringVar(listOfEntries= entryList, passStringVar= StringVarToPass)
         )
      passListBtn.grid(row= winRowCount +1, column= 0, pady=20)

userWindow = Tk()
userWindow.title('FaceCap Auto-Label')
# Get the Data (CSV) file location from user
dataFileName = StringVar()
Label(userWindow, text="Select a Data file:").grid(column = 0, row = 0, pady=20)
dataFileBtn = Button(userWindow, text='Browse Data Files', width=18)
dataFileBtn.config(command=lambda: 
   Fn.File_selection(dataFileName,"Select A Data File", [("CSV File", "*.csv")] ) 
   )
dataFileBtn.grid(column = 1, row = 0, pady=20)

# Get the Layout file location from the user
layoutFilePath = StringVar()
Label(userWindow, text="Select a Layout file:").grid(column = 0, row = 2)
layoutFileBtn = Button(userWindow, text='Browse Layout Files', width=18)
layoutFileBtn.config(command=lambda:
   Fn.File_selection(layoutFilePath, "Select A Layout File", [("PNG File", "*.png"),("JPEG File", "*.jpeg"),("JPG File", "*.jpg")] ) 
   )
layoutFileBtn.grid(column = 1, row = 2)

usrMarkerCount = IntVar()
Label(userWindow, text='Enter how many markers you are using:', font=('bold', 10)).grid(column= 0, row= 3)
Entry(userWindow, textvariable=usrMarkerCount).grid(column= 1, row=3)

labelStringVar = StringVar()
initialLabelsBtn = Button(userWindow, text='Initialize Labels')
initialLabelsBtn.config(command =lambda:
   InputLabelsWindow(usrLabelCount= int(usrMarkerCount.get()),StringVarToPass= labelStringVar)
   )
initialLabelsBtn.grid(column = 1, row = 4)

initialUsrCoords = []
initialPlotBtn = Button(userWindow, text='Initialize Label coordinates')
initialPlotBtn.config(command =lambda:
   Fn.PlotInitialLayout(
      dataFilePath= dataFileName.get(),
      layoutPath= layoutFilePath.get(),
      usrLabelCount = usrMarkerCount.get(),
      listOfLabels = Fn.CsStringToStringList(labelStringVar.get()),
      listForCoords = initialUsrCoords
      )
   )
initialPlotBtn.grid(column = 1, row = 5)

userWindow.mainloop()
# --------------------------------------------------------------------------------------------------------------
preMarkerDict = Fn.PrepareData(Path(dataFileName.get()))
# print(preMarkerDict)
# print('\n Marker Arrays')    
# for key in preMarkerDict:
#    print(key)
#    print(preMarkerDict[key])

print('\n',"Initial Marker Positions")
firstCoords = Fn.DictToInitPosList(dictOfMarkers = preMarkerDict)

preMarkerCount = len(preMarkerDict.keys())
print("User Marker Count",usrMarkerCount.get())
# labelList = Fn.CsStringToStringList(labelStringVar.get())
# for x in range(usrMarkerCount.get()):
#    print('{}'.format(x+1) + '.' + labelList[x] +'\n')

#Eucledian Distance between marker in different frames
point1 = preMarkerDict['marker1'][0,:]
point2 = preMarkerDict['marker1'][1,:]
dist = np.linalg.norm(point1 - point2)

initialUsrCoordCount = len(initialUsrCoords)
print("USER INPUT COORDINATES", "| Count:", initialUsrCoordCount, '\n')
for i in initialUsrCoords: print(initialUsrCoords)

print( '\n', "Initial Coordinates in order: \n")
orderedList = Fn.From2DTo3D(xyPoints= initialUsrCoords, xyzPoints= firstCoords)
for elem in orderedList: print(elem)