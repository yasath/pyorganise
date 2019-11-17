import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from platform import system
# import pyorganise


def to_YesNo(input_value):
    if input_value == 0:
        return("No")
    elif input_value == 1:
        return("Yes")
    else:
        return


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

    if verbose_mode.get() == 1:
        message_body += ("Copy mode: "+to_YesNo(copy_mode.get())) + "\n"
        message_body += ("Verbose mode: "+to_YesNo(verbose_mode.get())) + "\n"
        message_body += ("Subfolder mode: "+to_YesNo(subfolder_mode.get()))
        message_body += "\n\n"

    message_body += "Are you sure you want to organise this folder?"
    doublecheck_result = messagebox.askyesno("Input submitted!",
                                             message_body)

    if doublecheck_result is True:
        for widget in root.winfo_children():
            widget.destroy()
    else:
        return

    processing_title = ttk.Label(root, text="Processing...",
                                 font=(SYS_FONT, 18, "bold"))
    processing_title.grid(row=0, sticky="w", pady=(5, 10), padx=10)

    ttk.Separator(root).grid(sticky="ew", row=1, columnspan=3)

    scrollbar = ttk.Scrollbar(root)
    textbox = tk.Text(root, width=60, height=15, font=(SYS_FONT, 12),
                      wrap="word")
    scrollbar.grid(row=2, column=2, pady=20, padx=(0, 20), sticky="nesw")
    textbox.grid(row=2, column=0, pady=20, padx=(20, 0), columnspan=2,
                 sticky="w")
    scrollbar.config(command=textbox.yview)
    textbox.config(yscrollcommand=scrollbar.set)

    # TO INSERT INTO TEXTBOX: https://stackoverflow.com/a/24965264

    # TO USE PROGRESS BAR: https://stackoverflow.com/a/20749393

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300,
                                   mode="determinate", maximum=100, value=50)
    progress_bar.grid(row=3, column=0, sticky="w", padx=20, pady=(0, 20))

    done_button = ttk.Button(root, text="Done", state="disabled")
    done_button.grid(row=3, column=1, sticky="e", pady=(0, 20))


# DEFINE THE WINDOW

root = tk.Tk()
root.title("Folder Organiser")
root.resizable(False, False)

if system() == "Darwin":
    root.configure(background="#ececec")
    SYS_FONT = "TkDefaultFont"
elif system() == "Windows":
    SYS_FONT = "Segoe UI"
else:
    SYS_FONT = "TkDefaultFont"

# INPUT SECTION

input_title = ttk.Label(root, text="Input", font=(SYS_FONT, 18, "bold"))
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

options_title = ttk.Label(root, text="Options", font=(SYS_FONT, 18, "bold"))
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
