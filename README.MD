# Sistema de Recomendación de Películas

Este proyecto implementa un sistema de recomendación de películas utilizando técnicas de aprendizaje automático y procesamiento de texto, desplegado mediante FastAPI en [Render](https://render.com/). El sistema ofrece diferentes funciones, entre ellas la de recomendaciones personalizadas basadas en una matriz de similitud preentrenada.

## Descripción del Problema

El objetivo de este proyecto es crear un sistema de recomendación que permita a los usuarios obtener recomendaciones de películas similares a una seleccionada. Este tipo de sistema es útil para ofrecer recomendaciones personalizadas a usuarios de plataformas de streaming o aplicaciones de cine.

## Estructura del Proyecto

- `models2.py`: Contiene las funciones principales para procesar y generar recomendaciones basadas en similitudes, de acuerdo con los requerimientos específicos del problema.
- `main.py`: Define los endpoints de FastAPI y aplica los decoradores necesarios para el despliegue. Esta configuración facilita la interacción con el modelo desde una API.
- `model.py`: Contiene el modelo original de recomendaciones y sus configuraciones iniciales.
- `Modelo.ipynb`: Un Jupyter Notebook que documenta el proceso de desarrollo y ajuste del modelo, incluyendo análisis exploratorio y validaciones de desempeño.
- `Datasets/test.csv`: dataset limpio utilizado para buscar las recomendaciones y demás información requerida por las funciones get.
- `Datasets/sim.pkl`: Matriz de similitud serializada que se utiliza en el modelo para calcular recomendaciones basadas en contenido similar.

## Configuración del Sistema de Recomendación

El sistema utiliza una matriz de similitud preentrenada (`sim.pkl`), ubicada en la carpeta `Datasets`, para calcular recomendaciones basadas en el contenido de las películas. Este archivo contiene una matriz serializada que representa la similitud entre películas, basada en características seleccionadas como género, sinopsis, actores y equipo de producción. 
La matriz se generó a partir de la mitad de los datos de `test.csv` debido a que si se utiliza el total de los datos para realizar la matriz de similitud, esta matriz pesaría más de 1GB

### Principales Funciones en `models2.py`

Las funciones de `models2.py` están diseñadas para satisfacer los requisitos del sistema de recomendación, tales como:
- **Función de recomendación por similitud**: Utiliza la matriz de similitud para recomendar películas similares.
- **Función de búsqueda de director**: Permite obtener información sobre las películas dirigidas por un director específico.
- **Manejo de colecciones**: Recomienda películas de una colección si la película seleccionada pertenece a alguna, y complementa las recomendaciones con otras películas similares.

### Configuración de `main.py` para FastAPI

`main.py` contiene los decoradores y configuraciones de FastAPI necesarios para desplegar el sistema de recomendación como una API. Los endpoints definidos permiten:
- Realizar consultas de recomendaciones de películas.
- Buscar información específica, como directores y detalles de películas.
- Desplegar el modelo en un entorno de servidor con Render.com.

## Despliegue

El sistema ha sido desplegado en [Render](https://render.com/), lo que permite acceder a la API desde cualquier lugar. La configuración en `main.py` está diseñada para facilitar el despliegue en un entorno de producción, garantizando que las rutas y funcionalidades estén disponibles a través de la web.

## Instalación y Ejecución Local

Si deseas ejecutar el proyecto localmente, sigue los siguientes pasos:

1. **Clona el repositorio**:
    ```bash
    git clone https://github.com/tuusuario/Sistema-de-Recomendacion-de-Peliculas.git
    cd Sistema-de-Recomendacion-de-Peliculas
    ```

2. **Instala las dependencias**:
    Se recomienda crear un entorno virtual y luego instalar las dependencias.
    ```bash
    python -m venv env
    source env/bin/activate  # En Windows: env\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Ejecución del servidor de FastAPI**:
    ```bash
    uvicorn main:app --reload
    ```

4. **Acceso a la API**:
   Abre tu navegador o herramienta de consulta de API y navega a `http://127.0.0.1:8000` para ver la documentación generada automáticamente por FastAPI.

## Endpoints Disponibles
- `GET /cantidad_filmaciones_mes/{mes}`: Devuelve la cantidad de películas que fueron estrenadas en el mes consultado en la totalidad del dataset.
- `GET /cantidad_filmaciones_dia/{dia}`: Devuelve la cantidad de películas que fueron estrenadas en el día consultado en la totalidad del dataset.
- `GET /score_titulo/{titulo}`: Devuelve el score que tiene la película
- `GET /votos_titulo/{titulo}`: Retorna los votos que tiene la película si al menos tiene 2000 votos
- `GET /get_actor/{nombre_actor}`: Se ingresa el nombre de un actor que se encuentre dentro de un dataset y devuelve el éxito del mismo medido a través del retorno. Además, la cantidad de películas en las que ha participado y el promedio de retorno.
- `GET /director/{nombre_director}`: Retorna todas las películas dirigidas por el director indicado.
- `GET /recomendacion/{titulo}`: Devuelve una lista de recomendaciones basadas en una película específica.

## Dependencias

Este proyecto utiliza las siguientes librerías de Python:
- **FastAPI**: Para crear y manejar la API.
- **Scikit-learn**: Para el procesamiento de datos y cálculo de similitudes.
- **Pandas**: Para la manipulación y análisis de datos.
- **Uvicorn**: Para ejecutar el servidor ASGI compatible con FastAPI.
- **Numpy**: Para transformar la matriz de similitud

## Créditos

Este proyecto fue desarrollado con fines educativos y de aprendizaje en el campo de ciencia de datos y machine learning aplicado a recomendaciones de contenido.

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

