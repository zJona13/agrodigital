from conexionBD import Conexion

class Actividad:
    def registrar(self, cultivo_id, descripcion, fecha, actividad_tipo_id, detalle):
        #Abrir la conexión a la base de datos
        con = Conexion().open
        
        # Crear un cursor para ejecutar la consulta
        cursor = con.cursor()
        
        try:
            #1: Insertar en la tabla actividad
            sql = """
                INSERT INTO actividad (cultivo_id, descripcion, fecha, actividad_tipo_id, total)
                VALUES (%s, %s, %s, %s, 0)
            """
            cursor.execute(sql, [cultivo_id, descripcion, fecha, actividad_tipo_id])
            
            #Obtener el ID de la actividad registrada, el cual será utilizada para registrar el detalle
            actividad_id = cursor.lastrowid
            
            #2: Insertar en la tabla actividad_detalle
            sql_detalle = """
                INSERT INTO actividad_detalle (actividad_id, descripcion, precio_unitario, cantidad, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """

            total = 0
            for item in detalle:
                cursor.execute(sql_detalle, 
                                [
                                    actividad_id, 
                                    item['descripcion'], 
                                    item['precio_unitario'], 
                                    item['cantidad'],
                                    float(item['precio_unitario']) * float(item['cantidad'])
                                ])
                total += float(item['precio_unitario']) * float(item['cantidad'])    
                
            #3: Actualizar el total de la actividad, en función al detalle
            sql_actualizar_total = """
                UPDATE actividad SET total = %s WHERE id = %s
            """
            cursor.execute(sql_actualizar_total, [total, actividad_id])
            
            # Retonar true si todas las operaciones se realizaron correctamente
            con.commit()
            return True, actividad_id
        except Exception as e:
            # Si hay un error entonces se revoca toda la transacción
            con.rollback()
            return False, str(e)    
        finally:
            # Cerrar el cursor y la conexión
            cursor.close()
            con.close()

    def anular(self, id):

            #Abrir la conexión
            con = Conexion().open

            #Crear un cursor para ejecutar una setencia SQL
            cursor = con.cursor()

            #Definir la sentencia SQL para validar la baja del agricultor
            sql = """
            select estado_id from actividad where id = %s
            """
            #Ejecutar el cursor
            cursor.execute(sql, [id])
            
            #Recuperar el resultado de la consulta sql select
            resultado = cursor.fetchone()
            
            if resultado:
                # Si el agricultor ya está dado de baja, retornar un mensaje
                if resultado['estado_id'] == 2:
                    return False, 'La actividad ha sido anulada'
                else:
                    #Ejecutar la sentencia SQL para dar de baja al agricultor
                    sql = """
                            update actividad set estado_id=2, fecha_hora_anulacion=now() where id = %s
                        """
                    #Ejecutar el cursor
                    cursor.execute(sql, [id])

                    #Confirmar los datos en la BD
                    con.commit()

                    #Cierra el cursor y la conexión a la BD
                    cursor.close()
                    con.close()
            else:
                return False, 'La actividad no existe'
            
            #Retonar un valor boolean (true)
            return True,'Ok'