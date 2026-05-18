import streamlit as st
import pandas as pd

import backend

st.set_page_config(page_title="Carretera A", layout="wide")
st.title("Carretera A - Buscador de rutas")
st.write("Interfaz de Streamlit para encontrar rutas en el grafo de carreteras.")

with st.sidebar:
    st.header("Configuración")
    ciudades = backend.get_nodes()
    origen = st.selectbox("Ciudad origen", ciudades, index=ciudades.index('Jiloyork') if 'Jiloyork' in ciudades else 0)
    destino = st.selectbox("Ciudad destino", ciudades, index=ciudades.index('MTY') if 'MTY' in ciudades else 0)
    buscar = st.button("Buscar ruta")

if buscar:
    resultado = backend.search_route(origen, destino)

    if resultado['route'] is None:
        st.error("No se encontró una ruta entre las ciudades seleccionadas. Verifica las conexiones del grafo.")
    else:
        ruta = resultado['route']
        costo = resultado['cost']

        st.subheader("Ruta encontrada")
        st.write(" → ".join(ruta))
        st.metric(label="Costo total", value=f"{costo}")

        coordenadas = [
            {
                'city': ciudad,
                'latitude': backend.coord[ciudad][0],
                'longitude': backend.coord[ciudad][1]
            }
            for ciudad in ruta
        ]

        df_ruta = pd.DataFrame(coordenadas)
        st.write("### Detalles de la ruta")
        st.dataframe(df_ruta)

        st.write("### Mapa de la ruta")
        st.map(df_ruta)

        st.write("### Conexiones usadas")
        for i in range(len(ruta) - 1):
            origen_c = ruta[i]
            destino_c = ruta[i + 1]
            distancia = backend.conexiones[origen_c][destino_c]
            st.write(f"{origen_c} → {destino_c}: {distancia} km")
else:
    st.info("Selecciona origen y destino, luego haz clic en \"Buscar ruta\".")
