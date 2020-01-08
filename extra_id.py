from os import path, stat
from platform import system
from datetime import date
from re import search


def log(string):
    tk_instance.configure(state="normal")
    tk_instance.insert("end", "\n")
    tk_instance.insert("end", string)
    tk_instance.yview("end")
    tk_instance.configure(state="disabled")


def verbose_log(string):
    if verbose_mode:
        log(string)


def creation_date(path_to_file):
    if system() == "Windows":
        return(path.getctime(path_to_file))
    else:
        os_stat = stat(path_to_file)
        try:
            return(date.fromtimestamp(os_stat.st_birthtime))
        except AttributeError:  # used if platform not supported, e.g. Linux
            return(date.fromtimestamp(os_stat.st_mtime))


def extra_id(file_path, file_category, verbose_option, tk_label):

    original_filename = path.split(file_path[0] + file_path[1])[1]
    extension = file_path[1][1:]

    global verbose_mode
    verbose_mode = verbose_option
    global tk_instance
    tk_instance = tk_label

    # research other audio extensions that can hold the same type of ID3 tags
    # possibly m4a (esp. from iTunes), aac, flac, wav
    if extension == "mp3":
        # EXTERNAL music_tag.PY FILE
        # acoustid thing here
        # look up in musicbrainz database
        # return song metadata
        # file renamed with 'Artist - Title'
        # folder extended with ['Artist', '[Year] Album']
        # tag song metadata with mutagen
        pass

    if extension == "jpg":
        # EXTERNAL exif_tag.PY FILE
        # read exif data from image
        # check for device metadata and return string, e.g. 'iPhone 6'
        # find date created and return string, e.g. '2019.04.22'
        # check location and map coordinates to location (DIFFICULT)
        # original filename kept
        # folder extended with ['iPhone 6', '2019.04.22', 'IMG_2203.jpg']
        pass

    if extension in ["docx", "pptx", "pdf"]:
        date_created = creation_date(file_path[0] + file_path[1])
        verbose_log("'{0}' was created on {1}".format(original_filename,
                                                      date_created))
        date_created = (str(date_created)).replace("-", ".")
        if not search("[0-9][0-9][0-9][0-9].[0-9][0-9].[0-9][0-9]",
                      original_filename):
                        new_filename = "[{0}] {1}".format(date_created,
                                                          original_filename)
        else:
            verbose_log("'{0}' already contains a date so will not be renamed"
                        .format(original_filename))
            new_filename = original_filename
        new_category = file_category
        new_category.append(str(date_created.split(".")[0]))
        return(new_filename, new_category)

    if extension == "vcf":
        # EXTERNAL vcf_tag.PY FILE
        # read vcf contact data using vobject library
        # file renamed with 'First Middle Last'
        pass

    return(original_filename, file_category)
