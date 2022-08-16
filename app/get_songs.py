
import random
import json
import requests
from .oauth import get_access_token
from .config import settings
from trainer import detect




def get_song():


    emotion = {
    'Happy':settings.happy_playlist_id,
    'Sad':settings.sad_playlist_id,
    'Neutral':settings.neutral_playlist_id}


    results = detect.detect()

    cls = results['class']
    confidence = results['confidence'][-1]
    playlist_id = emotion[cls[-1]]
    image = results['image'][-1]

    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    PARAMS = 'items(added_by.id,track(name,href,album(name,href)))'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {get_access_token()}'}
    
    response = requests.get(url=url,params=PARAMS, headers=headers)
    response_dict = json.loads(response.text)

    
    num_songs = len(response_dict['items'])
    songs_list = response_dict['items']
    music_id = random.randint(0, num_songs-1)

    song_item = songs_list[music_id]
    
    song = {'music_id':music_id,
            'music_title':song_item['track']['name'],
            'music_link':song_item['track']['href'],
            'class_of_emotion':cls[-1],
            'confidence(%)':confidence,
            'image':image}



    return song


"""def play_song():


    BODY = {'context_url':'https://api.spotify.com/v1/tracks/7CIa25JJTGo1JvehNLIqFj'}
    print(requests.put('https://api.spotify.com/v1/me/player/play',data=BODY, headers=headers).reason)

#print(get_song())
"""
