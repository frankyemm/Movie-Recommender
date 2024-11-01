import ast
import numpy as np

def desanida_column(extract_value: str, text, limit: int = None):
    # Verificar si el valor es una cadena y no está vacío
    if isinstance(text, str) and text not in ['', 'None']:
        try:
            # Intentar convertir la cadena a un objeto (lista o diccionario)
            data = ast.literal_eval(text)
            # Si el resultado es una lista, extraer valores de cada diccionario en la lista
            if isinstance(data, list):
                values = [item.get(extract_value, np.nan) for item in data if isinstance(item, dict)]
                # Limitar la cantidad de valores si se ha especificado un límite
                return values[:limit] if limit is not None else values
            # Si el resultado es un diccionario, extraer el valor directamente
            elif isinstance(data, dict):
                return data.get(extract_value, np.nan)
        except (ValueError, SyntaxError, TypeError):
            return np.nan
    # Retornar NaN si text no es una cadena válida o es NaN
    return np.nan

def extraer_directores(text):
    # Verificar si el valor es una cadena y no está vacío
    if isinstance(text, str) and text not in ['', 'None']:
        try:
            # Intentar convertir la cadena a una lista de diccionarios
            data = ast.literal_eval(text)
            # Filtrar solo los nombres donde el 'job' es 'Director'
            if isinstance(data, list):
                return [item.get('name', np.nan) for item in data if isinstance(item, dict) and item.get('job') == 'Director']
        except (ValueError, SyntaxError, TypeError):
            return np.nan
    # Retornar NaN si text no es una cadena válida o es NaN
    return np.nan