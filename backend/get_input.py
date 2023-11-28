import sys
import csv
import os
from io import StringIO
from time import sleep

def create_feature_list():
    dict_list = []

    #Create key:value pairs of possible descriptors and their matching
    #attribute names as used by the Spotify API
    danceability = {'dancy': ['min_danceability', .8],
                    'groovy': ['min_danceability', .8],
                    'rhythmic': ['min_danceability', .8],
                    'danceable': ['min_danceability', .8]}
    dict_list.append(danceability)

    duration = {'long': ['min_duration', 240000],
                'short': ['max_duration', 180000]}
    dict_list.append(duration)

    energy = {'energetic': ['min_energy', .8],
            'lively': ['min_energy', .7], 
            'intense': ['min_energy', .8],
            'low-energy': ['max_energy', .5]}
    dict_list.append(energy)

    instrumentalness = {'instrumental':['min_instrumentalness', .7],
                        'lyric-less':['min_instrumentalness', .7]}
    dict_list.append(instrumentalness)

    liveness = {'live': ['min_liveness', .8],
                'raw': ['min_liveness', .8]}
    dict_list.append(liveness)

    loudness = {'loud': ['min_loudness', -10],
                'quiet': ['max_loudness', -20],
                'soft': ['max_loudness', -20]}
    dict_list.append(loudness)

    mode = {'major': ['mode', 1],
            'minor': ['mode', 0]}
    dict_list.append(mode)

    popularity = {'popular': ['min_popularity', 90],
                'trending': ['min_popularity', 90],
                'underground': ['max_popularity', 50]}
    dict_list.append(popularity)

    speechiness = {'spoken-word': ['min_speechiness', .7],
                'lyrical': ['min_speechiness', .5],
                'vocal': ['min_speechiness', .5]}
    dict_list.append(speechiness)

    tempo = {'fast': ['min_tempo', 120], 
            'slow': ['max_tempo', 80], 
            'uptempo': ['min_tempo', 120],
            'downtempo': ['max_tempo', 70]}
    dict_list.append(tempo)

    valence = {'happy': ['min_valence', .7],
            'sad': ['max_valence', .5],
            'upbeat': ['max_valence', .7]}
    dict_list.append(valence)

    return dict_list

def create_genre_list():

    genres = ["acoustic", "afrobeat", "alt-rock", "alternative", "ambient", 
            "anime", "black-metal", "bluegrass", "blues", "bossanova", 
            "brazil", "breakbeat", "british", "cantopop", "chicago-house", 
            "children", "chill", "classical", "club", "comedy", "country", 
            "dance", "dancehall", "death-metal", "deep-house", "detroit-techno", 
            "disco", "disney", "drum-and-bass", "dub", "dubstep", "edm", 
            "electro", "electronic", "emo", "folk", "forro", "french", 
            "funk", "garage", "german", "gospel", "goth", "grindcore", 
            "groove", "grunge", "guitar", "hard-rock", "hardcore", 
            "hardstyle", "heavy-metal", "hip-hop", "holidays", "honky-tonk", 
            "house", "idm", "indian", "indie", "indie-pop", "industrial", 
            "iranian", "j-dance", "j-idol", "j-pop", "j-rock", "jazz", 
            "k-pop", "kids", "latin", "latino", "malay", "mandopop", 
            "metal", "metal-misc", "metalcore", "minimal-techno", 
            "movies", "mpb", "new-age", "new-release", "opera", "pagode", 
            "party", "philippines-opm", "piano", "pop", "pop-film", 
            "post-dubstep", "power-pop", "progressive-house", "psych-rock", 
            "punk", "punk-rock", "r-n-b", "rainy-day", "reggae", 
            "reggaeton", "road-trip", "rock", "rock-n-roll", "rockabilly", 
            "romance", "salsa", "samba", "sertanejo", 
            "show-tunes", "singer-songwriter", "ska", "sleep", 
            "songwriter", "soul", "soundtracks", "spanish", "study", 
            "summer", "swedish", "synth-pop", "tango", "techno", "trance", 
            "trip-hop", "turkish", "work-out", "world-music"]
    
    return genres

def create_key_list():

    key_list = ['a', 'bb', 'c', 'c#', 'd', 'eb', 'e',
            'f', 'f#', 'g', 'g#']
    
    return key_list

def process_string(value):
    value = value.lower()

    # Check if the string contains 'from the' or 'by'
    if 'from' not in value and 'by' not in value and 'like' not in value:
        # Replace spaces with hyphens
        return value.replace(' ', '-')
    else:
        return value
    
def clean_input(input):

    csv_file = StringIO(input)
    reader = csv.reader(csv_file)
    #convert string of comma-separated values into list, remove spaces
    result_list = [process_string(element.strip()) for element in next(reader, [])]

    return result_list

def get_misc_features(term, trait_dict, dict_list):
    for dict in dict_list:
        for key in dict.keys():
            if term == key:
                pair = dict[key]
                trait_dict[pair[0]] = pair[1]

def get_genre(term, trait_dict, genres):
    for genre in genres:
        if term == genre:
            trait_dict['genre'] = term

def get_artist(term, trait_dict):
    if "by " in term:
        trait_dict['artist'] = term.replace("by ", "")

def get_similar_artist(term, trait_dict):
    if "like " in term:
        trait_dict['seed_artists'] = term.replace("like ", "")

def get_target_bpm(term, trait_dict):
    if "-bpm" in term:
        term = term.replace("-", " ")
        trait_dict['tempo'] = term.replace(" bpm", "")

def get_key(term, trait_dict, key_list):
    if "major" in term or "minor" in term:
       for key in key_list:
           if key in term:
               trait_dict['key'] = (key_list.index(key) + 1)

def get_time_signature(term, trait_dict):
    if "/4" in term:
        term = term.replace("-", " ")
        term = term.replace("/4", "")
        trait_dict['time-signature'] = term.replace("in ", "")

def get_features(clean_input):
    
    trait_dict = {}
    dict_list = create_feature_list()

    genres = create_genre_list()
    key_list = create_key_list()

    for term in clean_input:
        get_genre(term, trait_dict, genres)
        get_artist(term, trait_dict)
        get_similar_artist(term, trait_dict)
        get_target_bpm(term, trait_dict)
        get_key(term, trait_dict, key_list)
        get_time_signature(term, trait_dict)
        get_misc_features(term, trait_dict, dict_list)

    return trait_dict



def process_input(user_input):

    trait_dict = {}
    search_flag = True

    # params_test = {
    #     'seed_artists': 'carly rae jepsen',
    #     'type': 'track',
    #     'limit': 10,
    #     'min_tempo': 120,
    #     'max_valence': .7,
    #     'genre': 'hardcore'
    # }

    # params_test = {
    #     'min_valence': 0.7,
    #     'artist': 'arctic monkeys',
    #     'type': 'track',
    #     'limit': 30
    # }

    cleaned = clean_input(user_input)

    trait_dict = get_features(cleaned)
    trait_dict['type'] = 'track'
    trait_dict['limit'] = 50

    if 'seed_artists' in trait_dict.keys() or 'seed_genres' in trait_dict.keys():
        search_flag = False

    #Print parameters to other file
    
    temp_file_path = 'backend/temp_params.py'
    with open(temp_file_path, 'w') as f:
        f.write('params = ')
        f.write(f'{trait_dict}')
        f.flush()
        f.close()

    os.rename(temp_file_path, 'backend/params.py')

    print(f"Python script executed with user input: {trait_dict}")

    return search_flag