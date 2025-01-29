# streamlit_app.py

import streamlit as st
import requests
import ast
st.set_page_config(page_title="Mi Sistema de Recomendación", layout="wide")

def main():
    st.title("Sistema de Recomendación de Películas")
    st.write("Esta aplicación utiliza un backend (FastAPI) que expone varios endpoints para consultar información sobre películas.")

    # ------------------------------------------------------
    # 1. Inyectamos el CSS para el efecto de flip en portada
    # ------------------------------------------------------
    flip_card_css = """
    <style>
    /* Contenedor principal de la tarjeta (flip-card) */
    .flip-card {
        background-color: transparent;
        width: 200px;   /* Ancho fijo de la tarjeta */
        height: 300px;  /* Alto fijo de la tarjeta */
        perspective: 1000px; /* Crear el contexto 3D */
        margin-bottom: 20px; /* Espaciado vertical entre tarjetas */
    }

    /* Contenedor interno que realiza la rotación */
    .flip-card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.6s;
        transform-style: preserve-3d;
    }

    /* Efecto hover: al pasar el ratón, rota 180 grados */
    .flip-card:hover .flip-card-inner {
        transform: rotateY(180deg);
    }

    /* Caras frontal y trasera */
    .flip-card-front, .flip-card-back {
        position: absolute;
        width: 100%;
        height: 100%;
        -webkit-backface-visibility: hidden;
        backface-visibility: hidden;
        border-radius: 6px;
        overflow: hidden;
    }

    /* Cara frontal con la portada (imagen) */
    .flip-card-front img {
        width: 100%;
        height: 100%;
        object-fit: cover; /* Ajustar la imagen al contenedor */
    }

    /* Cara trasera con el overview */
    .flip-card-back {
        background-color: #1e1e1e;
        color: #fff;
        transform: rotateY(180deg);
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px;
    }

    /* Truncar texto si es demasiado largo */
    .flip-card-back p {
        margin: 0;
        text-align: justify;
        overflow: hidden;
        text-overflow: ellipsis;
        
        /* Para limitar la cantidad de líneas que se muestran (ejemplo: 6) */
        display: -webkit-box;
        -webkit-line-clamp: 6;  
        -webkit-box-orient: vertical;
    }
    </style>
    """

    st.markdown(flip_card_css, unsafe_allow_html=True)

    # URL base de tu API local de FastAPI
    API_URL = "http://127.0.0.1:8000"

    # Menú lateral con todas las opciones (endpoints)
    menu = [
        "Inicio (Root)",
        "Cantidad de filmaciones por mes",
        "Cantidad de filmaciones por día",
        "Score título",
        "Votos título",
        "Get actor",
        "Get director",
        "Recomendación"
    ]
    choice = st.sidebar.selectbox("Elige una opción", menu)

    # -----------------------------
    # 2. Sección de "Inicio (Root)"
    # -----------------------------
    if choice == "Inicio (Root)":
        st.subheader("Bienvenida")
        st.write("Al hacer clic en 'Consultar', se mostrará el mensaje de bienvenida de la API.")
        if st.button("Consultar"):
            try:
                resp = requests.get(f"{API_URL}/")
                if resp.status_code == 200:
                    data = resp.json()
                    st.json(data)
                else:
                    st.error("Error al consultar la API.")
            except Exception as e:
                st.error(f"Error: {e}")

    # --------------------------------------------
    # 3. Cantidad de filmaciones por mes (/cantidad_filmaciones_mes/{mes})
    # --------------------------------------------
    elif choice == "Cantidad de filmaciones por mes":
        st.subheader("Cantidad de filmaciones por mes")
        mes = st.text_input("Ingresa un mes (ejemplo: enero, febrero...)")
        if st.button("Consultar"):
            try:
                resp = requests.get(f"{API_URL}/cantidad_filmaciones_mes/{mes}")
                if resp.status_code == 200:
                    data = resp.json()
                    if "error" in data:
                        st.error(data["error"])
                    else:
                        st.success(data["message"])
                else:
                    st.error("Error al consultar la API.")
            except Exception as e:
                st.error(f"Error: {e}")

    # ---------------------------------------------
    # 4. Cantidad de filmaciones por día (/cantidad_filmaciones_dia/{dia})
    # ---------------------------------------------
    elif choice == "Cantidad de filmaciones por día":
        st.subheader("Cantidad de filmaciones por día")
        dia = st.text_input("Ingresa un día (ejemplo: lunes, martes...)")
        if st.button("Consultar"):
            try:
                resp = requests.get(f"{API_URL}/cantidad_filmaciones_dia/{dia}")
                if resp.status_code == 200:
                    data = resp.json()
                    if "error" in data:
                        st.error(data["error"])
                    else:
                        st.success(data["message"])
                else:
                    st.error("Error al consultar la API.")
            except Exception as e:
                st.error(f"Error: {e}")

    # -----------------------------
    # 5. Score título (/score_titulo/{titulo})
    # -----------------------------
    elif choice == "Score título":
        st.subheader("Score título")
        titulo = st.text_input("Ingresa el título de la película:")
        if st.button("Consultar"):
            try:
                resp = requests.get(f"{API_URL}/score_titulo/{titulo}")
                if resp.status_code == 200:
                    data = resp.json()
                    if "error" in data:
                        st.error(data["error"])
                    else:
                        st.success(data["message"])
                else:
                    st.error("Error al consultar la API.")
            except Exception as e:
                st.error(f"Error: {e}")

    # ------------------------------
    # 6. Votos título (/votos_titulo/{titulo})
    # ------------------------------
    elif choice == "Votos título":
        st.subheader("Votos título")
        titulo = st.text_input("Ingresa el título de la película:")
        if st.button("Consultar"):
            try:
                resp = requests.get(f"{API_URL}/votos_titulo/{titulo}")
                if resp.status_code == 200:
                    data = resp.json()
                    if "error" in data:
                        st.error(data["error"])
                    else:
                        st.info(data["message"])
                else:
                    st.error("Error al consultar la API.")
            except Exception as e:
                st.error(f"Error: {e}")

    # --------------------------------
    # 7. Get actor (/get_actor/{nombre_actor})
    # --------------------------------
    elif choice == "Get actor":
        st.subheader("Get actor")
        actor = st.text_input("Ingresa el nombre del actor o actriz:")
        if st.button("Consultar"):
            try:
                resp = requests.get(f"{API_URL}/get_actor/{actor}")
                if resp.status_code == 200:
                    data = resp.json()
                    if "error" in data:
                        st.error(data["error"])
                    else:
                        st.success(data["message"])
                else:
                    st.error("Error al consultar la API.")
            except Exception as e:
                st.error(f"Error: {e}")

    # ---------------------------------
    # 8. Get director (/get_director/{nombre_director})
    # ---------------------------------
    elif choice == "Get director":
        st.subheader("Get director")
        director = st.text_input("Ingresa el nombre del director:")
        if st.button("Consultar"):
            try:
                resp = requests.get(f"{API_URL}/get_director/{director}")
                if resp.status_code == 200:
                    data = resp.json()
                    if "error" in data:
                        st.error(data["error"])
                    else:
                        # Mostramos mensaje principal
                        st.success(data["message"])
                        # Mostramos la info de las películas dirigidas
                        if "movies" in data:
                            st.write("Películas dirigidas:")
                            for m in data["movies"]:
                                st.write(f"- **{m['title']}** (Fecha: {m['release_date']})")
                                st.write(f"  - Return: {m['individual_return']}")
                                st.write(f"  - Budget: {m['budget']}, Revenue: {m['revenue']}")
                                st.write("---")
                else:
                    st.error("Error al consultar la API.")
            except Exception as e:
                st.error(f"Error: {e}")

    # --------------------------------------------------
    # 9. Recomendación (/recomendacion/{titulo})
    #    con efecto de flip en la portada
    # --------------------------------------------------
    elif choice == "Recomendación":
        st.subheader("Recomendación")
        titulo = st.text_input("Ingresa el título de la película:")
        n_recs = st.number_input("Cantidad de recomendaciones", min_value=1, max_value=10, value=5)
        if st.button("Consultar"):
            try:
                url = f"{API_URL}/recomendacion/{titulo}?n_recommendations={n_recs}"
                resp = requests.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    if "error" in data:
                        st.error(data["error"])
                    else:
                        st.success("Recomendaciones encontradas:")
                        
                        # data["recommendations"] es la lista de recomendaciones
                        recommendations = data["recommendations"]
                        n_cols = 4 # Máximo de columnas por fila

                        # Mostramos cada recomendación con la animación de flip
                    for i in range(0, len(recommendations), n_cols):
                        row = recommendations[i : i + n_cols]
                        # Creamos tantas columnas como recomendaciones haya en este bloque
                        cols = st.columns(len(row))

                        for j, rec in enumerate(row):
                            with cols[j]:
                                poster = rec.get("poster", "")
                                overview = rec.get("overview", "Sin descripción.")
                                title = rec.get("title", "Título no disponible")

                                # Convertir géneros de string a lista, si hace falta
                                import ast
                                genres_str = rec.get("genres", "[]")
                                try:
                                    genres_list = ast.literal_eval(genres_str)
                                except:
                                    genres_list = []
                                # Formatear géneros en backticks
                                genres_md = ", ".join([f"`{g}`" for g in genres_list])

                                # Estructura HTML para flip-card
                                card_html = f"""
                                <div class="flip-card">
                                    <div class="flip-card-inner">
                                        <div class="flip-card-front">
                                            <img src="{poster}" alt="Poster">
                                        </div>
                                        <div class="flip-card-back">
                                            <p>{overview}</p>
                                        </div>
                                    </div>
                                </div>
                                """

                                st.markdown(f"**Recomendación {i + j + 1}:**")
                                st.markdown(card_html, unsafe_allow_html=True)
                                st.write(f"- **Título:** {title}")
                                st.write(f"- **Géneros:** {genres_md}")
                                st.write(f"- **Puntuación:** {rec.get('vote_average')}")
                                st.write(f"- **Popularidad:** {rec.get('popularity')}")
                                st.write("---")
                else:
                    st.error("Error al consultar la API.")
            except Exception as e:
                st.error(f"Error: {e}")


if __name__ == "__main__":
    main()