import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from platform import system


def browse_button():
    root.update_idletasks()
    filename = filedialog.askdirectory()

    entryOne.delete(0, "end")
    entryOne.insert(0, filename)


def quit_button():
    quit_result = messagebox.askyesno("Quit",
                                      "Are you sure you want to exit?")
    if quit_result == True:
        root.destroy()
    else:
        pass


def start_button():
    message_body = entryOne.get() + "\n\n"
    message_body += ("Copy mode: "+str(copy_mode.get())) + "\n"
    message_body += ("Verbose mode: "+str(verbose_mode.get())) + "\n"
    message_body += ("Subfolder mode: "+str(subfolder_mode.get()))
    messagebox.showinfo("Input submitted!",
                        message_body)

    # for widget in root.winfo_children():
    #    widget.destroy()


# DEFINE THE WINDOW

root = tk.Tk()
root.title("Folder Organiser")
if system() != "Darwin":
    root.resizable(True, False)
    root.minsize(450, 0)
else:
    root.resizable(False, False)
root.grid_columnconfigure(0, weight=1)

if system() == "Darwin":
    root.configure(background="#ececec")
    BIG_FONT = "TkDefaultFont"
elif system() == "Windows":
    BIG_FONT = "Segoe UI"
else:
    BIG_FONT = "TkDefaultFont"

# INPUT SECTION

titleOne = ttk.Label(root, text="Input", font=(BIG_FONT, 18, "bold"))
titleOne.grid(row=0, sticky="w", pady=(5, 10), padx=10)

ttk.Separator(root).grid(sticky="ew", row=1, columnspan=3)

# Folder input

labelOne = ttk.Label(root, text="Choose folder:")
labelOne.grid(row=2, sticky="w", pady=(10, 0), padx=10)

labelTwo = ttk.Label(root, text="Choose the directory to be organised",
                     foreground="grey")
labelTwo.grid(row=3, sticky="w", pady=(0, 0), padx=10)

entryOne = ttk.Entry(root)
entryOne.grid(row=4, column=0, padx=(10, 0), pady=10, columnspan=2,
              sticky="nesw")

buttonOne = ttk.Button(root, text="Browse", command=browse_button)
buttonOne.grid(row=4, column=2, padx=(0,10), pady=10, sticky="e")

# OPTIONS SECTION

titleTwo = ttk.Label(root, text="Options", font=(BIG_FONT, 18, "bold"))
titleTwo.grid(row=6, sticky="w", pady=(0, 10), padx=10)

ttk.Separator(root).grid(sticky="ew", row=7, columnspan=3)

# Option checkboxes

copy_mode = tk.IntVar()
checkboxOne = ttk.Checkbutton(root, text="Copy mode", variable=copy_mode)
checkboxOne.grid(row=8, sticky="w", column=0, pady=(12, 0), padx=10)

labelThree = ttk.Label(root, text="Copies files instead of moving them",
                       foreground="grey")
labelThree.grid(row=9, sticky="w", padx=10)

verbose_mode = tk.IntVar()
checkboxTwo = ttk.Checkbutton(root, text="Verbose mode", variable=verbose_mode)
checkboxTwo.grid(row=10, sticky="w", column=0, pady=(10, 0), padx=10)

labelFour = ttk.Label(root, text="More detailed log of the process",
                      foreground="grey")
labelFour.grid(row=11, sticky="w", padx=10)

subfolder_mode = tk.IntVar()
checkboxThree = ttk.Checkbutton(root, text="Subfolder mode",
                                variable=subfolder_mode)
checkboxThree.grid(row=8, sticky="w", column=1, pady=(12, 0))

labelFive = ttk.Label(root, text="Leaves subfolders alone", foreground="grey")
labelFive.grid(row=9, column=1, sticky="w")

# Start and Quit buttons

buttonTwo = ttk.Button(root, text="Quit", command=quit_button)
buttonTwo.grid(row=12, column=1, sticky="e", pady=(20,10))

buttonThree = ttk.Button(root, text="Start", command=start_button)
buttonThree.grid(row=12, column=2, sticky="w", pady=(20,10), padx=(0,10))

root.mainloop()
