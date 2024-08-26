import requests
import json
def movie_data_from_tmdb(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?query={movie_name}&include_adult=false&language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlMjBjMGRlMTU4ZTllYmE1ZjViMDQ1YWFkMmVjYTA3NSIsIm5iZiI6MTcyNDY1Mjk1MC45MzczNDUsInN1YiI6IjVlZTlkYzNlMTY4NWRhMDAzNjI5ODc1ZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VQS6z9TVtiem10Ev-1qhecdTEkl0BxpatxEBHoq7KEw"
    }
    response = requests.get(url, headers=headers)
    # take the first result
    movie_id = response.json()['results'][0]['id']
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    response = requests.get(url, headers=headers)
    # convert 
    movie_data = response.json()
    poster = f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}"
    genres = [i['name'] for i in movie_data['genres']]
    link = movie_data['homepage']
    imdb_id = movie_data['imdb_id']
    overview = movie_data['overview']
    return {
        'movie': movie_name,
        'poster': poster,
        'genres': genres,
        'link': link,
        'imdb_id': imdb_id,
        'overview': overview
    }

if __name__ == '__main__':
    print(movie_data_from_tmdb('inception'))