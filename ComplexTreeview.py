# Reference: http://pythonbeginners.com/python-beginner-tutorial/python-tkinter/tkinter-frames
# Reference: https://stackoverflow.com/questions/34276663/tkinter-gui-layout-using-frames-and-grid
# grid reference: https://stackoverflow.com/questions/34276663/tkinter-gui-layout-using-frames-and-grid

import os
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

import _thread
import pandas as pd
import time


class TableViewer():
    def __init__(self, master, newTitle):
        self.newWindow = Toplevel(master)
        self.newWindow.title(newTitle)

        # declare frames
        self.leftframe = ttk.Frame(self.newWindow, width=100, height=300, pad=10)
        self.rightframe = ttk.Frame(self.newWindow, width=200, height=300, pad=10)
        self.bottomframe = ttk.Frame(self.newWindow, width=300, height=50, pad=5)

        # arrange frames
        self.arrangeBottomFrame()
        self.arrangeLeftFrameUI()
        self.arrangeRightFrameUI()

        # place your widgets(2 frames) into windows
        self.leftframe.grid(row=1, column=1)
        self.rightframe.grid(row=1, column=2, sticky=W+E+N+S) # sticky="WE" means the inside-objects can extend to west and east
        self.rightframe.grid_rowconfigure(0, weight=1)
        self.bottomframe.grid(row=2, column=1, sticky="WE", columnspan=2)

        # set a variable of chosen condition
        self.currentCondition = "ALL"

    def arrangeBottomFrame(self):
        self.lbl_status = ttk.Label(self.bottomframe, text="Count = ")
        self.lbl_status.pack(side=LEFT)

    def arrangeRightFrameUI(self):
        # configure grid 7*3
        self.rightframe.grid_rowconfigure(0, weight=1)
        self.rightframe.grid_rowconfigure(6, weight=1)
        self.rightframe.grid_columnconfigure(0, weight=1)
        self.rightframe.grid_columnconfigure(2, weight=1)


        L1 = Label(self.rightframe, text="Display greater than ")
        self.ety_Greater = Entry(self.rightframe, width=5)
        btn_filter_Greater = ttk.Button(self.rightframe, text="Filter Greater", command=self.filter_greater, width=10)

        L2 = Label(self.rightframe, text="Display less than ")
        self.ety_Less = Entry(self.rightframe, width=5)
        btn_filter_Less = ttk.Button(self.rightframe, text="Filter Less", command=self.filter_less, width=10)

        btn_showAll = ttk.Button(self.rightframe, text="Show All Data", command=self.showAllData, width=20)

        # arrange each objects, and put objects on 3rd, 4th, 5th row-grid
        L1.grid(row=3, column=0)
        self.ety_Greater.grid(row=3, column=1)
        btn_filter_Greater.grid(row=3, column=2)

        L2.grid(row=4, column=0, sticky=W)
        self.ety_Less.grid(row=4, column=1)
        btn_filter_Less.grid(row=4, column=2)

        btn_showAll.grid(row=5, columnspan=3)


    def arrangeLeftFrameUI(self):
        # read data from file
        dataFileDir = "./testData.csv"
        if os.path.exists(dataFileDir):
            self.tableData = pd.read_csv(dataFileDir)
        
        # create a TreeView with columns
        colnames = self.tableData.columns
        self.tree = ttk.Treeview(self.leftframe)
        self.tree["columns"] = tuple(colnames.values)
        for col in colnames:
            self.tree.column(column=col, width=100)
            self.tree.heading(column=col, text=col)

        # show all content
        self.showAllData()

        # attach a scrollbar to the frame
        treeScroll = ttk.Scrollbar(self.leftframe)
        treeScroll.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=treeScroll.set)

        # put tree and scroll beside each other in the left frame
        self.tree.pack(side=LEFT)
        treeScroll.pack(side=LEFT, fill=Y)

    def showAllData(self):
        self.tree.delete(*self.tree.get_children())

        for i, row in self.tableData.iterrows():
            self.tree.insert('', index=i, text="item"+str(i+1), values=tuple(row.values))
        self.updateStatusBar()
        # print("Tree View Count = " + str(len(self.tree.get_children())))

    def filter_greater(self):
        self.currentCondition = "GREATER"
        self.tree.delete(*self.tree.get_children())
        comparedValue = float(self.ety_Greater.get())
        for i, row in self.tableData[self.tableData['value']>=comparedValue].iterrows():
            self.tree.insert('', index=i, text="item"+str(i+1), values=tuple(row.values))
        self.updateStatusBar()
        # print("Tree View Count = " + str(len(self.tree.get_children())))

    def filter_less(self):
        self.currentCondition = "LESS"
        self.tree.delete(*self.tree.get_children())
        comparedValue = float(self.ety_Less.get())
        for i, row in self.tableData[self.tableData['value']<=comparedValue].iterrows():
            self.tree.insert('', index=i, text="item"+str(i+1), values=tuple(row.values))
        self.updateStatusBar()
        # print("Tree View Count = " + str(len(self.tree.get_children())))

    def updateTable(self):
        print("Current Condition is " + self.currentCondition)
        if self.currentCondition == "ALL":
            self.showAllData()
        elif self.currentCondition == "GREATER":
            self.filter_greater()
        elif self.currentCondition == "LESS":
            self.filter_less()
        else:
            print("Current Condition has wrong value!!")

    def updateStatusBar(self):
        self.lbl_status.config(text="Tree View Count = " + str(len(self.tree.get_children())))
        # print("Tree View Count = " + str(len(self.tree.get_children())))


    # test for dynamic update
    def addNewData2TableData(self, timestamp):
        # print(self.tableData)
        newitem = self.tableData.loc["2330 TT Equity"]
        newitem.loc["HIGH"] = 10.123 + timestamp
        self.tableData.loc["AlumiInsert"+str(timestamp)] = newitem
        self.updateTable()
        # print(newitem)



######### The following is for testing!!!

if __name__ == '__main__':
    _rootWindow = Tk()
    myTableViewer = TableViewer(_rootWindow, "Table View")
    
    _rootWindow.mainloop()
