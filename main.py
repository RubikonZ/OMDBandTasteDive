import requests
import requests_cache

requests_cache.install_cache('project_cache')


def get_movies_from_tastedive(st):
    my_param = {'type': 'movies', 'q': st, 'limit': 5}
    answer = requests.get('https://tastedive.com/api/similar', params=my_param)
    return answer.json()


def extract_movie_titles(tastedive_resp):
    movie_ls = []
    for movie in tastedive_resp['Similar']['Results']:
        movie_ls.append(movie['Name'])
    return movie_ls


if __name__ == '__main__':
    black_panther = get_movies_from_tastedive('Black Panther')
    print(extract_movie_titles(black_panther))


