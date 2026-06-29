import pymysql.cursors

def obtenerconexion():
   try:
        connection = pymysql.connect(host='jcachay.mysql.pythonanywhere-services.com',
                                    user='jcachay',
                                    password='abcDEF$123',
                                    database='jcachay$dawb_datos',
                                    cursorclass=pymysql.cursors.DictCursor)
        return connection
   except:
       raise
