import sys

# Adjust the paths according to your project structure
sys.path.append('path/to/spotify_search')
sys.path.append('path/to/spotify_recommendations')
sys.path.append('path/to/make_embeddings')

from params import params
from spotify_search import run_spotify_search
from spotify_recommendations import run_spotify_recommendations
from make_embeddings import write_html_with_embeds
from get_input import process_input

def main():

    user_input = sys.argv[1] if len(sys.argv) > 1 else "No input provided"
    #If input specifies artist or genre, returns true
    use_search = process_input(user_input)
    

    # Examples
    search_params = {
        'artist': 'the smiths',
        'type': 'track',
        'limit': 10,
        'min_tempo': 120,
    }

    recommendation_params = {
        'seed_genres': 'classical',
        'limit': 5,
    }

    if not use_search:
        track_urls = run_spotify_recommendations(params)
    else:
        track_urls = run_spotify_search(params)

    # Generate HTML with embeddings
    output_html_file = 'frontend/public/spotify_tracks.html'
    write_html_with_embeds(track_urls, output_html_file)

    print(f"HTML file with Spotify tracks generated: {output_html_file}")

if __name__ == '__main__':
    main()
