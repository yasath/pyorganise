import tkinter as tk
from tkinter import ttk

# DEFINE THE WINDOW

root = tk.Tk()
root.title("Folder Organiser")
root.geometry("600x350")
root.resizable(False, False)

# INPUT SECTION

titleOne = ttk.Label(root, text="Input", font=("TkDefaultFont", 18, "bold"))
titleOne.grid(row=0, sticky="w", pady=(5, 10), padx=10)

ttk.Separator(root).place(x=0, y=50, relwidth=1)

# Folder input
# (https://stackoverflow.com/questions/43516019/python-tkinter-browse-folder-button)

labelOne = ttk.Label(root, text="Choose folder:")
labelOne.grid(row=2, sticky="w", pady=(10, 0), padx=10)

labelTwo = ttk.Label(root, text="Choose the directory to be organised",
                     state="disabled")
labelTwo.grid(row=3, sticky="w", pady=(0, 0), padx=10)

entryOne = ttk.Entry(root, width=80)
entryOne.grid(row=4, column=0, padx=(20, 0), pady=10)

buttonOne = ttk.Button(root, text="Browse")
buttonOne.grid(row=4, column=1, pady=10)

# OPTIONS SECTION

titleTwo = ttk.Label(root, text="Options", font=("TkDefaultFont", 18, "bold"))
titleTwo.grid(row=5, sticky="w", pady=(0, 10), padx=10)

ttk.Separator(root).place(x=0, y=190, relwidth=1)

# Option checkboxes

copy_mode = tk.IntVar()
checkboxOne = ttk.Checkbutton(root, text="Copy mode", variable=copy_mode)
checkboxOne.grid(row=6, sticky="w", column=0, pady=(12, 0), padx=10)

labelThree = ttk.Label(root, text="Copies files instead of moving them",
                       state="disabled")
labelThree.grid(row=7, sticky="w", padx=10)

verbose_mode = tk.IntVar()
checkboxTwo = ttk.Checkbutton(root, text="Verbose mode", variable=verbose_mode)
checkboxTwo.grid(row=8, sticky="w", column=0, pady=(10, 0), padx=10)

labelFour = ttk.Label(root, text="More detailed log of the process",
                      state="disabled")
labelFour.grid(row=9, sticky="w", padx=10)

subfolder_mode = tk.IntVar()
checkboxThree = ttk.Checkbutton(root, text="Subfolder mode",
                                variable=subfolder_mode)
checkboxThree.grid(row=10, sticky="w", column=0, pady=(10, 0), padx=10)

labelFive = ttk.Label(root, text="Leaves subfolders alone", state="disabled")
labelFive.grid(row=11, sticky="w", padx=10)

root.mainloop()
