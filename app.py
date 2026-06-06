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
        "nic": "[1400] Manejo del dolor | [2210] Administración de analgésicos"
    },
    "Riesgo de infección": {
        "codigo": "[00004]", "dominio": "11", "clase": "1",
        "definicion": "Vulnerable a una invasión y multiplicación de organismos patógenos.",
        "causas": "Procedimientos invasivos, rotura de la integridad de la piel.",
        "noc": "[1902] Control del riesgo | [0703] Severidad de la infección",
        "nic": "[6550] Protección contra las infections | [6540] Control de infecciones"
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
    
    st.info(f"📋 **Condición médica actual:** {paciente_actual['nota']}")

# --- OPCIÓN 2: GESTIÓN DEL PAE ---
elif opcion == "🧠 Gestión del PAE":
    st.markdown('<h1 class="titulo-sice">🧠 Razonamiento Clínico</h1>', unsafe_allow_html=True)
    opciones_pacientes = [f"{p['cama']} - {p['nombre']}" for p in st.session_state.lista_pacientes]
    paciente_sel = st.selectbox("Evaluando al paciente:", opciones_pacientes)
    indice_sel = opciones_pacientes.index(paciente_sel)
    paciente_actual = st.session_state.lista_pacientes[indice_sel]
    
    st.subheader(f"📌 Plan: {paciente_actual['nombre']} ({paciente_actual['cama']})")
    st.markdown("---")
    
    st.markdown("### 1. Valoración (Signos y Síntomas)")
    sintoma_frio = st.checkbox("Temperatura corporal < 36.5 °C / Piel fría")
    sintoma_escalofrio = st.checkbox("Escalofríos o Cianosis periférica")
    sintoma_respiratorio = st.checkbox("Pausas respiratorias (Apnea) o Disnea")
    sintoma_oxigeno = st.checkbox("Baja saturación de oxígeno ($SpO_2 < 90\%$)")
    sintoma_autocuidado = st.checkbox("Incapacidad para realizar higiene por sí mismo")
    sintoma_atencion = st.checkbox("Dificultad para concentrarse / Omisión de tareas")

    st.markdown("---")
    st.markdown("### 2. Diagnóstico y Planificación")
    
    dx_activos = 0
    resumen_cuidados = []

    if sintoma_frio or sintoma_escalofrio:
        dx_activos += 1
        st.error("🚨 **NANDA DETECTADO:** [00006] Hipotermia")
        st.warning("⚠️ **ALERTA:** No infundir soluciones endovenosas frías. Calentamiento gradual.")
        p_hipo = st.slider("NOC [0800]: Temperatura cutánea normal", 1, 5, value=2, key="p_hipo")
        st.write("**NIC [3900]:**")
        act1 = st.checkbox("Monitorear temperatura cada 15-30 min.", value=True, key="a1")
        act2 = st.checkbox("Aplicar mantas calientes.", key="a2")
        resumen_cuidados.append({"dx": "Hipotermia", "inicial": 2, "final": p_hipo, "acts": [a for a, m in [("Monitoreo de temp.", act1), ("Mantas calientes", act2)] if m]})

    if sintoma_respiratorio or sintoma_oxigeno:
        dx_activos += 1
        st.error("🚨 **NANDA DETECTADO:** [00032] Patrón respiratorio ineficaz")
        st.warning("⚠️ **ALERTA:** Mantener equipo de aspiración disponible a pie de cama.")
        p_apnea = st.slider("NOC [0415]: Estado respiratorio", 1, 5, value=2, key="p_apnea")
        st.write("**NIC [3350]:**")
        act3 = st.checkbox("Vigilar esfuerzo respiratorio.", value=True, key="a3")
        act4 = st.checkbox("Administrar oxígeno según orden médica.", key="a4")
        resumen_cuidados.append({"dx": "Patrón respiratorio ineficaz", "inicial": 2, "final": p_apnea, "acts": [a for a, m in [("Vigilar esfuerzo resp.", act3), ("Oxigenoterapia", act4)] if m]})

    if sintoma_autocuidado or sintoma_atencion:
        dx_activos += 1
        st.error("🚨 **NANDA DETECTADO:** [00108] Déficit de autocuidado: Baño")
        p_auto = st.slider("NOC [0305]: Autocuidado: Higiene", 1, 5, value=1, key="p_auto")
        st.write("**NIC [1801]:**")
        act5 = st.checkbox("Asistir en el aseo general.", value=True, key="a5")
        act6 = st.checkbox("Monitorear integridad cutánea.", value=True, key="a6")
        resumen_cuidados.append({"dx": "Déficit de autocuidado: Baño", "inicial": 1, "final": p_auto, "acts": [a for a, m in [("Asistencia en baño", act5), ("Monitoreo cutáneo", act6)] if m]})

    # Cerramos el bloque de diagnósticos e indicamos qué hacer si no hay ninguno marcado
    if dx_activos == 0:
        st.info("⏱️ **Esperando Valoración:** Selecciona arriba los signos y síntomas identificados en el paciente para calcular los diagnósticos de enfermería.")
    
    else:
        st.markdown("---")
        st.markdown("### 3. Registro de Evaluación")
        if st.button("💾 Finalizar Turno y Registrar Cuidados"):
            st.success("✅ **Proceso de Atención de Enfermería completado.** La automatización del modelo SOAPIE se ha cargado con éxito para este turno.")
            st.markdown(f"### 📝 Nota de Enfermería (SOAPIE)")
            
            s_text = "Paciente refiere sintomatología asociada al motivo de ingreso."
            o_text = f"Evidencias clínicas evaluadas en la {paciente_actual['cama']} por el {enfermero}."
            a_text = ", ".join([item['dx'] for item in resumen_cuidados])
            p_text = "Restablecer patrones biológicos alterados."
            i_text = ". ".join([", ".join(item['acts']) for item in resumen_cuidados if item['acts']])
            e_text = ", ".join([f"Evolución NOC de {item['dx']}: {item['inicial']}/5 a {item['final']}/5" for item in resumen_cuidados])
            
            st.text_area("S (Subjetivo):", s_text, height=60)
            st.text_area("O (Objetivo):", o_text, height=60)
            st.text_area("A (Análisis/DxE):", f"Diagnósticos de Enfermería: {a_text}", height=60)
            st.text_area("P (Planificación):", p_text, height=60)
            st.text_area("I (Intervención):", f"Se ejecutó: {i_text}", height=60)
            st.text_area("E (Evaluación):", e_text, height=60)

# --- OPCIÓN 3: CALCULADORA DE GOTEO ---
elif opcion == "🧮 Calculadora de Goteo":
    st.markdown('<h1 class="titulo-sice">🧮 Calculadora de Infusión</h1>', unsafe_allow_html=True)
    volumen = st.number_input("Volumen de la solución (ml):", min_value=1, value=500)
    horas = st.number_input("Tiempo de infusión (Horas):", min_value=1, value=8)
    ml_hora = volumen / horas
    gotas_min = (volumen * 20) / (horas * 60)
    st.markdown("### 📊 Resultado:")
    st.info(f"💧 Velocidad de infusión: **{ml_hora:.1f} ml/hora**")
    st.success(f"⏱️ Ritmo de goteo: **{gotas_min:.0f} gotas por minuto**")

# --- OPCIÓN 4: DICCIONARIO NNN ---
elif opcion == "📖 Diccionario NNN":
    st.markdown('<h1 class="titulo-sice">📖 Vínculos NANDA, NOC y NIC</h1>', unsafe_allow_html=True)
    busqueda = st.text_input("🔍 Busca por nombre o código (Ej: Dolor, Hipotermia):")
    st.markdown("---")
    
    encontrado = False
    for dx, datos in diccionario_nanda.items():
        if busqueda.lower() in dx.lower() or busqueda.lower() in datos['codigo']:
            encontrado = True
            
            st.markdown(f"### 📋 {datos['codigo']} {dx}")
            st.caption(f"**Ubicación:** Dominio {datos['dominio']} | Clase {datos['clase']}")
            
            with st.expander("📚 Ver Definición Oficial NANDA"):
                st.write(datos['definicion'])
            with st.expander("🧬 Factores Relacionados / Causas"):
                st.write(datos['causas'])
            with st.expander("🎯 Resultados Sugeridos (NOC)"):
                st.write(datos['noc'])
            with st.expander("📋 Intervenciones Sugeridas (NIC)"):
                st.write(datos['nic'])
            st.markdown("---")
            
    if not encontrado and busqueda != "":
        st.error("❌ No se encontró ese diagnóstico en el prototipo.")
