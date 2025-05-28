from flask import Blueprint, request, jsonify, send_from_directory
from models.agricultor import Agricultor
from tools.security import validate_password
from tools.jwt_required import jwt_token_requerido
import os
from werkzeug.utils import secure_filename

ws_agricultor = Blueprint('ws_agricultor', __name__)

agricultor = Agricultor()

@ws_agricultor.route('/agricultor/registrar', methods=['POST'])
def registrar():
    # Recoger en "data" los parámetros de entrada, digitados por el usuario y que vienen en formato JSON
    data = request.get_json()

    # Obtener los datos
    dni = data.get('dni')
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    telefono = data.get('telefono')

    # Parámetro adicional para validar la contraseña
    password_confirm = data.get('password_confirm')

    # Validar si tenemos valores requeridos
    if not all([dni, nombre, email, password, telefono, password_confirm]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400
    
    # Validar si ambos password coinciden
    if password != password_confirm:
        return jsonify({'status': False, 'data': None, 'message': 'Las contraseñas ingresadas no coinciden'}), 500
    
    # Validar complejidad del password
    valida, mensaje = validate_password(password)  # Llamar a la función de validación
    if not valida:
        return jsonify({'status': False, 'data': None, 'message': mensaje}), 500

    try:
        agricultor.registrar(dni, nombre, email, password, telefono)
        return jsonify({'status': True, 'data': None, 'message': 'Agricultor registrado correctamente'}), 200

    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500

@ws_agricultor.route('/agricultor/actualizar', methods=['PUT'])
@jwt_token_requerido
def actualizar():
    # Recoger en "data" los parámetros de entrada, digitados por el usuario y que vienen en formato JSON
    data = request.get_json()

    # Obtener los datos
    id = data.get('id')
    dni = data.get('dni')
    nombre = data.get('nombre')
    email = data.get('email')
    telefono = data.get('telefono')

    # Validar si tenemos el id y al menos un dato a actualizar
    if not id:
        return jsonify({'status': False, 'data': None, 'message': 'Falta el ID del agricultor'}), 400

    if not any([dni, nombre, email, telefono]):
        return jsonify({'status': False, 'data': None, 'message': 'Debe proporcionar al menos un dato para actualizar'}), 400
    
    try:
        # Llamar a la función de actualización
        actualizado, mensaje = agricultor.actualizar(id, dni, nombre, email, telefono)
        
        if actualizado:
            return jsonify({'status': True, 'data': None, 'message': mensaje}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': mensaje}), 404

    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500
    
@ws_agricultor.route('/agricultor/actualizar_foto', methods=['POST'])
@jwt_token_requerido
def actualizar_foto():
    #obtener los datos: id, foto
    id = request.form.get('id')
    foto = request.files.get('foto')
        
    #validar si tenemos el id y la foto
    if not all([id, foto]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400
        
    try:
        #Cargar la foto
        name_foto = None
            
        if foto:
            #Obtiene: ".jpg", ".png", etc.
            extension = os.path.splitext(foto.filename)[1]
            #Ejemplo: "1.jpg", "2.png", etc.
            nombre_foto = secure_filename(f"{id}{extension}")
            ruta_foto = os.path.join('uploads', 'img', 'agricultor', nombre_foto)
            foto.save(ruta_foto)
                
            #Almancer el nombre de la foto asociada al agricultor en la base de datos
            agricultor.actualizar_foto(id, nombre_foto)
            return jsonify({'status': True, 'data': None, 'message': 'Foto actualizada correctamente'}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': 'No se pudo actualizar la foto'}), 400
            
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500

@ws_agricultor.route('/agricultor/foto/<id>', methods=['GET'])
@jwt_token_requerido
def obtener_foto(id):
    if not all([id]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400
    
    try:
        resultado = agricultor.obtener_foto(id)
        if resultado:
            return send_from_directory('uploads/img/agricultor', resultado['foto'])
        else:
            return send_from_directory('uploads/img/agricultor', 'none.jpg')
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500
    
@ws_agricultor.route('/agricultor/dar_baja', methods=['DELETE'])
@jwt_token_requerido
def dar_baja():
    #Recoger en "data" los parámetros de entrada
    data = request.get_json()
    
    #obtener los datos: id
    id = data.get('id')
        
    #validar si tenemos el id
    if not all([id]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400
        
    try:
        resultado, mensaje = agricultor.dar_baja(id)
        if resultado:
            return jsonify({'status': True, 'data': None, 'message': 'Agricultor dado de baja correctamente'}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': mensaje}), 400
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500    
    
    
    