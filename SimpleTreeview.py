### File Name: Tkinter ttk Treeview Simple Demo
### Reference: http://knowpapa.com/ttk-treeview/

from tkinter import *
from tkinter import ttk

root = Tk()

tree = ttk.Treeview(root)

tree["columns"] = ("one", "two")
tree.column("one", width=150)
tree.column("two", width=100)
tree.heading("one", text="column A")
tree.heading("two", text="column B")


### insert format -> insert(parent, index, iid=None, **kw)
### reference: https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview
tree.insert("", 0, text="Line 1", values=("1A", "1b"))
tree.insert("", "end", text="sub dir 2", values=("2A", "2B"))


### insert sub-item, method 1
id2 = tree.insert("", "end", "dir2", text="Dir 2")
tree.insert(id2, "end", text="sub dir 2-1", values=("2A", "2B"))
tree.insert(id2, "end", text="sub dir 2-2", values=("2A-2", "2B-2"))

### insert sub-item, method 2
tree.insert("", "end", "dir3", text="Dir 3")
tree.insert("dir3", "end", text=" sub dir 3", values=("3A", "3B"))

tree.pack()
root.mainloop()
