import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from platform import system


def browse_button():
    root.update_idletasks()
    filename = filedialog.askdirectory()

    folder_input.delete(0, "end")
    folder_input.insert(0, filename)


def quit_button():
    quit_result = messagebox.askyesno("Quit",
                                      "Are you sure you want to exit?")
    if quit_result is True:
        root.destroy()
    else:
        pass


def start_button():
    message_body = folder_input.get() + "\n\n"
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

input_title = ttk.Label(root, text="Input", font=(BIG_FONT, 18, "bold"))
input_title.grid(row=0, sticky="w", pady=(5, 10), padx=10)

ttk.Separator(root).grid(sticky="ew", row=1, columnspan=3)

# Folder input

input_label = ttk.Label(root, text="Choose folder:")
input_label.grid(row=2, sticky="w", pady=(10, 0), padx=10)

input_description = ttk.Label(root,
                              text="Choose the directory to be organised",
                              foreground="grey")
input_description.grid(row=3, sticky="w", pady=(0, 0), padx=10)

folder_input = ttk.Entry(root)
folder_input.grid(row=4, column=0, padx=(10, 0), pady=10, columnspan=2,
                  sticky="nesw")

folder_button = ttk.Button(root, text="Browse", command=browse_button)
folder_button.grid(row=4, column=2, padx=(0, 10), pady=10, sticky="e")

# OPTIONS SECTION

options_title = ttk.Label(root, text="Options", font=(BIG_FONT, 18, "bold"))
options_title.grid(row=6, sticky="w", pady=(0, 10), padx=10)

ttk.Separator(root).grid(sticky="ew", row=7, columnspan=3)

# Option checkboxes

copy_mode = tk.IntVar()
copy_checkbox = ttk.Checkbutton(root, text="Copy mode", variable=copy_mode)
copy_checkbox.grid(row=8, sticky="w", column=0, pady=(12, 0), padx=10)

copy_description = ttk.Label(root, text="Copies files instead of moving them",
                             foreground="grey")
copy_description.grid(row=9, sticky="w", padx=10)

verbose_mode = tk.IntVar()
verbose_checkbox = ttk.Checkbutton(root, text="Verbose mode",
                                   variable=verbose_mode)
verbose_checkbox.grid(row=10, sticky="w", column=0, pady=(10, 0), padx=10)

verbose_description = ttk.Label(root, text="More detailed log of the process",
                                foreground="grey")
verbose_description.grid(row=11, sticky="w", padx=10)

subfolder_mode = tk.IntVar()
subfolder_checkbox = ttk.Checkbutton(root, text="Subfolder mode",
                                     variable=subfolder_mode)
subfolder_checkbox.grid(row=8, sticky="w", column=1, pady=(12, 0))

subfolder_description = ttk.Label(root, text="Leaves subfolders alone",
                                  foreground="grey")
subfolder_description.grid(row=9, column=1, sticky="w")

# Start and Quit buttons

quit_option = ttk.Button(root, text="Quit", command=quit_button)
quit_option.grid(row=12, column=1, sticky="e", pady=(20, 10))

start_option = ttk.Button(root, text="Start", command=start_button)
start_option.grid(row=12, column=2, sticky="w", pady=(20, 10), padx=(0, 10))

root.mainloop()
