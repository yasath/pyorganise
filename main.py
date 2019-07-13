from os import path
from os import rename
from os import makedirs
from shutil import copyfile
import glob
from gooey import Gooey, GooeyParser

# Global Constants
from format_classification import file_formats as FORMAT_CATEGORIES
from os import sep as FOLDER_DELIMITER

# Submodules
import extra_id


@Gooey(program_name="Folder Organiser",
       progress_regex=r"^Inspecting file (?P<current>\d+)/(?P<total>\d+)...$",
       progress_expr="current / total * 100",
       image_dir="images/gooey_img")
def main():
    desc = "Neatly rename and organise your files into helpful subfolders"

    parser = GooeyParser(description=desc)

    input_group = parser.add_argument_group(
        "Input")
    input_group.add_argument(
        "-i", "--input_folder",
        required=True,
        metavar="Choose folder:",
        help="Choose the directory to be organised",
        widget="DirChooser")

    optional_group = parser.add_argument_group(
        "Optional",
        gooey_options={
                      'columns': 2
                      })

    optional_group.add_argument(
        "-c", "--copy",
        metavar="Copy mode:",
        action="store_true",
        help="Copies files instead of moving them")

    optional_group.add_argument(
        "-v", "--verbose",
        metavar="Verbose mode:",
        action="store_true",
        help="More detailed log of the process")

    args = parser.parse_args()

    directory_to_organise = args.required_field

    global copy_mode
    copy_mode = args.copy

    global verbose_mode
    verbose_mode = args.verbose

    unorganised_files = get_files(directory_to_organise)

    counter = 0

    for file_path in unorganised_files:
        counter += 1
        print("Inspecting file {0}/{1}...".format(counter,
                                                  len(unorganised_files)))

        file_category = find_filetype(file_path[1])
        verbose_print("File category for {0} identified as {1}"
                      .format(file_path[1], file_category))

        new_filename, file_category = extra_id.extra_id(file_path,
                                                        file_category,
                                                        verbose_mode)

        # print(new_filename)
        # print(file_category)

        file_move(directory_to_organise, file_path,
                  file_category, new_filename)


def verbose_print(string):
    if verbose_mode:
        print(string)


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
        print("Copied '{0}' to '{1}'\n".format(new_filename,
                                               short_path[1:]))
    else:
        rename(original_path, new_path)
        print("Moved '{0}' to '{1}'\n".format(new_filename,
                                              short_path[1:]))


# MAIN PROGRAM

if __name__ == "__main__":
    main()
