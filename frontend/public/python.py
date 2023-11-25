import sys
import csv
from io import StringIO

def process_string(value):
    value = value.lower()

    # Check if the string contains 'from the' or 'by'
    if 'from' not in value and 'by' not in value:
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

dict_list = []

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
            'quiet': ['max_loudness', -40],
            'soft': ['max_loudness', -40]}
dict_list.append(loudness)

mode = {'major': ['mode', 1],
        'minor': ['mode', 0]}
dict_list.append(mode)

popularity = {'popular': ['min_popularity', 90],
            'trending': ['min_popularity', 90],
            'underground': ['min_popularity', 30]}
dict_list.append(popularity)

speechiness = {'spoken-word': ['min_speechiness', .7],
             'lyrical': ['min_speechiness', .5],
              'vocal': ['min_speechiness', .5]}
dict_list.append(speechiness)

tempo = {'fast': ['min_tempo', 120], 
         'slow': ['max_tempo', 70], 
         'uptempo': ['min_tempo', 120],
         'downtempo': ['max_tempo', 70]}
dict_list.append(tempo)

valence = {'happy': ['min_valence', .7],
           'sad': ['max_valence', .4],
           'upbeat': ['max_valence', .7]}
dict_list.append(valence)

#list of keys
key_list = ['a', 'bb', 'c', 'c#', 'd', 'eb', 'e',
            'f', 'f#', 'g', 'g#']

#create dict to store key/value pairs
trait_dict = {}

def get_misc_features(term):
    for dict in dict_list:
        for key in dict.keys():
            if term == key:
                pair = dict[key]
                trait_dict[pair[0]] = pair[1]

def get_genre(term):
    for genre in genres:
        if term == genre:
            trait_dict['genre'] = term

def get_artist(term):
    if "by " in term:
        trait_dict['artist'] = term.replace("by ", "")

def get_target_bpm(term):
    if "-bpm" in term:
        term = term.replace("-", " ")
        trait_dict['target_bpm'] = term.replace(" bpm", "")

def get_key(term):
    if "major" in term or "minor" in term:
       for key in key_list:
           if key in term:
               trait_dict['key'] = (key_list.index(key) + 1)

def get_time_signature(term):
    if "/4" in term:
        term = term.replace("-", " ")
        term = term.replace("/4", "")
        trait_dict['time-signature'] = term.replace("in ", "")


# Get user input from command line arguments
user_input = sys.argv[1] if len(sys.argv) > 1 else "No input provided"

#Clean user input into csv
user_input = clean_input(user_input)

for term in user_input:
    get_genre(term)
    get_artist(term)
    get_target_bpm(term)
    get_key(term)
    get_time_signature(term)
    get_misc_features(term)

# Print a message using the user input
print(f"Python script executed with user input: {trait_dict}")
