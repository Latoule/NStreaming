from flask import Flask, render_template
import requests
from to_json import json_to_ls, info_json, nb_episodes, BA, get_genres, get_id, search
from flask import request

app = Flask(__name__)

frembed_url= "https://pastebin.com/raw/KSuWET4Q"
frembed_url= requests.get(frembed_url).text

api_token= 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzNTI4Y2Q2Zjk3OGM1ZGMzMmE1ZDIwOGJmOWY1NTJiMCIsIm5iZiI6MTc2MTA0OTkwOS44MjUsInN1YiI6IjY4Zjc3ZDM1ZjM5ODJjOGZkZTNhMzk2MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.T-TEqoxpBq-QWj94GVOVJ_EMlsHP3cGAvJBTw5IZXTw'
BASE_IMG_URL = "https://image.tmdb.org/t/p/w200"

@app.route('/')
def home():
    return render_template('index.html', rated_movies=json_to_ls(api_token, "https://api.themoviedb.org/3/movie/top_rated?language=fr-FR"), 
    trending_movies=json_to_ls(api_token, "https://api.themoviedb.org/3/trending/movie/day?language=fr-FR"), base_img_url=BASE_IMG_URL, 
    trending_tv=json_to_ls(api_token, "https://api.themoviedb.org/3/trending/tv/day?language=fr-FR"), 
    rated_tv=json_to_ls(api_token, "https://api.themoviedb.org/3/tv/top_rated?language=fr-FR"))


@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=fr-FR"
    movie = info_json(api_token, url)

    return render_template('movie_page.html', movie=movie, base_img_url=BASE_IMG_URL, frembed_url=frembed_url, 
    BA=BA(api_token, f'https://api.themoviedb.org/3/movie/{movie_id}/videos?language=fr-FR'))

@app.route('/tv/<int:tv_id>/s<int:season>/ep<int:episode>')
def tv_detail(tv_id, season, episode):
    url= f"https://api.themoviedb.org/3/tv/{tv_id}?language=fr-FR"
    tv= info_json(api_token, url)
    return render_template('tv_page.html', movie=tv, base_img_url=BASE_IMG_URL, current_episode=episode, 
    nb_episodes=range(nb_episodes(api_token, f"https://api.themoviedb.org/3/tv/{tv_id}/season/{season}?language=fr-FR")), 
    seasons=range(tv['nb_season']), season=season, BA=BA(api_token, f'https://api.themoviedb.org/3/tv/{tv_id}/videos?language=fr-FR'), frembed_url=frembed_url  )

@app.route('/movie/p/<int:nb_page>')
def movie(nb_page):
    return render_template('movie_index.html', rated_movies=json_to_ls(api_token, f'https://api.themoviedb.org/3/movie/top_rated?language=fr-FR&page={nb_page}'), 
    trending_movies=json_to_ls(api_token, f'https://api.themoviedb.org/3/trending/movie/day?language=fr-FR&page={nb_page}'), base_img_url=BASE_IMG_URL,  
    genres= get_genres(api_token, f'https://api.themoviedb.org/3/genre/movie/list?language=fr&page={nb_page}')['genres'], 
    nb_page=nb_page)

@app.route('/movie/genre/<genre>/p/<int:nb_page>')
def genre_movie(genre, nb_page):
    genres= get_genres(api_token, "https://api.themoviedb.org/3/genre/movie/list?language=fr")['genres']
    id = get_id(genre, genres)
    return render_template('genre_movie.html', genre=genre, genre_id=id, nb_page=nb_page, 
    search_resultmovie=json_to_ls(api_token, f'https://api.themoviedb.org/3/discover/movie?with_genres={id}&language=fr-FR&page={nb_page}'), base_img_url=BASE_IMG_URL,
    genres= get_genres(api_token, "https://api.themoviedb.org/3/genre/movie/list?language=fr")['genres'])


@app.route('/search')
def search_media():
    query = request.args.get('q', '')
    return render_template('search.html', query=query, base_img_url=BASE_IMG_URL, 
                           search_resultmovie=search(api_token, f'https://api.themoviedb.org/3/search/movie?query={query}&language=fr-FR'), 
                            search_resulttv=search(api_token, f'https://api.themoviedb.org/3/search/tv?query={query}&language=fr-FR') )

@app.route('/tv/p/<int:nb_page>')
def tv(nb_page):
    return render_template('tv_index.html', trending_tv=json_to_ls(api_token, f'https://api.themoviedb.org/3/trending/tv/day?language=fr-FR&page={nb_page}'), 
    rated_tv=json_to_ls(api_token, f'https://api.themoviedb.org/3/tv/top_rated?language=fr-FR&page={nb_page}'), base_img_url=BASE_IMG_URL,
    genres= get_genres(api_token, f'https://api.themoviedb.org/3/genre/tv/list?language=fr&page={nb_page}')['genres'], 
    nb_page=nb_page)

@app.route('/tv/genre/<genre>/p/<int:nb_page>')
def genre_tv(genre, nb_page):
    genres= get_genres(api_token, "https://api.themoviedb.org/3/genre/tv/list?language=fr")['genres']
    id = get_id(genre, genres)
    return render_template('genre_tv.html', genre=genre, genre_id=id, 
    genres= genres, search_resulttv= json_to_ls(api_token, f'https://api.themoviedb.org/3/discover/tv?with_genres={id}&language=fr-FR&page={nb_page}'), base_img_url=BASE_IMG_URL, nb_page=nb_page)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
