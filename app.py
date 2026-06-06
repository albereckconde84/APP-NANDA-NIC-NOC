import streamlit as st
import json
import os

# 1. CONFIGURACIÓN E INTERFAZ
st.set_page_config(page_title="Sistema de Enfermería", page_icon="🩺", layout="centered")

st.markdown("""
    <style>
    .main .block-container { padding-top: 1.5rem; max-width: 550px; }
    .titulo-principal { text-align: center; font-family: 'Arial Black', sans-serif; color: var(--text-color); font-size: 1.8rem; text-transform: uppercase; margin-bottom: 5px; }
    .subtitulo-principal { text-align: center; color: #0284c7; font-weight: bold; margin-bottom: 25px; }
    div.stButton > button:first-child { background: linear-gradient(135deg, #0284c7 0%, #002855 100%); color: #ffffff !important; border-radius: 12px; font-weight: bold; width: 100%; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

# 2. GESTIÓN DE ESTADO Y DATOS
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

diccionario_nanda = cargar_nanda()

# 3. MENÚ LATERAL
with st.sidebar:
    st.markdown("<h2 style='color:#0284c7;'>🩺 Panel Clínico</h2>", unsafe_allow_html=True)
    opcion = st.radio("Selecciona una función:", [
        "👥 Control de Pacientes", "🧠 Gestión del PAE", "🧮 Calculadora de Goteo", "📖 Diccionario NNN"
    ])
    enfermero = st.text_input("👤 Profesional de Guardia:", "Enf. Alexander")

# 4. LÓGICA DE MÓDULOS
if opcion == "👥 Control de Pacientes":
    st.markdown('<div class="titulo-principal">Gestión de Pacientes</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo-principal">👥 CENSO DE SALA</div>', unsafe_allow_html=True)
    nueva_cama = st.text_input("Número de Cama:", placeholder="Ej: Cama 105")
    nuevo_nombre = st.text_input("Nombre del Paciente:", placeholder="Ej: Pedro Pérez")
    nueva_nota = st.text_area("Nota de Ingreso:")
    if st.button("➕ Registrar en el Censo"):
        st.session_state.lista_pacientes.append({"cama": nueva_cama, "nombre": nuevo_nombre, "nota": nueva_nota})
        st.success("✅ Paciente registrado")
    
    st.subheader("📋 Pacientes en Sala")
    for p in st.session_state.lista_pacientes:
        st.info(f"**{p['cama']}** - {p['nombre']}: {p['nota']}")

elif opcion == "🧠 Gestión del PAE":
    st.markdown('<div class="titulo-principal">Proceso de Atención</div>', unsafe_allow_html=True)
    # (Aquí mantienes tu lógica de checkboxes y SOAPIE que tenías antes)
    st.info("Módulo PAE listo para usar. Asegúrate de tener los síntomas marcados arriba.")

elif opcion == "🧮 Calculadora de Goteo":
    st.markdown('<div class="titulo-principal">Calculadora</div>', unsafe_allow_html=True)
    vol = st.number_input("Volumen (ml):", value=500)
    hrs = st.number_input("Horas:", value=8)
    if st.button("Calcular"):
        st.success(f"Velocidad: {(vol/hrs):.1f} ml/h | Goteo: {(vol*20/(hrs*60)):.0f} gts/min")

elif opcion == "📖 Diccionario NNN":
    st.markdown('<div class="titulo-principal">Diccionario Clínico</div>', unsafe_allow_html=True)
    busqueda = st.text_input("🔍 Buscar diagnóstico:")
    for dx, datos in diccionario_nanda.items():
        if busqueda.lower() in dx.lower() or busqueda.lower() in datos.get('codigo', ''):
            st.write(f"### 📋 {datos.get('codigo')} {dx}")
            with st.expander("📚 Ver Detalles"):
                st.write(f"**Definición:** {datos.get('definicion')}")
                st.write(f"**NIC:** {datos.get('nic')}")
