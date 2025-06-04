from flask import Blueprint, request, jsonify
from models.cultivo import Cultivo
from tools.jwt_required import jwt_token_requerido
from util import CustomJSONEncoder
import json

ws_cultivo = Blueprint('ws_cultivo', __name__)

modelo = Cultivo()

@ws_cultivo.route('/cultivo/listar/<id>', methods=['GET'])
@jwt_token_requerido
def listar(id):
    try:
        resultado = modelo.listar(id)
        data = json.dumps(resultado, cls = CustomJSONEncoder)
        return jsonify({'status': True, 'data': json.loads(data), 'message': 'Lista de cultivos'}), 200
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500
