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
    st.markdown('<div class="subtitulo-principal">🧠 RAZONAMIENTO CLÍNICO</div>', unsafe_allow_html=True)
    
    # Selección de paciente
    opciones_pacientes = [f"{p['cama']} - {p['nombre']}" for p in st.session_state.lista_pacientes]
    paciente_sel = st.selectbox("Evaluando al paciente:", opciones_pacientes)
    indice_sel = opciones_pacientes.index(paciente_sel)
    paciente_actual = st.session_state.lista_pacientes[indice_sel]
    
    st.subheader(f"📌 Plan: {paciente_actual['nombre']} ({paciente_actual['cama']})")
    st.markdown("---")
    
    # --- AQUÍ VA TU LÓGICA DE CHECKS Y FORMULARIO ---
    st.markdown("### 1. Valoración (Signos y Síntomas)")
    sintoma_frio = st.checkbox("Temperatura corporal < 36.5 °C / Piel fría")
    sintoma_escalofrio = st.checkbox("Escalofríos o Cianosis periférica")
    sintoma_respiratorio = st.checkbox("Pausas respiratorias (Apnea) o Disnea")
    sintoma_oxigeno = st.checkbox("Baja saturación de oxígeno (SpO2 < 90%)")
    sintoma_autocuidado = st.checkbox("Incapacidad para realizar higiene por sí mismo")
    sintoma_atencion = st.checkbox("Dificultad para concentrarse / Omisión de tareas")

    st.markdown("---")
    st.markdown("### 2. Diagnóstico y Planificación")
    
    dx_activos = 0
    resumen_cuidados = []

    if sintoma_frio or sintoma_escalofrio:
        dx_activos += 1
        st.error("🚨 **NANDA DETECTADO:** [00006] Hipotermia")
        p_hipo = st.slider("NOC [0800]: Temperatura cutánea", 1, 5, value=2, key="p_hipo")
        act1 = st.checkbox("Monitorear temperatura cada 15-30 min.", value=True, key="a1")
        act2 = st.checkbox("Aplicar mantas calientes.", key="a2")
        lista_acts = ["Monitoreo de temp." if act1 else "", "Mantas calientes" if act2 else ""]
        resumen_cuidados.append({"dx": "Hipotermia", "inicial": 2, "final": p_hipo, "acts": [a for a in lista_acts if a]})

    if sintoma_respiratorio or sintoma_oxigeno:
        dx_activos += 1
        st.error("🚨 **NANDA DETECTADO:** [00032] Patrón respiratorio ineficaz")
        p_apnea = st.slider("NOC [0415]: Estado respiratorio", 1, 5, value=2, key="p_apnea")
        act3 = st.checkbox("Vigilar esfuerzo respiratorio.", value=True, key="a3")
        act4 = st.checkbox("Administrar oxígeno.", key="a4")
        lista_acts = ["Vigilar esfuerzo resp." if act3 else "", "Oxigenoterapia" if act4 else ""]
        resumen_cuidados.append({"dx": "Patrón respiratorio ineficaz", "inicial": 2, "final": p_apnea, "acts": [a for a in lista_acts if a]})

    if dx_activos > 0:
        if st.button("💾 Finalizar Turno y Registrar"):
            st.success("✅ Proceso completado.")
            # Aquí generas el SOAPIE que ya tenías
            st.write("---")
            st.text_area("Nota SOAPIE (Análisis):", value="Análisis generado automáticamente basado en síntomas marcados.")

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
