import streamlit as st
import json
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Sistema de Enfermería", page_icon="🩺", layout="centered")

# --- CSS (Mantenido igual) ---
st.markdown("""
    <style>
    .main .block-container { padding-top: 1.5rem; max-width: 550px; }
    .titulo-principal { text-align: center; font-family: 'Arial Black', sans-serif; color: var(--text-color); font-size: 1.8rem; text-transform: uppercase; }
    .subtitulo-principal { text-align: center; color: #0284c7; font-weight: bold; margin-bottom: 25px; }
    div.stButton > button:first-child { background: linear-gradient(135deg, #0284c7 0%, #002855 100%); color: #ffffff !important; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- ESTADO Y CARGA DE DATOS ---
if "lista_pacientes" not in st.session_state:
    st.session_state.lista_pacientes = [
        {"cama": "104-A", "nombre": "María Pérez", "nota": "Post-operatorio inmediato."},
        {"cama": "104-B", "nombre": "Juan Blanco", "nota": "Síndrome febril."}
    ]

@st.cache_data
def cargar_nanda():
    if os.path.exists("nanda_data.json"):
        with open("nanda_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

data = cargar_nanda()

# --- MENÚ LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='color:#0284c7;'>🩺 Panel Clínico</h2>", unsafe_allow_html=True)
    opcion = st.radio("Selecciona una función:", [
        "👥 Control de Pacientes", "🧠 Gestión del PAE", "🧮 Calculadora de Goteo", "📖 Diccionario NNN"
    ])
    enfermero = st.text_input("👤 Profesional de Guardia:", "Enf. Alexander")

# --- LÓGICA DE NAVEGACIÓN ---
if opcion == "👥 Control de Pacientes":
    st.markdown('<div class="titulo-principal">Gestión de Pacientes</div>', unsafe_allow_html=True)
    # [Aquí iría tu formulario de registro original que ya tenías]
    st.write("Censo de sala: (Añade aquí tu lógica de registro de pacientes)")

elif opcion == "🧠 Gestión del PAE":
    st.markdown('<div class="titulo-principal">Proceso de Atención</div>', unsafe_allow_html=True)
    # --- AQUÍ ESTÁ LA LÓGICA QUE VISTE EN TU FOTO image_393f2c.png ---
    st.markdown("### 1. Valoración (Signos y Síntomas)")
    s1 = st.checkbox("Pausas respiratorias (Apnea) o Disnea")
    s2 = st.checkbox("Baja saturación de oxígeno (SpO2 < 90%)")
    
    if s1 or s2:
        st.error("🚨 NANDA DETECTADO: [00032] Patrón respiratorio ineficaz")
        val = st.slider("Estado respiratorio (NOC):", 1, 5, 3)
        if st.button("Finalizar Turno y Registrar"):
            st.success("Proceso completado.")
            st.text_area("Nota SOAPIE:", "Análisis generado automáticamente basado en síntomas marcados.")

elif opcion == "🧮 Calculadora de Goteo":
    st.markdown('<div class="titulo-principal">Calculadora de Goteo</div>', unsafe_allow_html=True)
    vol = st.number_input("Volumen (ml):", value=500)
    hrs = st.number_input("Horas:", value=8)
    st.success(f"Ritmo: {(vol*20)/(hrs*60):.0f} gotas/min")

elif opcion == "📖 Diccionario NNN":
    st.markdown('<div class="titulo-principal">Diccionario Clínico</div>', unsafe_allow_html=True)
    busqueda = st.text_input("🔍 Buscar diagnóstico:")
    for dx, datos in data.items():
        if busqueda.lower() in dx.lower():
            st.write(f"### 📋 {dx}")
            st.write(datos.get('definicion', 'Sin datos'))
