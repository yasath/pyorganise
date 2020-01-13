from acoustid import match
from itertools import groupby


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
    return(matched)
