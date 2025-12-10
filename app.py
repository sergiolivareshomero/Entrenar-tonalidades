import streamlit as st
import random

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Entrenador Armónico", layout="centered")

# CSS para mejorar la apariencia en móviles
# - Botones al 100% de ancho
# - Pestañas más grandes y fáciles de tocar
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        height: 50px;
        margin-bottom: 5px;
        font-weight: bold;
        border-radius: 10px;
    }
    /* Aumentar tamaño de fuente en pestañas */
    button[data-baseweb="tab"] {
        font-size: 1.2rem;
    }
    div[data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. LÓGICA MUSICAL ---
NOTAS_REALES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTAS_VISUALES = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
# Intervalos de la escala mayor (semitonos): T-T-S-T-T-T-S
INTERVALOS_MAYOR = [0, 2, 4, 5, 7, 9, 11] 
GRADOS_ROMANOS = ["I", "II", "III", "IV", "V", "VI", "VII"]
# Cualidades por grado en escala mayor: M, m, m, M, M, m, dim
CUALIDADES = ['M', 'm', 'm', 'M', 'M', 'm', 'dim']

# --- 3. FUNCIONES DE ESTADO ---

def generar_pregunta():
    """Genera una nueva pregunta aleatoria y la guarda en la sesión."""
    indice_ton = random.randint(0, 11)
    indice_grado = random.randint(0, 6)
    
    # Calcular respuesta correcta matemáticamente
    semitonos = INTERVALOS_MAYOR[indice_grado]
    indice_nota_resp = (indice_ton + semitonos) % 12
    nota_resp = NOTAS_REALES[indice_nota_resp]
    cualidad_resp = CUALIDADES[indice_grado]
    
    # Guardar todo en session_state para que no se pierda al recargar
    st.session_state['tonalidad_nombre'] = NOTAS_VISUALES[indice_ton]
    st.session_state['grado_nombre'] = GRADOS_ROMANOS[indice_grado]
    st.session_state['grado_numero'] = indice_grado + 1
    st.session_state['respuesta_correcta'] = f"{nota_resp}{cualidad_resp}"
    
    # Resetear mensajes
    st.session_state['mensaje'] = ""
    st.session_state['color_mensaje'] = "black"

def verificar(respuesta_usuario):
    """Comprueba si el botón pulsado es el correcto."""
    correcta = st.session_state['respuesta_correcta']
    
    if respuesta_usuario == correcta:
        st.session_state['mensaje'] = f"¡CORRECTO! ✅\nEra {respuesta_usuario}. Siguiente..."
        st.session_state['color_mensaje'] = "green"
        # Generar la siguiente pregunta inmediatamente para que aparezca tras el rerun
        generar_pregunta()
    else:
        st.session_state['mensaje'] = f"❌ Incorrecto. No es {respuesta_usuario}."
        st.session_state['color_mensaje'] = "red"

# Inicializar juego si es la primera vez que se carga
if 'respuesta_correcta' not in st.session_state:
    generar_pregunta()

# --- 4. INTERFAZ GRÁFICA (FRONTEND) ---

st.title("🎵 Entrenador Tonal")

# Panel de Pregunta (Diseño visual destacado)
st.markdown(f"""
    <div style="text-align: center; padding: 15px; background-color: #f0f2f6; border-radius: 15px; margin-bottom: 15px; border: 1px solid #ddd;">
        <h4 style="margin:0; color: #666; font-weight: normal;">Encuentra el acorde</h4>
        <h1 style="margin: 5px 0; font-size: 2.5em; color: #31333F;">Grado {st.session_state['grado_nombre']}</h1>
        <p style="font-size: 1.1em; margin:0;">({st.session_state['grado_numero']}) de <b>{st.session_state['tonalidad_nombre']} Mayor</b></p>
    </div>
""", unsafe_allow_html=True)

# Panel de Feedback (Mensajes de acierto/error)
if st.session_state['mensaje']:
    color = st.session_state['color_mensaje']
    if color == "green":
        st.success(st.session_state['mensaje'])
    else:
        st.error(st.session_state['mensaje'])

st.write("---")

# --- 5. BOTONERA ORGANIZADA EN PESTAÑAS ---
# Usamos pestañas para evitar el scroll infinito en el móvil
tab_mayor, tab_menor, tab_dis = st.tabs(["🔵 Mayores", "🔴 Menores", "⚪ Disminuidos"])

def crear_rejilla_botones(tab, sufijo_visual, sufijo_logico):
    """Crea una cuadrícula de 3x4 botones dentro de una pestaña"""
    with tab:
        # Creamos 3 columnas para que queden compactos
        cols = st.columns(3)
        for i, nota_vis in enumerate(NOTAS_VISUALES):
            nota_logica = NOTAS_REALES[i]
            
            # Repartimos los botones en las 3 columnas (0, 1, 2)
            columna_actual = cols[i % 3]
            
            with columna_actual:
                # Texto que ve el usuario vs Valor que usa el programa
                texto_boton = f"{nota_vis}{sufijo_visual}"
                valor_respuesta = f"{nota_logica}{sufijo_logico}"
                
                # Al pulsar, verificamos y recargamos la página
                if st.button(texto_boton, key=f"btn_{valor_respuesta}"):
                    verificar(valor_respuesta)
                    st.rerun()

# Generar contenido de cada pestaña
crear_rejilla_botones(tab_mayor, "", "M")      # Pestaña Mayores
crear_rejilla_botones(tab_menor, "m", "m")     # Pestaña Menores
crear_rejilla_botones(tab_dis, "dim", "dim")   # Pestaña Disminuidos
