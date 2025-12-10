import streamlit as st
import random

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Entrenador Armónico", layout="centered")

# CSS OPTIMIZADO PARA MÓVIL Y GRID 3x4 COMPACTO
st.markdown("""
    <style>
    /* Estilo de los botones para que sean pequeños y quepan dos rejillas */
    .stButton button {
        width: 100%;
        margin: 0px 0px 4px 0px !important;
        padding: 0px !important;
        font-size: 0.75rem !important; /* Letra más pequeña para que quepa */
        font-weight: bold;
        height: 35px; /* Altura fija para uniformidad */
        line-height: 1.2;
    }
    
    /* Reducir espacio entre columnas */
    div[data-testid="column"] {
        padding: 0 2px !important;
    }
    
    /* Ajustes generales del contenedor */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }
    
    /* Títulos de las cajas más pequeños */
    h5 {
        font-size: 0.9rem !important;
        text-align: center;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. LÓGICA MUSICAL ---
NOTAS_REALES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTAS_VISUALES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'] 
# He simplificado las notas visuales (quitando los bemoles /Db) para que el texto sea más corto
# y quepa mejor en la cuadrícula compacta del móvil.

INTERVALOS_MAYOR = [0, 2, 4, 5, 7, 9, 11] 
GRADOS_ROMANOS = ["I", "II", "III", "IV", "V", "VI", "VII"]
CUALIDADES = ['M', 'm', 'm', 'M', 'M', 'm', 'dim']

# --- 3. FUNCIONES DE ESTADO ---

def generar_pregunta():
    """Genera pregunta aleatoria (Excluyendo Grado VII/Disminuido)."""
    indice_ton = random.randint(0, 11)
    # Rango 0-5 para excluir el 6 (VII dim)
    indice_grado = random.randint(0, 5)
    
    semitonos = INTERVALOS_MAYOR[indice_grado]
    indice_nota_resp = (indice_ton + semitonos) % 12
    nota_resp = NOTAS_REALES[indice_nota_resp]
    cualidad_resp = CUALIDADES[indice_grado]
    
    st.session_state['tonalidad_nombre'] = NOTAS_VISUALES[indice_ton]
    st.session_state['grado_nombre'] = GRADOS_ROMANOS[indice_grado]
    st.session_state['grado_numero'] = indice_grado + 1
    st.session_state['respuesta_correcta'] = f"{nota_resp}{cualidad_resp}"
    st.session_state['mensaje'] = ""
    st.session_state['color_mensaje'] = "black"

def verificar(respuesta_usuario):
    correcta = st.session_state['respuesta_correcta']
    if respuesta_usuario == correcta:
        st.session_state['mensaje'] = f"¡BIEN! ✅ {respuesta_usuario}"
        st.session_state['color_mensaje'] = "green"
        generar_pregunta()
    else:
        st.session_state['mensaje'] = f"❌ No es {respuesta_usuario}"
        st.session_state['color_mensaje'] = "red"

if 'respuesta_correcta' not in st.session_state:
    generar_pregunta()

# --- 4. INTERFAZ GRÁFICA ---

st.title("🎵 Entrenador Tonal")

# Panel Pregunta
st.markdown(f"""
    <div style="text-align: center; padding: 10px; background-color: #f1f3f6; border-radius: 10px; margin-bottom: 10px; border: 1px solid #ddd;">
        <h4 style="margin:0; color: #888; font-size: 0.8em;">ACORDE A ENCONTRAR</h4>
        <h2 style="margin: 0; color: #333;">Grado {st.session_state['grado_nombre']}</h2>
        <p style="font-size: 0.9em; margin:0;">de <b>{st.session_state['tonalidad_nombre']} Mayor</b></p>
    </div>
""", unsafe_allow_html=True)

# Feedback pequeño
if st.session_state['mensaje']:
    color_css = "#d4edda" if st.session_state['color_mensaje'] == "green" else "#f8d7da"
    text_color = "#155724" if st.session_state['color_mensaje'] == "green" else "#721c24"
    st.markdown(f"""
        <div style="background-color: {color_css}; color: {text_color}; padding: 5px; border-radius: 5px; text-align: center; margin-bottom: 10px; font-size: 0.9em; font-weight: bold;">
            {st.session_state['mensaje']}
        </div>
    """, unsafe_allow_html=True)

# --- 5. ESTRUCTURA DE DOS COLUMNAS (IZQ / DER) ---

# Creamos dos columnas principales al 50% cada una
col_izq, col_der = st.columns(2)

# Función para generar la rejilla 3x4
def crear_rejilla_3x4(col_padre, titulo, sufijo_visual, sufijo_logico):
    with col_padre:
        with st.container(border=True):
            st.markdown(f"##### {titulo}") # Título pequeño
            
            # Rejilla interna de 3 columnas
            # Al haber 12 notas, se crearán 4 filas automáticamente (3x4=12)
            cols_grid = st.columns(3)
            
            for i, nota_vis in enumerate(NOTAS_VISUALES):
                nota_logica = NOTAS_REALES[i]
                col_index = i % 3 # Cicla 0, 1, 2
                
                with cols_grid[col_index]:
                    # Texto del botón
                    txt = f"{nota_vis}{sufijo_visual}"
                    val = f"{nota_logica}{sufijo_logico}"
                    
                    if st.button(txt, key=f"btn_{val}"):
                        verificar(val)
                        st.rerun()

# --- GENERAR LOS PANELES ---

# Panel Izquierdo: MAYORES
# Sufijo visual vacío (ej: "C"), lógico "M" (ej: "CM")
crear_rejilla_3x4(col_izq, "🔵 Mayores", "", "M")

# Panel Derecho: MENORES
# Sufijo visual "m" (ej: "Cm"), lógico "m" (ej: "Cm")
crear_rejilla_3x4(col_der, "🔴 Menores", "m", "m")
