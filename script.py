from os import path
from os import rename
from os import makedirs
from os import sep as FOLDER_DELIMITER
import glob
from progress.bar import ChargingBar

# Global Constants
from format_classification import file_formats as FORMAT_CATEGORIES

# Future Features (THESE CURRENTLY DO NOTHING)
COPY_MODE = False  # Set to True to copy files instead of moving them


def input_directory():
    while True:
        try:
            directory = input("Please enter the directory to organise: ")
            if not path.isdir(directory):
                raise NotADirectoryError("Invalid directory entered",
                                         directory)
            break
        except NotADirectoryError:
            print("The entered directory is not valid. Try again.\n")
    return(directory)


def get_files(directory):
    file_array = glob.glob(directory+FOLDER_DELIMITER+"*")

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
    for folder in file_category:
        new_path += (FOLDER_DELIMITER + folder)

    try:
        makedirs(new_path)
    except FileExistsError:
        pass

    if new_filename:
        new_path += (FOLDER_DELIMITER + new_filename)
    else:
        original_filename = path.split(original_path)[1]
        new_path += (FOLDER_DELIMITER + original_filename)

    rename(original_path, new_path)


def main():
    directory_to_organise = input_directory()
    unorganised_files = get_files(directory_to_organise)

    progress_bar = ChargingBar("Organising files...",
                               max=len(unorganised_files))

    for file_path in unorganised_files:
        file_category = find_filetype(file_path[1])
        # file_category = extra_categories(file_path, file_category)
        # new_filename = file_rename(file_path)
        new_filename = None
        file_move(directory_to_organise, file_path,
                  file_category, new_filename)
        progress_bar.next()
    progress_bar.finish()


# MAIN PROGRAM

if __name__ == "__main__":
    main()
