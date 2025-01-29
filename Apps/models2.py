import pandas as pd
import requests

class MovieSys:
    def __init__(self, movies_df_path: str, similarity_path: str):
        # Cargar el DataFrame de películas
        self.movies_df = pd.read_csv(movies_df_path)
        self.weighted_similarity = pd.read_pickle(similarity_path)
        if 'release_date' in self.movies_df.columns:
            self.movies_df['release_date'] = pd.to_datetime(self.movies_df['release_date'], format='%Y-%m-%d', errors='coerce')
        else:
            print("Warning: La columna 'release_date' no existe en el archivo CSV.")
        # Preprocesar columnas y mapas de meses y días
        self.month_map = {
            "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
            "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
            "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
        }
        self.day_map = {
            "lunes": 1, "martes": 2, "miércoles": 3, "jueves": 4,
            "viernes": 5, "sábado": 6, "domingo": 0
        }
        

    def cantidad_filmaciones_mes(self, mes: str):
        month_num = self.month_map.get(mes.lower())
        if month_num is None:
            return {"error": "Mes inválido"}
        month_count = self.movies_df[self.movies_df['release_date'].dt.month == month_num].shape[0]
        return {"message": f"{month_count} películas fueron estrenadas en el mes de {mes.lower()}"}

    def cantidad_filmaciones_dia(self, dia: str):
        day_num = self.day_map.get(dia.lower())
        if day_num is None:
            return {"error": "Día inválido"}
        day_count = self.movies_df[self.movies_df['release_date'].dt.dayofweek == day_num].shape[0]
        return {"message": f"{day_count} películas fueron estrenadas en los días {dia.lower()}"}
    
    def score_titulo(self, titulo: str):
        movie = self.movies_df[self.movies_df['title'].str.lower() == titulo.lower()]
        if movie.empty:
            return {"error": "Película no encontrada"}
        title = movie.iloc[0]['title']
        year = movie.iloc[0]['release_year']
        score = movie.iloc[0]['popularity']
        return {"message": f"La película {title} fue estrenada en el año {year} con un score/popularidad de {score}"}
    
    def votos_titulo(self, titulo: str):
        movie = self.movies_df[self.movies_df['title'].str.lower() == titulo.lower()]
        if movie.empty:
            return {"error": "Película no encontrada"}
        vote_count = movie.iloc[0]['vote_count']
        if vote_count < 2000:
            return {"message": "La película no cumple con el mínimo de 2000 valoraciones"}
        vote_average = movie.iloc[0]['vote_average']
        title = movie.iloc[0]['title']
        year = movie.iloc[0]['release_year']
        return {"message": f"La película {title} fue estrenada en el año {year}. La misma cuenta con un total de {vote_count} valoraciones, con un promedio de {vote_average}"}

    def get_actor(self, nombre_actor: str):
        actor_movies = self.movies_df[self.movies_df['cast'].str.contains(nombre_actor, case=False, na=False)]
        if actor_movies.empty:
            return {"error": "Actor no encontrado"}
        actor_names = actor_movies['cast'].apply(
            lambda x: next((name for name in x.split(',') if nombre_actor.lower() in name.lower()), nombre_actor)
        ).unique()
        
        # Convertimos el nombre exacto a una cadena, seleccionando el primer valor
        exact_actor_name = str(actor_names[0]) if actor_names.size > 0 else nombre_actor
        exact_actor_name = exact_actor_name.strip("'[]'")
        total_return = round(actor_movies['return'].sum(), 3)
        movie_count = actor_movies.shape[0]
        average_return = round(total_return / movie_count if movie_count > 0 else 0, 3)
        return {"message": f"El actor {exact_actor_name} ha participado de {movie_count} cantidad de filmaciones, el mismo ha conseguido un retorno de {total_return} con un promedio de {average_return} por filmación"}
    
    def get_director(self, nombre_director: str):
        # Filtramos las películas del director (sin distinguir mayúsculas y minúsculas)
        director_movies = self.movies_df[self.movies_df['crew'].str.contains(nombre_director, case=False, na=False)]
        
        # Si no hay películas encontradas, retornamos un error
        if director_movies.empty:
            return {"error": "Director no encontrado"}
        
        # Obtenemos el nombre exacto del director tal como está en el DataFrame
        director_names = director_movies['crew'].apply(
            lambda x: next((name for name in x.split(',') if nombre_director.lower() in name.lower()), nombre_director)
        ).unique()
        
        # Convertimos el nombre exacto a una cadena, seleccionando el primer valor
        exact_director_name = str(director_names[0]) if director_names.size > 0 else nombre_director
        exact_director_name = exact_director_name.strip("'[]'")
        # Recopilamos la información de las películas dirigidas por el director
        director_info = []
        for _, movie in director_movies.iterrows():
            title = movie['title']
            release_date = movie['release_date']
            
            # Convertimos la fecha a formato 'YYYY-MM-DD'
            formatted_date = str(release_date)

            individual_return = movie['return']
            budget = movie['budget']
            revenue = movie['revenue']
            director_info.append({
                "title": title,
                "release_date": formatted_date[:10],
                "individual_return": individual_return,
                "budget": budget,
                "revenue": revenue
                })
        
        # Devolvemos el mensaje con el nombre exacto sin lista ni corchetes
        return {"message": f"El director {exact_director_name} ha dirigido las siguientes películas:", "movies": director_info}

    def recomendacion(self, titulo, n_recommendations=5):
        """
        Devuelve recomendaciones de películas basadas en similitud y/o colección.
        Además, para cada recomendación, se llama a la API de OMDb usando el imdb_id
        para obtener el póster de la película.
        """
        # Convertir el título ingresado a minúsculas
        title_lower = titulo.lower()

        # Verificar si el título existe en la base de datos, ignorando mayúsculas/minúsculas
        if title_lower not in self.movies_df['title'].str.lower().values:
            return {"error": "El título no se encuentra en la base de datos."}

        # Obtener el índice de la película y el título original para mantener el formato correcto
        movie = self.movies_df[self.movies_df['title'].str.lower() == title_lower]
        titulo = movie.iloc[0]['title']
        movie_index = movie.index[0]
        movie_genres = movie.iloc[0]['genres']  # Obtener los géneros de la película dada

        # Verificar si el índice está dentro de los límites de la matriz de similitud
        if movie_index >= len(self.weighted_similarity):
            # Si el índice está fuera de rango, usar similitud de géneros
            similar_movies = self.movies_df[self.movies_df['genres'].apply(
                lambda x: any(genre in x for genre in movie_genres)
            )]
            # Excluir la película original
            similar_movies = similar_movies[similar_movies.index != movie_index]
            # Ordenar y tomar las top-n recomendaciones
            similar_movies = similar_movies.sort_values(by=['popularity', 'vote_count'], ascending=False).head(n_recommendations)

            # Convertir a un DataFrame para manipular y extraer pósters
            final_recommendations = similar_movies
        else:
            # Verificar si la película pertenece a una colección
            collection_name = self.movies_df.loc[movie_index, 'belongs_to_collection']
            collection_movies = pd.DataFrame()

            if pd.notna(collection_name):
                # Obtener todas las películas de esa colección (excepto la original)
                collection_movies = self.movies_df[self.movies_df['belongs_to_collection'] == collection_name]
                collection_movies = collection_movies[collection_movies.index != movie_index]

            # Si la colección tiene suficientes películas, retornarlas
            if len(collection_movies) >= n_recommendations:
                final_recommendations = collection_movies.head(n_recommendations)
            else:
                # Calcular similitudes
                similarity_scores = list(enumerate(self.weighted_similarity[movie_index]))
                similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

                # Índices recomendados que no estén en la misma colección
                recommended_indices = [
                    i[0] for i in similarity_scores[1:] 
                    if i[0] not in collection_movies.index
                ][:n_recommendations - len(collection_movies)]

                # Películas adicionales
                additional_recommendations = self.movies_df.iloc[recommended_indices]

                # Concatenar colección + recomendaciones extra
                final_recommendations = pd.concat([collection_movies, additional_recommendations]).head(n_recommendations)

        # Aquí solicitamos también la columna 'imdb_id', asumimos que existe en el CSV
        # (si no está, agrégala en tu test.csv).
        # Creamos un DataFrame temporal para manipular las recomendaciones.
        recommended_movies = final_recommendations[['title', 'genres', 'vote_average', 'popularity', 'imdb_id', 'overview']].copy()

        # Para cada película recomendada, llamamos a la API de OMDb para obtener el póster
        for idx, row in recommended_movies.iterrows():
            imdb_id = row['imdb_id']
            poster_url = self._get_poster_from_omdb(imdb_id)
            recommended_movies.at[idx, 'poster'] = poster_url

        # Retornamos la información en formato de lista de diccionarios
        return {
            "recommendations": recommended_movies.to_dict(orient="records")
        }

    def _get_poster_from_omdb(self, imdb_id: str) -> str:
        """
        Función auxiliar para obtener el póster de la película a partir del imdb_id,
        usando la API de OMDb.
        """
        if pd.notna(imdb_id) and imdb_id != '':
            api_key = open("key.txt", 'r').read()  # Reemplázalo con tu propia API Key
            url = f"https://www.omdbapi.com/?i={imdb_id}&apikey={api_key}"
            
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    # 'Poster' podría no existir si la API no encuentra el póster
                    return data.get('Poster', 'Póster no disponible')
            except Exception as e:
                print(f"Error al consultar OMDb: {e}")
        
        # Si no hay imdb_id o la consulta falla, devolvemos un valor por defecto
        return "Póster no disponible"