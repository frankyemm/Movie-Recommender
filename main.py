from fastapi import FastAPI
from models2 import MovieSys

# Configuración del archivo y enlace de Google Drive
movies_df_path = 'Datasets/test.csv'
similarity_path = "Datasets/sim.pkl"  # ID del archivo

# Inicializar MovieSys Sistema-de-Recomendacion-de-Peliculas\main.py
movie_sys = MovieSys(movies_df_path, similarity_path)

# Crear instancia de FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de consulta de películas"}

@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    return movie_sys.cantidad_filmaciones_mes(mes)

@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    return movie_sys.cantidad_filmaciones_dia(dia)

@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    return movie_sys.score_titulo(titulo)

@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str):
    return movie_sys.votos_titulo(titulo)

@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    return movie_sys.get_actor(nombre_actor)

@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str):
    return movie_sys.get_director(nombre_director)

@app.get("/recomendacion/{title}")
def recomendacion(title: str, n_recommendations: int = 5):
    return movie_sys.recomendacion(title, n_recommendations)
