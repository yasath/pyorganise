import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from platform import system
import icons
import base64
import pyorganise


def about_dialog():
    about = tk.Toplevel()
    about.title("About")
    about.resizable(False, False)
    about.grab_set()

    if system() == "Darwin":
        about.configure(background="#ececec")

    input_title = ttk.Label(about, text="Folder Organiser",
                            font=(SYS_FONT, 18, "bold"))
    input_title.grid(row=0, pady=(60, 5), padx=30)

    ttk.Separator(about).grid(sticky="ew", row=1, columnspan=2)

    input_label = ttk.Label(about, text="Created by Yasath Dias")
    input_label.grid(row=2, pady=(5, 60), padx=30)

    about.update()


def to_yes_no(input_value):
    if input_value == 0:
        return("No")
    elif input_value == 1:
        return("Yes")
    else:
        return


def browse_button():
    root.update_idletasks()
    filename = filedialog.askdirectory()
    if filename:
        folder_input.delete(0, "end")
        folder_input.insert(0, filename)


def quit_button():
    quit_result = messagebox.askyesno("Quit",
                                      "Are you sure you want to exit?")
    if quit_result is True:
        root.destroy()
    else:
        pass


def undo_button(copy_int):
    if copy_int == 0:
        message = """Are you sure that you want to undo the process and move
                     the files back to their original directories?"""
    else:
        message = """Are you sure that you want to undo the process and delete
                     the copied files and new directories?"""

    undo_result = messagebox.askyesno("Undo",
                                      message)
    if undo_result is True:
        print("undid")
    else:
        pass


def done_button(copy_int):
    root.destroy()

    """
    for widget in root.winfo_children():
        widget.destroy()

    undo_option = ttk.Button(root, text="Undo",
                             command=lambda: undo_button(copy_int))
    undo_option.grid(row=0, column=0, sticky="e", padx=(200, 0), pady=150)

    quit_option = ttk.Button(root, text="Quit", command=quit_button)
    quit_option.grid(row=0, column=1, sticky="w", padx=(0, 200), pady=150)
    """


def start_button():
    message_body = folder_input.get() + "\n\n"

    if verbose_mode.get() == 1:
        message_body += ("Copy mode: "+to_yes_no(copy_mode.get())) + "\n"
        message_body += ("Verbose mode: "+to_yes_no(verbose_mode.get())) + "\n"
        message_body += ("Subfolder mode: "+to_yes_no(subfolder_mode.get()))
        message_body += "\n\n"

    message_body += "Are you sure you want to organise this folder?"
    doublecheck_result = messagebox.askyesno("Input submitted!",
                                             message_body)

    directory_to_organise = folder_input.get()
    copy_int = copy_mode.get()
    verbose_int = verbose_mode.get()
    subfolder_int = subfolder_mode.get()

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
    textbox.tag_config("error", foreground="red")

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300,
                                   mode="determinate", maximum=100, value=50)
    progress_bar.grid(row=3, column=0, sticky="w", padx=20, pady=(0, 20))

    done_option = ttk.Button(root, text="Done", state="disabled",
                             command=lambda: done_button(copy_int))
    done_option.grid(row=3, column=1, sticky="e", pady=(0, 20))

    pyorganise.main_organise(directory_to_organise,
                             copy_int,
                             verbose_int,
                             subfolder_int,
                             textbox,
                             progress_bar)

    done_option.config(state="normal")


# DEFINE THE WINDOW

root = tk.Tk()
root.title("Folder Organiser")
root.resizable(False, False)

if system() == "Darwin":
    root.configure(background="#ececec")
    SYS_FONT = "TkDefaultFont"
    root.createcommand("tkAboutDialog", about_dialog)
elif system() == "Windows":
    SYS_FONT = "Segoe UI"
else:
    SYS_FONT = "TkDefaultFont"

menubar = tk.Menu(root)
# helpmenu = tk.Menu(menubar, tearoff=0)
# helpmenu.add_command(label="Documentation", command=open_pdf)
# menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)

tk_icon = tk.PhotoImage(data=base64.b64decode(icons.program_icon))
root.wm_iconphoto(True, tk_icon)

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
