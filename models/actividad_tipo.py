from conexionBD import Conexion

class ActividadTipo:
    def listar(self):
        #Abrir la conexión a la base de datos
        con = Conexion().open
        
        # Crear un cursor para ejecutar la consulta
        cursor = con.cursor()
        
        sql = """
            SELECT *
            FROM actividad_tipo ORDER BY descripcion ASC
        """
        
        cursor.execute(sql)
        
        resultado = cursor.fetchall()
        
        cursor.close()
        con.close()
        
        if resultado:
            return resultado
        else:
            return None