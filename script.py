from os import path
from os import rename
from os import makedirs
from shutil import copyfile
import glob
from gooey import Gooey, GooeyParser
import sys

# Global Constants
from format_classification import file_formats as FORMAT_CATEGORIES
from os import sep as FOLDER_DELIMITER


@Gooey(program_name="Folder Organiser",
       progress_regex=r"^Inspecting file (?P<current>\d+)/(?P<total>\d+)...$",
       progress_expr="current / total * 100",
       image_dir="images/gooey_img")
def main():
    desc = "Neatly rename and organise your files into helpful subfolders"

    parser = GooeyParser(description=desc)

    parser.add_argument(
        "required_field",
        metavar="Choose folder:",
        help="Choose the directory to be organised",
        widget="DirChooser")

    parser.add_argument(
        "-c", "--copy",
        metavar="Copy mode:",
        action="store_true",
        help="""Enabling this option copies files into subfolders instead of
 moving them""".replace("\n", ""))

    args = parser.parse_args()

    directory_to_organise = args.required_field
    copy_mode = args.copy

    unorganised_files = get_files(directory_to_organise)

    counter = 0

    for file_path in unorganised_files:
        counter += 1
        print("Inspecting file {}/{}...".format(counter,
                                                len(unorganised_files)))

        file_category = find_filetype(file_path[1])
        # file_category = extra_categories(file_path, file_category)
        # new_filename = file_rename(file_path)
        new_filename = None
        file_move(directory_to_organise, file_path,
                  file_category, new_filename, copy_mode)

        sys.stdout.flush()


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


def file_move(original_directory, file_path, file_category, new_filename,
              copy_mode):
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

    if new_filename:
        new_path += (FOLDER_DELIMITER + new_filename)
        short_path += (FOLDER_DELIMITER + new_filename)
    else:
        original_filename = path.split(original_path)[1]
        new_path += (FOLDER_DELIMITER + original_filename)
        short_path += (FOLDER_DELIMITER + original_filename)

    if copy_mode:
        copyfile(original_path, new_path)
        print("Copied '{0}' to '{1}'\n".format(original_filename,
                                               short_path[1:]))
    else:
        rename(original_path, new_path)
        print("Moved '{0}' to '{1}'\n".format(original_filename,
                                              short_path[1:]))


# MAIN PROGRAM

if __name__ == "__main__":
    main()
