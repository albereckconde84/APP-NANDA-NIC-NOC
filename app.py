import streamlit as st
import json
import os

# Configuración inicial
st.set_page_config(page_title="Sistema de Enfermería", page_icon="🩺", layout="wide")

# --- 1. CARGA SEGURA DE DATOS ---
def cargar_nanda():
    path = "nanda_data.json"
    if not os.path.exists(path):
        st.error(f"❌ ERROR: No se encuentra el archivo '{path}' en la carpeta raíz.")
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"❌ ERROR al leer el JSON: {e}")
        return {}

diccionario_nanda = cargar_nanda()

# --- 2. BARRA LATERAL ---
with st.sidebar:
    opcion = st.radio("Selecciona una función:", [
        "👥 Control de Pacientes", 
        "🧠 Gestión del PAE", 
        "🧮 Calculadora de Goteo", 
        "📖 Diccionario NNN"
    ])

# --- 3. LÓGICA DE NAVEGACIÓN ---

if opcion == "👥 Control de Pacientes":
    st.title("👥 Control de Pacientes")
    # Pega aquí todo tu bloque original de pacientes

elif opcion == "🧠 Gestión del PAE":
    st.title("🧠 Gestión del PAE")
    if not diccionario_nanda:
        st.warning("⚠️ La base de datos NANDA no está cargada.")
    else:
        # Pega aquí el formulario de valoración que configuramos
        st.write("Formulario de valoración listo.")

elif opcion == "🧮 Calculadora de Goteo":
    st.title("🧮 Calculadora de Goteo")
    # Pega aquí tu código de calculadora

elif opcion == "📖 Diccionario NNN":
    st.title("📖 Diccionario NNN")
    if not diccionario_nanda:
        st.error("No hay datos para mostrar.")
    else:
        busqueda = st.text_input("Buscar diagnóstico:")
        # Aquí va la lógica de filtrado del diccionario
        for dx, datos in diccionario_nanda.items():
            if busqueda.lower() in dx.lower():
                st.write(f"### {dx}")
