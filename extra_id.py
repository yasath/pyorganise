from os import path, stat
from platform import system
from datetime import date
from re import search

from exif import Image

from mutagen.mp3 import MP3

import metadata_tag.music_tag as music_tag
ACOUSTID_KEY = "wrGJUq3wJo"


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

    if extension == "mp3":
        mp3_file = MP3(file_path[0] + file_path[1])
        if mp3_file.info.length > 30:
            if mp3_file.tags is None:
                mp3_file.add_tags()
                mp3_file.save()
            matched = music_tag.acoustid_match(ACOUSTID_KEY, file_path[0] +
                                               file_path[1])
            verbose_log("'{0}' identified as '{1} - {2}'".format(
                                                         original_filename,
                                                         matched[0],
                                                         matched[1]))
            artist, title, album, year, art, trackno, genre = music_tag.lookup(
                                                              matched)
            verbose_log("Song identified as track {0} of '{1}' released in {2}"
                        .format(trackno, album, year))
            try:
                music_tag.tag(file_path[0] + file_path[1],
                              artist, title, album, year, art, trackno, genre)
                verbose_log("ID3 metadata has successfully been embedded")
            except Exception:
                verbose_log("ID3 tagging failed so metadata was not embedded")
            new_filename = "{0} - {1}.{2}".format(artist, title, extension)
            album_folder_name = "[{0}] {1}".format(year, album)
            new_category = file_category
            new_category.extend([artist, album_folder_name])
            return(new_filename, new_category)
        else:
            verbose_log("'{0}' is shorter than 30 seconds so will not be"
                        .format(original_filename) + " identified as a song")
            return(original_filename, file_category)

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
