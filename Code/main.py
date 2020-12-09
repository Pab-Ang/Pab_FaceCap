from numpy.lib.npyio import save
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
Label(userWindow, text='Enter how many labels you are using:', font=('bold', 10)).grid(column= 0, row= 3)
Entry(userWindow, textvariable=usrMarkerCount).grid(column= 1, row=3)

labelStringVar = StringVar()
initialLabelsBtn = Button(userWindow, text='Initialize Labels')
initialLabelsBtn.config(command =lambda:
   Fn.InputLabelsWindow(usrLabelCount= int(usrMarkerCount.get()),StringVarToPass= labelStringVar)
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

initialUsrCoordCount = len(initialUsrCoords)
print("USER INPUT COORDINATES", "| Count:", initialUsrCoordCount, '\n')
for coord in initialUsrCoords: print(coord)

# print( '\n', "Initial Coordinates in order: \n")
# orderedList = Fn.From2DTo3D(xyPoints= initialUsrCoords, xyzPoints= firstCoords)
# for elem in orderedList: print(elem)

# ordered data
usrLabelList = Fn.CsStringToStringList(labelStringVar.get())

resultFinal = Fn.MarkerDictHungMatch(dataFilePath =dataFileName.get(), labelList=usrLabelList, usrCoords= initialUsrCoords)
resultFinalDF = pd.DataFrame(resultFinal)
print('Resultado Final: \n', resultFinalDF)

# saveWin = Tk()
# saveWin.title('Save As')
export_file_path = filedialog.asksaveasfilename(title= 'Save As', initialdir= Path.cwd(), defaultextension='.csv', filetype=[("CSV File", "*.csv")])
resultFinalDF.to_csv(export_file_path, index = False, header=True)