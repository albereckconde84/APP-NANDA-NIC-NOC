import streamlit as st

# Configuración de la pantalla móvil
st.set_page_config(page_title="PAE Móvil Avanzado", page_icon="🩺", layout="centered")

st.title("🩺 Asistente Digital PAE")
st.write("Planificación del Proceso de Atención de Enfermería en tiempo real.")
st.markdown("---")

# 1. MÓDULO DE VALORACIÓN (Signos y Síntomas)
st.header("1. Valoración Clínica")
st.write("Selecciona todas las características definitorias presentes en el paciente:")

# Formulario de síntomas organizado
sintoma_frio = st.checkbox("Temperatura corporal por debajo de 36.5 °C / Piel fría al tacto")
sintoma_escalofrio = st.checkbox("Escalofríos / Piloerección / Cianosis periférica")
sintoma_respiratorio = st.checkbox("Pausas en la respiración (Apnea) / Disnea")
sintoma_oxigeno = st.checkbox("Baja saturación de oxígeno ($SpO_2 < 90\%$) / Uso de músculos accesorios")
sintoma_autocuidado = st.checkbox("Incapacidad para lavar el cuerpo o realizar higiene por sí mismo")
sintoma_atencion = st.checkbox("Dificultad para concentrarse / Omisión de tareas de cuidado personal")

st.markdown("---")

# 2. MÓDULO DE DIAGNÓSTICO, NOC Y NIC (Lógica interconectada)
st.header("2. Juicio Clínico y Plan de Cuidados")

# Listas para verificar qué diagnósticos se activan
diagnosticos_activos = 0

# --- CASO 1: HIPOTERMIA ---
if sintoma_frio or sintoma_escalofrio:
    diagnosticos_activos += 1
    st.error("🚨 DIAGNÓSTICO NANDA: [00006] Hipotermia")
    st.caption("**Dominio 11:** Seguridad/Protección | **Clase 6:** Termorregulación")
    
    # NOC
    st.info("🎯 **Resultado NOC: [0800] Termorregulación**")
    puntos_hipo = st.slider("Indicador: Temperatura cutánea dentro del rango normal", 1, 5, value=2, key="noc_hipo")
    st.write(f"Puntuación basal actual: **{puntos_hipo} / 5** (Meta: Alcanzar 5)")
    
    # NIC
    st.success("📋 **Intervención NIC: [3900] Regulación de la temperatura**")
    st.checkbox("Actividad: Monitorear la temperatura corporal del paciente cada 15-30 minutos.")
    st.checkbox("Actividad: Aplicar mantas calientes o dispositivos de calentamiento pasivo.")
    st.checkbox("Actividad: Mantener un ambiente hospitalario templado y libre de corrientes de aire.")
    st.markdown("---")

# --- CASO 2: APNEA (Patrón respiratorio ineficaz) ---
if sintoma_respiratorio or sintoma_oxigeno:
    diagnosticos_activos += 1
    st.error("🚨 DIAGNÓSTICO NANDA: [00032] Patrón respiratorio ineficaz (Asociado a Apnea)")
    st.caption("**Dominio 4:** Actividad/Reposo | **Clase 4:** Respuestas cardiovasculares/pulmonares")
    
    # NOC
    st.info("🎯 **Resultado NOC: [0415] Estado respiratorio**")
    puntos_apnea = st.slider("Indicador: Saturación de oxígeno e intercambio gaseoso", 1, 5, value=2, key="noc_apnea")
    st.write(f"Puntuación basal actual: **{puntos_apnea} / 5** (Meta: Alcanzar 4 o 5)")
    
    # NIC
    st.success("📋 **Intervención NIC: [3350] Monitorización respiratoria / [3140] Manejo de la vía aérea**")
    st.checkbox("Actividad: Vigilar la frecuencia, ritmo, profundidad y esfuerzo de las respiraciones.")
    st.checkbox("Actividad: Administrar oxígeno suplementario según prescripción médica y necesidad.")
    st.checkbox("Actividad: Colocar al paciente en posición Semi-Fowler (45°) para favorecer la ventilación.")
    st.markdown("---")

# --- CASO 3: DÉFICIT DE AUTOCUIDADO (Atención/Cuidado) ---
if sintoma_autocuidado or sintoma_atencion:
    diagnosticos_activos += 1
    st.error("🚨 DIAGNÓSTICO NANDA: [00108] Déficit de autocuidado: Baño/Higiene")
    st.caption("**Dominio 4:** Actividad/Reposo | **Clase 5:** Autocuidado")
    
    # NOC
    st.info("🎯 **Resultado NOC: [0305] Autocuidado: Higiene**")
    puntos_auto = st.slider("Indicador: Capacidad para mantener la higiene personal de forma independiente", 1, 5, value=1, key="noc_auto")
    st.write(f"Puntuación basal actual: **{puntos_auto} / 5** (Meta: Alcanzar 3 o 4)")
    
    # NIC
    st.success("📋 **Intervención NIC: [1801] Ayuda con el autocuidado: Baño/Higiene**")
    st.checkbox("Actividad: Proporcionar asistencia hasta que el paciente sea totalmente capaz de asumir el autocuidado.")
    st.checkbox("Actividad: Alentar la participación del paciente en sus actividades de baño según su tolerancia.")
    st.checkbox("Actividad: Monitorizar la integridad cutánea del paciente durante el proceso de aseo.")
    st.markdown("---")

# Si no hay síntomas seleccionados
if diagnosticos_activos == 0:
    st.warning("⏱️ El sistema está listo. Selecciona los síntomas arriba para activar el Proceso de Enfermería.")
