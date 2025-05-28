from conexionBD import Conexion
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
class Agricultor:
    def __init__(self):
        #instanciar la clase passwordhasher
        self.ph = PasswordHasher()

    def login(self, email, password):
        #abrir la conexion
        con= Conexion().open

        #crear un cursos para ejecutar una sentencia sql
        cursor=con.cursor()

        #definir la sentencia sql y sus parametros
        sql="select id, dni, nombre, email, telefono, password from agricultor where email = %s"

        #ejecutar la sentencia sql y enviarle los valores a los parametros
        cursor.execute(sql,[email])

        #recuperar los registros que devuelve el cursos. como devuelvo un solo registro utilizo "fetchone"
        resultado = cursor.fetchone()

        #cierra el cursor y la conexion a la bd
        cursor.close()
        con.close()

        if resultado: # si se han encontrado los datos del usuario filtrado mediante su email, entonces se procede a verificar el password
            try:
                #verificar si el password almacenado en la bd es el mismo password que ha digitado el usuario
                self.ph.verify(resultado['password'],password)
                return resultado
            except VerifyMismatchError: # si el password no coincide, entonces devuelve none
                return None

                #si no se han encontrado las credenciales del usuario se retorna none
        return None

    def registrar(self, dni, nombre, email, password, telefono):
        #abrir la conexion
        con= Conexion().open

        #crear un cursos para ejecutar una sentencia sql
        cursor = con.cursor()

        #definir la sentencia sql y sus parametros
        sql = """
                insert into agricultor(dni, nombre, email, password, telefono) 
                values(%s, %s, %s, %s, %s)
            """

        #Cifrar password
        password_hasher = self.ph.hash(password)

        #Ejecutar el cursor
        cursor.execute(sql, [dni, nombre, email, password_hasher, telefono])

        # Confirmar los cambios en la base de datos
        con.commit()

        # Cerrar el cursor y la conexión a la BD
        cursor.close()
        con.close()

        #Retonar un valor boolean(True)
        return True      
    
    def actualizar(self, dni, nombre, email, telefono, id):
        #Abrir la conexión
        con = Conexion().open

        #Crear un cursor para ejecutar una setencia SQL
        cursor = con.cursor()

        #Definir la sentencia SQL y sus parámetros
        sql = """
        update agricultor set dni=%s, nombre=%s, email=%s, telefono=%s
        where id = %s
        """
        #Ejecutar el cursor
        cursor.execute(sql, [dni, nombre, email, telefono, id])

        #Confirmar los datos en la BD
        con.commit()

        #Cierra el cursor y la conexión a la BD
        cursor.close()
        con.close()

        #Retonar un valor boolean (true)
        return True

    def actualizar_foto(self, id, foto):

        #Abrir la conexión
        con = Conexion().open

        #Crear un cursor para ejecutar una setencia SQL
        cursor = con.cursor()

        #Definir la sentencia SQL y sus parámetros
        sql = """
        update agricultor set foto=%s
        where id = %s
        """
        #Ejecutar el cursor
        cursor.execute(sql, [foto, id])

        #Confirmar los datos en la BD
        con.commit()

        #Cierra el cursor y la conexión a la BD
        cursor.close()
        con.close()

        #Retonar un valor boolean (true)
        return True

    def obtener_foto(self, id):
        #abrir la conexion
        con= Conexion().open

        #crear un cursos para ejecutar una sentencia sql
        cursor=con.cursor()

        #definir la sentencia sql y sus parametros
        sql="select foto from agricultor where id = %s"

        #ejecutar la sentencia sql y enviarle los valores a los parametros
        cursor.execute(sql,[id])

        #recuperar los registros que devuelve el cursos. como devuelvo un solo registro utilizo "fetchone"
        resultado = cursor.fetchone()

        #cierra el cursor y la conexion a la bd
        cursor.close()
        con.close()
        
        if resultado:
            return resultado

        return None
    
    def dar_baja(self, id):

        #Abrir la conexión
        con = Conexion().open

        #Crear un cursor para ejecutar una setencia SQL
        cursor = con.cursor()

        #Definir la sentencia SQL para validar la baja del agricultor
        sql = """
        select baja from agricultor where id = %s
        """
        #Ejecutar el cursor
        cursor.execute(sql, [id])
        
        #Recuperar el resultado de la consulta sql select
        resultado = cursor.fetchone()
        
        if resultado:
            # Si el agricultor ya está dado de baja, retornar un mensaje
            if resultado['baja'] == True:
                return False, 'Agricultor ya dado de baja'
            else:
                #Ejecutar la sentencia SQL para dar de baja al agricultor
                sql = """
                        update agricultor set baja=True, fecha_hora_baja=now() where id = %s
                    """
                #Ejecutar el cursor
                cursor.execute(sql, [id])

                #Confirmar los datos en la BD
                con.commit()

                #Cierra el cursor y la conexión a la BD
                cursor.close()
                con.close()
        else:
            return False, 'Agricultor no encontrado'
        
        #Retonar un valor boolean (true)
        return True,'Ok'