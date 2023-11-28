import requests

def get_oembed_code(track_url):
    oembed_url = 'https://open.spotify.com/oembed'
    params = {'url': track_url}
    response = requests.get(oembed_url, params=params)
    if response.status_code == 200:
        return response.json()['html']
    else:
        raise Exception(f"Error fetching oEmbed code: {response.text}")

def write_html_with_embeds(track_urls, output_file):
    html_content = '<html><head><title>Spotify Tracks</title></head><body>'

    for url in track_urls:
        embed_code = get_oembed_code(url)
        html_content += embed_code + '<br>'  # Adding a line break for spacing

    html_content += '</body></html>'

    with open(output_file, 'w') as file:
        file.write(html_content)

# Example usage
track_urls = [
    'https://open.spotify.com/track/5rJqv6nBKQQrFPY2B4pZib',
    'https://open.spotify.com/track/69yfbpvmkIaB10msnKT7Q5',
]

output_html_file = 'frontend/public/spotify_tracks.html'
write_html_with_embeds(track_urls, output_html_file)
