import pandas as pd
import joblib
import gdown

class MovieSys:
    def __init__(self, movies_df_path: str):
        # Cargar el DataFrame de películas
        self.movies_df = pd.read_csv(movies_df_path)
        
        # Descargar y cargar la matriz de similitud desde Google Drive
        #output = 'weighted_similarity.joblib'
        #gdown.download(similarity_url, output, quiet=False)
        #self.weighted_similarity = joblib.load(output)
        
        # Preprocesar columnas y mapas de meses y días
        self.movies_df['release_date'] = pd.to_datetime(self.movies_df['release_date'], errors='coerce')
        self.month_map = {
            "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
            "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
            "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
        }
        self.day_map = {
            "lunes": 0, "martes": 1, "miércoles": 2, "jueves": 3,
            "viernes": 4, "sábado": 5, "domingo": 6
        }

    def cantidad_filmaciones_mes(self, mes: str):
        month_num = self.month_map.get(mes.lower())
        if month_num is None:
            return {"error": "Mes inválido"}
        month_count = self.movies_df[self.movies_df['release_date'].dt.month == month_num].shape[0]
        return {"message": f"{month_count} cantidad de películas fueron estrenadas en el mes de {mes}"}

    def cantidad_filmaciones_dia(self, dia: str):
        day_num = self.day_map.get(dia.lower())
        if day_num is None:
            return {"error": "Día inválido"}
        day_count = self.movies_df[self.movies_df['release_date'].dt.dayofweek == day_num].shape[0]
        return {"message": f"{day_count} cantidad de películas fueron estrenadas en los días {dia}"}

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
        total_return = actor_movies['return'].sum()
        movie_count = actor_movies.shape[0]
        average_return = total_return / movie_count if movie_count > 0 else 0
        return {"message": f"El actor {nombre_actor} ha participado de {movie_count} cantidad de filmaciones, el mismo ha conseguido un retorno de {total_return} con un promedio de {average_return} por filmación"}

    def get_director(self, nombre_director: str):
        director_movies = self.movies_df[self.movies_df['crew'].str.contains(nombre_director, case=False, na=False)]
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
                "release_date": release_date,
                "individual_return": individual_return,
                "budget": budget,
                "revenue": revenue
            })
        return {"message": f"El director {nombre_director} ha dirigido las siguientes películas:", "movies": director_info}

    # def recomendacion(self, title, n_recommendations=5):
    #     if title not in self.movies_df['title'].values:
    #         return {"error": "El título no se encuentra en la base de datos."}

    #     movie_index = self.movies_df[self.movies_df['title'] == title].index[0]
    #     similarity_scores = list(enumerate(self.weighted_similarity[movie_index]))
    #     similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    #     recommended_indices = [i[0] for i in similarity_scores[1:n_recommendations + 10]]
        
    #     recommendations = self.movies_df.iloc[recommended_indices]
    #     collection_name = self.movies_df.loc[movie_index, 'belongs_to_collection']
    #     if pd.notna(collection_name):
    #         collection_movies = recommendations[recommendations['belongs_to_collection'] == collection_name]
    #         other_movies = recommendations[recommendations['belongs_to_collection'] != collection_name]
    #         other_movies = other_movies.sort_values(by=['popularity', 'vote_count'], ascending=False)
    #         final_recommendations = pd.concat([collection_movies, other_movies]).head(n_recommendations)
    #     else:
    #         final_recommendations = recommendations.sort_values(by=['popularity', 'vote_count'], ascending=False).head(n_recommendations)
        
    #     return {"recommendations": final_recommendations[['title', 'genres', 'vote_average', 'popularity']].to_dict(orient="records")}