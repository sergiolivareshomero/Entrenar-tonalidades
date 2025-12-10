import streamlit as st
import random

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Entrenador Armónico", layout="centered")

# CSS para botones compactos y estilo móvil
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        margin-bottom: 2px; /* Menos margen para compactar */
        font-weight: bold;
        padding: 0.25rem 0.5rem;
    }
    div[data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }
    /* Reducir padding general para ganar espacio en móvil */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. LÓGICA MUSICAL ---
NOTAS_REALES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTAS_VISUALES = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']

# Intervalos de la escala mayor (semitonos): T-T-S-T-T-T-S
INTERVALOS_MAYOR = [0, 2, 4, 5, 7, 9, 11] 
GRADOS_ROMANOS = ["I", "II", "III", "IV", "V", "VI", "VII"]

# Cualidades: M, m, m, M, M, m, (dim eliminado)
CUALIDADES = ['M', 'm', 'm', 'M', 'M', 'm', 'dim']

# --- 3. FUNCIONES DE ESTADO ---

def generar_pregunta():
    """Genera una nueva pregunta aleatoria (SIN GRADO VII / DISMINUIDO)."""
    indice_ton = random.randint(0, 11)
    
    # IMPORTANTE: Ahora el rango es (0, 5) en lugar de (0, 6).
    # Esto excluye el índice 6, que corresponde al Grado VII (Disminuido).
    indice_grado = random.randint(0, 5)
    
    # Calcular respuesta correcta
    semitonos = INTERVALOS_MAYOR[indice_grado]
    indice_nota_resp = (indice_ton + semitonos) % 12
    nota_resp = NOTAS_REALES[indice_nota_resp]
    cualidad_resp = CUALIDADES[indice_grado]
    
    # Guardar en sesión
    st.session_state['tonalidad_nombre'] = NOTAS_VISUALES[indice_ton]
    st.session_state['grado_nombre'] = GRADOS_ROMANOS[indice_grado]
    st.session_state['grado_numero'] = indice_grado + 1
    st.session_state['respuesta_correcta'] = f"{nota_resp}{cualidad_resp}"
    
    # Resetear mensajes
    st.session_state['mensaje'] = ""
    st.session_state['color_mensaje'] = "black"

def verificar(respuesta_usuario):
    """Verifica y recarga."""
    correcta = st.session_state['respuesta_correcta']
    
    if respuesta_usuario == correcta:
        st.session_state['mensaje'] = f"¡CORRECTO! ✅\nEra {respuesta_usuario}. Siguiente..."
        st.session_state['color_mensaje'] = "green"
        generar_pregunta()
    else:
        st.session_state['mensaje'] = f"❌ Incorrecto. No es {respuesta_usuario}."
        st.session_state['color_mensaje'] = "red"

# Inicializar
if 'respuesta_correcta' not in st.session_state:
    generar_pregunta()

# --- 4. INTERFAZ GRÁFICA ---

st.title("🎵 Entrenador Tonal")

# Panel Pregunta
st.markdown(f"""
    <div style="text-align: center; padding: 10px; background-color: #f8f9fa; border-radius: 12px; margin-bottom: 10px; border: 1px solid #dee2e6;">
        <h4 style="margin:0; color: #666; font-weight: normal; font-size: 0.9em;">Encuentra el acorde</h4>
        <h1 style="margin: 0; font-size: 2.2em; color: #31333F;">Grado {st.session_state['grado_nombre']}</h1>
        <p style="font-size: 1em; margin:0;">({st.session_state['grado_numero']}) de <b>{st.session_state['tonalidad_nombre']} Mayor</b></p>
    </div>
""", unsafe_allow_html=True)

# Feedback
if st.session_state['mensaje']:
    if st.session_state['color_mensaje'] == "green":
        st.success(st.session_state['mensaje'], icon="✅")
    else:
        st.error(st.session_state['mensaje'], icon="🚨")

# --- 5. BOTONERA EN CONTENEDORES ---

# Función auxiliar para crear cuadrículas de botones
def crear_rejilla(contenedor, titulo, sufijo_visual, sufijo_logico, columnas=4):
    contenedor.markdown(f"**{titulo}**")
    cols = contenedor.columns(columnas) # 4 columnas para que sea muy compacto
    
    for i, nota_vis in enumerate(NOTAS_VISUALES):
        nota_logica = NOTAS_REALES[i]
        col_idx = i % columnas
        
        with cols[col_idx]:
            texto = f"{nota_vis}{sufijo_visual}"
            valor = f"{nota_logica}{sufijo_logico}"
            
            if st.button(texto, key=f"btn_{valor}"):
                verificar(valor)
                st.rerun()

# CONTENEDOR 1: MAYORES
with st.container(border=True):
    # Usamos 4 columnas para que ocupe menos altura (3 filas de 4 botones)
    crear_rejilla(st, "🔵 Acordes Mayores", "", "M", columnas=4)

# CONTENEDOR 2: MENORES
with st.container(border=True):
    crear_rejilla(st, "🔴 Acordes Menores", "m", "m", columnas=4)
