from os import path, stat
from platform import system
from datetime import date
from re import search
from exif import Image


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
    new_filename = None
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

    if extension in ["jpg", "tiff", "tif"]:
        with open(file_path[0] + file_path[1], "rb") as image_file:
            current_image = Image(image_file)
        if not current_image.has_exif:
            verbose_log("'{0}' does not contain EXIF data so will not be"
                        .format(original_filename) + " categorised based on" +
                        " device")
            return(original_filename, file_category)
        else:
            try:
                image_device = current_image.model
                date_created = (str(creation_date(file_path[0]
                                                  + file_path[1]))).replace(
                                                  "-", ".")
                verbose_log("'{0}' was taken on '{1}' on {2}"
                            .format(original_filename, image_device,
                                    date_created))
                new_category = file_category
                new_category.append(image_device)
                new_category.append(date_created)
                return(original_filename, new_category)
            except Exception:
                verbose_log("The EXIF data of '{0}' does not contain the"
                            .format(original_filename)
                            + " device it was taken on")
                return(original_filename, file_category)

    if extension in ["docx", "pptx", "pdf"]:
        date_created = (str(creation_date(file_path[0] +
                        file_path[1]))).replace("-", ".")
        verbose_log("'{0}' was created on {1}".format(original_filename,
                                                      date_created))
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
        with open(file_path[0] + file_path[1]) as vcard:
            for line in vcard.readlines():
                if "FN:" in line:
                    verbose_log("'{0}' detected contact as '{1}'"
                                .format(original_filename, line[3:].strip()))
                    new_filename = line[3:].strip() + "." + extension
        if not new_filename:
            verbose_log("'{0}' does not contain FN: variable so contact name"
                        .format(original_filename) + " cannot be detected")
            new_filename = original_filename
        return(new_filename, file_category)

    return(original_filename, file_category)
