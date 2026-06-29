from flask import Flask, render_template, request, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from peliculaAD import (
    clsPelicula,
    insertar_pelicula,
    actualizar_peliculaAD,
    eliminar_peliculaAD,
    leer_peliculas,
    leer_pelicula_xID,
    leer_pelicula_xNombre,
    leer_peliculas_genero
)
from markupsafe import escape

# ==========================================================
# CONFIGURACIÓN DE USUARIOS JWT
# ==========================================================

class User(object):

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id


users = [

    User(1, "user1", "abcxyz"),
    User(2, "user2", "abcxyz")

]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):

    user = username_table.get(username, None)

    if user and user.password.encode("utf-8") == password.encode("utf-8"):
        return user


def identity(payload):

    user_id = payload["identity"]

    return userid_table.get(user_id, None)


# ==========================================================
# CONFIGURACIÓN FLASK
# ==========================================================

app = Flask(__name__)

app.debug = True

app.config["SECRET_KEY"] = "super-secret"

jwt = JWT(app, authenticate, identity)


# ==========================================================
# RUTAS HTML
# ==========================================================

@app.route("/")
def listar_peliculas():

    try:

        resultado = leer_peliculas()

        return render_template("lista.html", datos=resultado)

    except:

        return render_template("error500.html")


@app.route("/agregarpelicula")
def inicio():

    return render_template("form_pelicula.html")


@app.route("/cargareditarpelicula/<int:idPelicula>")
def cargareditarpelicula(idPelicula):

    datos = leer_pelicula_xID(idPelicula)

    return render_template(
        "form_pelicula_edit.html",
        pelicula=datos[0]
    )


@app.route("/guardar_pelicula", methods=["POST"])
def guardar_pelicula():

    try:

        objPelicula = clsPelicula(

            0,

            request.form["titulo"],
            request.form["director"],
            request.form["anio"],
            request.form["duracion"],
            request.form["genero"],
            request.form["clasificacion"],
            request.form["trailer"],
            request.form["sinopsis"]

        )

        if insertar_pelicula(objPelicula):

            return render_template("exito.html")

        return "<h2>Error al insertar película</h2>"

    except Exception as e:

        return "<h2>" + repr(e) + "</h2>"


@app.route("/actualizar_pelicula", methods=["POST"])
def actualizar_pelicula():

    try:

        objPelicula = clsPelicula(

            request.form["idPelicula"],

            request.form["titulo"],
            request.form["director"],
            request.form["anio"],
            request.form["duracion"],
            request.form["genero"],
            request.form["clasificacion"],
            request.form["trailer"],
            request.form["sinopsis"]

        )

        if actualizar_peliculaAD(objPelicula):

            return render_template("exito.html")

        return "<h2>Error al actualizar</h2>"

    except Exception as e:

        return "<h2>" + repr(e) + "</h2>"


@app.route("/eliminar_pelicula/<int:idPelicula>")
def eliminar_pelicula(idPelicula):

    try:

        if eliminar_peliculaAD(idPelicula):

            return render_template("exito.html")

        return "<h2>Error al eliminar</h2>"

    except Exception as e:

        return "<h2>" + repr(e) + "</h2>"


# ==========================================================
# API REST
# ==========================================================

@app.route("/api")
def api_info():

    return jsonify({
        "code": 1,
        "data": {
            "nombre": "API REST Películas",
            "version": "1.0",
            "framework": "Flask",
            "seguridad": "JWT",
            "metodos": "GET y POST únicamente"
        },
        "message": "API funcionando correctamente"
    })


@app.route("/api_status")
def api_status():

    return jsonify({
        "code": 1,
        "data": [],
        "message": "Servidor activo"
    })


# ==========================================================
# LISTAR TODAS LAS PELICULAS
# ==========================================================

@app.route("/api_peliculas", methods=["GET"])
@jwt_required()
def api_peliculas():

    rpta = dict()

    try:

        rpta["code"] = 1
        rpta["data"] = leer_peliculas()
        rpta["message"] = "Listado correcto"

        return jsonify(rpta)

    except Exception as e:

        rpta["code"] = -1
        rpta["data"] = []
        rpta["message"] = repr(e)

        return jsonify(rpta)


# ==========================================================
# LEER PELICULA POR ID
# ==========================================================

@app.route("/api_pelicula/<int:idPelicula>", methods=["GET"])
@jwt_required()
def api_pelicula(idPelicula):

    rpta = dict()

    try:

        datos = leer_pelicula_xID(idPelicula)

        if len(datos) > 0:

            rpta["code"] = 1
            rpta["data"] = datos[0]
            rpta["message"] = "Película encontrada"

        else:

            rpta["code"] = 0
            rpta["data"] = []
            rpta["message"] = "Película no encontrada"

        return jsonify(rpta)

    except Exception as e:

        rpta["code"] = -1
        rpta["data"] = []
        rpta["message"] = repr(e)

        return jsonify(rpta)


# ==========================================================
# GUARDAR PELICULA
# ==========================================================

@app.route("/api_guardar_pelicula", methods=["POST"])
@jwt_required()
def api_guardar_pelicula():

    rpta = dict()

    try:

        objPelicula = clsPelicula(

            0,

            request.json["titulo"],
            request.json["director"],
            request.json["anio"],
            request.json["duracion"],
            request.json["genero"],
            request.json["clasificacion"],
            request.json["trailer"],
            request.json["sinopsis"]

        )

        datos = leer_pelicula_xNombre(request.json["titulo"])

        if len(datos) == 1 and datos[0]["contador"] == 0:

            if insertar_pelicula(objPelicula):

                rpta["code"] = 1
                rpta["data"] = []
                rpta["message"] = "Película registrada"

                return jsonify(rpta)

        rpta["code"] = 0
        rpta["data"] = []
        rpta["message"] = "La película ya existe"

        return jsonify(rpta)

    except Exception as e:

        rpta["code"] = -1
        rpta["data"] = []
        rpta["message"] = repr(e)

        return jsonify(rpta)


# ==========================================================
# ACTUALIZAR PELICULA - MODIFICADO: CAMBIADO DE PUT A POST
# ==========================================================

@app.route("/api_actualizar_pelicula", methods=["POST"])
@jwt_required()
def api_actualizar_pelicula():

    rpta = dict()

    try:

        objPelicula = clsPelicula(

            request.json["id"],

            request.json["titulo"],
            request.json["director"],
            request.json["anio"],
            request.json["duracion"],
            request.json["genero"],
            request.json["clasificacion"],
            request.json["trailer"],
            request.json["sinopsis"]

        )

        if actualizar_peliculaAD(objPelicula):

            rpta["code"] = 1
            rpta["data"] = []
            rpta["message"] = "Película actualizada"

        else:

            rpta["code"] = 0
            rpta["data"] = []
            rpta["message"] = "No fue posible actualizar"

        return jsonify(rpta)

    except Exception as e:

        rpta["code"] = -1
        rpta["data"] = []
        rpta["message"] = repr(e)

        return jsonify(rpta)


# ==========================================================
# ELIMINAR PELICULA - MODIFICADO: CAMBIADO DE DELETE A POST
# ==========================================================

@app.route("/api_eliminar_pelicula", methods=["POST"])
@jwt_required()
def api_eliminar_pelicula():

    rpta = dict()

    try:
        # Ahora el ID viene en el JSON del body en lugar de la URL
        idPelicula = request.json["id"]

        if eliminar_peliculaAD(idPelicula):

            rpta["code"] = 1
            rpta["data"] = []
            rpta["message"] = "Película eliminada correctamente"

        else:

            rpta["code"] = 0
            rpta["data"] = []
            rpta["message"] = "No fue posible eliminar"

        return jsonify(rpta)

    except Exception as e:

        rpta["code"] = -1
        rpta["data"] = []
        rpta["message"] = repr(e)

        return jsonify(rpta)


# ==========================================================
# BUSCAR PELICULA POR NOMBRE
# ==========================================================

@app.route("/api_buscar_nombre/<string:titulo>", methods=["GET"])
@jwt_required()
def api_buscar_nombre(titulo):

    rpta = dict()

    try:

        datos = leer_pelicula_xNombre(titulo)

        rpta["code"] = 1
        rpta["data"] = datos
        rpta["message"] = "Consulta realizada"

        return jsonify(rpta)

    except Exception as e:

        rpta["code"] = -1
        rpta["data"] = []
        rpta["message"] = repr(e)

        return jsonify(rpta)


# ==========================================================
# BUSCAR POR GENERO
# ==========================================================

@app.route("/api_genero/<string:genero>", methods=["GET"])
@jwt_required()
def api_genero(genero):

    rpta = dict()

    try:

        rpta["code"] = 1
        rpta["data"] = leer_peliculas_genero(genero)
        rpta["message"] = "Consulta correcta"

        return jsonify(rpta)

    except Exception as e:

        rpta["code"] = -1
        rpta["data"] = []
        rpta["message"] = repr(e)

        return jsonify(rpta)


# ==========================================================
# VERIFICAR SI EXISTE UNA PELICULA
# ==========================================================

@app.route("/api_existe_pelicula/<string:titulo>", methods=["GET"])
@jwt_required()
def api_existe_pelicula(titulo):

    rpta = dict()

    try:

        datos = leer_pelicula_xNombre(titulo)

        existe = datos[0]["contador"] > 0

        rpta["code"] = 1
        rpta["data"] = {
            "existe": existe
        }

        rpta["message"] = "Consulta correcta"

        return jsonify(rpta)

    except Exception as e:

        rpta["code"] = -1
        rpta["data"] = []
        rpta["message"] = repr(e)

        return jsonify(rpta)


# ==========================================================
# TOTAL DE PELICULAS
# ==========================================================

@app.route("/api_total_peliculas", methods=["GET"])
@jwt_required()
def api_total_peliculas():

    rpta = dict()

    try:

        datos = leer_peliculas()

        rpta["code"] = 1
        rpta["data"] = {
            "total": len(datos)
        }

        rpta["message"] = "Cantidad de películas"

        return jsonify(rpta)

    except Exception as e:

        rpta["code"] = -1
        rpta["data"] = []
        rpta["message"] = repr(e)

        return jsonify(rpta)


# ==========================================================
# USUARIO AUTENTICADO
# ==========================================================

@app.route("/api_usuario", methods=["GET"])
@jwt_required()
def api_usuario():

    rpta = dict()

    rpta["code"] = 1

    rpta["data"] = {

        "id": current_identity.id,
        "usuario": current_identity.username

    }

    rpta["message"] = "Usuario autenticado"

    return jsonify(rpta)


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    app.run()
