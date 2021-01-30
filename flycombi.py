#!/usr/bin/python3
import sys
import csv
from grafo import *
from biblioteca import *
from collections import defaultdict

RANDOM_WALK1 = 1000
RANDOM_WALK2 = 250
RAPIDO = 0
BARATO = 1
VUELOS = 2

def separar_lineas(linea):
	lista = []
	lista = linea.rstrip().split(" ", 1)
	operaciones = lista[0]
	if len(lista) > 1:
			parametros = lista[1].split(',')
	else:
		parametros = None
	return operaciones, parametros

def listar_operaciones():
	print("camino_mas")
	print("camino_escalas")
	print("centralidad")
	print("centralidad_aprox")
	print("nueva_aerolinea")
	print("vacaciones")

def cargar_instrucciones(instrucciones):
	operaciones = []
	for linea in instrucciones:
		operaciones.append(linea)
	return operaciones

def cargar_datos(grafo, aeropuertos_csv, vuelos_csv):
	ciudades = defaultdict(list)
	archivo_aeropuertos = open(aeropuertos_csv, newline='')
	archivo_vuelos = open(vuelos_csv,newline='')
	data_aeropuertos = csv.reader(archivo_aeropuertos, delimiter=',')
	data_vuelos = csv.reader(archivo_vuelos, delimiter=',')

	for info_aeropuertos in data_aeropuertos:
		ciudades[info_aeropuertos[0]].append(info_aeropuertos[1])
		grafo.agregar_vertice(info_aeropuertos[1])
	for info_vuelos in data_vuelos:
		grafo.agregar_arista(info_vuelos[0], info_vuelos[1], [int(info_vuelos[2]), int(info_vuelos[3]), int(info_vuelos[4])]) #se podria hacer lista

	archivo_aeropuertos.close()
	archivo_vuelos.close()
	return ciudades

def flycombi(aeropuertos_csv, vuelos_csv, instrucciones):
	grafo = Grafo()
	ciudades = cargar_datos(grafo, aeropuertos_csv, vuelos_csv)
	for linea in instrucciones:
		operacion, parametros = separar_lineas(linea)
		realizar_operaciones(grafo, operacion, parametros, ciudades)

def camino_mas(grafo, especificacion, ciudad_origen, ciudad_destino):
	if especificacion == "barato":
		descripcion = BARATO
	else:
		descripcion = RAPIDO
	origen_actual = ""
	destino_actual = ""
	minimo_actual = {destino_actual:float('inf')}
	for origen in ciudad_origen:
		padres, distancia = dijkstra(grafo, origen, descripcion)
	for destino in ciudad_destino:
		if distancia[destino] < minimo_actual[destino_actual]:
			padres_origen = padres
			origen_actual = origen
			destino_actual = destino
			minimo_actual[destino_actual] = distancia[destino]
	recorrido = traceback(origen_actual, destino_actual, padres_origen, [])
	recorrido.append(origen_actual)	
	imprimir_viajes(recorrido)

def imprimir_viajes(recorrido):
	for viaje in reversed(recorrido):
		if viaje == recorrido[0]:
			print(viaje)
		else:
			print("{} -> ".format(viaje), end = '')

def camino_escalas(grafo, ciudad_origen, ciudad_destino):
	origen_actual = ""
	destino_actual = ""
	minimo_actual = {destino_actual:float('inf')}
	for origen in ciudad_origen:
		padres, orden = bfs(grafo, origen)
		for destino in ciudad_destino:
			if orden[destino] < minimo_actual[destino_actual]:
				padres_origen = padres
				origen_actual = origen
				destino_actual = destino
				minimo_actual[destino_actual] = orden[destino]
	recorrido = traceback(origen_actual, destino_actual, padres_origen, [])
	recorrido.append(origen_actual)
	imprimir_viajes(recorrido)

def traceback(origen, destino, padres, recorrido):
	recorrido.append(destino)
	if padres[destino] == origen:
		return recorrido
	traceback(origen, padres[destino], padres, recorrido)
	return recorrido

def centralidad(grafo, n):
	centralidad = betweeness_centralidad(grafo)
	centralidad_items = list(centralidad.items())
	
	centralidad_items.sort(key=lambda x: x[1], reverse = True)
	for i in range(0, n):
		if i == n-1:
			print((centralidad_items[i][0]))
		else:
			print("{}, ".format(centralidad_items[i][0]),end = '')

def imprimir_camino_centralidad(camino, n):
	for i in range(n-1):
		print("{}, ".format(camino[i][0]),end = "")
	print("{}".format(camino[n-1][0]))

def centralidad_aproximada(grafo, n):
	aux = {}
	n_aux = int(n)
	for v in grafo:
		aux[v] = 0
	for i in range(1500):
		camino = random_walk(grafo, 500)	
		for v in camino:
			aux[v] += 1
	cent = ordenar_vertices(aux)
	
	for i in range(0, n):
		if i == n-1:
			print((cent[i][0]))
		else:
			print("{}, ".format(cent[i][0]),end = '')

def vacaciones(grafo, n, ciudad_origen):
	for origen in ciudad_origen:
		recorrido = dfs_cambiado(grafo, origen, int(n))
		if len(recorrido) > 0:
			break
	if recorrido:		
		print("{} -> ".format(recorrido[0]), end = '')
		for viaje in recorrido:
			if viaje == recorrido[-1]:
				continue
			else:
				print("{} -> ".format(viaje),end = '')
		print("{}".format(recorrido[-1]))
	else:
		print("No se encontro recorrido")

def nueva_aerolinea(grafo, ruta):
	arbol = mst_prim(grafo, BARATO)
	caminos = []
	with open(ruta, "w", newline = '') as archivo:
		csvwriter = csv.writer(archivo, delimiter=',')
		exportar_aerolinea(arbol, archivo, caminos)
	print("OK")
	return caminos

def realizar_operaciones(grafo, operacion, parametros, ciudades):
	if operacion == "listar_operaciones": 
		listar_operaciones() 

	elif operacion == "camino_mas": #1 estrella
		camino_mas(grafo, parametros[0], ciudades[parametros[1]], ciudades[parametros[2]])

	elif operacion == "camino_escalas": #1 estrella
		camino_escalas(grafo, ciudades[parametros[0]], ciudades[parametros[1]])

	elif operacion == "centralidad": #3 estrellas
		centralidad(grafo, int(parametros[0]))

	elif operacion == "vacaciones": #3 estrellas
		vacaciones(grafo, parametros[1], ciudades[parametros[0]])

	elif operacion == "centralidad_aprox": #1 estrella
		centralidad_aproximada(grafo, int(parametros[0]))

	elif operacion == "nueva_aerolinea": #1 estrella
		nueva_aerolinea(grafo, parametros[0])
	
#El programa empieza aca
if __name__ == "__main__":
	if len(sys.argv) == 3:
		flycombi(sys.argv[1], sys.argv[2], sys.stdin)
	else:
		print("Error en cantidad de parametros.")
		sys.exit()
