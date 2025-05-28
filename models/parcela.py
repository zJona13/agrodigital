from conexionBD import Conexion

class Parcela:
    def listar(self, agricultor_id):
        
        #Abrir la conexión
        con = Conexion().open

        #Crear un cursor para ejecutar una setencia SQL
        cursor = con.cursor()

        #Definir la sentencia SQL y sus parámetros
        sql = """SELECT p.nombre, p.ubicacion, p.area, pc.lat, pc.lng FROM parcela p INNER JOIN parcela_coordenadas pc ON (p.id=pc.parcela_id) WHERE p.agricultor_id=%s ORDER BY p.id, pc.id"""
        #Ejecutar el cursor
        cursor.execute(sql, [agricultor_id])

        #Obtener los resultados de la consulta
        registros = cursor.fetchall()

        #Cerrar el cursor y la conexión
        cursor.close()
        con.close()
        if not registros:
            return []
        #preparar el resultado
        parcelas_dict = {}
        for row in registros:
            parcela_id = row['id']
            if parcela_id not in parcelas_dict:
                parcelas_dict[parcela_id]={
                "id": row['id'],
                "nombre": row['nombre'],
                "ubicacion": row['ubicacion'],
                "area": row['area'],
                "coordenadas": []
                }
                
            coordenada = {"lat": float(row['lat']), "lng": float(row['lng'])}
            parcelas_dict[parcela_id]["coordenadas"].append(coordenada)
        return list(parcelas_dict.values())