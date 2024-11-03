
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler

# Cargar el archivo CSV
movies_df = pd.read_csv('Datasets/test.csv')

# Normalizar 'vote_count' y 'popularity' para ponderación
scaler = MinMaxScaler()
movies_df[['vote_count', 'popularity']] = scaler.fit_transform(movies_df[['vote_count', 'popularity']])

# Crear una columna combinada para 'genres', 'overview', 'cast', y 'crew' para similitud de contenido
movies_df['content'] = (
    movies_df['genres'].fillna('') + " " +
    movies_df['overview'].fillna('') + " " +
    movies_df['cast'].fillna('') + " " +
    movies_df['crew'].fillna('')
)

# Vectorizar el texto combinado con TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies_df['content'])

# Vectorizar únicamente 'genres' para calcular la similitud específica de géneros
tfidf_genres = TfidfVectorizer(stop_words='english')
genres_matrix = tfidf_genres.fit_transform(movies_df['genres'].fillna(''))

# Calcular la similitud de coseno en ambas matrices (contenido y géneros)
content_similarity = cosine_similarity(tfidf_matrix)
genre_similarity = cosine_similarity(genres_matrix)

# Construir la matriz de similitud ponderada sumando los pesos de 'vote_average', 'popularity' y 'genres'
weighted_similarity = (
    content_similarity +
    (movies_df['vote_average'].values[:, None] * 0.25) +
    (movies_df['popularity'].values[:, None] * 0.5) +
    (genre_similarity * 0.25)  # Ponderación de géneros
)

# Filtrado colaborativo (SVD)
reader = Reader(rating_scale=(1, 10))
data = Dataset.load_from_df(movies_df[['id', 'vote_average', 'vote_count']], reader)
trainset, testset = train_test_split(data, test_size=0.2)
svd = SVD()
svd.fit(trainset)

# Función de recomendación avanzada
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

if __name__ == '__main__':
    recomendacion('Toy Story')