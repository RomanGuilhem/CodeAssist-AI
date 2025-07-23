import streamlit as st
import google.generativeai as genai
from PIL import Image
import toml

try:
    GOOGLE_API_KEY = st.secrets["api_key"]
except KeyError:
    try:
        secrets = toml.load(".streamlit/secrets.toml")
        GOOGLE_API_KEY = secrets["api_key"]
    except FileNotFoundError:
        st.error("No se encontró el archivo secrets.toml. Asegúrate de que exista y contenga la clave 'api_key'.")
        st.stop()
    except KeyError:
        st.error("El archivo secrets.toml no contiene la clave 'api_key'.")
        st.stop()
    except Exception as e:
        st.error(f"Error al cargar el archivo secrets.toml: {e}")
        st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

try:
    model = genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    st.error(f"Error al cargar el modelo: {e}. Asegúrate de tener instalada la última versión de google-generativeai.")
    st.stop()

def mostrar_imagen(imagen_path):
    try:
        imagen = Image.open(imagen_path)
        st.image(imagen, width=250)
    except FileNotFoundError:
        st.error(f"No se encontró la imagen: {imagen_path}")
    except Exception as e:
        st.error(f"Error al cargar la imagen: {e}")

st.title("CodeAssist AI con Messi")

opcion = st.sidebar.selectbox(
    "¿Qué querés hacer hoy?",
    ["Generar código", "Corregir código", "Explicar código"]
)

if opcion == "Generar código":
    st.subheader("Messi te ayuda a GENERAR código")
    mostrar_imagen("images/messi.genera.png")
    input_usuario = st.text_area("Escribí lo que querés que Messi programe por vos")

    if st.button("Generar"):
        try:
            response = model.generate_content(f"Hablá como si fueras Lionel Messi, siendo humilde, claro y argentino. Generá el siguiente código en el lenguaje más adecuado: {input_usuario}")
            st.markdown("Messi responde:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error al generar el código: {e}")

elif opcion == "Corregir código":
    st.subheader("Messi te ayuda a CORREGIR tu código")
    mostrar_imagen("images/messi.corrector.png")
    input_usuario = st.text_area("Pegá el código que querés corregir")

    if st.button("Corregir"):
        try:
            response = model.generate_content(f"Hablá como si fueras Messi y explicá qué errores tiene este código y cómo corregirlo, paso a paso, de forma clara y humilde:\n\n{input_usuario}")
            st.markdown("Messi responde:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error al corregir el código: {e}")

elif opcion == "Explicar código":
    st.subheader("Messi te ayuda a EXPLICAR tu código")
    mostrar_imagen("images/messi.explica.png")
    input_usuario = st.text_area("Pegá el código que querés que Messi explique")

    if st.button("Explicar"):
        try:
            response = model.generate_content(f"Imaginá que sos Lionel Messi y tenés que explicarle este código a alguien que está aprendiendo. Sé humilde, claro y amigable:\n\n{input_usuario}")
            st.markdown("Messi responde:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error al explicar el código: {e}")