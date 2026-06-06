import streamlit as st
import json

# Configuración de página
st.set_page_config(page_title="Sistema de Gestión de Cuidado", layout="wide")

# Cargar datos
@st.cache_data
def cargar_datos():
    with open("nanda_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

data = cargar_datos()

# Lógica de Sugerencia Automática
def sugerir_diagnostico(texto_subjetivo, texto_objetivo):
    texto_total = (texto_subjetivo + " " + texto_objetivo).lower()
    
    if "frío" in texto_total or "temperatura baja" in texto_total:
        return "Hipotermia"
    elif "calor" in texto_total or "fiebre" in texto_total:
        return "Hipertermia"
    elif "dolor" in texto_total:
        return "Dolor agudo"
    elif "respiración" in texto_total or "aire" in texto_total:
        return "Patrón respiratorio ineficaz"
    elif "infección" in texto_total or "herida" in texto_total:
        return "Riesgo de infección"
    return None

# Título y navegación
st.title("🩺 Sistema de Gestión de Cuidado (PAE)")
opcion = st.sidebar.radio("Menú", ["🧠 Gestión del PAE", "Otras Herramientas"])

if opcion == "🧠 Gestión del PAE":
    st.header("📝 Valoración de Enfermería")
    
    with st.form("formulario_valoracion"):
        col1, col2 = st.columns(2)
        with col1:
            subjetivo = st.text_area("S: ¿Qué refiere el paciente?")
        with col2:
            objetivo = st.text_area("O: Hallazgos objetivos (Signos vitales, piel)")
        
        submitted = st.form_submit_button("Analizar Datos Clínicos")
    
    if submitted:
        if not subjetivo or not objetivo:
            st.error("⚠️ Debes completar los datos subjetivos y objetivos para el análisis.")
        else:
            st.success("Valoración capturada.")
            
            sugerencia = sugerir_diagnostico(subjetivo, objetivo)
            
            if sugerencia:
                st.info(f"🔍 El sistema sugiere: **{sugerencia}**")
                seleccion = sugerencia
            else:
                seleccion = st.selectbox("Seleccione diagnóstico manualmente:", list(data.keys()))
            
            # Despliegue de resultados
            diag = data[seleccion]
            st.markdown(f"### [ {diag['codigo']} ] {seleccion}")
            st.write(f"**Dominio:** {diag['dominio']} | **Clase:** {diag['clase']}")
            
            with st.expander("📖 Ver detalles técnicos"):
                st.write(f"**Definición:** {diag['definicion']}")
                st.write(f"**Causas:** {diag['causas']}")
            
            st.markdown("---")
            st.subheader("🚀 Plan de Cuidados (SOAPIE)")
            st.write(f"**🎯 NOC:** {diag['noc']}")
            st.write(f"**📋 NIC:** {diag['nic']}")
            
            st.caption("Nota: Los diagnósticos son sugerencias basadas en NANDA-I 2021-2023 y requieren validación profesional.")

elif opcion == "Otras Herramientas":
    st.write("Aquí puedes colocar el resto de tus funciones previas.")
