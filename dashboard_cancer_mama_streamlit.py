import streamlit as st
import pandas as pd
import plotly.express as px


# =====================
# Dashboard de Cáncer de Mama - Streamlit
# =====================

# Cargar el CSV limpio

st.set_page_config(layout="wide", page_title="Dashboard Cáncer de Mama", page_icon="🎀", initial_sidebar_state="expanded")



# Eliminar fondo rosado y usar colores predeterminados


st.title("🎀 Dashboard Interactivo de Cáncer de Mama")
st.markdown("""
<span style='font-size:18px; color:#E75480;'>
Explora los datos de cáncer de mama de manera sencilla y visual. Utiliza los filtros para analizar los casos y entender mejor la información.
</span>
""", unsafe_allow_html=True)

# Colores temáticos para el mes del cáncer de mama
color_map = {"Maligno": "#E75480", "Benigno": "#FFC0CB"}  # Rosa fuerte y rosa claro

# Cargar datos
try:
    df = pd.read_csv("cancer_mama_limpio_espanol.csv")
except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")
    st.stop()

# =====================
# Filtros en la barra lateral
# =====================

st.sidebar.header("🎛️ Filtros de Datos")
st.sidebar.markdown("<span style='color:#E75480;font-size:15px;'>Filtra los datos para personalizar las visualizaciones.</span>", unsafe_allow_html=True)

# Filtro por diagnóstico
diagnosticos = sorted(df["Diagnóstico"].unique())
diag_sel = st.sidebar.multiselect("Diagnóstico", diagnosticos, default=diagnosticos)


# Mostrar las columnas disponibles para ayudar al usuario

# Mostrar las columnas disponibles con descripciones
st.sidebar.markdown("<b><span style='color:#E75480;'>Variables disponibles:</span></b>", unsafe_allow_html=True)
col_descripciones = {
    "Radio_Medio_1": "Radio promedio del tumor (primer análisis)",
    "Textura_Media_1": "Textura promedio del tumor",
    "Perímetro_Medio_1": "Perímetro promedio",
    "Área_Media_1": "Área promedio",
    "Diagnóstico": "Tipo de tumor (Maligno o Benigno)"
}
for col in df.columns:
    desc = col_descripciones.get(col, "")
    st.sidebar.markdown(f"<span style='color:#E75480'><b>{col}</b></span>: <span style='color:#E75480'>{desc}</span>", unsafe_allow_html=True)

# NUEVO: Sección informativa y decorativa en la barra lateral
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("<span style='color:#E75480;font-size:17px;'><b>🎀 Mes Rosa</b></span>", unsafe_allow_html=True)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/7/7c/Pink_ribbon.svg", width=80)
st.sidebar.markdown("<span style='color:#E75480;'>El lazo rosa es símbolo internacional de la concientización sobre el cáncer de mama. ¡Infórmate y comparte!</span>", unsafe_allow_html=True)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("<span style='color:#E75480;font-size:15px;'>¿Sabías que la detección temprana salva vidas? Realiza tus chequeos periódicos y consulta a tu médico ante cualquier duda.</span>", unsafe_allow_html=True)

# Intentar usar 'Radio_Medio_1', si no existe usar la primera columna que contenga 'Radio' o la primera numérica
col_radio = None
for col in df.columns:
    if "radio" in col.lower():
        col_radio = col
        break
if col_radio is None:
    num_cols = df.select_dtypes(include=["int64", "float64"]).columns
    if len(num_cols) > 0:
        col_radio = num_cols[0]
    else:
        st.error("No se encontró una columna de radio o numérica para filtrar.")
        st.stop()

# Filtro por rango de radio
radio_min, radio_max = float(df[col_radio].min()), float(df[col_radio].max())
radio_range = st.sidebar.slider(f"Rango de {col_radio}", radio_min, radio_max, (radio_min, radio_max))

# Aplicar filtros
filtro = (
    df["Diagnóstico"].isin(diag_sel) &
    (df[col_radio] >= radio_range[0]) &
    (df[col_radio] <= radio_range[1])
)
df_filtrado = df[filtro]


# =====================
# Distribución creativa de los gráficos y tabla
# =====================

st.markdown("<hr style='border:1px solid #E75480;'>", unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 Casos Filtrados")
    st.markdown("<span style='color:#E75480;'>Esta tabla muestra los casos que cumplen con los filtros seleccionados. Puedes ordenar y buscar dentro de la tabla.</span>", unsafe_allow_html=True)
    st.dataframe(df_filtrado, height=400, use_container_width=True)
    # Botón para descargar el CSV filtrado
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar casos filtrados en CSV",
        data=csv,
        file_name="casos_filtrados_cancer_mama.csv",
        mime="text/csv"
    )
    st.markdown("<span style='color:#222;'>Gráfico de pastel que muestra la proporción de casos malignos y benignos.</span>", unsafe_allow_html=True)
    st.subheader("🥧 Proporción de Diagnóstico")
    st.markdown("<span style='color:#E75480;'>Gráfico de pastel que muestra la proporción de casos malignos y benignos.</span>", unsafe_allow_html=True)
    grafico_pie = px.pie(
        df_filtrado,
        names="Diagnóstico",
        color="Diagnóstico",
        color_discrete_map=color_map,
        title="Proporción de Diagnóstico"
    )
    grafico_pie.update_layout()
    st.plotly_chart(grafico_pie, use_container_width=True, key="grafico_pie")

    st.markdown("<span style='color:#E75480;'>Este gráfico de barras muestra cuántos casos hay de cada tipo de diagnóstico. El color rosa representa los casos benignos y el rosa fuerte los malignos.</span>", unsafe_allow_html=True)
    st.subheader("📊 Casos por Tipo de Diagnóstico")
    st.markdown("<span style='color:#E75480;'>Este gráfico de barras muestra cuántos casos hay de cada tipo de diagnóstico. El color rosa representa los casos benignos y el rosa fuerte los malignos.</span>", unsafe_allow_html=True)
    grafico_barra = px.bar(
        df_filtrado["Diagnóstico"].value_counts().reset_index(),
        x="Diagnóstico",
        y="count",
        color="Diagnóstico",
        color_discrete_map=color_map,
        labels={"Diagnóstico": "Tipo de diagnóstico", "count": "Cantidad de casos"},
        title="Cantidad de Casos por Diagnóstico"
    )
    grafico_barra.update_layout()
    st.plotly_chart(grafico_barra, use_container_width=True, key="grafico_barra1")

    # Gráfico de dispersión: Área vs Radio
    if "Área_Media_1" in df_filtrado.columns and "Radio_Medio_1" in df_filtrado.columns:
        st.subheader("🔬 Dispersión Área vs Radio del Tumor")
        fig_disp = px.scatter(
            df_filtrado,
            x="Radio_Medio_1",
            y="Área_Media_1",
            color="Diagnóstico",
            color_discrete_map=color_map,
            labels={"Radio_Medio_1": "Radio promedio", "Área_Media_1": "Área promedio"},
            title="Relación entre Radio y Área del Tumor"
        )
        st.plotly_chart(fig_disp, use_container_width=True)

    # Histograma: Radio del Tumor
    if "Radio_Medio_1" in df_filtrado.columns:
        st.subheader("📈 Histograma del Radio del Tumor")
        fig_hist_radio = px.histogram(
            df_filtrado,
            x="Radio_Medio_1",
            color="Diagnóstico",
            color_discrete_map=color_map,
            nbins=20,
            title="Distribución del Radio del Tumor"
        )
        st.plotly_chart(fig_hist_radio, use_container_width=True)

   
# =====================
# Clasificación por Severidad del Tumor
# =====================

st.subheader("🩺 Clasificación por Severidad del Tumor")
if "Área_Media_1" in df.columns:
    # Calcular percentiles para definir rangos
    q1 = df["Área_Media_1"].quantile(0.33)
    q2 = df["Área_Media_1"].quantile(0.66)

    def clasificar_severidad(area):
        if area < q1:
            return "Leve"
        elif area < q2:
            return "Moderado"
        else:
            return "Severo"

    df_filtrado["Severidad"] = df_filtrado["Área_Media_1"].apply(clasificar_severidad)

    fig_severidad = px.histogram(
        df_filtrado,
        x="Severidad",
        color="Diagnóstico",
        barmode="group",
        color_discrete_map=color_map,
        title="Clasificación de Tumores por Severidad (basado en Área)"
    )
    st.plotly_chart(fig_severidad, use_container_width=True)
else:
    st.warning("No se encontró la columna 'Área_Media_1' para clasificar severidad.")



# =====================
# Footer
# =====================

st.markdown("---")
st.markdown("<span style='color:#E75480;font-size:18px;'>🎀 <b>Mes de Concientización sobre el Cáncer de Mama</b></span>", unsafe_allow_html=True)
st.markdown("<span style='font-size:15px;'>Los colores del dashboard representan la lucha, esperanza y concientización sobre el cáncer de mama. Explora los datos y comparte el conocimiento.</span>", unsafe_allow_html=True)


with st.expander("ℹ️ Explicación de variables", expanded=False):
    st.markdown("""
    <span style='color:#E75480;'>
    <b>Variables del Dataset:</b><br>
    <b>Diagnóstico</b>: Tipo de tumor (<b>Maligno</b> o <b>Benigno</b>).<br>
    <b>Radio_Medio_1</b>: Radio promedio del tumor (primer análisis).<br>
    <b>Textura_Media_1</b>: Textura promedio del tumor.<br>
    <b>Perímetro_Medio_1</b>: Perímetro promedio del tumor.<br>
    <b>Área_Media_1</b>: Área promedio del tumor.<br>
    <b>Suavidad_Media_1</b>: Suavidad promedio del tumor.<br>
    <b>Compacidad_Media_1</b>: Compacidad promedio del tumor.<br>
    <b>Concavidad_Media_1</b>: Concavidad promedio del tumor.<br>
    <b>Puntos_Concavos_Medios_1</b>: Puntos cóncavos medios.<br>
    <b>Simetría_Media_1</b>: Simetría promedio.<br>
    <b>Dimensión_Fractal_Media_1</b>: Dimensión fractal promedio.<br>
    <b>Edad</b>: Edad de la paciente.<br>
    <b>Hospital</b>: Centro médico donde se realizó el estudio.<br>
    <b>ID_Paciente</b>: Identificador único de la paciente.<br>
    <b>Fecha_Diagnóstico</b>: Fecha en que se realizó el diagnóstico.<br>
    <b>Observaciones</b>: Comentarios adicionales del médico.<br>
    <br>
    <b>¿Cómo interpretar los gráficos?</b><br>
    <ul>
      <li>El gráfico de pastel muestra la proporción de tumores malignos y benignos.</li>
      <li>El gráfico de barras indica la cantidad de casos por tipo de diagnóstico.</li>
    <b>¡Recuerda!</b> Todos los datos son anónimos y sirven para concientizar y educar sobre el cáncer de mama.<br>
    </span>
    """, unsafe_allow_html=True)


#   streamlit run "De criss/De criss/dashboard_cancer_mama_streamlit.py"

