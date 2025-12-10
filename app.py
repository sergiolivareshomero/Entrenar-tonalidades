import streamlit as st
import random

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Entrenador Armónico", layout="centered")

# CSS para ajustar botones en móvil
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        margin-bottom: 5px;
    }
    div[data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA MUSICAL ---
NOTAS_REALES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTAS_VISUALES = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
INTERVALOS_MAYOR = [0, 2, 4, 5, 7, 9, 11] # Semitonos desde la tónica
GRADOS_ROMANOS = ["I", "II", "III", "IV", "V", "VI", "VII"]
CUALIDADES = ['M', 'm', 'm', 'M', 'M', 'm', 'dim']

# --- FUNCIONES DE ESTADO ---
def generar_pregunta():
    """Genera una nueva pregunta y la guarda en la sesión."""
    indice_ton = random.randint(0, 11)
    indice_grado = random.randint(0, 6)
    
    # Calcular respuesta correcta
    semitonos = INTERVALOS_MAYOR[indice_grado]
    indice_nota_resp = (indice_ton + semitonos) % 12
    nota_resp = NOTAS_REALES[indice_nota_resp]
    cualidad_resp = CUALIDADES[indice_grado]
    
    # Guardar en session_state
    st.session_state['tonalidad_nombre'] = NOTAS_VISUALES[indice_ton]
    st.session_state['grado_nombre'] = GRADOS_ROMANOS[indice_grado]
    st.session_state['grado_numero'] = indice_grado + 1
    st.session_state['respuesta_correcta'] = f"{nota_resp}{cualidad_resp}"
    st.session_state['mensaje'] = ""
    st.session_state['color_mensaje'] = "black"

def verificar(respuesta_usuario):
    """Callback cuando se pulsa un botón."""
    correcta = st.session_state['respuesta_correcta']
    
    if respuesta_usuario == correcta:
        st.session_state['mensaje'] = f"¡CORRECTO! Era {respuesta_usuario}. Siguiente..."
        st.session_state['color_mensaje'] = "green"
        # Generar la siguiente pregunta inmediatamente
        generar_pregunta()
    else:
        st.session_state['mensaje'] = f"Incorrecto, no es {respuesta_usuario}. Intenta de nuevo."
        st.session_state['color_mensaje'] = "red"

# --- INICIALIZACIÓN ---
if 'respuesta_correcta' not in st.session_state:
    generar_pregunta()

# --- INTERFAZ GRÁFICA (FRONTEND) ---
st.title("🎵 Entrenador Tonal")

# 1. Mostrar Pregunta
st.markdown(f"""
    <div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="margin:0; color: #555;">¿Cuál es el acorde?</h3>
        <h1 style="margin:0; font-size: 3em;">Grado {st.session_state['grado_nombre']}</h1>
        <p style="font-size: 1.2em;">({st.session_state['grado_numero']}) de <b>{st.session_state['tonalidad_nombre']} Mayor</b></p>
    </div>
""", unsafe_allow_html=True)

# 2. Mostrar Feedback
if st.session_state['mensaje']:
    color = st.session_state['color_mensaje']
    if color == "green":
        st.success(st.session_state['mensaje'])
    else:
        st.error(st.session_state['mensaje'])

st.write("---")

# 3. Botonera (Grid)
# Creamos 3 columnas: Mayor | Menor | Disminuido
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Mayor**")
with col2:
    st.markdown("**Menor**")
with col3:
    st.markdown("**Disminuido**")

# Iteramos las notas para crear las filas
for i, nota_vis in enumerate(NOTAS_VISUALES):
    nota_logica = NOTAS_REALES[i]
    
    # Botón Mayor
    with col1:
        if st.button(f"{nota_vis}", key=f"btn_{i}_M"):
            verificar(f"{nota_logica}M")
            st.rerun()

    # Botón Menor
    with col2:
        if st.button(f"{nota_vis}m", key=f"btn_{i}_m"):
            verificar(f"{nota_logica}m")
            st.rerun()

    # Botón Disminuido
    with col3:
        if st.button(f"dim", key=f"btn_{i}_dim"): # Texto corto para ahorrar espacio
            verificar(f"{nota_logica}dim")
            st.rerun()
