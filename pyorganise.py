from os import path
from os import rename
from os import makedirs
from os import walk
from glob import glob
from shutil import copyfile

# Global Constants
from format_classification import file_formats as FORMAT_CATEGORIES
from os import sep as FOLDER_DELIMITER

# Submodules
import extra_id


def main_organise(directory_to_organise, copy_int,
                  verbose_int, subfolder_int, tk_label):

    global copy_mode  # Copy mode: Copies files instead of moving them
    copy_mode = bool(copy_int)

    global verbose_mode  # Verbose mode: More detailed log of the process
    verbose_mode = bool(verbose_int)

    global subfolder_mode  # Subfolder mode: Leaves subfolders alone
    subfolder_mode = bool(subfolder_int)

    global tk_instance
    tk_instance = tk_label

    unorganised_files = get_files(directory_to_organise)

    counter = 0

    for file_path in unorganised_files:
        counter += 1
        log("Inspecting file {0}/{1}...".format(counter,
                                                len(unorganised_files)))

        file_category = find_filetype(file_path[1].lower())
        verbose_log("File category for {0} identified as {1}"
                    .format(file_path[1], file_category))

        new_filename, file_category = extra_id.extra_id(file_path,
                                                        file_category,
                                                        verbose_mode)

        # log(new_filename)
        # log(file_category)

        file_move(directory_to_organise, file_path,
                  file_category, new_filename)


def log(string):
    tk_instance.configure(state="normal")
    tk_instance.insert("end", "\n")
    tk_instance.insert("end", string)
    tk_instance.configure(state="disabled")


def verbose_log(string):
    if verbose_mode:
        log(string)


def get_files(directory):
    if subfolder_mode:
        file_array = []
        original_array = glob(directory+FOLDER_DELIMITER+"*")
        for item in original_array:
            if not path.isdir(item):
                file_array.append(item)
    else:
        file_array = []
        for paths, subdirs, files in walk(directory):
            for name in files:
                file_array.append(path.join(paths, name))

    split_file_array = []
    for file_path in file_array:
        split_file_array.append(path.splitext(file_path))

    return(split_file_array)


def find_filetype(file_extension):
    for category in FORMAT_CATEGORIES:
        for subcategory in category[1]:
            if type(subcategory) is list:
                if file_extension == ("."+subcategory[0]):
                    return([category[0], subcategory[1]])
            else:
                if file_extension == ("."+subcategory):
                    return([category[0]])
    return(["Miscellaneous"])


def file_move(original_directory, file_path, file_category, new_filename):
    original_path = file_path[0] + file_path[1]

    new_path = original_directory
    short_path = ""
    for folder in file_category:
        new_path += (FOLDER_DELIMITER + folder)
        short_path += (FOLDER_DELIMITER + folder)

    try:
        makedirs(new_path)
    except FileExistsError:
        pass

    if not new_filename:
        new_filename = path.split(original_path)[1]

    new_path += (FOLDER_DELIMITER + new_filename)
    short_path += (FOLDER_DELIMITER + new_filename)

    if copy_mode:
        copyfile(original_path, new_path)
        log("Copied '{0}' to '{1}'\n".format(new_filename,
                                             short_path[1:]))
    else:
        rename(original_path, new_path)
        log("Moved '{0}' to '{1}'\n".format(new_filename,
                                            short_path[1:]))
