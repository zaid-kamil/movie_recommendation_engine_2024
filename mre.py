import pandas as pd
from joblib import load

def get_id_from_movie(movie_name, df):
    try:return df[df['names'].str.lower()==movie_name.lower()].index.tolist()[0]
    except: return -1

def get_random_movie_from_keyword(keyword, df):
    try: return df[df['overview'].str.lower().str.contains(keyword.lower())].sample(1).index.tolist()[0]
    except: return -1

def get_recommendation(query='', by='name', count=10):
    df = pd.read_parquet('recommender/models/clean_movies.parquet')
    sim = load('recommender/models/similarity.joblib')
    print(f'query: {query}, by: {by}, count: {count}')
    match by:
        case 'name':
            movie_id = get_id_from_movie(query, df)
            if movie_id == -1:
                return 'Movie not found'
            else:
                sim_scores = list(enumerate(sim[movie_id]))
                sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
                sim_scores = sim_scores[count+1::-1]
                movie_indices = [i[0] for i in sim_scores]
                return df['names'].iloc[movie_indices].tolist()
        case 'word':
            movie_ids = get_random_movie_from_keyword(query, df)
            if movie_ids == -1:
                return 'Movie not found'
            else:
                sim_scores = list(enumerate(sim[movie_ids]))
                sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
                sim_scores = sim_scores[count+1::-1]
                movie_indices = [i[0] for i in sim_scores]
                return df['names'].iloc[movie_indices].tolist()
            

if __name__ == '__main__':
    print(get_recommendation('inception', by='name', count=10))