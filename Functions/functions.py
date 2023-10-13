Functions:

"""Create artists songs list"""

import re

artists = []
for elem in soup.select("div.o-chart-results-list-row-container li.lrv-u-width-100p"):
    text = elem.select("span")[0].get_text().replace("\n","").replace("\t","")
    artists.append(text)
    
artists= [elem for elem in [artist for artist in artists if artist.isdigit() == False] if elem != "-"]

""" Search song Function"""

def search_song1(df: pd.DataFrame, limit=1)-> pd.DataFrame:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                           client_secret=client_secret))
    chunks = np.array_split(df, 50)
    chunks_ids = []
    for index, chunk in enumerate(chunks):
        print("Collecting IDs for chunk...",index)
        for index, row in chunk.iterrows():
            try:
                title, artist = row['Title'], row['Artist']  # Get title and artist from row
                query = "tracks: " + f"{title}" + "artist: " + f"{artist}"
                results = sp.search(q=query, limit=limit)
                track_id = results['tracks']['items'][0]['id']
                chunks_ids.append(track_id) 
            except Exception as e:
                print(f"Song not found for Title: {title}, Artist: {artist}")
                print(f"Error occurred: {e}")
                chunks_ids.append("None")
        time.sleep(20)
    return pd.DataFrame(chunks_ids, columns=['track_id'])

    """ Audio features function"""

    def get_audio_features(track_ids):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
    
    chunks = np.array_split(track_ids, 50)  # Split track_ids into chunks
    audio_features = []
    for index, chunk in enumerate(chunks):
        print(f"Collecting audio features for Chunk: {index}")
        list_of_ids = chunk.tolist()
        features = sp.audio_features(list_of_ids)
        audio_features += features
            # Introduce a time delay between requests to avoid rate limiting
        time.sleep(20)
    return pd.DataFrame(audio_features)