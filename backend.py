from arbol import Nodo
from math import sin, cos, acos, radians
from typing import Dict, Tuple, List, Optional
import json
import os


# =========================
# GRAFO DE CONEXIONES
# =========================

conexiones: Dict[str, Dict[str, int]] = {
    'Jiloyork': {'CDMX': 125, 'QRO': 513},
    'MORELOS': {'QRO': 524},
    'CDMX': {
        'Jiloyork': 125,
        'QRO': 423,
        'HGO': 491,
        'dexcani el alto': 34
    },
    'HGO': {
        'CDMX': 491,
        'QRO': 356,
        'MEXICALI': 309,
        'MTY': 346
    },
    'QRO': {
        'SLP': 203,
        'MORELOS': 514,
        'Jiloyork': 513,
        'CDMX': 423,
        'MTY': 603,
        'SONORA': 437,
        'HGO': 356,
        'MEXICALI': 313,
        'AGS': 599
    },
    'SLP': {
        'AGS': 390,
        'QRO': 203
    },
    'AGS': {
        'SLP': 390,
        'QRO': 599
    },
    'SONORA': {
        'QRO': 437,
        'MEXICALI': 394
    },
    'MEXICALI': {
        'MTY': 296,
        'HGO': 309,
        'QRO': 313
    },
    'MTY': {
        'MEXICALI': 296,
        'QRO': 603,
        'HGO': 346
    },
    'dexcani el alto': {
        'CDMX': 34
    }
}


# =========================
# COORDENADAS
# =========================

coord: Dict[str, Tuple[float, float]] = {
    'Jiloyork': (19.952408902750292, -99.53304570197712),
    'CDMX': (19.432684900517486, -99.13333701698),
    'QRO': (20.587956563302367, -100.38793290667115),
    'MORELOS': (18.930555912984644, -99.22237799899486),
    'HGO': (20.127000042049925, -98.73156416258126),
    'AGS': (21.856150731885958, -102.28915655184271),
    'SLP': (22.151749211629454, -100.97643458591887),
    'SONORA': (29.07865856228773, -110.94760761628041),
    'MEXICALI': (29.07865856228773, -110.94760761628041),
    'MTY': (25.66616067388393, -100.32880810205178),
    'dexcani el alto': (19.92162330052597, -99.48796021530332)
}


# =========================
# DISTANCIA GEOGRÁFICA
# =========================

def geodist(lat1: float, lon1: float,
            lat2: float, lon2: float) -> float:

    lat1r = radians(lat1)
    lon1r = radians(lon1)
    lat2r = radians(lat2)
    lon2r = radians(lon2)

    val = (
        (sin(lat1r) * sin(lat2r)) +
        (cos(lat1r) * cos(lat2r) * cos(lon1r - lon2r))
    )

    val = max(-1.0, min(1.0, val))

    rad_grad = 57.29577951

    return (acos(val) * rad_grad) * 111.32


# =========================
# FUNCIÓN HEURÍSTICA
# =========================

def f_cost(nodo: Nodo, meta: str) -> float:

    lat1, lon1 = coord[nodo.get_datos()]
    lat2, lon2 = coord[meta]

    d = int(geodist(lat1, lon1, lat2, lon2))

    return nodo.get_costo() + d


# =========================
# BÚSQUEDA UCS / A*
# =========================

def buscar_solucion_USC(
        estado_inicial: str,
        solucion: str
) -> Optional[Nodo]:

    solucionado = False

    nodos_visitados: List[Nodo] = []
    nodos_frontera: List[Nodo] = []

    nodo_inicial = Nodo(estado_inicial)
    nodo_inicial.set_costo(0)

    nodos_frontera.append(nodo_inicial)

    while (not solucionado) and nodos_frontera:

        nodos_frontera.sort(
            key=lambda nodo: f_cost(nodo, solucion)
        )

        nodo = nodos_frontera.pop(0)

        nodos_visitados.append(nodo)

        if nodo.get_datos() == solucion:
            solucionado = True
            return nodo

        dato_nodo = nodo.get_datos()

        lista_hijos: List[Nodo] = []

        for un_hijo in conexiones.get(dato_nodo, {}):

            hijo = Nodo(un_hijo)

            costo = conexiones[dato_nodo][un_hijo]

            hijo.set_costo(
                nodo.get_costo() + costo
            )

            hijo.set_padre(nodo)

            lista_hijos.append(hijo)

            if not hijo.en_lista(nodos_visitados):

                if hijo.en_lista(nodos_frontera):

                    for n in nodos_frontera:

                        if (
                            n.igual(hijo)
                            and n.get_costo() > hijo.get_costo()
                        ):

                            nodos_frontera.remove(n)
                            nodos_frontera.append(hijo)
                            break

                else:
                    nodos_frontera.append(hijo)

        nodo.set_hijos(lista_hijos)

    return None


# =========================
# OBTENER RUTA
# =========================

def get_route(
        nodo_solucion: Nodo,
        estado_inicial: str
) -> List[str]:

    resultado: List[str] = []

    nodo = nodo_solucion

    while nodo.get_padre() is not None:

        resultado.append(nodo.get_datos())

        nodo = nodo.get_padre()

    resultado.append(estado_inicial)

    return list(reversed(resultado))


# =========================
# BUSCAR RUTA
# =========================

def search_route(
        estado_inicial: str,
        solucion: str
) -> Dict[str, Optional[object]]:

    if estado_inicial not in conexiones:
        return {
            'route': None,
            'cost': None,
            'error': 'Ciudad inicial no existe'
        }

    if solucion not in conexiones:
        return {
            'route': None,
            'cost': None,
            'error': 'Ciudad destino no existe'
        }

    nodo_solucion = buscar_solucion_USC(
        estado_inicial,
        solucion
    )

    if nodo_solucion is None:
        return {
            'route': None,
            'cost': None,
            'error': 'No existe ruta'
        }

    ruta = get_route(
        nodo_solucion,
        estado_inicial
    )

    return {
        'route': ruta,
        'cost': nodo_solucion.get_costo(),
        'error': None
    }


# =========================
# LISTAR NODOS
# =========================

def get_nodes() -> List[str]:
    return sorted(conexiones.keys())


# =========================
# OBTENER COORDENADAS
# =========================

def get_coordinates_for_route(
        route: List[str]
) -> List[Tuple[str, float, float]]:

    return [
        (node, coord[node][0], coord[node][1])
        for node in route
        if node in coord
    ]


# =========================
# AGREGAR CIUDAD
# =========================

def agregar_ciudad(
        nombre: str,
        lat: float,
        lon: float
) -> bool:

    if nombre in conexiones:
        return False

    conexiones[nombre] = {}
    coord[nombre] = (lat, lon)

    return True


# =========================
# AGREGAR RUTA
# =========================

def agregar_ruta(
        origen: str,
        destino: str,
        costo: int,
        bidireccional: bool = True
) -> bool:

    if origen not in conexiones:
        return False

    if destino not in conexiones:
        return False

    conexiones[origen][destino] = costo

    if bidireccional:
        conexiones[destino][origen] = costo

    return True


# =========================
# GUARDAR DATOS
# =========================

ARCHIVO = "rutas.json"


def guardar_datos():

    data = {
        "conexiones": conexiones,
        "coord": coord
    }

    with open(ARCHIVO, "w", encoding="utf-8") as archivo:

        json.dump(
            data,
            archivo,
            indent=4,
            ensure_ascii=False
        )


# =========================
# CARGAR DATOS
# =========================

def cargar_datos():

    global conexiones
    global coord

    if not os.path.exists(ARCHIVO):
        return

    with open(ARCHIVO, "r", encoding="utf-8") as archivo:

        data = json.load(archivo)

        conexiones = data["conexiones"]

        coord = {
            k: tuple(v)
            for k, v in data["coord"].items()
        }


# =========================
# EJEMPLO DE USO
# =========================

if __name__ == "__main__":

    cargar_datos()

    print("\nCIUDADES DISPONIBLES:\n")
    print(get_nodes())

    print("\nAGREGANDO NUEVA CIUDAD...\n")

    agregar_ciudad(
        "PUEBLA",
        19.0412967,
        -98.2061996
    )

    agregar_ruta(
        "CDMX",
        "PUEBLA",
        130
    )

    agregar_ruta(
        "QRO",
        "PUEBLA",
        280
    )

    guardar_datos()

    print("\nBUSCANDO RUTA...\n")

    resultado = search_route(
        "Jiloyork",
        "PUEBLA"
    )

    print(resultado)
    
