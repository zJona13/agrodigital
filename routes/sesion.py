from flask import Blueprint, request, jsonify
from models.agricultor import Agricultor
from tools.jwt_utils import generar_token

#crar un modelo blueprint para implementar el servicio web para iniciar sesion
ws_sesion= Blueprint('ws_sesion', __name__)

#instanciar un objeto de la clase agricultor
agricultor = Agricultor()

#crear un endopointpara el inicip de sesion
@ws_sesion.route('/login', methods=['POST'])
def login():

    #recoger en "data" los parametros de entrada, digitados por el usuario y que vienen en formato JSON
    data=request.get_json()

    #obtener el email y passwoe de data
    email= data.get("email")
    password= data.get("password")

    #validar si tenemos valores en email y password
    if not all([email, password]):
        return jsonify({'status':False, 'data':None, 'message': 'Faltan datos obligatorios'}),400

    try:
    #ejecutar el metodo login, enviarle los parametros y recibir el resultado
        resultado = agricultor.login(email, password)

        if resultado:#si hay datos en el resultado
            token = generar_token({'usuario': resultado['id']}, 60*60)

            resultado['token'] = token

            resultado.pop('password', None)

            return jsonify({'status':True,'data': resultado,'message': 'Inicio de sesion satisfactorio'}),200

        else: 
            #si no hay datos en el resultdo
            return jsonify({'status':False,'data': None, 'message': 'credenciales invalidas'}),401
    except Exception as e:
        return jsonify({'status':False,'data': None, 'message': str(e)}),500