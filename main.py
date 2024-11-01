from fastapi import FastAPI
import pandas as pd
from joblib import load

app = FastAPI()

# Cargar el dataset
movies_df = pd.read_parquet("movies_data.parquet")
weighted_similarity = load("weighted_similarity.joblib")

# Función auxiliar para procesar meses en español
month_map = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
}

# Función auxiliar para procesar días en español
day_map = {
    "lunes": 0, "martes": 1, "miércoles": 2, "jueves": 3,
    "viernes": 4, "sábado": 5, "domingo": 6
}

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de consulta de películas"}

@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    month_num = month_map.get(mes.lower())
    if month_num is None:
        return {"error": "Mes inválido"}
    # Filtrar las películas por mes
    movies_df['release_date'] = pd.to_datetime(movies_df['release_date'], errors='coerce')
    month_count = movies_df[movies_df['release_date'].dt.month == month_num].shape[0]
    return {"message": f"{month_count} cantidad de películas fueron estrenadas en el mes de {mes}"}

@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    day_num = day_map.get(dia.lower())
    if day_num is None:
        return {"error": "Día inválido"}
    # Filtrar las películas por día
    movies_df['release_date'] = pd.to_datetime(movies_df['release_date'], errors='coerce')
    day_count = movies_df[movies_df['release_date'].dt.dayofweek == day_num].shape[0]
    return {"message": f"{day_count} cantidad de películas fueron estrenadas en los días {dia}"}

@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    movie = movies_df[movies_df['title'].str.lower() == titulo.lower()]
    if movie.empty:
        return {"error": "Película no encontrada"}
    title = movie.iloc[0]['title']
    year = movie.iloc[0]['release_year']
    score = movie.iloc[0]['popularity']
    return {"message": f"La película {title} fue estrenada en el año {year} con un score/popularidad de {score}"}

@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str):
    movie = movies_df[movies_df['title'].str.lower() == titulo.lower()]
    if movie.empty:
        return {"error": "Película no encontrada"}
    vote_count = movie.iloc[0]['vote_count']
    if vote_count < 2000:
        return {"message": "La película no cumple con el mínimo de 2000 valoraciones"}
    vote_average = movie.iloc[0]['vote_average']
    title = movie.iloc[0]['title']
    year = movie.iloc[0]['release_year']
    return {"message": f"La película {title} fue estrenada en el año {year}. La misma cuenta con un total de {vote_count} valoraciones, con un promedio de {vote_average}"}

@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    actor_movies = movies_df[movies_df['cast'].str.contains(nombre_actor, case=False, na=False)]
    if actor_movies.empty:
        return {"error": "Actor no encontrado"}
    total_return = actor_movies['return'].sum()
    movie_count = actor_movies.shape[0]
    average_return = total_return / movie_count if movie_count > 0 else 0
    return {"message": f"El actor {nombre_actor} ha participado de {movie_count} cantidad de filmaciones, el mismo ha conseguido un retorno de {total_return} con un promedio de {average_return} por filmación"}

@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str):
    director_movies = movies_df[movies_df['crew'].str.contains(nombre_director, case=False, na=False)]
    if director_movies.empty:
        return {"error": "Director no encontrado"}
    director_info = []
    for _, movie in director_movies.iterrows():
        title = movie['title']
        release_date = movie['release_date']
        individual_return = movie['return']
        budget = movie['budget']
        revenue = movie['revenue']
        director_info.append({
            "title": title,
            "release_date": release_date
        })
    return {"message": f"El director {nombre_director} ha dirigido las siguientes películas:", "movies": director_info}

@app.get("/recomendacion/title")
def recomendacion(title, n_recommendations=5):
    # Verificar si el título existe en la base de datos
    if title not in movies_df['title'].values:
        print("El título no se encuentra en la base de datos.")
        return
    
    # Encontrar el índice de la película de interés
    movie_index = movies_df[movies_df['title'] == title].index[0]
    
    # Obtener la colección de la película (si existe)
    collection_name = movies_df.loc[movie_index, 'belongs_to_collection']
    
    # Obtener índices de películas similares
    similarity_scores = list(enumerate(weighted_similarity[movie_index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similar_movies_indices = [i[0] for i in similarity_scores[1:n_recommendations + 10]]  # Obtener suficientes películas
    
    # Filtrar y priorizar recomendaciones
    recommendations = movies_df.iloc[similar_movies_indices]
    if pd.notna(collection_name):  # Si la película pertenece a una colección
        # Películas de la misma colección primero
        collection_movies = recommendations[recommendations['belongs_to_collection'] == collection_name]
        # Luego las películas similares por géneros y ordenadas por popularidad y votos
        other_movies = recommendations[recommendations['belongs_to_collection'] != collection_name]
        other_movies = other_movies.sort_values(by=['popularity', 'vote_count'], ascending=False)
        
        # Combinar ambas listas
        final_recommendations = pd.concat([collection_movies, other_movies]).head(n_recommendations)
    else:
        # Si no pertenece a una colección, solo ordenar por popularidad y votos
        final_recommendations = recommendations.sort_values(by=['popularity', 'vote_count'], ascending=False).head(n_recommendations)
    
    print(f"Películas recomendadas para '{title}':")
    for _, row in final_recommendations.iterrows():
        print(f"{row['title']} - Géneros: {row['genres']}, Puntuación: {row['vote_average']}, Popularidad: {row['popularity']}, Reparto: {row['cast']}, Director: {row['crew']}")
