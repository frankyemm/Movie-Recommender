import pandas as pd
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# Función para generar palabras clave de cada fila
def extract_keywords(row):
    keywords = []
    
    # Extraer palabras clave de cada columna y manejar listas, strings, y NaN de forma segura
    if isinstance(row['genres'], list):
        keywords.extend([genre.replace(" ", "") for genre in row['genres'] if pd.notna(genre)])
    elif pd.notna(row['genres']):
        keywords.extend(row['genres'].replace(" ", "").split(','))
    
    if isinstance(row['cast'], list):
        keywords.extend([actor.replace(" ", "") for actor in row['cast'] if pd.notna(actor)])
    elif pd.notna(row['cast']):
        keywords.extend(row['cast'].replace(" ", "").split(','))

    if isinstance(row['crew'], list):
        keywords.extend([member.replace(" ", "") for member in row['crew'] if pd.notna(member)])
    elif pd.notna(row['crew']):
        keywords.extend(row['crew'].replace(" ", "").split(','))

    if isinstance(row['production_companies'], list):
        keywords.extend([company.replace(" ", "") for company in row['production_companies'] if pd.notna(company)])
    elif pd.notna(row['production_companies']):
        keywords.extend(row['production_companies'].replace(" ", "").split(','))

    if isinstance(row['tagline'], str):
        tagline_keywords = [word for word in row['tagline'].split() if word.lower() not in ENGLISH_STOP_WORDS]
        keywords.extend(tagline_keywords)
    
    # Eliminar duplicados y unir palabras clave en una cadena de texto
    return list(set(keywords))