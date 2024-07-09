from flask import Blueprint, request, jsonify, abort
from .models import Ativo
from . import db
from app.services.alphavantage_service import get_stock_quote, get_all_symbols

main = Blueprint('main', __name__)

@main.route('/ativos', methods=['POST'])
def create_ativo():
    """
    Inserir um novo ativo
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - nome
            - quantidade
          properties:
            nome:
              type: string
            quantidade:
              type: integer
    responses:
      201:
        description: Ativo criado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
            nome:
              type: string
            quantidade:
              type: integer
            valor:
              type: number
              format: float
      400:
        description: Requisição inválida
    """
    data = request.get_json()
    if not data or 'nome' not in data or 'quantidade' not in data:
        abort(400, description="Missing 'nome' or 'quantidade' in request data")
    
    symbol = data['nome']
    valor = get_stock_quote(symbol)
    if valor is None:
        abort(400, description=f"Could not fetch valor for symbol: {symbol}")

    novo_ativo = Ativo(nome=data['nome'], quantidade=data['quantidade'], valor=valor)
    db.session.add(novo_ativo)
    db.session.commit()
    
    return jsonify(novo_ativo.to_dict()), 201

@main.route('/ativos', methods=['GET'])
def get_ativos():
    """
    Obter lista de ativos
    ---
    responses:
      200:
        description: Lista de ativos
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nome:
                type: string
              quantidade:
                type: integer
    """
    ativos = Ativo.query.all()
    return jsonify([ativo.to_dict() for ativo in ativos]), 200

@main.route('/ativos/<int:id>', methods=['GET'])
def get_ativo(id):
    """
    Obter um ativo específico
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do ativo
    responses:
      200:
        description: Detalhes do ativo
        schema:
          type: object
          properties:
            id:
              type: integer
            nome:
              type: string
            quantidade:
              type: integer
      404:
        description: Ativo não encontrado
    """
    ativo = Ativo.query.get_or_404(id)
    return jsonify(ativo.to_dict()), 200

@main.route('/ativos/symbols', methods=['GET'])
def get_all_symbols_route():
    """
    Obter lista de símbolos de ativos
    ---
    responses:
      200:
        description: Lista de símbolos de ativos
        schema:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
              symbol:
                type: string
    """
    symbols = get_all_symbols()
    return jsonify(symbols), 200




@main.route('/ativos/<int:id>', methods=['PUT'])
def update_ativo(id):
    """
    Alterar quantidade de um ativo
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do ativo
      - in: body
        name: body
        schema:
          type: object
          properties:
            quantidade:
              type: integer
    responses:
      200:
        description: Ativo atualizado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
            nome:
              type: string
            quantidade:
              type: integer
      404:
        description: Ativo não encontrado
      400:
        description: Requisição inválida
    """
    data = request.get_json()
    if not data or 'quantidade' not in data:
        abort(400, description="Missing 'quantidade' in request data")
    
    ativo = Ativo.query.get_or_404(id)
    ativo.quantidade = data['quantidade']
    db.session.commit()
    
    return jsonify(ativo.to_dict()), 200

@main.route('/ativos/<int:id>', methods=['DELETE'])
def delete_ativo(id):
    """
    Deletar um ativo
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do ativo
    responses:
      204:
        description: Ativo deletado com sucesso
      404:
        description: Ativo não encontrado
    """
    ativo = Ativo.query.get_or_404(id)
    db.session.delete(ativo)
    db.session.commit()
    return '', 204
