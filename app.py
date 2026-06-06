import streamlit as st
from datetime import datetime

# Configuración de la pantalla móvil y estilo base
st.set_page_config(page_title="SICE - Enfermería Pro", page_icon="🩺", layout="centered")

# --- DISEÑO ADAPTATIVO CON VARIABLES DE STREAMLIT ---
st.markdown("""
    <style>
    /* Ajustes generales del contenedor móvil */
    .main .block-container {
        padding-top: 1.5rem;
        max-width: 550px;
    }
    
    /* Título principal con color adaptativo del tema */
    .titulo-sice {
        text-align: center;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: 700;
        margin-bottom: 20px;
    }

    /* Botón moderno que respeta el contraste */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: white !important;
        border: none;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
        width: 100%;
        margin-top: 15px;
    }
    
    div.stButton > button:first-child:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 12px rgba(2, 132, 199, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE MEMORIA PARA PACIENTES ---
if "lista_pacientes" not in st.session_state:
    st.session_state.lista_pacientes = [
        {"cama": "104-A", "nombre": "María Pérez", "nota": "Post-operatorio inmediato. Requiere monitorización respiratoria continua."},
        {"cama": "104-B", "nombre": "Juan Blanco", "nota": "Ingreso clínico por síndrome febril en estudio. Escalofríos constantes."}
    ]

# --- MENÚ DE NAVEGACIÓN LATERAL ---
with st.sidebar:
    st.header("🏥 Menú SICE")
    st.write("Sistema Integral de Cuidados")
    opcion = st.radio("Selecciona una función:", [
        "👥 Control de Pacientes",
        "🧠 Gestión del PAE",
        "🧮 Calculadora de Goteo",
        "📖 Diccionario NNN"
    ])
    st.markdown("---")
    enfermero = st.text_input("👤 Profesional de Guardia:", "Enf. Alexander")

# --- BASE DE DATOS (Diccionario Clínico) ---
diccionario_nanda = {
    "Hipotermia": {
        "codigo": "[00006]", "dominio": "11", "clase": "6",
        "definicion": "Temperatura corporal central por debajo del rango de variación normal debido a la falla de la termorregulación.",
        "causas": "Exposición al entorno frío, desnutrición, trauma, inactividad.",
        "noc": "[0800] Termorregulación | [0801] Termorregulación: recién nacido",
        "nic": "[3900] Regulación de la temperatura | [3800] Tratamiento de la hipotermia"
    },
    "Patrón respiratorio ineficaz": {
        "codigo": "[00032]", "dominio": "4", "clase": "4",
        "definicion": "La inspiración y/o espiración no proporciona una ventilación adecuada.",
        "causas": "Ansiedad, deformidad de la pared torácica, fatiga de los músculos respiratorios.",
        "noc": "[0415] Estado respiratorio | [0403] Estado respiratorio: ventilación",
        "nic": "[3350] Monitorización respiratoria | [3140] Manejo de la vía aérea"
    },
    "Déficit de autocuidado: Baño": {
        "codigo": "[00108]", "dominio": "4", "clase": "5",
        "definicion": "Deterioro de la capacidad para realizar o completar por sí mismo las actividades de baño/higiene.",
        "causas": "Debilidad, trastornos cognitivos, barreras ambientales, dolor.",
        "noc": "[0305] Autocuidado: Higiene | [0300] Autocuidado: AVDI",
        "nic": "[1801] Ayuda con el autocuidado: Baño/Higiene"
    },
    "Dolor agudo": {
        "codigo": "[00132]", "dominio": "12", "clase": "1",
        "definicion": "Experiencia sensitiva y emocional desagradable aproximada a un daño tisular real o potencial.",
        "causas": "Agentes lesivos biológicos, químicos, físicos o psicológicos.",
        "noc": "[1605] Control del dolor | [2102] Nivel del dolor",
        "nic": "[1400] Manejo del dolor | #2210 Administración de analgésicos"
    },
    "Riesgo de infección": {
        "codigo": "[00004]", "dominio": "11", "clase": "1",
        "definicion": "Vulnerable a una invasión y multiplicación de organismos patógenos.",
        "causas": "Procedimientos invasivos, rotura de la integridad de la piel.",
        "noc": "[1902] Control del riesgo | [0703] Severidad de la infección",
        "nic": "[6550] Protección contra las infecciones | [6540] Control de infecciones"
    }
}

# --- OPCIÓN 1: CONTROL DE PACIENTES ---
if opcion == "👥 Control de Pacientes":
    st.markdown('<h1 class="titulo-sice">👥 Censo de Pacientes</h1>', unsafe_allow_html=True)
    st.write("Gestiona los ingresos y asignación de camas en tu servicio.")
    
    st.markdown("---")
    st.subheader("➕ Registrar Nuevo Ingreso")
    nueva_cama = st.text_input("Número de Cama / Ubicación:", placeholder="Ej: Cama 105")
    nuevo_nombre = st.text_input("Nombre del Paciente:", placeholder="Ej: Pedro José Infante")
    nueva_nota = st.text_area("Nota de Ingreso / Diagnóstico Médico:", placeholder="Ej: Neumonía...")
    
    if st.button("➕ Registrar en el Censo"):
        if nueva_cama and nuevo_nombre:
            st.session_state.lista_pacientes.append({
                "cama": nueva_cama, "nombre": nuevo_nombre, "nota": nueva_nota if nueva_nota else "Sin notas."
            })
            st.success(f"✅ ¡Paciente {nuevo_nombre} asignado con éxito!")
            
    st.markdown("---")
    st.subheader("📋 Pacientes Actualmente en Sala")
    opciones_pacientes = [f"{p['cama']} - {p['nombre']}" for p in st.session_state.lista_pacientes]
    paciente_sel = st.selectbox("Selecciona un paciente para revisar su reporte:", opciones_pacientes)
    indice_sel = opciones_pacientes.index(paciente_sel)
    paciente_actual = st.session_state.lista_pacientes[indice_sel]
