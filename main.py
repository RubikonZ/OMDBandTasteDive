import requests
import requests_cache
import os
import json

requests_cache.install_cache('project_cache')
omdb_key = os.environ.get('omdb_key')


def get_movies_from_tastedive(st:str):
    my_param = {'type': 'movies', 'q': st, 'limit': 5}
    answer = requests.get('https://tastedive.com/api/similar', params=my_param)
    # print(f'Got answer from {answer.url} (Either from API or cache)')
    return answer.json()


def extract_movie_titles(tastedive_resp):
    movie_ls = []
    for movie in tastedive_resp['Similar']['Results']:
        movie_ls.append(movie['Name'])
    return movie_ls


def get_related_movies(ls_of_movies:list):
    final_ls = []
    for movie in ls_of_movies:
        ans = get_movies_from_tastedive(movie)
        for mov in extract_movie_titles(ans):
            if mov not in final_ls:
                final_ls.append(mov)
    return final_ls


def get_movie_data(movie):
    my_param = {'t': movie, 'r': 'json', 'apikey': omdb_key}
    resp = requests.get('http://www.omdbapi.com/', params=my_param)
    return resp.json()


def get_movie_rating(omdb_dict):
    try:
        for review in omdb_dict['Ratings']:
            if review['Source'] == 'Rotten Tomatoes':
                return int(review['Value'].strip('%'))
    except KeyError:
        return 0

def get_sorted_recommendations(ls_of_movies):
    # get 5 related movies for each movie
    ls_of_rel_mov = get_related_movies(ls_of_movies)

    ls_of_tup = []
    for movie in ls_of_rel_mov:
        ls_of_tup.append((movie, get_movie_rating(get_movie_data(movie))))

    final_movie_ls = []
    for movie in sorted(ls_of_tup, key=lambda x: (x[1], x[0]), reverse=True):
        final_movie_ls.append(movie[0])
    return final_movie_ls

if __name__ == '__main__':
    print(get_sorted_recommendations(['Black Panther', 'Thor']))
    # print(json.dumps(get_movie_data('Thor'), indent=4))
    # print(get_movie_rating(get_movie_data('Thor')))

