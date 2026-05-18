# Viaje por carretera con busqueda A*
from arbol import Nodo
from math import sin, cos, acos, radians

def f_cost(nodo, meta):
    lat1, lon1 = coord[nodo.get_datos()]
    lat2, lon2 = coord[meta]
    d = int(geodist(lat1, lon1, lat2, lon2))
    return nodo.get_costo() + d

def geodist(lat1, lon1, lat2, lon2):
    lat1r = radians(lat1)
    lon1r = radians(lon1)
    lat2r = radians(lat2)
    lon2r = radians(lon2)
    val = (sin(lat1r) * sin(lat2r)) + (cos(lat1r) * cos(lat2r) * cos(lon1r - lon2r))
    val = max(-1.0, min(1.0, val))
    rad_grad = 57.29577951
    return (acos(val) * rad_grad) * 11.32

def buscar_solucion_USC(conexiones, estado_inicial, solucion):
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    nodo_inicial = Nodo(estado_inicial)
    nodo_inicial.set_costo(0)
    nodos_frontera.append(nodo_inicial)
    while not solucionado and nodos_frontera:
        # Ordenar la lista de Nodos Frontera por f(n)=g(n)+h(n)
        nodos_frontera.sort(key=lambda nodo: f_cost(nodo, solucion))
        nodo = nodos_frontera[0]

        # Extraer el nodo y aladir a visitados
        nodos_visitados.append(nodos_frontera.pop(0))
        if nodo.get_datos() == solucion:
            # Solucion encontrada
            solucionado = True
            return nodo
        else:
            # Expandir los nodo hijo (Ciudades por conexion)
            dato_nodo = nodo.get_datos()
            lista_hijos = []
            for un_hijo in conexiones[dato_nodo]:
                hijo = Nodo(un_hijo)
                # Calcular costo acumulado g(n)
                costo = conexiones[dato_nodo][un_hijo]
                hijo.set_costo(nodo.get_costo() + costo)
                lista_hijos.append(hijo)
                if not hijo.en_lista(nodos_visitados):
                    # Si esta en la lista se sustituye con
                    # el nuevo valor del costo si es menor
                    if hijo.en_lista(nodos_frontera):
                        for n in nodos_frontera:
                            if n.igual(hijo) and n.get_costo() > hijo.get_costo():
                                nodos_frontera.remove(n)
                                nodos_frontera.append(hijo)
                    else:
                        nodos_frontera.append(hijo)
            nodo.set_hijos(lista_hijos)

if __name__ == "__main__":
    conexiones = {
        'Jiloyork':{'CDMX': 125, 'QRO':513},
        'MORELOS':{'QRO':524},
        'CDMX':{'Jiloyork': 125, 'QRO':423, 'HGO':491},
        'HGO':{'CDMX':491, 'QRO':356, 'MEXICALI':309, 'MTY':346},
        'QRO':{'SLP':203, 'MORELOS':514, 'Jiloyork':513, 'CDMX':423, 'MTY':603,\
                'SONORA':437, 'HGO':356, 'MEXICALI':313, 'AGS':599},
        'SLP':{'AGS':390, 'QRO':203},
        'AGS':{'SLP':390, 'QRO':599},
        'SONORA':{'QRO':437, 'MEXICALI':394},
        'MEXICALI':{'MTY':296, 'HGO':309, 'QRO':313},
        'MTY':{'MEXICALI':296, 'QRO':603, 'HGO':346}
    }

coord = {
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

estado_inicial = 'Jiloyork'
solucion = 'MTY'
nodo_solucion = buscar_solucion_USC(conexiones, estado_inicial, solucion)
# Mostrar el Resultado
resultado = []
nodo = nodo_solucion
while nodo.get_padre() != None:
    resultado.append(nodo.get_datos())
    nodo = nodo.get_padre()
resultado.append(estado_inicial)
resultado.reverse()
print(resultado)
print('Costo:: ', str(nodo_solucion.get_costo()))

