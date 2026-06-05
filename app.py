import streamlit as st

# Configuración de la pantalla móvil
st.set_page_config(page_title="PAE Digital", page_icon="🩺", layout="centered")

st.title("🩺 Sistema de Soporte PAE")
st.write("Herramienta móvil para el Proceso de Atención de Enfermería")
st.markdown("---")

# 1. MÓDULO DE VALORACIÓN
st.header("1. Valoración del Paciente")
st.subheader("Características definitorias observadas:")

# Casillas de verificación para el enfermero
evidencia_1 = st.checkbox("El paciente refiere dolor (Escala EVA > 3)")
evidencia_2 = st.checkbox("Expresión facial de dolor (gestos, ceño fruncido)")
evidencia_3 = st.checkbox("Alteración de constantes vitales (Taquicardia, Taquipnea)")
evidencia_4 = st.checkbox("Postura de protección / Defensa de la zona")

st.markdown("---")

# 2. MÓDULO DE DIAGNÓSTICO (Lógica de asociación)
st.header("2. Diagnóstico Sugerido")

# Si el enfermero marca al menos 2 características, la app sugiere el diagnóstico NANDA
if (int(evidencia_1) + int(evidencia_2) + int(evidencia_3) + int(evidencia_4)) >= 2:
    st.error("🚨 DIAGNÓSTICO NANDA DETECTADO:")
    st.subheader("**[00132] Dolor agudo**")
    st.write("**Dominio 12:** Confort | **Clase 1:** Confort físico")
    
    st.markdown("---")
    
    # 3. MÓDULO DE PLANIFICACIÓN (NOC)
    st.header("3. Planificación (NOC)")
    st.info("🎯 Resultado sugerido para alcanzar:")
    st.subheader("**[1605] Control del dolor**")
    
    st.write("Evalúa el estado inicial del paciente (Escala de Likert):")
    # Escala Likert interactiva
    puntuacion_inicial = st.slider("Indicador: Refiere dolor controlado", 1, 5, value=2, 
                                   help="1: Nunca demostrado, 5: Siempre demostrado")
    
    st.write(f"Puntuación basal actual: **{puntuacion_inicial} / 5**")
    st.write("🎯 *Meta para el final del turno: Alcanzar puntuación de 4 o 5.*")
    
    st.markdown("---")
    
    # 4. MÓDULO DE INTERVENCIÓN/EJECUCIÓN (NIC)
    st.header("4. Ejecución (NIC)")
    st.success("📋 Plan de cuidados (Intervenciones requeridas):")
    st.subheader("**[1400] Manejo del dolor**")
    
    # Checklist de actividades para el enfermero en el turno
    st.checkbox("Actividad: Realizar una valoración exhaustiva del dolor (localización, características, duración).")
    st.checkbox("Actividad: Asegurar que el paciente reciba los analgésicos correspondientes según prescripción médica.")
    st.checkbox("Actividad: Enseñar el uso de técnicas no farmacológicas (relajación, musicoterapia, calor/frío).")
    st.checkbox("Actividad: Monitorizar el grado de satisfacción del paciente con el alivio del dolor a intervalos especificados.")

else:
    st.warning("⏱️ Esperando datos de valoración... (Selecciona al menos 2 síntomas para generar el proceso).")
