import streamlit as st
import numpy as np
import plotly.graph_objects as go

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Modelo de Leontief", layout="wide")

COLOR = "#8e44ad"

# =========================
# ESTILO FINAL LIMPIO
# =========================
st.markdown(f"""
<style>

html, body, .stApp {{
    background-color: #0e1117;
    color: white;
}}

.center-wrapper {{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 55vh;
}}

.center-box {{
    width: 100%;
    max-width: 450px;
    text-align: center;
}}

.title {{
    font-size:48px;
    font-weight:800;
    color:{COLOR};
    margin-bottom:20px;
}}

.section {{
    font-size:32px;
    font-weight:bold;
    text-align:center;
    color:{COLOR};
    margin-bottom:15px;
}}

.card {{
    background-color:#1c1f26;
    padding:18px;
    border-radius:15px;
    text-align:center;
    border:1px solid #2a2f3a;
    transition: all 0.3s ease;
}}

.card:hover {{
    transform: translateY(-5px);
    box-shadow:0px 10px 20px rgba(0,0,0,0.4);
}}

div.stButton > button {{
    background-color:{COLOR};
    color:white;
    border-radius:12px;
    height:50px;
    font-size:17px;
}}

div.stButton > button:hover {{
    background-color:#6d2c91;
    transform: scale(1.03);
}}

</style>
""", unsafe_allow_html=True)

# =========================
# ESTADO
# =========================
if "pantalla" not in st.session_state:
    st.session_state.pantalla = "inicio"

# =========================
# MATRIZ
# =========================
A = np.array([
    [0.15, 0.05, 0.10, 0.02],
    [0.04, 0.12, 0.18, 0.06],
    [0.20, 0.15, 0.25, 0.10],
    [0.03, 0.08, 0.20, 0.18]
])

# =========================
# INICIO
# =========================
if st.session_state.pantalla == "inicio":

    st.markdown('<div class="center-wrapper"><div class="center-box">', unsafe_allow_html=True)

    st.markdown('<div class="title">📊 Modelo de Leontief</div>', unsafe_allow_html=True)

    if st.button("🚀 Iniciar análisis", use_container_width=True):
        st.session_state.pantalla = "formulario"
        st.rerun()

    st.markdown('</div></div>', unsafe_allow_html=True)

# =========================
# FORMULARIO
# =========================
elif st.session_state.pantalla == "formulario":

    st.markdown('<div class="section">📥 Ingresar demandas</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        ganaderia = st.number_input("🐄 Ganadería", value=100.0)
        minas = st.number_input("⛏️ Minas", value=80.0)

    with col2:
        manufactura = st.number_input("🏭 Manufactura", value=150.0)
        construccion = st.number_input("🏗️ Construcción", value=120.0)

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
                st.error(f"Error en cálculo: {e}")

# =========================
# RESULTADOS
# =========================
elif st.session_state.pantalla == "resultados":

    x = st.session_state.x
    d = st.session_state.d

    sectores = ["Ganadería", "Minas", "Manufactura", "Construcción"]

    st.markdown('<div class="section">📊 Resultados</div>', unsafe_allow_html=True)

    # TARJETAS ✅
    cols = st.columns(4)

    for i in range(4):
        with cols[i]:
            st.markdown(f"""
            <div class="card">
                <h4>{sectores[i]}</h4>
                <h2>{x[i]:.2f}</h2>
            </div>
            """, unsafe_allow_html=True)

    # GRÁFICA ✅
    fig = go.Figure()

    fig.add_bar(x=sectores, y=d, name="Demanda", marker_color="#3498db")
    fig.add_bar(x=sectores, y=x, name="Producción", marker_color=COLOR)

    fig.update_layout(
        template="plotly_dark",
        title="Comparación: Demanda vs Producción",
        barmode="group"
    )

    st.plotly_chart(fig, use_container_width=True)

    # INTERPRETACIÓN ✅
    max_sector = sectores[np.argmax(x)]

    st.markdown(f"""
    ### 🧠 Interpretación
    El sector con mayor producción total requerida es **{max_sector}**.

    Esto indica que este sector genera una mayor demanda indirecta 
    dentro del sistema económico, siendo clave en la interdependencia entre sectores.
    """)

    # BOTÓN VOLVER ✅
    c1, c2, c3 = st.columns([2,3,2])
    with c2:
        if st.button("🔄 Nuevo análisis", use_container_width=True):
            st.session_state.pantalla = "inicio"
            st.rerun()