from flask import Blueprint, request, jsonify
from models.actividad_tipo import ActividadTipo
from tools.jwt_required import jwt_token_requerido

ws_actividad_tipo = Blueprint('ws_actividad_tipo', __name__)

modelo = ActividadTipo()

@ws_actividad_tipo.route('/actividad/tipo/listar', methods=['GET'])
@jwt_token_requerido
def listar():
    try:
        resultado = modelo.listar()
        if resultado:
            return jsonify({'status': True, 'data': resultado, 'message': 'Lista de tipos de actividad'}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': 'No se encontraron tipos de actividad'}), 404
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500