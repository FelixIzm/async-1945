from tkinter import filedialog
from tkinter import *

root = Tk()
root.withdraw()
filename = filedialog.askdirectory()
print(filename)


