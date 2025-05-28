from flask import Blueprint, request, jsonify
from models.parcela import Parcela
from tools.jwt_required import jwt_token_requerido

ws_parcela = Blueprint('ws_parcela', __name__)

modelo = Parcela()

@ws_parcela.route('/parcela/listar/<id>', methods=['GET'])
@jwt_token_requerido
def listar(id):
    try:
        resultado = modelo.listar(id)
        return jsonify({'status': True, 'data': resultado, 'message': 'Lista de parcelas'}), 200
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500