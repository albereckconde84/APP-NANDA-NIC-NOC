import streamlit as st
import json

# Configuración de interfaz
st.set_page_config(page_title="Sistema de Enfermería", page_icon="🩺", layout="wide")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .titulo-principal { text-align: center; font-family: 'Arial Black', sans-serif; color: var(--text-color); font-size: 1.8rem; text-transform: uppercase; }
    .subtitulo-principal { text-align: center; color: #0284c7; font-weight: bold; margin-bottom: 25px; }
    div.stButton > button { background: linear-gradient(135deg, #0284c7 0%, #002855 100%); color: white !important; border-radius: 12px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- MEMORIA DE PACIENTES ---
if "lista_pacientes" not in st.session_state:
    st.session_state.lista_pacientes = [
        {"cama": "104-A", "nombre": "María Pérez", "nota": "Post-operatorio inmediato."},
        {"cama": "104-B", "nombre": "Juan Blanco", "nota": "Síndrome febril."}
    ]

# --- DATOS NANDA ---
@st.cache_data
def cargar_nanda():
    with open("nanda_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

diccionario_nanda = cargar_nanda()

# --- BARRA LATERAL (EL ÚNICO MENÚ) ---
with st.sidebar:
    st.markdown("<h2 style='color:#0284c7;'>🩺 Panel Clínico</h2>", unsafe_allow_html=True)
    opcion = st.radio("Selecciona una función:", [
        "👥 Control de Pacientes", 
        "🧠 Gestión del PAE", 
        "🧮 Calculadora de Goteo", 
        "📖 Diccionario NNN"
    ])
    enfermero = st.text_input("👤 Profesional:", "Enf. Alexander")

# --- LÓGICA DE NAVEGACIÓN ---

# 1. CONTROL DE PACIENTES
if opcion == "👥 Control de Pacientes":
    st.markdown('<div class="titulo-principal">Gestión de Pacientes</div>', unsafe_allow_html=True)
    st.subheader("➕ Registrar Nuevo Ingreso")
    nueva_cama = st.text_input("Ubicación:", placeholder="Ej: Cama 105")
    nuevo_nombre = st.text_input("Nombre del Paciente:")
    if st.button("➕ Registrar en el Censo"):
        st.session_state.lista_pacientes.append({"cama": nueva_cama, "nombre": nuevo_nombre, "nota": "Sin notas."})
        st.success("✅ Paciente registrado")
    
    st.subheader("📋 Pacientes en Sala")
    for p in st.session_state.lista_pacientes:
        st.info(f"**{p['cama']}** - {p['nombre']}")

# 2. GESTIÓN DEL PAE
elif opcion == "🧠 Gestión del PAE":
    st.markdown('<div class="titulo-principal">Proceso de Atención</div>', unsafe_allow_html=True)
    # Aquí va la lógica de valoración que configuramos antes...
    st.write("Módulo de PAE activo")

# 3. CALCULADORA
elif opcion == "🧮 Calculadora de Goteo":
    st.markdown('<div class="titulo-principal">Calculadora de Goteo</div>', unsafe_allow_html=True)
    vol = st.number_input("Volumen (ml):", value=500)
    hrs = st.number_input("Horas:", value=8)
    st.success(f"Ritmo: {(vol*20)/(hrs*60):.0f} gotas/min")

# 4. DICCIONARIO
elif opcion == "📖 Diccionario NNN":
    st.markdown('<div class="titulo-principal">Diccionario Clínico</div>', unsafe_allow_html=True)
    busqueda = st.text_input("🔍 Buscar:")
    # (Aquí tu lógica de búsqueda del diccionario)
