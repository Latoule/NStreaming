import requests
import unicodedata

def BA(api_token, url):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    result = response.json()
    if result.get('results') and len(result['results']) > 0:
        video_key = result['results'][0]['key']
        video = f'https://www.youtube.com/embed/{video_key}'
        return video
    else:
        return None

def no_accents(text):
    if not text:
        return None
    no_accents = ''.join(
    c for c in unicodedata.normalize('NFD', text)
    if unicodedata.category(c) != 'Mn'
    )
    return no_accents

def json_to_ls(api_token, url):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    result = response.json()
    
    movies_list = []
    for movie in result.get("results", []):
        if movie.get('name'):
            title = no_accents(movie.get('name'))
        else:
            title = no_accents(movie.get('title'))
        if title and movie.get('overview') and movie.get('poster_path'):
            movies_list.append({
                "title": title,
                "poster_path": movie.get("poster_path"),
                "id": movie.get("id")
            })

    return movies_list

def info_json(api_token, url):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    result = response.json()
    
    if result.get('name'):  
        media_type = 'tv'
        title = no_accents(result.get('name'))
        nb_season = result.get('number_of_seasons')
    else:
        media_type = 'movie'
        title = no_accents(result.get('title'))
        nb_season= None
    title= no_accents(title)
    movie_param = {'id': result.get('id'), 'title': title, 
    'type': media_type, 'overview': no_accents(result.get('overview')), 
    'poster_path': result.get('poster_path'), 'nb_season': nb_season}

    return movie_param


def nb_episodes(api_token, url):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    result = response.json()
    nb_episodes=len(result["episodes"])

    return nb_episodes



def get_genres(api_token, url):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    result = response.json()

    for i in result['genres']:
        i['name'] = no_accents(i['name'])
    
    return result



def get_id(x, list):
    index= next((i for i, genre in enumerate(list) if genre['name'] == x), None)
    return list[index]['id']

def search(api_token, url):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    result = response.json().get("results", [])

    movies_list = []
    for movie in result:
        if movie.get('name'):  
            media_type = 'tv'
            title = no_accents(movie.get('name'))
        else:
            media_type = 'movie'
            title = no_accents(movie.get('title'))

        if title and movie.get('overview') and movie.get('poster_path') and (BA(api_token, f'https://api.themoviedb.org/3/movie/{movie.get('id')}/videos?language=fr-FR') or 
                                                                             BA(api_token, f'https://api.themoviedb.org/3/tv/{movie.get('id')}/videos?language=fr-FR')):
            movies_list.append({
                "title": title,
                "media_type": media_type,
                "poster_path": movie.get("poster_path"),
                "id": movie.get("id")
            })

    return movies_list
