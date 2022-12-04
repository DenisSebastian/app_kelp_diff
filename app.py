import streamlit as st
import pandas as pd
import os
import plotly.express as px
import numpy as np
import pydeck as pdk
import base64

#style
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
# add_bg_from_local('images/Macrocystis2.JPG')    



st.subheader("SAT 01: Blue Alert")
st.markdown('**Prototipo de Plataforma**: Satellite monitoring of the cover of Kelp forest ecosystems')
# st.markdown("##### Prototipo de Plataforma:")

st.markdown("##### Visualización Espacial (solo prueba):")

# np.random.seed(42) 
# chart_data = pd.DataFrame(
#    np.random.randn(1000, 2) / [200, 200] + [-33.35586626066772, -71.65975190473253],
#    columns=['lat', 'lon'])
chart_data =  pd.read_csv("data/csv/coords_mar.csv")

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/satellite-v9',
    initial_view_state=pdk.ViewState(
        latitude=-33.35586626066772,
        longitude=-71.65975190473253,
        zoom=12,
        pitch=20,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=chart_data,
           get_position='[X, Y]',
           radius=50,
           elevation_scale=4,
           elevation_range=[0, 100],
           pickable=True,
           extruded=True,
        ),
        # pdk.Layer(
        #     'ScatterplotLayer',
        #     data=chart_data,
        #     get_position='[lon, lat]',
        #     get_color='[200, 30, 0, 160]',
        #     get_radius=200,
        # ),
    ],
))


st.markdown("##### Análisis de Serie de Tiempo:")
col1, col2 = st.columns(2)

with col1:
    # Selección de Bases
    base_select = st.selectbox(
        label = "Seleccione Índice",
        options = ["Kelp", "PAR", "SST"])


    
# # checkbox para remove NA values de la serie
# data_radio = st.radio(
#      label = "Seleccione tipo de datos",
#      options = ('Raw (con NAs)', 'NAs Interpolados'),
#      horizontal =True)


# # 
# if base_select == 'NAs Interpolados':
#     base_select = base_select+"_i"
#     colname = "ndvi_interpolated"
# else:
#     colname = "ndvi"



# Generación path
wd = os.getcwd()
file_name = str(base_select + "_data.csv")
files_csv = "data/csv"
fullname = os.path.join(wd,files_csv , file_name)

os.path.exists(fullname)

# Lectura de Base
df = pd.read_csv(fullname)
#df = df.set_index("date")

with col2:
    # Selector de Serie
    serie_filter = st.selectbox("Seleccionar Serie", pd.unique(df["Site"]))


title_plot = str("Time Serie "+ base_select +" en "+serie_filter)
df_serie = df.loc[(df.Site == serie_filter)]




# Generación de Visualización
width = 750
height = 550

fig = px.line(df_serie, x='date', y=base_select, title=title_plot
        #,width = width, height= height
)

fig.update_traces(line_color='#02818a', line_width=1)
#fig.update_layout(
#    plot_bgcolor='white'
#)

fig.update_xaxes(rangeslider_visible=True,
     rangeselector=dict(
        buttons=list([
            dict(count=6, label="6 meses", step="month", stepmode="backward"),
            dict(count=1, label="1 año", step="year", stepmode="backward"),
            dict(count=2, label="2 años", step="year", stepmode="backward"),
            dict(count=5, label="5 años", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)
st.plotly_chart(fig, use_container_width=False)


col1, col2, col3 = st.columns(3)
col1.metric("Temperatura", "17 °C", "1.2 °C")
col2.metric("Viento", "12 kph", "-8%")
col3.metric("Humedad", "86%", "4%")

# Descipción de la APP

st.subheader("Descipción:")
st.markdown("**Bosques de algas**")
st.write("Los bosques submarinos son sistemas ecológicos complejos y altamente productivos, caracterizado por la presencia de grandes algas capaces de formar un dosel sobre los fondos submarinos. Estos bosques forman hábitat, refugio, sitios de desove y alimentación, para un gran número de invertebrados y peces (Ruz et al. 2021; Vega et al. 2005, Teagle et al. 2017, Carbajal et al. 2021, Bularz et al. 2022), otorgan diversos servicios ecosistémicos de soporte (mantenimiento de biodiversidad, protección contra oleaje), de regulación (por ejemplo el ciclaje de nutrientes, captación de carbono y producción de oxígeno), de provisión (alimentos, materia prima para biomateriales, biocombustibles, etc) y culturales (turismo y recreación, beneficios estéticos, entre otros).")

# st.latex(r'''
# NDVI = \frac{NIR-RED}{NIR+RED}
#      ''')

# st.image("images/descp_ndvi.jpeg")
# st.markdown("**Autor:** [denis.berroeta@uai.cl](denis.berroeta@uai.cl)")


## https://discuss.streamlit.io/t/event-handling-of-pydeck-chart-map-in-streamlit/10842
# https://discuss.streamlit.io/t/showing-geotiff-raster-data/11170/4
# https://github.com/randyzwitch/streamlit-folium
