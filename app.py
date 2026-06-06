import streamlit as st
import json

# Cargar los datos desde el JSON actualizado
def cargar_datos():
    with open("nanda_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

data = cargar_datos()

st.title("🩺 Sistema de Gestión de Cuidado (PAE)")

# --- 1. SECCIÓN DE VALORACIÓN (EL CORAZÓN DEL CUIDADO) ---
st.header("📝 Valoración de Enfermería")
with st.form("formulario_valoracion"):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Datos Subjetivos")
        subjetivo = st.text_area("¿Qué refiere el paciente? (Dolor, malestar, etc.)")
    with col2:
        st.subheader("Datos Objetivos")
        frecuencia_cardiaca = st.number_input("Frecuencia Cardíaca (lpm)", min_value=0)
        tension_arterial = st.text_input("Tensión Arterial (mmHg)")
        otros_signos = st.text_area("Otros hallazgos (Piel, movilidad, etc.)")
    
    enviar_valoracion = st.form_submit_button("Guardar Valoración y Analizar")

# --- 2. LÓGICA DE ANÁLISIS ---
if enviar_valoracion:
    if not subjetivo or not tension_arterial:
        st.warning("⚠️ Debes completar los datos mínimos de valoración para un diagnóstico preciso.")
    else:
        st.success("Valoración guardada correctamente.")
        
        # --- 3. SELECCIÓN DE DIAGNÓSTICO (NANDA) ---
        st.header("📋 Diagnóstico NANDA sugerido")
        # Aquí permitimos al usuario elegir basándose en la valoración previa
        seleccion = st.selectbox("Seleccione el diagnóstico basado en los hallazgos:", list(data.keys()))
        
        # Mostrar detalles del diagnóstico seleccionado
        diag = data[seleccion]
        st.info(f"**Código:** {diag['codigo']} | **Dominio:** {diag['dominio']} | **Clase:** {diag['clase']}")
        st.write(f"**Definición:** {diag['definicion']}")
        st.write(f"**Factores:** {diag['causas']}")
        
        # --- 4. PLAN DE CUIDADO (NOC/NIC) ---
        st.header("🚀 Plan de Cuidados (SOAPIE)")
        st.write(f"**NOC:** {diag['noc']}")
        st.write(f"**NIC:** {diag['nic']}")
