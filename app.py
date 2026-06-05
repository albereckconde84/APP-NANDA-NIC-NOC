import streamlit as st
from datetime import datetime

# Configuración de la pantalla móvil y estilo
st.set_page_config(page_title="SICE - Enfermería Pro", page_icon="🩺", layout="centered")

# --- ESTILOS VISUALES PARA MÓVIL ---
st.markdown("""
    <style>
    .main .block-container { padding-top: 2rem; }
    div.stButton > button:first-child { width: 100%; margin-top: 10px; }
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
    st.write("Sistema Integral de Cuidados de Enfermería")
    opcion = st.radio("Selecciona una función:", [
        "👥 Control de Pacientes",
        "🧠 Gestión del PAE",
        "🧮 Calculadora de Goteo",
        "📖 Diccionario NNN"
    ])
    st.markdown("---")
    enfermero = st.text_input("👤 Profesional de Guardia:", "Enf. Alexander")

# --- BASE DE DATOS EXPANDIDA (Diccionario Clínico) ---
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
        "causas": "Ansiedad, deformidad de la pared torácica, fatiga de los músculos respiratorios, síndrome de hipoventilación.",
        "noc": "[0415] Estado respiratorio | [0403] Estado respiratorio: ventilación",
        "nic": "[3350] Monitorización respiratoria | [3140] Manejo de la vía aérea | [3320] Oxigenoterapia"
    },
    "Déficit de autocuidado: Baño": {
        "codigo": "[00108]", "dominio": "4", "clase": "5",
        "definicion": "Deterioro de la capacidad para realizar o completar por sí mismo las actividades de baño/higiene.",
        "causas": "Debilidad, trastornos cognitivos, barreras ambientales, dolor, alteración de la movilidad.",
        "noc": "[0305] Autocuidado: Higiene | [0300] Autocuidado: Actividades de la vida diaria",
        "nic": "[1801] Ayuda con el autocuidado: Baño/Higiene | [1610] Baño a la cama"
    },
    "Dolor agudo": {
        "codigo": "[00132]", "dominio": "12", "clase": "1",
        "definicion": "Experiencia sensitiva y emocional desagradable aproximada a un daño tisular real o potencial, de inicio súbito o lento.",
        "causas": "Agentes lesivos biológicos, químicos, físicos o psicológicos.",
        "noc": "[1605] Control del dolor | [2102] Nivel del dolor",
        "nic": "[1400] Manejo del dolor | [2210] Administración de analgésicos"
    },
    "Riesgo de infección": {
        "codigo": "[00004]", "dominio": "11", "clase": "1",
        "definicion": "Vulnerable a una invasión y multiplicación de organismos patógenos, que puede comprometer la salud.",
        "causas": "Procedimientos invasivos, rotura de la integridad de la piel, defensas primarias inadecuadas.",
        "noc": "[1902] Control del riesgo | [0703] Severidad de la infección",
        "nic": "[6550] Protección contra las infecciones | [6540] Control de infecciones"
    }
}

# --- OPCIÓN 1: CONTROL DE PACIENTES ---
if opcion == "👥 Control de Pacientes":
    st.title("👥 Censo y Control de Pacientes")
    st.write("Gestiona los ingresos y asignación de camas en tu servicio.")
    
    st.markdown("---")
    st.subheader("➕ Registrar Nuevo Ingreso / Cambio de Cama")
    nueva_cama = st.text_input("Número de Cama / Ubicación:", placeholder="Ej: Cama 105, Cuna 2")
    nuevo_nombre = st.text_input("Nombre y Apellido del Paciente:", placeholder="Ej: Pedro José Infante")
    nueva_nota = st.text_area("Nota de Ingreso / Diagnóstico Médico:", placeholder="Ej: Neumonía bilateral...")
    
    if st.button("➕ Registrar en el Censo"):
        if nueva_cama and nuevo_nombre:
            st.session_state.lista_pacientes.append({
                "cama": nueva_cama, "nombre": nuevo_nombre, "nota": nueva_nota if nueva_nota else "Sin notas adicionales."
            })
            st.success(f"✅ ¡Paciente {nuevo_nombre} asignado con éxito a la {nueva_cama}!")
        else:
            st.error("⚠️ Por favor, rellena al menos la Cama y el Nombre del paciente.")
            
    st.markdown("---")
    st.subheader("📋 Pacientes Actualmente en Sala")
    opciones_pacientes = [f"{p['cama']} - {p['nombre']}" for p in st.session_state.lista_pacientes]
    paciente_sel = st.selectbox("Selecciona un paciente para revisar su reporte:", opciones_pacientes)
    indice_sel = opciones_pacientes.index(paciente_sel)
    paciente_actual = st.session_state.lista_pacientes[indice_sel]
    
    st.info(f"📋 **Condición médica actual:** {paciente_actual['nota']}")

# --- OPCIÓN 2: GESTIÓN DEL PAE ---
elif opcion == "🧠 Gestión del PAE":
    st.title("🧠 Razonamiento Clínico Dinámico")
    opciones_pacientes = [f"{p['cama']} - {p['nombre']}" for p in st.session_state.lista_pacientes]
    paciente_sel = st.selectbox("Evaluando al paciente:", opciones_pacientes)
    indice_sel = opciones_pacientes.index(paciente_sel)
    paciente_actual = st.session_state.lista_pacientes[indice_sel]
    
    st.subheader(f"📌 Plan de Cuidados para: {paciente_actual['nombre']} ({paciente_actual['cama']})")
    st.markdown("---")
    
    st.write("**1. Valoración (Signos y Síntomas)**")
    sintoma_frio = st.checkbox("Temperatura corporal < 36.5 °C / Piel fría")
    sintoma_escalofrio = st.checkbox("Escalofríos o Cianosis periférica")
    sintoma_respiratorio = st.checkbox("Pausas respiratorias (Apnea) o Disnea")
    sintoma_oxigeno = st.checkbox("Baja saturación de oxígeno ($SpO_2 < 90\%$)")
    sintoma_autocuidado = st.checkbox("Incapacidad para realizar higiene por sí mismo")
    sintoma_atencion = st.checkbox("Dificultad para concentrarse / Omisión de tareas")

    st.markdown("---")
    st.write("**2. Diagnóstico y Planificación**")
    dx_activos = 0
    resumen_cuidados = []

    if sintoma_frio or sintoma_escalofrio:
        dx_activos += 1
        st.error("🚨 NANDA: [00006] Hipotermia")
        p_hipo = st.slider("NOC [0800]: Temperatura cutánea normal", 1, 5, value=2, key="p_hipo")
        act1 = st.checkbox("Monitorear temperatura cada 15-30 min.", value=True, key="a1")
        act2 = st.checkbox("Aplicar mantas calientes.", key="a2")
        resumen_cuidados.append({"dx": "Hipotermia", "inicial": 2, "final": p_hipo, "acts": [a for a, m in [("Monitoreo de temp.", act1), ("Mantas calientes", act2)] if m]})

    if sintoma_respiratorio or sintoma_oxigeno:
        dx_activos += 1
        st.error("🚨 NANDA: [00032] Patrón respiratorio ineficaz")
        p_apnea = st.slider("NOC [0415]: Estado respiratorio", 1, 5, value=2, key="p_apnea")
        act3 = st.checkbox("Vigilar esfuerzo respiratorio.", value=True, key="a3")
        act4 = st.checkbox("Administrar oxígeno según orden médica.", key="a4")
        resumen_cuidados.append({"dx": "Patrón respiratorio ineficaz", "inicial": 2, "final": p_apnea, "acts": [a for a, m in [("Vigilar esfuerzo resp.", act3), ("Oxigenoterapia", act4)] if m]})

    if sintoma_autocuidado or sintoma_atencion:
        dx_activos += 1
        st.error("🚨 NANDA: [00108] Déficit de autocuidado: Baño")
        p_auto = st.slider("NOC [0305]: Autocuidado: Higiene", 1, 5, value=1, key="p_auto")
        act5 = st.checkbox("Asistir en el aseo general.", value=True, key="a5")
        act6 = st.checkbox("Monitorear integridad cutánea.", key="a6")
        resumen_cuidados.append({"dx": "Déficit de autocuidado: Baño", "inicial": 1, "final": p_auto, "acts": [a for a, m in [("Asistencia en baño", act5), ("Monitoreo cutáneo", key="a6")] if m]})

    if dx_activos > 0:
        st.markdown("---")
        st.write("**3. Registro de Evaluación**")
        if st.button("💾 Finalizar Turno y Registrar Cuidados", type="primary"):
            st.balloons()
            st.success("✅ Datos procesados con éxito.")
            st.markdown(f"### 📝 Nota de Enfermería (SOAPIE) - {paciente_actual['nombre']}")
            
            s_text = "Paciente refiere sintomatología asociada al motivo de ingreso hospitalario."
            o_text = f"Evidencias clínicas evaluadas en la {paciente_actual['cama']} por el {enfermero}. Diagnóstico médico: {paciente_actual['nota']}."
            a_text = ", ".join([item['dx'] for item in resumen_cuidados])
            p_text = "Restablecer patrones biológicos alterados y asegurar el confort."
            i_text = ". ".join([", ".join(item['acts']) for item in resumen_cuidados if item['acts']])
            e_text = ", ".join([f"Evolución NOC de {item['dx']}: {item['inicial']}/5 a {item['final']}/5" for item in resumen_cuidados])
            
            st.text_area("S (Subjetivo):", s_text, height=60)
            st.text_area("O (Objetivo):", o_text, height=60)
            st.text_area("A (Análisis/Dx):", f"Diagnósticos: {a_text}", height=60)
            st.text_area("P (Planificación):", p_text, height=60)
            st.text_area("I (Intervención):", f"Se ejecutó: {i_text}", height=60)
            st.text_area("E (Evaluación):", e_text, height=60)
    else:
        st.warning("⏱️ Selecciona los síntomas de valoración para activar la lógica clínica.")

# --- OPCIÓN 3: CALCULADORA DE GOTEO ---
elif opcion == "🧮 Calculadora de Goteo":
    st.title("🧮 Calculadora de Infusión Endovenosa")
    volumen = st.number_input("Volumen de la solución (ml):", min_value=1, value=500)
    horas = st.number_input("Tiempo de infusión (Horas):", min_value=1, value=8)
    ml_hora = volumen / horas
    gotas_min = (volumen * 20) / (horas * 60)
    st.markdown("### 📊 Resultado del Cálculo:")
    st.info(f"💧 Velocidad de infusión: **{ml_hora:.1f} ml/hora**")
    st.success(f"⏱️ Ritmo de goteo: **{gotas_min:.0f} gotas por minuto**")

# --- OPCIÓN 4: DICCIONARIO EXPANDIDO (NUEVO) ---
elif opcion == "📖 Diccionario NNN":
    st.title("📖 Vínculos NANDA, NOC y NIC")
    st.write("Consulta las definiciones y relaciones del lenguaje estandarizado.")
    
    busqueda = st.text_input("🔍 Busca por nombre o código (Ej: Dolor, Infección, 00032):")
    st.markdown("---")
    
    encontrado = False
    for dx, datos in diccionario_nanda.items():
        if busqueda.lower() in dx.lower() or busqueda.lower() in datos['codigo']:
            encontrado = True
            st.error(f"📋 {datos['codigo']} {dx}")
            st.write(f"**Ubicación Taxonómica:** Dominio {datos['dominio']} | Clase {datos['clase']}")
            
            # Sub-bloques organizados para la lectura clínica rápida
            with st.expander("📚 Ver Definición Oficial NANDA"):
                st.write(datos['definicion'])
                
            with st.expander("🧬 Factores Relacionados / Causas"):
                st.write(datos['causas'])
                
            with st.expander("🎯 Resultados Sugeridos (NOC)"):
                st.info(datos['noc'])
                
            with st.expander("📋 Intervenciones Sugeridas (NIC)"):
                st.success(datos['nic'])
            st.markdown("###")
            
    if not encontrado and busqueda != "":
        st.error("❌ No se encontró ese diagnóstico en el prototipo. Intenta con 'Dolor', 'Infección' o 'Hipotermia'.")
