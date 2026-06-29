import pymysql.cursors

def obtenerconexion():
   try:
        connection = pymysql.connect(host='localhost',
                                    user='root',
                                    password='',
                                    database='prepc2',
                                    cursorclass=pymysql.cursors.DictCursor)
        return connection
   except:
       raise