import streamlit as st
import numpy as np
import plotly.graph_objects as go

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Modelo de Leontief", layout="wide")

COLOR = "#8e44ad"

# =========================
# ESTILOS
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
}}

.section {{
    font-size:30px;
    font-weight:bold;
    color:{COLOR};
    margin-top:20px;
}}

.card {{
    background-color:#1c1f26;
    padding:18px;
    border-radius:15px;
    text-align:center;
    border:1px solid #2a2f3a;
}}

div.stButton > button {{
    background-color:{COLOR};
    color:white;
    border-radius:12px;
    height:50px;
    font-size:17px;
}}

</style>
""", unsafe_allow_html=True)

# =========================
# SECTORES
# =========================
sectores_totales = [
    "Ganadería",
    "Minas",
    "Manufactura",
    "Construcción",
    "Comercio",
    "Transporte",
    "Energía",
    "Servicios"
]

# =========================
# MATRIZ GENERAL 8x8
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
# TÍTULO
# =========================
st.markdown('<div class="title">📊 Modelo de Leontief</div>', unsafe_allow_html=True)

# =========================
# INFORMACIÓN
# =========================
with st.expander("ℹ️ Información sobre el modelo"):

    st.markdown("""
    ## ¿Qué es el modelo de Leontief?

    El modelo insumo-producto de Leontief analiza cómo los sectores económicos dependen unos de otros.

    ## Fórmula principal

    x = (I - A)^(-1)d

    ## Conceptos utilizados

    ### Matriz A
    Representa los coeficientes técnicos entre sectores económicos.

    ### Matriz identidad I
    Matriz utilizada para construir el sistema económico.

    ### Vector d
    Representa la demanda final.

    ### Vector x
    Producción total requerida.

    ### Matriz inversa
    Permite resolver sistemas de ecuaciones lineales.

    ### Encadenamientos productivos
    Relaciones de dependencia entre sectores económicos.
    """)

# =========================
# SELECCIÓN DE SECTORES
# =========================
st.markdown('<div class="section">Seleccionar sectores</div>', unsafe_allow_html=True)

seleccionados = st.multiselect(
    "Escoge 4 sectores:",
    sectores_totales,
    max_selections=4
)

if len(seleccionados) == 4:

    indices = [sectores_totales.index(s) for s in seleccionados]

    A = A_total[np.ix_(indices, indices)]

    st.markdown('<div class="section">Ingresar demandas</div>', unsafe_allow_html=True)

    demandas = []

    cols = st.columns(2)

    for i, sector in enumerate(seleccionados):

        with cols[i % 2]:
            valor = st.number_input(
                f"Demanda para {sector}",
                min_value=0.0,
                value=100.0
            )
            demandas.append(valor)

    if st.button("📊 Calcular producción"):

        d = np.array(demandas)

        I = np.eye(4)

        matriz = I - A

        determinante = np.linalg.det(matriz)

        # =========================
        # VALIDAR INVERTIBILIDAD
        # =========================
        if abs(determinante) < 1e-10:

            st.error("""
            ❌ No es posible resolver el modelo de Leontief.

            La matriz (I - A) no es invertible.

            Esto significa que el sistema económico no posee una solución única.

            Matemáticamente, una matriz no invertible tiene determinante igual a cero, lo cual impide calcular su inversa.

            En términos económicos, esto puede interpretarse como una dependencia excesiva o inconsistencia entre sectores económicos.
            """)

        else:

            x = np.linalg.solve(matriz, d)

            st.markdown('<div class="section">Resultados</div>', unsafe_allow_html=True)

            cols = st.columns(4)

            for i in range(4):
                with cols[i]:
                    st.markdown(f"""
                    <div class="card">
                        <h4>{seleccionados[i]}</h4>
                        <h2>{x[i]:.2f}</h2>
                    </div>
                    """, unsafe_allow_html=True)

            # =========================
            # GRÁFICA
            # =========================
            fig = go.Figure()

            fig.add_bar(
                x=seleccionados,
                y=d,
                name="Demanda"
            )

            fig.add_bar(
                x=seleccionados,
                y=x,
                name="Producción"
            )

            fig.update_layout(
                template="plotly_dark",
                title="Demanda vs Producción",
                barmode="group"
            )

            st.plotly_chart(fig, use_container_width=True)

            # =========================
            # INTERPRETACIÓN
            # =========================
            max_sector = seleccionados[np.argmax(x)]

            st.markdown(f"""
            ## 🧠 Interpretación

            El sector con mayor producción requerida es **{max_sector}**.

            Esto indica que dicho sector genera mayores efectos indirectos dentro del sistema económico y posee una fuerte relación de dependencia con los demás sectores seleccionados.
            """)