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

# --- MEMORIA Y DATOS ---
if "lista_pacientes" not in st.session_state:
    st.session_state.lista_pacientes = [
        {"cama": "104-A", "nombre": "María Pérez", "nota": "Post-operatorio inmediato."},
        {"cama": "104-B", "nombre": "Juan Blanco", "nota": "Síndrome febril."}
    ]

@st.cache_data
def cargar_nanda():
    with open("nanda_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

diccionario_nanda = cargar_nanda()

# --- NAVEGACIÓN ---
with st.sidebar:
    st.markdown("<h2 style='color:#0284c7;'>🩺 Panel Clínico</h2>", unsafe_allow_html=True)
    opcion = st.radio("Selecciona una función:", ["👥 Control de Pacientes", "🧠 Gestión del PAE", "🧮 Calculadora de Goteo", "📖 Diccionario NNN"])
    enfermero = st.text_input("👤 Profesional:", "Enf. Alexander")

# --- LÓGICA DE GESTIÓN DEL PAE ---
if opcion == "🧠 Gestión del PAE":
    st.markdown('<div class="titulo-principal">Proceso de Atención</div>', unsafe_allow_html=True)
    
    # 1. Selección de Paciente
    opciones_pacientes = [f"{p['cama']} - {p['nombre']}" for p in st.session_state.lista_pacientes]
    paciente_sel = st.selectbox("Evaluando al paciente:", opciones_pacientes)
    indice = opciones_pacientes.index(paciente_sel)
    paciente_actual = st.session_state.lista_pacientes[indice]
    
    st.markdown("### 1. Valoración (S y O)")
    col1, col2 = st.columns(2)
    with col1:
        subjetivo = st.text_area("S: ¿Qué refiere el paciente?")
    with col2:
        objetivo = st.text_area("O: Hallazgos objetivos (Signos vitales)")

    st.markdown("### 2. Signos Clínicos")
    # Chequeos rápidos que ayudan a la sugerencia automática
    s_frio = st.checkbox("Temperatura baja / Piel fría")
    s_resp = st.checkbox("Patrón respiratorio alterado")
    s_dolor = st.checkbox("Refiere dolor")
    
    if st.button("Analizar Caso y Sugerir Diagnóstico"):
        # Lógica de sugerencia inteligente
        sugerencia = None
        if s_frio: sugerencia = "Hipotermia"
        elif s_resp: sugerencia = "Patrón respiratorio ineficaz"
        elif s_dolor: sugerencia = "Dolor agudo"
        
        if sugerencia:
            st.success(f"🔍 El sistema sugiere el diagnóstico: **{sugerencia}**")
            dx = diccionario_nanda.get(sugerencia)
            if dx:
                st.info(f"**Código:** {dx['codigo']} | **Definición:** {dx['definicion']}")
                st.write(f"**NOC:** {dx['noc']}")
                st.write(f"**NIC:** {dx['nic']}")
        else:
            st.warning("No se detectó un patrón automático. Selecciona un diagnóstico del diccionario.")

# --- MANTENIMIENTO DE OTROS MÓDULOS ---
elif opcion == "👥 Control de Pacientes":
    # ... (Aquí tu código original de control de pacientes)
    st.write("Módulo de censo activo")

elif opcion == "🧮 Calculadora de Goteo":
    # ... (Aquí tu código original de calculadora)
    st.write("Calculadora activa")

elif opcion == "📖 Diccionario NNN":
    # ... (Aquí tu código original de diccionario)
    st.write("Diccionario activo")
