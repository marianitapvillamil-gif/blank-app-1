import streamlit as st
import numpy as np
import plotly.graph_objects as go

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Modelo de Leontief",
    layout="wide"
)

COLOR = "#8e44ad"

# =========================
# ESTILO
# =========================
st.markdown(f"""
<style>

html, body, .stApp {{
    background-color: #0e1117;
    color: white;
}}

.title {{
    font-size:48px;
    font-weight:800;
    color:{COLOR};
    text-align:center;
    margin-bottom:20px;
}}

.subtitle {{
    font-size:24px;
    text-align:center;
    color:#cccccc;
    margin-bottom:40px;
}}

.section {{
    font-size:32px;
    font-weight:bold;
    color:{COLOR};
    text-align:center;
    margin-top:20px;
    margin-bottom:25px;
}}

.card {{
    background-color:#1c1f26;
    padding:18px;
    border-radius:15px;
    text-align:center;
    border:1px solid #2a2f3a;
    transition:0.3s;
}}

.card:hover {{
    transform: translateY(-5px);
    box-shadow:0px 10px 20px rgba(0,0,0,0.5);
}}

.info-box {{
    background-color:#1c1f26;
    padding:25px;
    border-radius:15px;
    border:1px solid #2a2f3a;
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
# SECTORES
# =========================
sectores_totales = [
    "🐄 Ganadería",
    "⛏️ Minas",
    "🏭 Manufactura",
    "🏗️ Construcción",
    "🛒 Comercio",
    "🚚 Transporte",
    "⚡ Energía",
    "💼 Servicios"
]

# =========================
# MATRIZ GENERAL
# =========================
A_total = np.array([
    [0.15,0.05,0.10,0.02,0.04,0.03,0.02,0.01],
    [0.04,0.12,0.18,0.06,0.05,0.04,0.03,0.02],
    [0.20,0.15,0.25,0.10,0.08,0.07,0.06,0.04],
    [0.03,0.08,0.20,0.18,0.06,0.05,0.04,0.03],
    [0.05,0.04,0.07,0.06,0.10,0.08,0.05,0.04],
    [0.02,0.03,0.05,0.04,0.07,0.12,0.06,0.05],
    [0.03,0.02,0.04,0.03,0.05,0.06,0.15,0.07],
    [0.01,0.02,0.03,0.02,0.04,0.05,0.06,0.10]
])

# =========================
# PANTALLA INICIO
# =========================
if st.session_state.pantalla == "inicio":

    st.markdown('<div class="title">📊 Modelo de Leontief</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="subtitle">
    Aplicación interactiva para análisis económico mediante álgebra lineal y Python
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,2,1])

    with c2:

        if st.button("🚀 Iniciar análisis", use_container_width=True):
            st.session_state.pantalla = "sectores"
            st.rerun()

        st.write("")

        if st.button("ℹ️ Información del modelo", use_container_width=True):
            st.session_state.pantalla = "info"
            st.rerun()

# =========================
# INFORMACIÓN
# =========================
elif st.session_state.pantalla == "info":

    st.markdown('<div class="section">ℹ️ Información del modelo</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">

    ## 📘 ¿Qué es el modelo de Leontief?

    El modelo insumo-producto de Leontief es una herramienta matemática y económica
    utilizada para analizar cómo distintos sectores económicos dependen unos de otros.

    Permite estudiar cómo cambios en la demanda de un sector afectan la producción
    total requerida de otros sectores relacionados.

    ---

    ## 🧮 Fórmula principal

    x = (I - A)^(-1)d

    ---

    ## 📌 Elementos del modelo

    ### 🔹 Matriz A
    Representa los coeficientes técnicos entre sectores económicos.
    Cada valor indica cuánto necesita un sector de otro para producir.

    ### 🔹 Matriz identidad I
    Matriz especial utilizada para construir el sistema económico.

    ### 🔹 Vector d
    Representa la demanda final de los sectores económicos.

    ### 🔹 Vector x
    Representa la producción total requerida para satisfacer la demanda.

    ### 🔹 Matriz inversa
    Permite resolver sistemas de ecuaciones lineales y calcular la solución del modelo.

    ---

    ## 📐 Conceptos matemáticos utilizados

    ✅ Matrices cuadradas  
    ✅ Matriz identidad  
    ✅ Matriz inversa  
    ✅ Determinantes  
    ✅ Sistemas de ecuaciones lineales  
    ✅ Álgebra lineal computacional  

    ---

    ## 🔄 Encadenamientos productivos

    Los sectores económicos no funcionan de forma aislada.
    Cuando aumenta la demanda de un sector,
    otros sectores deben producir más recursos e insumos.

    Por ejemplo:

    Construcción ➜ Manufactura ➜ Minería

    Esto genera relaciones de dependencia conocidas como
    encadenamientos productivos.

    ---

    ## ⚠️ Invertibilidad de la matriz

    Para resolver el modelo,
    la matriz (I - A) debe ser invertible.

    Si no es invertible:

    ❌ el sistema no tiene solución única  
    ❌ no se puede calcular la producción requerida  
    ❌ existe una inconsistencia matemática o económica

    Matemáticamente esto ocurre cuando el determinante de la matriz es igual a cero.

    </div>
    """, unsafe_allow_html=True)

    if st.button("⬅️ Volver al inicio"):
        st.session_state.pantalla = "inicio"
        st.rerun()

# =========================
# SELECCIÓN DE SECTORES
# =========================
elif st.session_state.pantalla == "sectores":

    st.markdown('<div class="section">📋 Seleccionar sectores</div>', unsafe_allow_html=True)

    seleccionados = st.multiselect(
        "Escoge exactamente 4 sectores:",
        sectores_totales,
        max_selections=4
    )

    if len(seleccionados) == 4:

        st.success("✅ Sectores seleccionados correctamente")

        if st.button("➡️ Continuar"):
            st.session_state.sectores = seleccionados
            st.session_state.pantalla = "demandas"
            st.rerun()

# =========================
# DEMANDAS
# =========================
elif st.session_state.pantalla == "demandas":

    sectores = st.session_state.sectores

    st.markdown('<div class="section">📥 Ingresar demandas</div>', unsafe_allow_html=True)

    demandas = []

    col1, col2 = st.columns(2)

    for i, sector in enumerate(sectores):

        with [col1, col2][i % 2]:

            valor = st.number_input(
                f"Demanda para {sector}",
                min_value=0.0,
                value=100.0
            )

            demandas.append(valor)

    if st.button("📊 Calcular producción", use_container_width=True):

        indices = [sectores_totales.index(s) for s in sectores]

        A = A_total[np.ix_(indices, indices)]

        I = np.eye(4)

        matriz = I - A

        determinante = np.linalg.det(matriz)

        # =========================
        # VALIDACIÓN
        # =========================
        if abs(determinante) < 1e-10:

            st.error("""
            ❌ No es posible resolver el modelo de Leontief.

            La matriz (I - A) no es invertible.

            Esto significa que el sistema económico no tiene una solución única.

            Matemáticamente, esto ocurre porque el determinante de la matriz es igual a cero,
            impidiendo calcular la matriz inversa.

            Económicamente, esto puede representar una dependencia excesiva
            o inconsistencia entre sectores económicos.
            """)

        else:

            x = np.linalg.solve(matriz, demandas)

            st.session_state.x = x
            st.session_state.d = demandas
            st.session_state.pantalla = "resultados"
            st.rerun()

# =========================
# RESULTADOS
# =========================
elif st.session_state.pantalla == "resultados":

    x = st.session_state.x
    d = st.session_state.d
    sectores = st.session_state.sectores

    st.markdown('<div class="section">📈 Resultados</div>', unsafe_allow_html=True)

    cols = st.columns(4)

    for i in range(4):

        with cols[i]:

            st.markdown(f"""
            <div class="card">
                <h4>{sectores[i]}</h4>
                <h2>{x[i]:.2f}</h2>
            </div>
            """, unsafe_allow_html=True)

    # =========================
    # GRÁFICA
    # =========================
    fig = go.Figure()

    fig.add_bar(
        x=sectores,
        y=d,
        name="📥 Demanda"
    )

    fig.add_bar(
        x=sectores,
        y=x,
        name="📈 Producción"
    )

    fig.update_layout(
        template="plotly_dark",
        title="Comparación entre Demanda y Producción",
        barmode="group"
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # INTERPRETACIÓN
    # =========================
    max_sector = sectores[np.argmax(x)]

    st.markdown(f"""
    ## 🧠 Interpretación económica

    El sector con mayor producción requerida es **{max_sector}**.

    Esto indica que dicho sector genera mayores efectos indirectos
    dentro del sistema económico y posee una fuerte relación
    de dependencia con los demás sectores seleccionados.

    Los resultados evidencian la existencia de encadenamientos productivos,
    donde cambios en la demanda de un sector afectan la producción
    requerida en otros sectores relacionados.
    """)

    c1, c2, c3 = st.columns([1,2,1])

    with c2:

        if st.button("🔄 Nuevo análisis", use_container_width=True):
            st.session_state.pantalla = "inicio"
            st.rerun()