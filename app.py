import streamlit as st

# Configuración de la interfaz móvil y estilo base
st.set_page_config(page_title="Sistema de Enfermería", page_icon="🩺", layout="centered")

# --- IDENTIDAD VISUAL (COLORES CARACTERÍSTICOS + BLANCO) ---
st.markdown("""
    <style>
    /* Fondo principal claro y limpio */
    .main {
        background-color: #ffffff;
    }
    
    /* Ajuste del contenedor principal para dispositivos móviles */
    .main .block-container {
        padding-top: 1.5rem;
        max-width: 550px;
    }
    
    /* Título Principal - Azul Oscuro */
    .titulo-principal {
        text-align: center;
        font-family: 'Arial Black', Gadget, sans-serif;
        color: #002855; 
        font-size: 1.8rem;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Subtítulo de Sección - Azul Cian */
    .subtitulo-principal {
        text-align: center;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        color: #0284c7; 
        font-size: 1rem;
        font-weight: bold;
        margin-bottom: 25px;
    }

    /* Botón de Acción con degradado azul sobre fondo blanco */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #002855 0%, #0284c7 100%);
        color: #ffffff !important;
        border: none;
        padding: 14px 28px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 1.05rem;
        box-shadow: 0 4px 8px rgba(0, 40, 85, 0.15);
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 15px;
    }
    
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(2, 132, 199, 0.25);
        background: linear-gradient(135deg, #0284c7 0%, #002855 100%);
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
    st.markdown("<h2 style='color:#0284c7;'>🩺 Panel Clínico</h2>", unsafe_allow_html=True)
    st.write("Planificación de Cuidados de Enfermería")
    opcion = st.radio("Selecciona una función:", [
        "👥 Control de Pacientes",
        "🧠 Gestión del PAE",
        "🧮 Calculadora de Goteo",
        "📖 Diccionario NNN"
    ])
    st.markdown("---")
    enfermero = st.text_input("👤 Profesional de Guardia:", "Enf. Alexander")

# --- BASE DE DATOS CLÍNICA (Diccionario NNN) ---
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
        "nic": "[6550] Protección contra las infecciones | [6540] Control de infecciones"
    }
}

# --- OPCIÓN 1: CONTROL DE PACIENTES ---
if opcion == "👥 Control de Pacientes":
    st.markdown('<div class="titulo-principal">Gestión de Pacientes</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo-principal">👥 CENSO DE SALA</div>', unsafe_allow_html=True)
    
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
    st.markdown('<div class="titulo-principal">Proceso de Atención</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo-principal">🧠 RAZONAMIENTO CLÍNICO</div>', unsafe_allow_html=True)
    
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
        st.warning("⚠️ **ALERTA:** No infundir soluciones endovenosas frías. Calentamiento gradual.")
        p_hipo = st.slider("NOC [0800]: Temperatura cutánea normal", 1, 5, value=2, key="p_hipo")
        st.write("**NIC [3900]:**")
        act1 = st.checkbox("Monitorear temperatura cada 15-30 min.", value=True, key="a1")
        act2 = st.checkbox("Aplicar mantas calientes.", key="a2")
        
        lista_acts = []
        if act1: lista_acts.append("Monitoreo de temp.")
        if act2: lista_acts.append("Mantas calientes")
        resumen_cuidados.append({"dx": "Hipotermia", "inicial": 2, "final": p_hipo, "acts": lista_acts})

    if sintoma_respiratorio or sintoma_oxigeno:
        dx_activos += 1
        st.error("🚨 **NANDA DETECTADO:** [00032] Patrón respiratorio ineficaz")
        st.warning("⚠️ **ALERTA:** Mantener equipo de aspiración disponible a pie de cama.")
        p_apnea = st.slider("NOC [0415]: Estado respiratorio", 1, 5, value=2, key="p_apnea")
        st.write("**NIC [3350]:**")
        act3 = st.checkbox("Vigilar esfuerzo respiratorio.", value=True, key="a3")
        act4 = st.checkbox("Administrar oxígeno según orden médica.", key="a4")
        
        lista_acts = []
        if act3: lista_acts.append("Vigilar esfuerzo resp.")
        if act4: lista_acts.append("Oxigenoterapia")
        resumen_cuidados.append({"dx": "Patrón respiratorio ineficaz", "inicial": 2, "final": p_apnea, "acts": lista_acts})

    if sintoma_autocuidado or sintoma_atencion:
        dx_activos += 1
        st.error("🚨 **NANDA DETECTADO:** [00108] Déficit de autocuidado: Baño")
        p_auto = st.slider("NOC [0305]: Autocuidado: Higiene", 1, 5, value=1, key="p_auto")
        st.write("**NIC [1801]:**")
        act5 = st.checkbox("Asistir en el aseo general.", value=True, key="a5")
        act6 = st.checkbox("Monitorear integridad cutánea.", key="a6")
        
        lista_acts = []
        if act5: lista_acts.append("Asistencia en baño")
        if act6: lista_acts.append("Monitoreo cutáneo")
        resumen_cuidados.append({"dx": "Déficit de autocuidado: Baño", "inicial": 1, "final": p_auto, "acts": lista_acts})

    if dx_activos == 0:
        st.info("⏱️ **Esperando Valoración:** Selecciona arriba los signos y síntomas identificados en el paciente.")
    
    else:
        st.markdown("---")
        st.markdown("### 3. Registro de Evaluación")
        if st.button("💾 Finalizar Turno y Registrar Cuidados"):
            st.success("✅ **Proceso de Atención de Enfermería completado.**")
            st.markdown("### 📝 Nota de Enfermería (SOAPIE)")
            
            s_text = "Paciente refiere sintomatología asociada al motivo de ingreso."
            o_text = f"Evidencias clínicas evaluadas en la {paciente_actual['cama']} por el {enfermero}."
            
            lista_dxs = [item['dx'] for item in resumen_cuidados]
            a_text = f"Diagnósticos de Enfermería: {', '.join(lista_dxs)}"
            p_text = "Restablecer patrones biológicos alterados."
            
            todas_las_acts = []
            for item in resumen_cuidados:
                todas_las_acts.extend(item['acts'])
            i_text = f"Se ejecutó: {', '.join(todas_las_acts)}"
            
            lista_evs = [f"Evolución NOC de {item['dx']}: {item['inicial']}/5 a {item['final']}/5" for item in resumen_cuidados]
            e_text = ", ".join(lista_evs)
            
            st.text_area(label="S (Subjetivo):", value=s_text, height=70)
            st.text_area(label="O (Objetivo):", value=o_text, height=70)
            st.text_area(label="A (Análisis/DxE):", value=a_text, height=70)
            st.text_area(label="P (Planificación):", value=p_text, height=70)
            st.text_area(label="I (Intervención):", value=i_text, height=70)
            st.text_area(label="E (Evaluación):", value=e_text, height=70)

# --- OPCIÓN 3: CALCULADORA DE GOTEO ---
elif opcion == "🧮 Calculadora de Goteo":
    st.markdown('<div class="titulo-principal">Infusión Endovenosa</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo-principal">🧮 CALCULADORA DE GOTEO</div>', unsafe_allow_html=True)
    
    volumen = st.number_input("Volumen de la solución (ml):", min_value=1, value=500)
    horas = st.number_input("Tiempo de infusión (Horas):", min_value=1, value=8)
    ml_hora = volumen / horas
    gotas_min = (volumen * 20) / (horas * 60)
    st.markdown("### 📊 Resultado:")
    st.info(f"💧 Velocidad de infusión: **{ml_hora:.1f} ml/hora**")
    st.success(f"⏱️ Ritmo de goteo: **{gotas_min:.0f} gotas por minuto**")

# --- OPCIÓN 4: DICCIONARIO NNN ---
elif opcion == "📖 Diccionario NNN":
    st.markdown('<div class="titulo-principal">Diccionario Clínico</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo-principal">📖 VÍNCULOS NANDA, NOC Y NIC</div>', unsafe_allow_html=True)
    
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
