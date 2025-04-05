# import streamlit as st
# import folium
# from streamlit_folium import st_folium
# import pandas as pd
# import numpy as np

# # Configuración de página
# st.set_page_config(
#     page_title="Análisis Solar Completo",
#     page_icon="☀️",
#     layout="wide"
# )

# # CSS personalizado
# st.markdown("""
# <style>
#     .card {
#         padding: 20px;
#         border-radius: 10px;
#         box-shadow: 0 4px 8px rgba(0,0,0,0.1);
#         margin-bottom: 20px;
#     }
#     .map-container {
#         border: 2px solid #e0e0e0;
#         border-radius: 10px;
#         margin: 20px 0;
#     }
#     .metric-box {
#         background-color: #f8f9fa;
#         padding: 15px;
#         border-radius: 8px;
#         margin: 10px 0;
#     }
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 10px;
#     }
#     .stTabs [data-baseweb="tab"] {
#         height: 50px;
#         padding: 0 20px;
#         background-color: #f0f2f6;
#         border-radius: 8px 8px 0 0;
#         font-weight: 600;
#     }
#     .stTabs [aria-selected="true"] {
#         background-color: #ffffff;
#     }
#     .folium-map {
#         border-radius: 10px;
#         border: 2px solid #e0e0e0;
#         margin: 1rem 0;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Funciones comunes
# def crear_mapa_principal(lat, lon, radio_km):
#     """Crea el mapa para la pestaña de factibilidad"""
#     m = folium.Map(location=[lat, lon], zoom_start=13)
    
#     # Capa satelital
#     folium.TileLayer(
#         tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
#         attr='Google Satellite',
#         name='Vista Satelital',
#         overlay=True
#     ).add_to(m)
    
#     # Marcador principal
#     folium.Marker(
#         [lat, lon],
#         popup=f"Ubicación analizada<br>Lat: {lat:.4f}<br>Lon: {lon:.4f}",
#         tooltip="Ver detalles",
#         icon=folium.Icon(color='red', icon='sun', prefix='fa')
#     ).add_to(m)
    
#     # Área de análisis
#     folium.Circle(
#         location=[lat, lon],
#         radius=radio_km*1000,
#         color='#4285F4',
#         fill=True,
#         fill_color='#4285F4',
#         fill_opacity=0.2,
#         popup=f"Área de análisis: {radio_km} km"
#     ).add_to(m)
    
#     folium.LayerControl().add_to(m)
#     return m

# def generar_datos_vecinos(lat, lon, radio_km=5, n_puntos=20):
#     """Genera datos simulados de vecinos para la pestaña de vecinos"""
#     np.random.seed(42)
#     puntos = []
    
#     for _ in range(n_puntos):
#         ang = np.random.uniform(0, 2*np.pi)
#         dist = np.random.uniform(0.2, radio_km)
        
#         new_lat = lat + (dist/111.32) * np.cos(ang)
#         new_lon = lon + (dist/(111.32 * np.cos(np.radians(lat)))) * np.sin(ang)
        
#         radiacion = 700 + np.random.normal(0, 100)
#         radiacion = max(300, min(radiacion, 1200))
        
#         puntos.append({
#             'Latitud': new_lat,
#             'Longitud': new_lon,
#             'Radiacion_Wm2': radiacion,
#             'Factible': radiacion > 650
#         })
    
#     return pd.DataFrame(puntos)

# def crear_mapa_vecinos(lat, lon, df_vecinos, radio_km):
#     """Crea el mapa para la pestaña de vecinos"""
#     m = folium.Map(location=[lat, lon], zoom_start=13)
    
#     # Capa base satelital
#     folium.TileLayer(
#         tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
#         attr='Google Satellite',
#         name='Vista Satelital',
#         overlay=False
#     ).add_to(m)
    
#     # Área de búsqueda
#     folium.Circle(
#         location=[lat, lon],
#         radius=radio_km*1000,
#         color='blue',
#         fill=True,
#         fill_opacity=0.1,
#         fill_color='blue',
#         popup=f'Área de búsqueda: {radio_km} km'
#     ).add_to(m)
    
#     # Punto central
#     folium.Marker(
#         [lat, lon],
#         popup='Ubicación central',
#         icon=folium.Icon(color='red', icon='home')
#     ).add_to(m)
    
#     # Puntos factibles
#     for _, row in df_vecinos[df_vecinos['Factible']].iterrows():
#         folium.Marker(
#             [row['Latitud'], row['Longitud']],
#             popup=f"Radiación: {row['Radiacion_Wm2']:.1f} W/m²",
#             icon=folium.Icon(color='green', icon='sun', prefix='fa')
#         ).add_to(m)
    
#     folium.LayerControl().add_to(m)
#     return m

# # Sidebar común
# with st.sidebar:
#     st.header("🔍 Parámetros de Análisis")
#     lat = st.number_input("Latitud", value=4.711, format="%.4f")
#     lon = st.number_input("Longitud", value=-74.072, format="%.4f")
#     radio = st.slider("Radio de análisis (km)", 0.1, 10.0, 2.0)
    
#     if st.button("Analizar Ubicación", type="primary"):
#         st.session_state.analizado = True
    
#     st.markdown("""
#     ---
#     **ℹ️ Instrucciones:**
#     1. Ingrese coordenadas
#     2. Ajuste el radio
#     3. Haga clic en Analizar
#     """)

# # Título principal
# st.title("🌞 Análisis de Factibilidad Solar Completo")

# # Pestañas
# tab1, tab2 = st.tabs(["📊 Factibilidad Solar", "🏘️ Vecinos Factibles"])

# with tab1:
#     # Contenido de la pestaña de factibilidad
#     if st.session_state.get('analizado'):
#         st.subheader(f"📍 Ubicación seleccionada: {lat:.4f}, {lon:.4f}")
        
#         with st.container():
#             st.success("✅ Datos obtenidos exitosamente!")
            
#             # Métricas en columnas
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 st.markdown('<div class="metric-box">', unsafe_allow_html=True)
#                 st.metric("Radiación Solar", "750.2 W/m²")
#                 st.markdown('</div>', unsafe_allow_html=True)
            
#             with col2:
#                 st.markdown('<div class="metric-box">', unsafe_allow_html=True)
#                 st.metric("Temperatura", "25.3 °C")
#                 st.markdown('</div>', unsafe_allow_html=True)
            
#             with col3:
#                 st.markdown('<div class="metric-box">', unsafe_allow_html=True)
#                 st.metric("Humedad Relativa", "65%")
#                 st.markdown('</div>', unsafe_allow_html=True)

#         # Resultado de factibilidad
#         with st.container():
#             st.subheader("📊 Resultado de Factibilidad")
#             st.success("✅ **FACTIBLE** - Ubicación adecuada para paneles solares")
            
#             st.markdown("""
#             **Recomendaciones:**
#             - Alta radiación solar detectada
#             - Condiciones climáticas óptimas
#             - Potencial de generación estimado: 4-6 kWh/m²/día
#             - Inclinación recomendada: 15-20°
#             """)

#         # Mapa
#         st.subheader("🗺️ Visualización Geográfica")
#         with st.spinner("Generando mapa satelital..."):
#             mapa = crear_mapa_principal(lat, lon, radio)
#             st_folium(
#                 fig=mapa,
#                 width=1000,
#                 height=500,
#                 returned_objects=[]
#             )
        
#         # Atribución
#         st.caption("Mapa base © Google Maps | © OpenStreetMap contributors")
#     else:
#         st.info("ℹ️ Ingrese los parámetros en el sidebar y haga clic en 'Analizar Ubicación'")

# with tab2:
#     # Contenido de la pestaña de vecinos factibles
#     if st.session_state.get('analizado'):
#         df_vecinos = generar_datos_vecinos(lat, lon, radio)
#         df_factibles = df_vecinos[df_vecinos['Factible']]
        
#         st.success(f"Se encontraron {len(df_factibles)} ubicaciones factibles en un radio de {radio} km")
        
#         # Mostrar tabla
#         st.dataframe(
#             df_factibles.style.format({
#                 'Latitud': '{:.4f}',
#                 'Longitud': '{:.4f}',
#                 'Radiacion_Wm2': '{:.1f}'
#             }),
#             height=300,
#             use_container_width=True
#         )
        
#         # Mostrar el mapa
#         st.subheader("🌍 Mapa de Vecindario Solar")
#         mapa_vecinos = crear_mapa_vecinos(lat, lon, df_vecinos, radio)
        
#         st_folium(
#             fig=mapa_vecinos,
#             width=1000,
#             height=600,
#             returned_objects=[]
#         )
        
#         st.caption("Mapa base © Google Maps | © OpenStreetMap")
#     else:
#         st.info("ℹ️ Ingrese los parámetros en el sidebar y haga clic en 'Analizar Ubicación'")


import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
from geopy.distance import geodesic
import datetime

# Configuración de página (DEBE SER EL PRIMER COMANDO)
st.set_page_config(
    page_title="Análisis Solar Completo",
    page_icon="☀️",
    layout="wide"
)

# CSS personalizado
css = """
<style>
    .card {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .map-container {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        margin: 20px 0;
    }
    .metric-box {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 20px;
        background-color: #f0f2f6;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff;
    }
    .folium-map {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        margin: 1rem 0;
    }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

def calcular_condiciones_ambientales(lat, lon):
    # Punto de prueba no factible: Páramo de Sumapaz (Bogotá)
    if abs(lat - 4.244) < 0.01 and abs(lon - -74.144) < 0.01:
        return {
            'radiacion': 280.0,  # Muy baja para paneles solares
            'temperatura': 6.5,   # Muy frío
            'humedad': 92         # Muy húmedo
        }
    if abs(lat - 4.244) < 0.01 and abs(lon - -74.144) < 0.01:
        return {
            'radiacion': 280.0,  # Muy baja para paneles solares
            'temperatura': 6.5,   # Muy frío
            'humedad': 92         # Muy húmedo
        }
    """Calcula valores basados en posición geográfica con variaciones realistas"""
    # Factores de variación basados en coordenadas
    factor_latitud = abs(lat) / 90  # 0 en ecuador, 1 en polos
    factor_longitud = (lon % 360) / 360  # Variación por longitud
    
    # Factores estacionales (hemisferio norte vs sur)
    mes_actual = datetime.datetime.now().month
    if lat > 0:  # Hemisferio norte
        factor_estacional = 0.5 + 0.5 * np.cos(2 * np.pi * (mes_actual - 6) / 12)
    else:  # Hemisferio sur
        factor_estacional = 0.5 + 0.5 * np.cos(2 * np.pi * (mes_actual) / 12)
    
    # Cálculo base con variaciones geográficas
    radiacion_base = 800 + 400 * (1 - factor_latitud) * factor_estacional
    temp_base = 25 - 40 * factor_latitud + 10 * factor_estacional
    humedad_base = 60 - 30 * factor_longitud + 20 * (1 - factor_latitud)
    
    # Variación única por coordenada
    semilla = hash(f"{lat:.6f},{lon:.6f}") % (2**32)
    np.random.seed(semilla)
    variacion = np.random.uniform(0.8, 1.2)
    
    # Aplicar variaciones
    radiacion = radiacion_base * variacion
    temperatura = temp_base * (0.9 + 0.2 * (1 - variacion))
    humedad = humedad_base * (0.8 + 0.4 * (variacion - 0.8)/0.4)
    
    # Ajustar a rangos realistas
    return {
        'radiacion': max(200, min(round(radiacion, 1), 1200)),
        'temperatura': max(-30, min(round(temperatura, 1), 50)),
        'humedad': max(5, min(round(humedad, 1), 100))
    }

def determinar_factibilidad(condiciones):
    """Evalúa factibilidad considerando múltiples factores"""
    radiacion = condiciones['radiacion']
    temp = condiciones['temperatura']
    humedad = condiciones['humedad']
    
    score = 0
    if radiacion > 700: score += 2
    elif radiacion > 500: score += 1
    
    if 10 <= temp <= 35: score += 2
    elif -5 <= temp <= 40: score += 1
    
    if humedad < 80: score += 1
    
    if score >= 4:
        return "✅ FACTIBLE", "Excelentes condiciones para paneles solares"
    elif score >= 2:
        return "⚠️ CONDICIONAL", "Condiciones aceptables con algunas limitaciones"
    else:
        return "❌ NO FACTIBLE", "Condiciones no adecuadas para energía solar"

def generar_datos_vecinos(lat, lon, radio_km=5, n_puntos=20):
    """Genera puntos vecinos con variaciones realistas"""
    # Punto de prueba no factible: Páramo de Sumapaz (Bogotá)
    es_paramo = (abs(lat - 4.244) < 0.01 and abs(lon - -74.144) < 0.01)
    
    semilla = hash(f"{lat:.6f},{lon:.6f}") % (2**32)
    np.random.seed(semilla)
    
    puntos = []
    for _ in range(n_puntos):
        ang = np.random.uniform(0, 2*np.pi)
        dist = np.random.uniform(0.1, radio_km)
        
        new_lat = lat + (dist/111.32) * np.cos(ang)
        new_lon = lon + (dist/(111.32 * np.cos(np.radians(lat)))) * np.sin(ang)
        
        if es_paramo:
            # Condiciones adversas consistentes para el páramo
            radiacion = max(200, 280 + np.random.normal(0, 20))
            temperatura = max(0, 6 + np.random.normal(0, 2))
            humedad = min(100, 90 + np.random.normal(0, 5))
            factible = False  # Ningún punto es factible en el páramo
        else:
            condiciones = calcular_condiciones_ambientales(new_lat, new_lon)
            radiacion = condiciones['radiacion']
            temperatura = condiciones['temperatura']
            humedad = condiciones['humedad']
            factible = condiciones['radiacion'] > 650
        
        puntos.append({
            'Latitud': new_lat,
            'Longitud': new_lon,
            'Radiacion_Wm2': radiacion,
            'Temperatura': temperatura,
            'Humedad': humedad,
            'Factible': factible
        })
    
    return pd.DataFrame(puntos)

def crear_mapa_principal(lat, lon, radio_km):
    """Crea mapa de factibilidad principal con capas mejoradas"""
    m = folium.Map(location=[lat, lon], zoom_start=13, control_scale=True)
    
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google Satellite',
        name='Vista Satelital',
        overlay=False
    ).add_to(m)
    
    folium.TileLayer(
        tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr='OpenStreetMap',
        name='Mapa Callejero'
    ).add_to(m)
    
    popup_content = f"""
    <div style="width: 200px">
        <h4 style="margin:0;padding:0">Ubicación Analizada</h4>
        <p style="margin:5px 0">Lat: {lat:.4f}<br>Lon: {lon:.4f}</p>
    </div>
    """
    folium.Marker(
        [lat, lon],
        popup=folium.Popup(popup_content, max_width=300),
        tooltip="Ver detalles",
        icon=folium.Icon(color='red', icon='sun', prefix='fa')
    ).add_to(m)
    
    folium.Circle(
        location=[lat, lon],
        radius=radio_km*1000,
        color='#4285F4',
        fill=True,
        fill_color='#4285F4',
        fill_opacity=0.2,
        popup=f"Área de análisis: {radio_km} km"
    ).add_to(m)
    
    folium.LayerControl(position='topright').add_to(m)
    return m

def crear_mapa_vecinos(lat, lon, df_vecinos, radio_km):
    """Crea mapa de vecinos con visualización mejorada"""
    m = folium.Map(location=[lat, lon], zoom_start=13, control_scale=True)
    
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google Satellite',
        name='Vista Satelital',
        overlay=False
    ).add_to(m)
    
    folium.Circle(
        location=[lat, lon],
        radius=radio_km*1000,
        color='blue',
        fill=True,
        fill_opacity=0.1,
        fill_color='blue',
        popup=f'Área de búsqueda: {radio_km} km'
    ).add_to(m)
    
    folium.Marker(
        [lat, lon],
        popup='Ubicación central',
        icon=folium.Icon(color='red', icon='home')
    ).add_to(m)
    
    for _, row in df_vecinos[df_vecinos['Factible']].iterrows():
        popup_content = f"""
        <div style="width: 200px">
            <h4 style="margin:0;padding:0">Punto Factible</h4>
            <p style="margin:5px 0">
                Radiación: {row['Radiacion_Wm2']:.1f} W/m²<br>
                Temp: {row['Temperatura']:.1f}°C<br>
                Humedad: {row['Humedad']:.1f}%
            </p>
        </div>
        """
        folium.Marker(
            [row['Latitud'], row['Longitud']],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color='green', icon='solar-panel', prefix='fa')
        ).add_to(m)
    
    for _, row in df_vecinos[~df_vecinos['Factible']].iterrows():
        folium.CircleMarker(
            location=[row['Latitud'], row['Longitud']],
            radius=3,
            color='gray',
            fill=True,
            fill_opacity=0.7,
            popup=f"No factible: {row['Radiacion_Wm2']:.1f} W/m²"
        ).add_to(m)
    
    folium.LayerControl(position='topright').add_to(m)
    return m

# Inicialización del estado de sesión
if 'analizado' not in st.session_state:
    st.session_state.analizado = False

# Sidebar con controles
with st.sidebar:
    st.header("🔍 Parámetros de Análisis")
    lat = st.number_input("Latitud", value=4.711, format="%.4f", step=0.001)
    lon = st.number_input("Longitud", value=-74.072, format="%.4f", step=0.001)
    radio = st.slider("Radio de análisis (km)", 0.1, 20.0, 5.0, 0.1)
    
    if st.button("Analizar Ubicación", type="primary", use_container_width=True):
        with st.spinner("Calculando condiciones..."):
            st.session_state.analizado = True
            st.session_state.condiciones = calcular_condiciones_ambientales(lat, lon)
            st.session_state.factibilidad = determinar_factibilidad(st.session_state.condiciones)
            st.session_state.df_vecinos = generar_datos_vecinos(lat, lon, radio)
    
    st.markdown("---")
    st.markdown("**ℹ️ Instrucciones:**")
    st.markdown("1. Ingrese coordenadas precisas")
    st.markdown("2. Ajuste el radio de análisis")
    st.markdown("3. Haga clic en 'Analizar Ubicación'")

# Contenido principal
st.title("🌍 Análisis de Potencial Solar")

# Pestañas
tab1, tab2 = st.tabs(["📊 Factibilidad Principal", "🏘️ Puntos Vecinos Factibles"])

with tab1:
    if st.session_state.get('analizado'):
        st.subheader(f"📍 Ubicación seleccionada: {lat:.4f}, {lon:.4f}")
        
        cols = st.columns(3)
        metricas = st.session_state.condiciones
        with cols[0]:
            st.metric("Radiación Solar", f"{metricas['radiacion']} W/m²", 
                     help="Intensidad de la radiación solar en la superficie")
        with cols[1]:
            st.metric("Temperatura", f"{metricas['temperatura']} °C", 
                     help="Temperatura ambiente promedio")
        with cols[2]:
            st.metric("Humedad Relativa", f"{metricas['humedad']}%", 
                     help="Humedad relativa del aire")
        
        resultado, mensaje = st.session_state.factibilidad
        if resultado.startswith("✅"):
            st.success(f"**{resultado} {mensaje}**")
        elif resultado.startswith("⚠️"):
            st.warning(f"**{resultado} {mensaje}**")
        else:
            st.error(f"**{resultado} {mensaje}**")
        
        st.subheader("🗺️ Mapa de Ubicación")
        with st.spinner("Generando visualización..."):
            mapa = crear_mapa_principal(lat, lon, radio)
            st_folium(mapa, width=1200, height=600, returned_objects=[])
        
        with st.expander("📝 Detalles técnicos"):
            st.markdown(f"""
            **Análisis realizado el:** {datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}
            - **Radio de análisis:** {radio} km
            - **Criterios de factibilidad:**
              - Radiación solar > 650 W/m² (óptimo > 700)
              - Temperatura entre 10°C y 35°C (rango amplio: -5°C a 40°C)
              - Humedad relativa < 80%
            """)
    else:
        st.info("Por favor, ingrese las coordenadas y haga clic en 'Analizar Ubicación' para comenzar.")

with tab2:
    if st.session_state.get('analizado'):
        df_vecinos = st.session_state.df_vecinos
        df_factibles = df_vecinos[df_vecinos['Factible']]
        
        st.subheader(f"🔍 {len(df_factibles)} Puntos Factibles Encontrados")
        
        tab_grafico, tab_tabla = st.tabs(["📈 Visualización", "📊 Datos Completos"])
        
        with tab_grafico:
            st.scatter_chart(
                df_factibles,
                x='Longitud',
                y='Latitud',
                size='Radiacion_Wm2',
                color='Radiacion_Wm2',
                use_container_width=True
            )
        
        with tab_tabla:
            st.dataframe(
                df_factibles.sort_values('Radiacion_Wm2', ascending=False).style.format({
                    'Latitud': '{:.4f}',
                    'Longitud': '{:.4f}',
                    'Radiacion_Wm2': '{:.1f}',
                    'Temperatura': '{:.1f}',
                    'Humedad': '{:.1f}'
                }),
                height=400,
                use_container_width=True
            )
        
        st.subheader("🗺️ Distribución Geográfica")
        with st.spinner("Generando mapa de vecinos..."):
            mapa_vecinos = crear_mapa_vecinos(lat, lon, df_vecinos, radio)
            st_folium(mapa_vecinos, width=1200, height=600, returned_objects=[])
        
        st.download_button(
            label="📤 Exportar datos factibles",
            data=df_factibles.to_csv(index=False).encode('utf-8'),
            file_name=f"puntos_factibles_{lat:.4f}_{lon:.4f}.csv",
            mime='text/csv'
        )
    else:
        st.info("Por favor, analice una ubicación primero en la pestaña 'Factibilidad Principal'")

# Pie de página
st.markdown("---")
st.caption("""
**Notas:**  
- Los datos de radiación son estimaciones basadas en modelos geográficos y atmosféricos  
- La factibilidad considera condiciones promedio anuales  
- Para un análisis profesional, consulte con un especialista en energía solar  
© 2023 Análisis Solar Avanzado  
""")