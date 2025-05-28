from flask import Blueprint, request, jsonify
from models.actividad import Actividad
from tools.jwt_required import jwt_token_requerido

#Crear un modulo blueprint para implementar el servicio web de Actividad
ws_actividad = Blueprint('ws_actividad', __name__)

#Instanciar la clase Actividad
modelo = Actividad()

#Implementar el endpoint para registrar una actividad
@ws_actividad.route('/actividad/registrar', methods=['POST'])
@jwt_token_requerido
def registrar():
    #Recoger los datos
    data = request.get_json()
    
    cultivo_id = data['cultivo_id']
    descripcion = data['descripcion']
    fecha = data['fecha']
    actividad_tipo_id = data['actividad_tipo_id']
    detalle = data.get('detalle', [])

    if not all([cultivo_id, descripcion, fecha, actividad_tipo_id, detalle]):
        return jsonify({'status': False, 'data': None, 'message':'Faltan datos obligatorios'}), 400
    
    try:
        estado, resultado = modelo.registrar(cultivo_id, descripcion, fecha, actividad_tipo_id, detalle)
        if estado:
            return jsonify({'status': True, 'data': {'actividad_id': resultado}, 'message': 'Actividad registrada correctamente'}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': resultado}), 500
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500
    
@ws_actividad.route('/actividad/anular', methods=['DELETE'])
@jwt_token_requerido
def anular():
    #Recoger en "data" los parámetros de entrada
    data = request.get_json()
    
    #obtener los datos: id
    id = data.get('id')
    
    #validar si tenemos el id
    if not all([id]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400
    
    try:
        resultado, mensaje = modelo.anular(id)
        if resultado:
            return jsonify({'status': True, 'data': None, 'message': 'La actividad se anuló correctamente'}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': mensaje}), 400
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500    
    