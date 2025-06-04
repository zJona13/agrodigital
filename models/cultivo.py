from conexionBD import Conexion

class Cultivo:
    def listar(self):
        #Abrir la conexión a la base de datos
        con = Conexion().open
        
        # Crear un cursor para ejecutar la consulta
        cursor = con.cursor()
        
        sql = """SELECT * FROM cultivo order by fecha_inicio desc, nombre_cultivo"""
        
        cursor.execute(sql)
        
        resultado = cursor.fetchall()
        
        cursor.close()
        con.close()
        
        if resultado:
            return resultado
        else:
            return None