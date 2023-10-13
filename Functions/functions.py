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

def song_recommender():
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                               client_secret=client_secret))
    song_title = input("What song title did you like listening to recently the most: ")
    song_artist = input("From which artist? ")
    query = "tracks: " + f"{song_title}" + " artist: " + f"{song_artist}"
    results = sp.search(q=query, limit=5)
    
    songs_dict = {"Artist": [], "Title": [], "id": []}
    for item in results['tracks']['items']:
        songs_dict['Title'].append(item['name'])
        songs_dict['Artist'].append(item['artists'][0]['name'])
        songs_dict['id'].append(item['id'])
    
    songs_df = pd.DataFrame(songs_dict)
    
    display(songs_df[["Artist", "Title"]])
    
    correct_song_index = int(input("Select the right song index: "))
    track_id = songs_df.iloc[correct_song_index, -1]

    list_of_ids = [track_id]
    user_song_audio_features = sp.audio_features(list_of_ids)
    user_song_audio_features_df = pd.DataFrame(user_song_audio_features)

    # Assuming 'user_song_audio_features' is a list of dictionaries
    user_song_audio_features_df = pd.DataFrame(user_song_audio_features)

# Filter out non-numeric columns
    numeric_columns = user_song_audio_features_df.select_dtypes(include=[np.number]).columns
    user_song_audio_features_df_numeric = user_song_audio_features_df[numeric_columns]

# Scale the numeric features
    user_song_audio_features_scaled_np = scaler.transform(user_song_audio_features_df_numeric)
    user_song_audio_features_scaled_df = pd.DataFrame(user_song_audio_features_scaled_np,
                                                  columns=user_song_audio_features_df_numeric.columns,
                                                  index=user_song_audio_features_df_numeric.index)


    user_song_tsne_features_np = tsne.embedding_
    user_song_tsne_features_df = pd.DataFrame(user_song_tsne_features_np, columns=["TSNE_1", "TSNE_2"])
    user_song_cluster = kmeans.predict(user_song_tsne_features_df)
    
    if track_id in concat_nhs_hs[concat_nhs_hs['Hot'] == "Y"]['id'].values:
        cpu_songs = concat_nhs_hs[(concat_nhs_hs['Hot'] == "Y")].sample(5)
        print("Nice!This is hot song. You will probably love listening to this popular songs as well:")
        display(cpu_songs[['Artist', 'Title']])
    else:
        cpu_songs = concat_nhs_hs[concat_nhs_hs['Hot'] == "N"].sample(5)
        print("Nice!This is not hot song You will probably love listening to these other songs as well:")
        display(cpu_songs[['Artist', 'Title']])