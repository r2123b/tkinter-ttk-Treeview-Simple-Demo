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
        # create a TreeView
        self.tree = ttk.Treeview(self.leftframe)
        self.tree["columns"] = ("Index", "Value")
        self.tree.column("Index", stretch=True, width=150)
        self.tree.column("Value", stretch=True, width=100)
        self.tree.heading("Index", text="Index")
        self.tree.heading("Value", text="Value")

        # attach a scrollbar to the frame
        treeScroll = ttk.Scrollbar(self.leftframe)
        treeScroll.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=treeScroll.set)

        # read data from file
        dataFileDir = "/Users/alumi/PycharmProjects/StocksInfoRetrieval/Data/data_mm.pkl"
        if os.path.exists(dataFileDir):
            self.tableData = pd.read_pickle(dataFileDir)
        self.showAllData()

        # put tree and scroll beside each other in the left frame
        self.tree.pack(side=LEFT)
        treeScroll.pack(side=LEFT, fill=Y)

    def insertItem2TreeView(self, itemText, values):
        ### insert format -> insert(parent, index, iid=None, **kw)
        ### reference: https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview
        myItemID = self.tree.insert("", "end", text=itemText, values=(values[0], values[1]))

        if myItemID == None:
            return False
        else:
            return True

    def showAllData(self):
        # first clear all
        self.tree.delete(*self.tree.get_children())
        for i in range(0, self.tableData['HIGH'].size):
            self.insertItem2TreeView("HIGH", [self.tableData['HIGH'].index[i], self.tableData['HIGH'].values[i]])

        self.updateStatusBar()
        # print("Tree View Count = " + str(len(self.tree.get_children())))

    def filter_greater(self):
        self.currentCondition = "GREATER"
        self.tree.delete(*self.tree.get_children())
        comparedValue = float(self.ety_Greater.get())
        for i in range(0, self.tableData['HIGH'].size):
            if (self.tableData['HIGH'].values[i] > comparedValue):
                self.insertItem2TreeView("HIGH", [self.tableData['HIGH'].index[i], self.tableData['HIGH'].values[i]])

        self.updateStatusBar()
        # print("Tree View Count = " + str(len(self.tree.get_children())))

    def filter_less(self):
        self.currentCondition = "LESS"
        self.tree.delete(*self.tree.get_children())
        comparedValue = float(self.ety_Less.get())
        for i in range(0, self.tableData['HIGH'].size):
            if (self.tableData['HIGH'].values[i] < comparedValue):
                self.insertItem2TreeView("HIGH", [self.tableData['HIGH'].index[i], self.tableData['HIGH'].values[i]])

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
def insert_loop(myGUI):
    i=0
    while(1):
        # myGUI.insertItem2TreeView("Alumi", ["Test", 10])
        myGUI.addNewData2TableData(i)
        # myGUI.showAllData()
        i += 1
        time.sleep(10)

if __name__ == '__main__':
    _rootWindow = Tk()
    myTableViewer = TableViewer(_rootWindow, "Table View")

    try:
        _thread.start_new_thread(insert_loop, (myTableViewer, ))
    except:
        print("Loop of insert is wrong!!\n")

    _rootWindow.mainloop()
