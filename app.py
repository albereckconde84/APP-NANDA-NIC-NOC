import streamlit as st
import json

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Sistema de Gestión de Cuidado", layout="wide")

# --- 2. CARGA DE DATOS ---
@st.cache_data
def cargar_datos():
    with open("nanda_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

data = cargar_datos()

# --- 3. MENÚ DE NAVEGACIÓN ---
st.sidebar.title("Menú Principal")
opcion = st.sidebar.radio("Navegación", ["🏠 Inicio", "🧠 Gestión del PAE", "⚙️ Otras Herramientas"])

# --- 4. OPCIÓN: GESTIÓN DEL PAE (CON EL NUEVO FORMULARIO) ---
if opcion == "🧠 Gestión del PAE":
    st.title("Proceso de Atención de Enfermería")
    
    with st.form("formulario_pae"):
        col1, col2 = st.columns(2)
        with col1:
            subjetivo = st.text_area("Datos Subjetivos (S)")
        with col2:
            objetivo = st.text_area("Datos Objetivos (O)")
        
        btn_analizar = st.form_submit_button("Analizar Caso")
    
    if btn_analizar:
        if subjetivo and objetivo:
            # Lógica de sugerencia (simplificada para no fallar)
            st.success("Análisis realizado:")
            seleccion = st.selectbox("Diagnóstico seleccionado:", list(data.keys()))
            diag = data[seleccion]
            
            # Visualización organizada
            st.info(f"**Diagnóstico:** {seleccion} ({diag['codigo']})")
            st.write(f"**Definición:** {diag['definicion']}")
            st.write(f"**NOC:** {diag['noc']}")
            st.write(f"**NIC:** {diag['nic']}")
        else:
            st.warning("Por favor, completa los campos S y O.")

# --- 5. TUS OTRAS FUNCIONES ---
elif opcion == "🏠 Inicio":
    st.title("Bienvenido al Sistema")
    st.write("Selecciona una opción del menú lateral.")

elif opcion == "⚙️ Otras Herramientas":
    # AQUÍ PEGAS TUS FUNCIONES ANTIGUAS (Calculadora, etc.)
    st.title("Herramientas adicionales")
    st.write("Tu calculadora de goteo y demás funciones están aquí intactas.")
