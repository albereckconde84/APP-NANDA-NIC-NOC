import streamlit as st
from datetime import datetime

# Configuración de la pantalla móvil
st.set_page_config(page_title="PAE Móvil Profesional", page_icon="🩺", layout="centered")

st.title("🩺 Asistente Digital PAE")
st.write("Herramienta de Gestión Hospitalaria y Proceso de Atención de Enfermería.")
st.markdown("---")

# Registro del profesional (Simulado para el reporte)
enfermero = st.text_input("👤 Nombre del Enfermero/a responsable:", "Enf. Alexander")

st.markdown("---")

# 1. MÓDULO DE VALORACIÓN (Signos y Síntomas)
st.header("1. Valoración Clínica")
st.write("Selecciona las características definitorias presentes en el paciente:")

sintoma_frio = st.checkbox("Temperatura corporal por debajo de 36.5 °C / Piel fría")
sintoma_escalofrio = st.checkbox("Escalofríos / Piloerección / Cianosis periférica")
sintoma_respiratorio = st.checkbox("Pausas en la respiración (Apnea) / Disnea")
sintoma_oxigeno = st.checkbox("Baja saturación de oxígeno ($SpO_2 < 90\%$)")
sintoma_autocuidado = st.checkbox("Incapacidad para lavar el cuerpo o realizar higiene")
sintoma_atencion = st.checkbox("Dificultad para concentrarse u omisión de tareas")

st.markdown("---")

# 2. MÓDULO DE DIAGNÓSTICO, NOC Y NIC
st.header("2. Juicio Clínico y Plan de Cuidados")

diagnosticos_activos = 0
resumen_cuidados = [] # Lista para almacenar lo que se hace en el turno

# --- CASO 1: HIPOTERMIA ---
if sintoma_frio or sintoma_escalofrio:
    diagnosticos_activos += 1
    st.error("🚨 DIAGNÓSTICO NANDA: [00006] Hipotermia")
    
    st.info("🎯 **Resultado NOC: [0800] Termorregulación**")
    puntos_hipo = st.slider("Indicador: Temperatura cutánea normal", 1, 5, value=2, key="noc_hipo")
    
    st.success("📋 **Intervención NIC: [3900] Regulación de la temperatura**")
    act1 = st.checkbox("Monitorear la temperatura corporal cada 15-30 minutos.")
    act2 = st.checkbox("Aplicar mantas calientes o calentamiento pasivo.")
    act3 = st.checkbox("Mantener un ambiente hospitalario templado.")
    
    # Almacenar datos para el reporte final si se ejecutan
    actividades_hechas = [a for a, m in [("Monitoreo de temp.", act1), ("Mantas calientes", act2), ("Control ambiental", act3)] if m]
    resumen_cuidados.append({"dx": "Hipotermia", "noc_inicial": 2, "noc_final": puntos_hipo, "actividades": actividades_hechas})
    st.markdown("---")

# --- CASO 2: APNEA (Patrón respiratorio ineficaz) ---
if sintoma_respiratorio or sintoma_oxigeno:
    diagnosticos_activos += 1
    st.error("🚨 DIAGNÓSTICO NANDA: [00032] Patrón respiratorio ineficaz")
    
    st.info("🎯 **Resultado NOC: [0415] Estado respiratorio**")
    puntos_apnea = st.slider("Indicador: Saturación de oxígeno e intercambio gaseoso", 1, 5, value=2, key="noc_apnea")
    
    st.success("📋 **Intervención NIC: [3350] Monitorización respiratoria**")
    act4 = st.checkbox("Vigilar la frecuencia, ritmo, profundidad y esfuerzo respiratorio.")
    act5 = st.checkbox("Administrar oxígeno suplementario según prescripción.")
    act6 = st.checkbox("Colocar al paciente en posición Semi-Fowler (45°).")
    
    actividades_hechas = [a for a, m in [("Monitoreo respiratorio", act4), ("Oxigenoterapia", act5), ("Posición Semi-Fowler", act6)] if m]
    resumen_cuidados.append({"dx": "Patrón respiratorio ineficaz", "noc_inicial": 2, "noc_final": puntos_apnea, "actividades": actividades_hechas})
    st.markdown("---")

# --- CASO 3: DÉFICIT DE AUTOCUIDADO ---
if sintoma_autocuidado or sintoma_atencion:
    diagnosticos_activos += 1
    st.error("🚨 DIAGNÓSTICO NANDA: [00108] Déficit de autocuidado: Baño")
    
    st.info("🎯 **Resultado NOC: [0305] Autocuidado: Higiene**")
    puntos_auto = st.slider("Indicador: Capacidad para mantener la higiene personal", 1, 5, value=1, key="noc_auto")
    
    st.success("📋 **Intervención NIC: [1801] Ayuda con el autocuidado: Baño**")
    act7 = st.checkbox("Proporcionar asistencia en el baño/higiene.")
    act8 = st.checkbox("Alentar la participación activa del paciente.")
    act9 = st.checkbox("Monitorizar la integridad cutánea durante el aseo.")
    
    actividades_hechas = [a for a, m in [("Asistencia en baño", act7), ("Fomento de autonomía", act8), ("Monitoreo cutáneo", act9)] if m]
    resumen_cuidados.append({"dx": "Déficit de autocuidado: Baño", "noc_inicial": 1, "noc_final": puntos_auto, "actividades": actividades_hechas})
    st.markdown("---")

# 3. MÓDULO DE EJECUCIÓN Y EVALUACIÓN (CIERRE DE TURNO)
if diagnosticos_activos > 0:
    st.header("3. Cierre de Turno y Evaluación")
    st.write("Al terminar tus intervenciones, presiona el botón para procesar el reporte oficial.")
    
    # Botón principal de guardado
    if st.button("💾 Finalizar Turno y Registrar Cuidados", type="primary"):
        st.balloons() # Animación festiva de éxito
        st.success("✅ ¡Registrado exitosamente en el historial del paciente!")
        
        # GENERACIÓN DEL REPORTE AUTOMÁTICO
        st.markdown("### 📋 REPORTE CLÍNICO GENERADO")
        st.text(f"Fecha/Hora de Cierre: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        st.text(f"Responsable del Turno: {enfermero}")
        st.markdown("---")
        
        # Redacción automática de la evolución clínica
        nota_evolucion = f"Se recibe paciente en el turno. Tras la valoración clínica de enfermería se identifican necesidades prioritarias. "
        
        for item in resumen_cuidados:
            st.write(f"📌 **Diagnóstico Tratado:** {item['dx']}")
            st.write(f"📈 **Evolución del Indicador (NOC):** Inició en {item['noc_inicial']}/5 ➔ Finalizó en {item['noc_final']}/5")
            
            if item['actividades']:
                st.write(f"✅ **Intervenciones completadas (NIC):** {', '.join(item['actividades'])}")
                nota_evolucion += f"Se ejecuta plan de cuidados enfocado en {item['dx']}, realizando intervenciones de: {', '.join(item['actividades'])}. "
            else:
                st.write("⚠️ *No se marcaron actividades realizadas para este diagnóstico.*")
            
            nota_evolucion += f"Se evalúa efectividad de los cuidados mediante indicador NOC, logrando una evolución de puntuación basal de {item['noc_inicial']}/5 a una puntuación final de {item['noc_final']}/5. "
            st.markdown("---")
        
        # Mostrar la Nota de Enfermería para copiar y pegar
        nota_evolucion += f"Queda paciente estable al cuidado del siguiente turno. Firmado: {enfermero}."
        st.subheader("📝 Nota de Evolución de Enfermería Automática:")
        st.info(nota_evolucion)
        
else:
    st.warning("⏱️ El sistema está listo. Selecciona los síntomas arriba para activar el Proceso de Enfermería.")
