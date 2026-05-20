import streamlit as st
import numpy as np
import plotly.graph_objects as go

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Modelo de Leontief", layout="wide")

COLOR = "#8e44ad"

# =========================
# ESTILO + CENTRADO + ANIMACIONES
# =========================
st.markdown(f"""
<style>
html, body, .stApp {{
    height: 100%;
    background-color: #0e1117;
    color: white;
}}

.center-screen {{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 85vh;
}}

.title {{
    font-size:75px;
    font-weight:900;
    text-align:center;
    color:{COLOR};
    margin-bottom:20px;
    animation: fadeIn 1.2s ease-in;
}}

.section {{
    font-size:40px;
    font-weight:bold;
    text-align:center;
    color:{COLOR};
    margin-bottom:25px;
    animation: fadeIn 1s ease-in;
}}

.card {{
    background-color:#1c1f26;
    padding:20px;
    border-radius:15px;
    text-align:center;
    border:1px solid #2a2f3a;
    transition: transform 0.3s;
}}

.card:hover {{
    transform: scale(1.05);
}}

div.stButton > button {{
    background-color:{COLOR};
    color:white;
    border-radius:12px;
    height:55px;
    font-size:18px;
    transition: all 0.3s ease;
}}

div.stButton > button:hover {{
    background-color:#6d2c91;
    transform: scale(1.05);
}}

@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(25px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
</style>
""", unsafe_allow_html=True)

# =========================
# ESTADO
# =========================
if "pantalla" not in st.session_state:
    st.session_state.pantalla = "inicio"

# =========================
# MATRIZ A
# =========================
A = np.array([
    [0.15, 0.05, 0.10, 0.02],
    [0.04, 0.12, 0.18, 0.06],
    [0.20, 0.15, 0.25, 0.10],
    [0.03, 0.08, 0.20, 0.18]
])

# =========================
# PANTALLA INICIO (CENTRADA)
# =========================
if st.session_state.pantalla == "inicio":

    st.markdown("""
    <div class="center-screen">
    """, unsafe_allow_html=True)

    st.markdown('<p class="title">📊 Modelo de Leontief</p>', unsafe_allow_html=True)

    if st.button("🚀 Iniciar análisis", use_container_width=True):
        st.session_state.pantalla = "formulario"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# FORMULARIO
# =========================
elif st.session_state.pantalla == "formulario":

    st.markdown('<p class="section">📥 Ingresar demandas</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        ganaderia = st.number_input("🐄 Ganadería", value=100.0)
        minas = st.number_input("⛏️ Minas", value=80.0)

    with col2:
        manufactura = st.number_input("🏭 Manufactura", value=150.0)
        construccion = st.number_input("🏗️ Construcción", value=120.0)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2,3,2])
    with c2:
        if st.button("📊 Calcular producción", use_container_width=True):

            d = np.array([ganaderia, minas, manufactura, construccion])
            I = np.eye(4)

            try:
                x = np.linalg.solve(I - A, d)

                st.session_state.x = x
                st.session_state.d = d
                st.session_state.pantalla = "resultados"

                st.rerun()

            except Exception as e:
                st.error(f"❌ Error en cálculo: {e}")

# =========================
# RESULTADOS
# =========================
elif st.session_state.pantalla == "resultados":

    x = st.session_state.x
    d = st.session_state.d

    sectores = ["Ganadería", "Minas", "Manufactura", "Construcción"]

    st.markdown('<p class="section">📊 Resultados</p>', unsafe_allow_html=True)

    # =========================
    # TARJETAS
    # =========================
    cols = st.columns(4)

    for i in range(4):
        with cols[i]:
            st.markdown(f"""
            <div class="card">
                <h4>{sectores[i]}</h4>
                <h2>{x[i]:.
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # GRÁFICA COMPARATIVA
    # =========================
    fig = go.Figure()

    fig.add_bar(x=sectores, y=d, name="Demanda", marker_color="#3498db")
    fig.add_bar(x=sectores, y=x, name="Producción", marker_color=COLOR)

    fig.update_layout(
        template="plotly_dark",
        title="Comparación: Demanda vs Producción",
        barmode="group"
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # INTERPRETACIÓN (ACTUALIZADA ✅)
    # =========================
    max_sector = sectores[np.argmax(x)]

    st.markdown(f"""
    ### 🧠 Interpretación
    El sector con mayor producción total requerida es **{max_sector}**.

    Esto indica que este sector genera una mayor demanda indirecta 
    dentro del sistema económico, siendo clave en la interdependencia entre sectores.
    """)

    # =========================
    # BOTÓN VOLVER
    # =========================
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2,3,2])
    with c2:
        if st.button("🔄 Nuevo análisis", use_container_width=True):
            st.session_state.pantalla = "inicio"
            st.rerun()