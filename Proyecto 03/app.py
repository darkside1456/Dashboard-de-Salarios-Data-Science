import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Dashboard de Salarios",
    page_icon="📊",
    layout="wide"
)

NIVELES_EXPERIENCIA = {
    "EN": "Junior",
    "MI": "Intermedio",
    "SE": "Senior",
    "EX": "Ejecutivo",
}

MODALIDAD_REMOTA = {
    0: "Presencial",
    50: "Híbrido",
    100: "Remoto",
}


@st.cache_data
def cargar_datos():
    datos = pd.read_csv("ds_salaries.csv")

    datos["salary_in_usd"] = pd.to_numeric(
        datos["salary_in_usd"],
        errors="coerce"
    )

    datos = datos.dropna(
        subset=["job_title", "salary_in_usd", "experience_level", "remote_ratio"]
    )

    datos["nivel_experiencia"] = datos["experience_level"].map(
        NIVELES_EXPERIENCIA
    )

    datos["modalidad"] = datos["remote_ratio"].map(
        MODALIDAD_REMOTA
    )

    return datos


datos = cargar_datos()

st.title("📊 Dashboard de salarios en Ciencia de Datos")
st.write(
    "Explora salarios por puesto, experiencia y modalidad de trabajo."
)

st.sidebar.header("Filtros")

experiencias = st.sidebar.multiselect(
    "Nivel de experiencia",
    options=sorted(datos["nivel_experiencia"].dropna().unique()),
    default=sorted(datos["nivel_experiencia"].dropna().unique())
)

modalidades = st.sidebar.multiselect(
    "Modalidad de trabajo",
    options=sorted(datos["modalidad"].dropna().unique()),
    default=sorted(datos["modalidad"].dropna().unique())
)

datos_filtrados = datos[
    datos["nivel_experiencia"].isin(experiencias)
    & datos["modalidad"].isin(modalidades)
]

columna_1, columna_2, columna_3 = st.columns(3)

columna_1.metric(
    "Salario promedio",
    f"${datos_filtrados['salary_in_usd'].mean():,.0f}"
)

columna_2.metric(
    "Registros analizados",
    f"{len(datos_filtrados):,}"
)

puesto_principal = (
    datos_filtrados.groupby("job_title")["salary_in_usd"]
    .mean()
    .idxmax()
)

columna_3.metric("Puesto mejor pagado", puesto_principal)

st.subheader("Salario promedio por nivel de experiencia")

por_experiencia = (
    datos_filtrados.groupby("nivel_experiencia")["salary_in_usd"]
    .mean()
    .reindex(["Junior", "Intermedio", "Senior", "Ejecutivo"])
)

st.bar_chart(por_experiencia)

st.subheader("Top 10 puestos por salario promedio")

por_puesto = (
    datos_filtrados.groupby("job_title")["salary_in_usd"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(por_puesto)

st.subheader("Datos filtrados")
st.dataframe(
    datos_filtrados[
        ["job_title", "nivel_experiencia", "modalidad", "salary_in_usd"]
    ],
    use_container_width=True
)