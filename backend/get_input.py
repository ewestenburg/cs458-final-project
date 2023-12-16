import sys
import csv
import os
from io import StringIO
from time import sleep

def create_feature_list():
    dict_list = []

    #Create key:value pairs of possible descriptors and their matching
    #attribute names as used by the Spotify API
    danceability = {
        'dancy': ['min_danceability', .8],
        'groovy': ['min_danceability', .8],
        'rhythmic': ['min_danceability', .8],
        'danceable': ['min_danceability', .8],
        'funky': ['min_danceability', .8],
        'jiving': ['min_danceability', .8],
        'swaying': ['min_danceability', .8],
        'bouncy': ['min_danceability', .8],
        'dynamic': ['min_danceability', .8],
        'fluid': ['min_danceability', .8],
        'lethargic': ['max_danceability', .2],
        'static': ['max_danceability', .2],
        'stiff': ['max_danceability', .2],
        'rigid': ['max_danceability', .2],
        'lit': ['min_danceability', .8],
        'vibey': ['max_danceability', .6],
        'clubby': ['min_danceability', .8],
        'uptight': ['max_danceability', .2],
        'awkward': ['max_danceability', .2],
        'clunky': ['max_danceability', .2],
        'immobile': ['max_danceability', .2],
        'lit': ['min_danceability', .8],
        'chill': ['max_danceability', .3],
        'vibey': ['max_danceability', .6],
        'edgy': ['min_danceability', .8],
        'hype': ['min_danceability', .7],
        'mellow': ['max_danceability', .3],
        'smooth': ['min_danceability', .8],
        'stiff': ['max_danceability', .2],
        'jamming': ['min_danceability', .8],
        'lazy': ['max_danceability', .2],
        'bopping': ['min_danceability', .8],
        'immobile': ['max_danceability', .1]
    }
    dict_list.append(danceability)

    duration = {
        'long': ['min_duration', 240000],
        'short': ['max_duration', 180000],
        'extended': ['min_duration', 300000],
        'brief': ['max_duration', 120000],
        'lengthy': ['min_duration', 270000],
        'compact': ['max_duration', 150000],
        'prolonged': ['min_duration', 320000],
        'fleeting': ['max_duration', 100000],
        'enduring': ['min_duration', 350000],
        'momentary': ['max_duration', 90000],
        'ephemeral': ['max_duration', 80000],
        'transient': ['max_duration', 70000],
        'marathon': ['min_duration', 400000],
        'snippet': ['max_duration', 60000],
        'epic': ['min_duration', 360000],
        'blip': ['max_duration', 50000],
        'sizable': ['min_duration', 280000],
        'quickie': ['max_duration', 90000],
        'lasting': ['min_duration', 340000]
    }
    dict_list.append(duration)

    energy = {
        'energetic': ['min_energy', .8],
        'lively': ['min_energy', .7], 
        'intense': ['min_energy', .8],
        'low-energy': ['max_energy', .5],
        'vigorous': ['min_energy', .8],
        'powerful': ['min_energy', .8],
        'dynamic': ['min_energy', .8],
        'spirited': ['min_energy', .8],
        'passive': ['max_energy', .3],
        'mellow': ['max_energy', .4],
        'relaxed': ['max_energy', .3],
        'subdued': ['max_energy', .3],
        'lethargic': ['max_energy', .2],
        'amped': ['min_energy', .8],
        'chill': ['max_energy', .3],
        'explosive': ['min_energy', .9],
        'calm': ['max_energy', .2],
        'fiery': ['min_energy', .8],
        'serene': ['max_energy', .2],
        'wild': ['min_energy', .9],
        'gentle': ['max_energy', .3],
        'raucous': ['min_energy', .9],
        'peaceful': ['max_energy', .2],
        'pumped': ['min_energy', .8],
        'chilled': ['max_energy', .3],
        'thrilling': ['min_energy', .9],
        'calm': ['max_energy', .2],
        'banging': ['min_energy', .9],
        'serene': ['max_energy', .2],
        'fiery': ['min_energy', .9],
        'soothing': ['max_energy', .3],
        'electric': ['min_energy', .9],
        'zen': ['max_energy', .2],
        'kinetic': ['min_energy', .8],
        'tranquil': ['max_energy', .2]
    }
    dict_list.append(energy)

    instrumentalness = {
        'instrumental':['min_instrumentalness', .7],
        'lyric-less':['min_instrumentalness', .7],
        'non-vocal': ['min_instrumentalness', .7],
        'accompaniment': ['min_instrumentalness', .7],
        'melodic': ['min_instrumentalness', .7],
        'harmonic': ['min_instrumentalness', .7],
        'vocal': ['max_instrumentalness', .3],
        'sung': ['max_instrumentalness', .3],
        'lyrical': ['max_instrumentalness', .3],
        'voiced': ['max_instrumentalness', .3],
        'choral': ['max_instrumentalness', .3],
        'backing': ['min_instrumentalness', .7],
        'acapella': ['max_instrumentalness', .1],
        'symphonic': ['min_instrumentalness', .8],
        'vocal-heavy': ['max_instrumentalness', .2],
        'orchestral': ['min_instrumentalness', .8],
        'songful': ['max_instrumentalness', .2],
        'beatless': ['min_instrumentalness', .8],
        'sing-along': ['max_instrumentalness', .1],
        'rhythmless': ['min_instrumentalness', .8],
        'wordy': ['max_instrumentalness', .1]
    }
    dict_list.append(instrumentalness)

    liveness = {
        'live': ['min_liveness', .8],
        'raw': ['min_liveness', .8],
        'concert': ['min_liveness', .8],
        'gig': ['min_liveness', .8],
        'stage': ['min_liveness', .8],
        'real': ['min_liveness', .8],
        'studio': ['max_liveness', .2],
        'produced': ['max_liveness', .2],
        'synthesized': ['max_liveness', .2],
        'programmed': ['max_liveness', .2],
        'artificial': ['max_liveness', .2]
    }
    dict_list.append(liveness)

    loudness = {
        'loud': ['min_loudness', -10],
        'quiet': ['max_loudness', -20],
        'soft': ['max_loudness', -20],
        'booming': ['min_loudness', -5],
        'thunderous': ['min_loudness', -5],
        'deafening': ['min_loudness', -5],
        'muffled': ['max_loudness', -25],
        'hushed': ['max_loudness', -30],
        'whispered': ['max_loudness', -30],
        'faint': ['max_loudness', -35],
        'inaudible': ['max_loudness', -40],
        'blasting': ['min_loudness', -3],
        'murmuring': ['max_loudness', -40],
        'roaring': ['min_loudness', -4],
        'whispering': ['max_loudness', -35],
        'thumping': ['min_loudness', -6],
        'muted': ['max_loudness', -30],
        'ear-splitting': ['min_loudness', -2],
        'silenced': ['max_loudness', -45],
        'resounding': ['min_loudness', -5],
        'soundless': ['max_loudness', -50]
    }
    dict_list.append(loudness)

    mode = {'major': ['mode', 1],
            'minor': ['mode', 0]}
    dict_list.append(mode)

    popularity = {
        'popular': ['min_popularity', 80],
        'trending': ['min_popularity', 90],
        'underground': ['max_popularity', 25],
        'famous': ['min_popularity', 85],
        'obscure': ['max_popularity', 40],
        'well-known': ['min_popularity', 85],
        'unknown': ['max_popularity', 15],
        'noted': ['min_popularity', 80],
        'unrecognized': ['max_popularity', 35],
        'mainstream': ['min_popularity', 80],
        'niche': ['max_popularity', 45],
        'hit': ['min_popularity', 95],
        'obscure': ['max_popularity', 20],
        'chart-topper': ['min_popularity', 90],
        'undiscovered': ['max_popularity', 10],
        'famous': ['min_popularity', 85],
        'hidden-gem': ['max_popularity', 25],
        'blockbuster': ['min_popularity', 90],
        'rare': ['max_popularity', 15],
        'hot': ['min_popularity', 95],
        'unheard': ['max_popularity', 10]
    }
    dict_list.append(popularity)

    speechiness = {
        'spoken-word': ['min_speechiness', .7],
        'lyrical': ['min_speechiness', .5],
        'vocal': ['min_speechiness', .5],
        'talkative': ['min_speechiness', .7],
        'narrative': ['min_speechiness', .6],
        'conversational': ['min_speechiness', .7],
        'eloquent': ['min_speechiness', .5],
        'chatty': ['min_speechiness', .7],
        'musical': ['max_speechiness', .3],
        'instrumental': ['max_speechiness', .2],
        'melodic': ['max_speechiness', .3]
    }
    dict_list.append(speechiness)

    tempo = {
        'fast': ['min_tempo', 120],
        'slow': ['max_tempo', 80],
        'uptempo': ['min_tempo', 120],
        'downtempo': ['max_tempo', 70],
        'brisk': ['min_tempo', 130],
        'leisurely': ['max_tempo', 60],
        'rapid': ['min_tempo', 140],
        'languid': ['max_tempo', 50],
        'speedy': ['min_tempo', 150],
        'sluggish': ['max_tempo', 55],
        'quick': ['min_tempo', 135],
        'snail-paced': ['max_tempo', 45],
        'blazing': ['min_tempo', 160],
        'snail-like': ['max_tempo', 40],
        'hurried': ['min_tempo', 145],
        'plodding': ['max_tempo', 50],
        'rushed': ['min_tempo', 155],
        'strolling': ['max_tempo', 55],
        'breakneck': ['min_tempo', 150],
        'crawling': ['max_tempo', 45],
        'sprinting': ['min_tempo', 165],
        'ambling': ['max_tempo', 60]
    }
    dict_list.append(tempo)

    valence = {
        'happy': ['min_valence', .7],
        'sad': ['max_valence', .5],
        'upbeat': ['min_valence', .7],
        'joyous': ['min_valence', .7],
        'sorrowful': ['max_valence', .3],
        'cheerful': ['min_valence', .7],
        'melancholy': ['max_valence', .4],
        'gleeful': ['min_valence', .7],
        'gloomy': ['max_valence', .3],
        'elated': ['min_valence', .8],
        'depressed': ['max_valence', .2],
        'ecstatic': ['min_valence', .8],
        'dismal': ['max_valence', .2],
        'radiant': ['min_valence', .7],
        'mournful': ['max_valence', .3],
        'delighted': ['min_valence', .7],
        'heavy-hearted': ['max_valence', .2],
        'jubilant': ['min_valence', .8],
        'blue': ['max_valence', .3],
        'exhilarated': ['min_valence', .8],
        'woeful': ['max_valence', .2],
        'blissful': ['min_valence', .7],
        'downcast': ['max_valence', .2],
        'contented': ['min_valence', .7],
        'forlorn': ['max_valence', .2],
        'vibrant': ['min_valence', .7],
        'desolate': ['max_valence', .1],
        'optimistic': ['min_valence', .7],
        'pessimistic': ['max_valence', .2],
        'lighthearted': ['min_valence', .8],
        'heartbroken': ['max_valence', .1],
        'bubbly': ['min_valence', .8],
        'sullen': ['max_valence', .2],
        'sunny': ['min_valence', .7],
        'somber': ['max_valence', .3],
        'exuberant': ['min_valence', .8],
        'morose': ['max_valence', .2],
        'spirited': ['min_valence', .7],
        'doleful': ['max_valence', .3],
        'euphoric': ['min_valence', .8],
        'bleak': ['max_valence', .1],
        'chipper': ['min_valence', .7],
        'miserable': ['max_valence', .2],
        'buoyant': ['min_valence', .8],
        'lugubrious': ['max_valence', .1],
        'jolly': ['min_valence', .7],
        'glum': ['max_valence', .2],
        'beaming': ['min_valence', .8],
        'crestfallen': ['max_valence', .1],
        'mirthful': ['min_valence', .8],
        'despondent': ['max_valence', .2],
        'cheery': ['min_valence', .7],
        'moody': ['max_valence', .2],
        'sunny': ['min_valence', .8],
        'brooding': ['max_valence', .2],
        'uplifting': ['min_valence', .8],
        'gloomy': ['max_valence', .2],
        'sparkly': ['min_valence', .8],
        'sombre': ['max_valence', .2],
        'bright': ['min_valence', .7],
        'morose': ['max_valence', .3],
        'jolly': ['min_valence', .7],
        'melancholic': ['max_valence', .2],
        'joyful': ['min_valence', .8],
        'downbeat': ['max_valence', .3],
        'playful': ['min_valence', .7],
        'somber': ['max_valence', .2],
        'hopeful': ['min_valence', .7],
        'dreary': ['max_valence', .3],
        'peppy': ['min_valence', .8],
        'bleak': ['max_valence', .1]
    }
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
    final_file_path = 'backend/params.py'

    # Write the trait dictionary to a temporary file
    with open(temp_file_path, 'w') as f:
        f.write('params = ')
        f.write(f'{trait_dict}')
        f.flush()
        f.close()

    # Delete the existing params.py file if it exists
    if os.path.exists(final_file_path):
        os.remove(final_file_path)

    # Rename the temp file to params.py
    os.rename(temp_file_path, final_file_path)

    print(f"Python script executed with user input: {trait_dict}")

    return search_flag