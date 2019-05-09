from os import path


def extra_id(file_path, file_category):

    original_filename = path.split(file_path[0] + file_path[1])[1]
    extension = file_path[1][1:]

    if extension == "mp3":
        # EXTERNAL .PY FILE
        # acoustid thing here
        # look up in musicbrainz database
        # return song metadata
        # file renamed with 'Artist - Title'
        # folder extended with ['Artist', '[Year] Album']
        # tag song metadata with mutagen
        pass

    if extension == "jpg":
        # EXTERNAL .PY FILE
        # read exif data from image
        # check for device metadata and return string, e.g. 'iPhone 6'
        # find date created and return string, e.g. '2019.04.22'
        # check location and map coordinates to location (DIFFICULT)
        # original filename kept
        # folder extended with ['iPhone 6', '2019.04.22', 'IMG_2203.jpg']
        pass

    if extension == "docx":
        # find date created and return string, e.g. '2018.11.27'
        # file renamed with '[yyyy.mm.dd]' appended before
        # folder extended with ['yyyy']
        pass

    return(original_filename, file_category)
