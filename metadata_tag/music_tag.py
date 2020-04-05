from acoustid import match
from itertools import groupby
import requests
from mutagen.id3 import ID3, TIT2, TPE1, TRCK, TALB, TDRC, TCON, APIC
from urllib.request import urlopen


def acoustid_match(api_key, file_path):
    match_count = 0
    possible_matches = []
    try:
        for score, id, title, artist in match(api_key, file_path):
            if match_count < 5:
                possible_matches.append([title, artist])
                match_count += 1
        try:
            counts = [(i, len(list(c))) for i, c in groupby(sorted(
                                                            possible_matches))]
            counts.sort(key=lambda x: x[1])
            matched = counts[-1][0]
        except Exception:
            matched = possible_matches[0]
        return([matched[1], matched[0]])
    except Exception as error:
        return([None, None])


def lookup(acoustid_matched_array):
    artist = acoustid_matched_array[0]
    title = acoustid_matched_array[1]
    url_artist = artist.lower().replace(" ", "+")
    url_title = title.lower().replace(" ", "+")
    api_request = ("https://itunes.apple.com/search?"+"term={0}+{1}&limit=1"
                   .format(url_artist, url_title))
    search_results = requests.get(api_request).json()

    album = search_results["results"][0]["collectionName"]
    year = search_results["results"][0]["releaseDate"][0:4]
    artwork = search_results["results"][0]["artworkUrl100"].replace("100x100",
                                                                    "600x600")
    track_number = search_results["results"][0]["trackNumber"]
    genre = search_results["results"][0]["primaryGenreName"]
    return(artist, title, album, year, artwork, track_number, genre)


def tag(file_path, artist, title, album, year, artwork, track_number, genre):
    audio_file = ID3(file_path)
    audio_file.add(TPE1(encoding=3, text=artist))
    audio_file.add(TIT2(encoding=3, text=title))
    audio_file.add(TALB(encoding=3, text=album))
    audio_file.add(TDRC(encoding=3, text=year))
    audio_file.add(TRCK(encoding=3, text=str(track_number)))
    audio_file.add(TCON(encoding=3, text=genre))
    artwork_url = urlopen(artwork)
    audio_file.add(APIC(
                        encoding=3,
                        mime="image/jpeg",
                        type=3, desc=u"Cover",
                        data=artwork_url.read()
    ))
    audio_file.save()
