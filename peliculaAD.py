import pymysql.cursors
from bd import obtenerconexion

# ==========================================================
# CLASE PELICULA
# ==========================================================

class clsPelicula:

    def __init__(self,
                 p_idPelicula=None,
                 p_titulo=None,
                 p_director=None,
                 p_anio=None,
                 p_duracion=None,
                 p_genero=None,
                 p_clasificacion=None,
                 p_trailer_url=None,
                 p_sinopsis=None):

        self.idPelicula = p_idPelicula
        self.titulo = p_titulo
        self.director = p_director
        self.anio = p_anio
        self.duracion = p_duracion
        self.genero = p_genero
        self.clasificacion = p_clasificacion
        self.trailer_url = p_trailer_url
        self.sinopsis = p_sinopsis


# ==========================================================
# INSERTAR
# ==========================================================

def insertar_pelicula(p_Pelicula):

    try:

        conn = obtenerconexion()

        if conn:

            with conn:

                with conn.cursor() as cursor:

                    sql = """
                    INSERT INTO peliculas
                    (
                        titulo,
                        director,
                        anio,
                        duracion,
                        genero,
                        clasificacion,
                        trailer_url,
                        sinopsis
                    )
                    VALUES
                    (%s,%s,%s,%s,%s,%s,%s,%s)
                    """

                    cursor.execute(sql,

                    (

                        p_Pelicula.titulo,
                        p_Pelicula.director,
                        p_Pelicula.anio,
                        p_Pelicula.duracion,
                        p_Pelicula.genero,
                        p_Pelicula.clasificacion,
                        p_Pelicula.trailer_url,
                        p_Pelicula.sinopsis

                    ))

                conn.commit()

            return True

        return False

    except Exception as e:

        print(repr(e))

        return False


# ==========================================================
# ACTUALIZAR
# ==========================================================

def actualizar_peliculaAD(p_Pelicula):

    try:

        conn = obtenerconexion()

        if conn:

            with conn:

                with conn.cursor() as cursor:

                    sql = """
                    UPDATE peliculas
                    SET
                        titulo=%s,
                        director=%s,
                        anio=%s,
                        duracion=%s,
                        genero=%s,
                        clasificacion=%s,
                        trailer_url=%s,
                        sinopsis=%s
                    WHERE id=%s
                    """

                    cursor.execute(sql,

                    (

                        p_Pelicula.titulo,
                        p_Pelicula.director,
                        p_Pelicula.anio,
                        p_Pelicula.duracion,
                        p_Pelicula.genero,
                        p_Pelicula.clasificacion,
                        p_Pelicula.trailer_url,
                        p_Pelicula.sinopsis,
                        p_Pelicula.idPelicula

                    ))

                conn.commit()

            return True

        return False

    except Exception as e:

        print(repr(e))

        return False


# ==========================================================
# ELIMINAR
# ==========================================================

def eliminar_peliculaAD(idPelicula):

    try:

        conn = obtenerconexion()

        if conn:

            with conn:

                with conn.cursor() as cursor:

                    sql = """
                    DELETE FROM peliculas
                    WHERE id=%s
                    """

                    cursor.execute(sql,(idPelicula))

                conn.commit()

            return True

        return False

    except Exception as e:

        print(repr(e))

        return False

# ==========================================================
# LEER TODAS LAS PELICULAS
# ==========================================================

def leer_peliculas():

    try:

        conn = obtenerconexion()

        resultado = None

        if conn:

            with conn:

                with conn.cursor() as cursor:

                    sql = """
                    SELECT
                        id,
                        titulo,
                        director,
                        anio,
                        duracion,
                        genero,
                        clasificacion,
                        trailer_url,
                        sinopsis
                    FROM peliculas
                    ORDER BY titulo
                    """

                    cursor.execute(sql)

                    resultado = cursor.fetchall()

        return resultado

    except Exception:

        raise


# ==========================================================
# LEER PELICULA POR ID
# ==========================================================

def leer_pelicula_xID(idPelicula):

    try:

        conn = obtenerconexion()

        resultado = None

        if conn:

            with conn:

                with conn.cursor() as cursor:

                    sql = """
                    SELECT
                        id,
                        titulo,
                        director,
                        anio,
                        duracion,
                        genero,
                        clasificacion,
                        trailer_url,
                        sinopsis
                    FROM peliculas
                    WHERE id=%s
                    """

                    cursor.execute(sql,(idPelicula))

                    resultado = cursor.fetchall()

        return resultado

    except Exception:

        raise


# ==========================================================
# VERIFICAR SI EXISTE POR NOMBRE
# ==========================================================

def leer_pelicula_xNombre(nombre):

    try:

        conn = obtenerconexion()

        resultado = None

        if conn:

            with conn:

                with conn.cursor() as cursor:

                    sql = """
                    SELECT
                        COUNT(*) AS contador
                    FROM peliculas
                    WHERE titulo=%s
                    """

                    cursor.execute(sql,(nombre))

                    resultado = cursor.fetchall()

        return resultado

    except Exception:

        raise


# ==========================================================
# BUSCAR POR GENERO
# ==========================================================

def leer_peliculas_genero(genero):

    try:

        conn = obtenerconexion()

        resultado = None

        if conn:

            with conn:

                with conn.cursor() as cursor:

                    sql = """
                    SELECT
                        id,
                        titulo,
                        director,
                        anio,
                        duracion,
                        genero,
                        clasificacion,
                        trailer_url,
                        sinopsis
                    FROM peliculas
                    WHERE genero=%s
                    ORDER BY titulo
                    """

                    cursor.execute(sql,(genero))

                    resultado = cursor.fetchall()

        return resultado

    except Exception:

        raise


# ==========================================================
# BUSCAR POR DIRECTOR
# ==========================================================

def leer_peliculas_director(director):

    try:

        conn = obtenerconexion()

        resultado = None

        if conn:

            with conn:

                with conn.cursor() as cursor:

                    sql = """
                    SELECT *
                    FROM peliculas
                    WHERE director=%s
                    ORDER BY titulo
                    """

                    cursor.execute(sql,(director))

                    resultado = cursor.fetchall()

        return resultado

    except Exception:

        raise


# ==========================================================
# BUSCAR POR CLASIFICACION
# ==========================================================

def leer_peliculas_clasificacion(clasificacion):

    try:

        conn = obtenerconexion()

        resultado = None

        if conn:

            with conn:

                with conn.cursor() as cursor:

                    sql = """
                    SELECT *
                    FROM peliculas
                    WHERE clasificacion=%s
                    ORDER BY titulo
                    """

                    cursor.execute(sql,(clasificacion))

                    resultado = cursor.fetchall()

        return resultado

    except Exception:

        raise

# ==========================================================
# BUSCAR POR AÑO
# ==========================================================

def leer_peliculas_anio(anio):

    try:

        conn = obtenerconexion()

        resultado = None

        if conn:

            with conn:

                with conn.cursor() as cursor:

                    sql = """
                    SELECT *
                    FROM peliculas
                    WHERE anio=%s
                    ORDER BY titulo
                    """

                    cursor.execute(sql, (anio))

                    resultado = cursor.fetchall()

        return resultado

    except Exception:

        raise


# ==========================================================
# BUSCAR POR DURACION
# ==========================================================

def leer_peliculas_duracion(duracion):

    try:

        conn = obtenerconexion()

        resultado = None

        if conn:

            with conn:

                with conn.cursor() as cursor:

                    sql = """
                    SELECT *
                    FROM peliculas
                    WHERE duracion=%s
                    ORDER BY titulo
                    """

                    cursor.execute(sql, (duracion))

                    resultado = cursor.fetchall()

        return resultado

    except Exception:

        raise


# ==========================================================
# BUSCAR POR RANGO DE AÑOS
# ==========================================================

def leer_peliculas_rango_anios(anioInicio, anioFin):

    try:

        conn = obtenerconexion()

        resultado = None

        if conn:

            with conn:

                with conn.cursor() as cursor:

                    sql = """
                    SELECT *
                    FROM peliculas
                    WHERE anio BETWEEN %s AND %s
                    ORDER BY anio
                    """

                    cursor.execute(sql, (anioInicio, anioFin))

                    resultado = cursor.fetchall()

        return resultado

    except Exception:

        raise


# ==========================================================
# BUSCAR TITULO PARCIAL
# ==========================================================

def leer_peliculas_like(titulo):

    try:

        conn = obtenerconexion()

        resultado = None

        if conn:

            with conn:

                with conn.cursor() as cursor:

                    sql = """
                    SELECT *
                    FROM peliculas
                    WHERE titulo LIKE %s
                    ORDER BY titulo
                    """

                    cursor.execute(sql, ("%" + titulo + "%",))

                    resultado = cursor.fetchall()

        return resultado

    except Exception:

        raise


# ==========================================================
# CONTAR TOTAL DE PELICULAS
# ==========================================================

def total_peliculas():

    try:

        conn = obtenerconexion()

        resultado = None

        if conn:

            with conn:

                with conn.cursor() as cursor:

                    sql = """
                    SELECT COUNT(*) AS total
                    FROM peliculas
                    """

                    cursor.execute(sql)

                    resultado = cursor.fetchall()

        return resultado

    except Exception:

        raise


# ==========================================================
# CONTAR PELICULAS POR GENERO
# ==========================================================

def total_genero(genero):

    try:

        conn = obtenerconexion()

        resultado = None

        if conn:

            with conn:

                with conn.cursor() as cursor:

                    sql = """
                    SELECT COUNT(*) AS total
                    FROM peliculas
                    WHERE genero=%s
                    """

                    cursor.execute(sql, (genero))

                    resultado = cursor.fetchall()

        return resultado

    except Exception:

        raise


# ==========================================================
# OBTENER ULTIMA PELICULA REGISTRADA
# ==========================================================

def ultima_pelicula():

    try:

        conn = obtenerconexion()

        resultado = None

        if conn:

            with conn:

                with conn.cursor() as cursor:

                    sql = """
                    SELECT *
                    FROM peliculas
                    ORDER BY id DESC
                    LIMIT 1
                    """

                    cursor.execute(sql)

                    resultado = cursor.fetchall()

        return resultado

    except Exception:

        raise