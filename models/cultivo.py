from conexionBD import Conexion

class Cultivo:
    def listar(self, id):
        #Abrir la conexión a la base de datos
        con = Conexion().open
        
        # Crear un cursor para ejecutar la consulta
        cursor = con.cursor()
        
        sql = """SELECT c.* FROM cultivo c INNER JOIN parcela p ON (c.parcela_id = p.id) WHERE p.agricultor_id = % order by fecha_inicio desc, nombre_cultivo"""
        
        cursor.execute(sql, [id])
        
        resultado = cursor.fetchall()
        
        cursor.close()
        con.close()
        
        if resultado:
            return resultado
        else:
            return None
