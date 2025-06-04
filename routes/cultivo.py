from flask import Blueprint, request, jsonify
from models.cultivo import Cultivo
from tools.jwt_required import jwt_token_requerido

ws_cultivo = Blueprint('ws_cultivo', __name__)

modelo = Cultivo()

@ws_cultivo.route('/cultivo/listar', methods=['GET'])
@jwt_token_requerido
def listar():
    try:
        resultado = modelo.listar()
        if resultado:
            return jsonify({'status': True, 'data': resultado, 'message': 'Lista de cultivos'}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': 'No se encontraron cultivos'}), 404
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500