import pymongo
import datetime
import numpy as np
from datetime import date
from werkzeug.security import check_password_hash


#devuelve True si se registro
def registro(email, username, password, medialocal, mediaremoto):
	myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
	mydb = myclient["practica"]
	mycol = mydb["usuarios"]
	usuario = {"username":username, "email":email, "clave":password, "mediaslocal":medialocal, "mediasremoto":mediaremoto}
	x = mycol.insert_one(usuario)
	return True


#Devuelve True si se logueo
#devuelve False si no esta registrado
def login(username, password):
	myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
	mydb = myclient["practica"]
	mycol = mydb["usuarios"]
	myquery = {"username":username}
	mydoc = mycol.find_one(myquery)
	if mydoc:
		comprobacion = check_password_hash(mydoc["clave"], password)
		if comprobacion:
			return True
		else:
			return False
	else:
		return False

def registrado(email):
# Mira en la base de datos local si el email que se ha insertado ya tiene cuenta
	myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
	mydb = myclient["practica"]
	mycol = mydb["usuarios"]
	myquery = {"email":email}
	mydoc = mycol.find_one(myquery)
	if mydoc:
		return True
	else:
		return False


def bbdd_medialocal(usuario):
# Da la media de los datos en la bbdd local
	myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
	mydb = myclient["practica"]
	mycol = mydb["cambios"]
	valores = 0
	for ind in mycol.find():
		valores = valores + ind.get("valor")
	num_valores = mycol.count_documents({})
	media = valores / num_valores
	return media


def bbdd_mediaremoto(usuario):
# Da la media de los datos de la bbdd remota
	return True


def obtener_numero_medias_local(usuario):
# Devuelve el numero de medias que haya pedido el usuario de forma local
	myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
	mydb = myclient["practica"]
	mycol = mydb["usuarios"]
	myquery = {"username":usuario}
	mydoc = mycol.find_one(myquery)
	if mydoc:
		media_anterior = mydoc.get("mediaslocal")
		nueva_media = media_anterior + 1
		mycol.update_one({"mediaslocal":media_anterior}, {"$set":{"mediaslocal":nueva_media}})
		return nueva_media


def obtener_numero_medias_remoto(usuario):
# Devuelve el numero de medias que haya pedido el usuario de forma remota
	return str(0)


def obtener_graficas_local(usuario):
# Devuelve la gráfica de los valores insertados en la base de datos local en función del tiempo.
	myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
	mydb = myclient["practica"]
	mycol = mydb["cambios"]
	eje_y = 0
	eje_x = 0
	data = []
	for ind in mycol.find():
		valor = ind.get("valor")
		data[ind] = valor
	print(eje_y)
	if eje_y:
		return True
	else:
		return False


def obtener_graficas_remoto(usuario):
# Devuelve la gráfica de los valores insertados en la base de datos remota en función del tiempo.
	return True

def insertar_cambio(valor):
	myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
	mydb = myclient["practica"]
	mycol = mydb["cambios"]
	now = datetime.datetime.now()
	hora = str(now.hour+2) + ":" + str(now.minute)
	today = date.today()
	fecha = today.strftime("%d/%m/%Y")
	cambio = {"valor":valor, "hora":hora, "fecha":fecha}
	x = mycol.insert_one(cambio)
	return True
