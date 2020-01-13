from acoustid import match
from itertools import groupby
import requests


def acoustid_match(api_key, file_path):
    match_count = 0
    possible_matches = []
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
    return(artist, title, album, year, artwork)
