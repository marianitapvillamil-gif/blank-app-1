import streamlit as st
import numpy as np
import plotly.graph_objects as go

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Modelo de Leontief", layout="wide")

# =========================
# COLOR
# =========================
COLOR = "#8e44ad"

# =========================
# ESTILO + ANIMACIONES PRO
# =========================
st.markdown(f"""
<style>
body {{
    background-color: #0e1117;
    color: white;
}}

.title {{
    font-size:75px;
    font-weight:900;
    text-align:center;
    color:{COLOR};
    animation: fadeIn 1.2s ease-in;
}}

.section {{
    font-size:42px;
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
    transition: transform 0.3s, box-shadow 0.3s;
}}

.card:hover {{
    transform: translateY(-8px);
    box-shadow:0px 8px 25px rgba(0,0,0,0.6);
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
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
</style>
""", unsafe_allow_html=True)

# =========================
# CONTROL
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

    st.markdown('<p class="title">📊 Modelo de Leontief</p>', unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2,3,2])
    with c2:
        if st.button("🚀 Iniciar análisis", use_container_width=True):
            st.session_state.pantalla = "formulario"
            st.rerun()

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

    cols = st.columns(4)

    for i in range(4):
        with cols[i]:
            st.markdown(f"""
            <div class="card">
                <h4>{sectores[i]}</h4>
                <h2>{x[i]:.2f}</h2>
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
    # INTERPRETACIÓN
    # =========================
    max_sector = sectores[np.argmax(x)]

    st.markdown(f"""
    ### 🧠 Interpretación
    El sector con mayor impacto es **{max_sector}**, ya que requiere mayor producción.
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