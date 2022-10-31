from flask import Flask, render_template, request, session, redirect, url_for

from extraccion import obtener_cambio
from database import registro, login, registrado, bbdd_medialocal, bbdd_mediaremoto, obtener_numero_medias_local, \
    obtener_numero_medias_remoto, obtener_graficas_local
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
# Details on the Secret Key: https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY
# NOTE: The secret key is used to cryptographically-sign the cookies used for storing
#       the session data.
app.secret_key = '0123456789'

#medias_local = 0

@app.route("/")
def hello():
    cambio = obtener_cambio()
    if "name" in session:
        medias_local = obtener_numero_medias_local(session["name"])
        medias_remoto = obtener_numero_medias_remoto(session["name"])
        return render_template("index.html", cambio=cambio, medias_local=medias_local, medias_remoto=medias_remoto)
    else:
        return render_template("index.html", cambio=cambio)


@app.route("/registro", methods=['GET'])
def lanzar_pagina_registro():
    return render_template("registro.html")


@app.route("/login", methods=['GET'])
def lanzar_pagina_login():
    return render_template("login.html")


@app.route("/logout", methods=['GET'])
def logout():
    session.pop('name', default=None)
    return redirect("/")


@app.route("/registro", methods=['POST'])
def procesar_registro():
	password = generate_password_hash(request.form["clave"])
	username = request.form["username"]
	email = request.form["email"]
	check_estado = registrado(email)
	if check_estado:
		return render_template("registrado.html")
	else:
		medialocal = 0
		mediaremoto = 0
		estado = registro(email, username, password, medialocal, mediaremoto)
		session["name"] = username
		return redirect("/")


@app.route("/login", methods=['POST'])
def procesar_login():
	estado = login(request.form["username"], request.form["clave"])
	if estado:
		session["name"] = request.form["username"]
	return redirect("/")


@app.route("/medialocal", methods=['POST'])
def media_local():
	if session["name"]:
		cambio = obtener_cambio()
		media = bbdd_medialocal(session["name"])
		medias_local = obtener_numero_medias_local(session["name"])
		medias_remoto = obtener_numero_medias_remoto(session["name"])
		graficas = obtener_graficas_local(session["name"])
		return render_template("index.html", media=media, cambio=cambio, medias_local=medias_local, medias_remoto=medias_remoto)
	else:
		return redirect("/")


@app.route("/mediaremoto", methods=['POST'])
def media_remoto():
	if session["name"]:
		media = bbdd_mediaremoto(session["name"])
		cambio = obtener_cambio()
		medias_local = obtener_numero_medias_local(session["name"])
		medias_remoto = obtener_numero_medias_remoto(session["name"])
		return render_template("index.html", media=media, cambio=cambio, medias_local=medias_local, medias_remoto=medias_remoto)
	else:
		return redirect("/")

@app.route("/graficas", methods=['GET'])
def graficas_externas():
	if session["name"]:
		return render_template("graficas.html")
	else:
		return redirect("/")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
