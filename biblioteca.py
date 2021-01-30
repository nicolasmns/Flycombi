from queue import *
from heapq import *
from grafo import *
import math
import random

def bfs(grafo, origen):
	visitados = set()
	padres = {}
	orden = {}
	q = Queue()
	visitados.add(origen)
	padres[origen] = None
	orden[origen] = 0
	q.put(origen)
	while not q.empty():
		v = q.get()
		for w in grafo.obtener_adyacentes(v):
			if w not in visitados:
				visitados.add(w)
				q.put(w)
				padres[w] = v
				orden[w] = orden[v] + 1
	return padres, orden

def dijkstra(grafo, origen, desc):
	dist = {}
	padre = {}
	for v in grafo:
		dist[v] = float('inf')
	dist[origen] = 0
	padre[origen] = None
	q = []
	heappush(q, (origen, dist[origen]))
	while q:
		v, peso = heappop(q)
		for w in grafo.obtener_adyacentes(v):
			if dist[v] + grafo.obt_peso(v, w)[desc] < dist[w]:
				dist[w] = dist[v] + grafo.obt_peso(v, w)[desc]
				padre[w] = v
				heappush(q, [w, dist[w]]) # o actualizo
	return padre, dist

def mst_prim(grafo, peso):
	vertice = grafo.vertice_aleatorio()
	visitados = set()
	visitados.add(vertice)
	heap = []
	arbol = Grafo()
	for v in grafo.obtener_vertices():
		arbol.agregar_vertice(v)
	for w in grafo.obtener_adyacentes(vertice):
		heappush(heap, (grafo.obt_peso(vertice, w)[peso], vertice, w))
	while heap:
		peso_arista, vertice, w = heappop(heap)
		if w in visitados:
			continue
		arbol.agregar_arista(vertice, w, grafo.obt_peso(vertice, w))
		visitados.add(w)
		for u in grafo.obtener_adyacentes(w):
			if u not in visitados: heappush(heap, (grafo.obt_peso(w, u)[peso], w, u))
	return arbol

def ordenar_vertices(orden):
	lista_vertices = []
	for v in orden:
		if orden[v] != float('inf'):
			lista_vertices.append((v, orden[v]))
	lista_vertices.sort(reverse = True, key = lambda x: x[1])
	return lista_vertices

def recorrido_dfs(grafo, sin_salida, camino, largo, largo_recorrido):
	if largo == largo_recorrido and camino[0] == camino[-1]:
		return camino
	if largo < largo_recorrido:
		ultimo = camino[-1]
		camino_actual = camino
		for w in grafo.obtener_adyacentes(ultimo):
			if w in sin_salida.get(largo, ()) or w in camino and largo < largo_recorrido - 1: 
				continue
			camino_actual.append(w)
			ciclo = recorrido_dfs(grafo, sin_salida, camino, largo + 1, largo_recorrido)
			if ciclo:
				return ciclo
	if largo not in sin_salida:
		sin_salida[largo] = set()
	sin_salida[largo].add(camino.pop())
	return []

def dfs_cambiado(grafo, origen, n):
	sin_salida = {}
	return recorrido_dfs(grafo,sin_salida, [origen], 1, n + 1)

def betweeness_centralidad(grafo):
	cent = {}
	for v in grafo.obtener_vertices():
		cent[v] = 0
	for v in cent:
		padre, distancias = bfs(grafo, v)
		cent_aux = {}
		for w in grafo: cent_aux[w] = 0
		vertices_ordenados = ordenar_vertices(distancias)
		for w, distancia in vertices_ordenados:
			if w == v:
				continue
			cent_aux[padre[w]] += 1 + cent_aux[w]
		for w in grafo.obtener_vertices():
			if w == v: continue
			cent[w] += cent_aux[w]
	return cent

def adyacente_aleatorio(grafo, v):
	adyacentes = grafo.obtener_adyacentes(v)
	return random.choice(adyacentes)

def _random_walk(grafo, n, ruta, v, contador):
	if contador >= n:
		return False
	ruta.append(v)
	siguiente = adyacente_aleatorio(grafo, v)
	_random_walk(grafo, n, ruta, siguiente, contador+1)
	return True

def random_walk(grafo, n):
	origen = grafo.vertice_aleatorio()
	ruta = []
	resultado = _random_walk(grafo, n, ruta, origen, 0)
	if resultado == False:
		print("Error")
	return ruta

def exportar_aerolinea(grafo, archivo, rutas=None):
	visitados = set()
	for v in grafo:
		visitados.add(v)
		for w in grafo.obtener_adyacentes(v):
			if w in visitados: continue
			tiempo, precio, vuelos = grafo.obt_peso(v, w)
			archivo.write(",".join([v, w, str(tiempo), str(precio), str(vuelos)])+"\n")
			if rutas != None:
				rutas.append(v)
	rutas.append(w)
