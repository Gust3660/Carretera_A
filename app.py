import streamlit as st
import pandas as pd
import backend

st.set_page_config(
    page_title="Carretera A",
    layout="wide"
)

st.title("Carretera A - Buscador de rutas")
st.write("Interfaz de usuario para encontrar rutas en el grafo de carreteras.")


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("Configuración")

    ciudades = backend.get_nodes()

    origen = st.selectbox(
        "Ciudad origen",
        ciudades,
        index=ciudades.index('Jiloyork')
        if 'Jiloyork' in ciudades else 0
    )

    destino = st.selectbox(
        "Ciudad destino",
        ciudades,
        index=ciudades.index('MTY')
        if 'MTY' in ciudades else 0
    )

    buscar = st.button("Buscar ruta")


# ==========================================
# FORMULARIO PARA AGREGAR CIUDADES
# ==========================================

st.sidebar.markdown("---")
st.sidebar.header("Agregar nueva ciudad")

with st.sidebar.form("form_ciudad"):

    nueva_ciudad = st.text_input("Nombre ciudad")

    latitud = st.number_input(
        "Latitud",
        format="%.10f"
    )

    longitud = st.number_input(
        "Longitud",
        format="%.10f"
    )

    guardar_ciudad = st.form_submit_button(
        "Agregar ciudad"
    )

    if guardar_ciudad:

        if nueva_ciudad.strip() == "":
            st.sidebar.error("Ingresa un nombre válido")

        else:

            agregado = backend.agregar_ciudad(
                nueva_ciudad,
                latitud,
                longitud
            )

            if agregado:

                backend.guardar_datos()

                st.sidebar.success(
                    f"Ciudad '{nueva_ciudad}' agregada"
                )

                st.rerun()

            else:
                st.sidebar.warning(
                    "La ciudad ya existe"
                )


# ==========================================
# FORMULARIO PARA AGREGAR RUTAS
# ==========================================

st.sidebar.markdown("---")
st.sidebar.header("Agregar nueva ruta")

ciudades_actualizadas = backend.get_nodes()

with st.sidebar.form("form_ruta"):

    origen_ruta = st.selectbox(
        "Origen",
        ciudades_actualizadas,
        key="origen_ruta"
    )

    destino_ruta = st.selectbox(
        "Destino",
        ciudades_actualizadas,
        key="destino_ruta"
    )

    costo = st.number_input(
        "Costo / Distancia",
        min_value=1,
        step=1
    )

    bidireccional = st.checkbox(
        "Bidireccional",
        value=True
    )

    guardar_ruta = st.form_submit_button(
        "Agregar ruta"
    )

    if guardar_ruta:

        if origen_ruta == destino_ruta:

            st.sidebar.error(
                "Origen y destino no pueden ser iguales"
            )

        else:

            agregado = backend.agregar_ruta(
                origen_ruta,
                destino_ruta,
                costo,
                bidireccional
            )

            if agregado:

                backend.guardar_datos()

                st.sidebar.success(
                    "Ruta agregada correctamente"
                )

            else:

                st.sidebar.error(
                    "Error agregando ruta"
                )


# ==========================================
# BÚSQUEDA DE RUTAS
# ==========================================

if buscar:

    resultado = backend.search_route(
        origen,
        destino
    )

    if resultado['route'] is None:

        st.error(
            "No se encontró una ruta entre las ciudades seleccionadas."
        )

    else:

        ruta = resultado['route']
        costo_total = resultado['cost']

        st.subheader("Ruta encontrada")

        st.success(" → ".join(ruta))

        st.metric(
            label="Costo total",
            value=f"{costo_total} km"
        )

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

        st.dataframe(
            df_ruta,
            use_container_width=True
        )

        st.write("### Conexiones usadas")

        for i in range(len(ruta) - 1):

            origen_c = ruta[i]
            destino_c = ruta[i + 1]

            distancia = backend.conexiones[
                origen_c
            ][destino_c]

            st.write(
                f"{origen_c} → {destino_c}: {distancia} km"
            )

else:

    st.info(
        "Selecciona origen y destino y luego haz clic en Buscar ruta."
    )
