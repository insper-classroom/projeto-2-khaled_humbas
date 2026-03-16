from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# carrega variáveis de ambiente
load_dotenv()
# carrega o flask
app = Flask(__name__)
def conectar_banco():
    """Connect to Aiven MySQL using environment variables"""
    
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            ssl_disabled=False
        )
        
        print("Conectado ao MySql da Aiven")
        return conn
        
    except Error as e:
        print(f"Erro de conexão: {e}")
        return None
#lista todos os imóveis
@app.route('/imovel', methods=["GET"])
def lista_todos():
    try:
        conn = conectar_banco()
        cursor = conn.cursor(dictionary=True) #dictionary = True para transformar em json
    except Exception as e:
        err_msg = f"Não podemos conectar ao banco. Erro: {e}"
        return jsonify({"erro": err_msg}), 500 #erro do servidor

    
    # selecionando tudo de imoveis
    try:
        cursor.execute("""SELECT * from imoveis""")
    except Exception as e:
        err_msg = f"Não foi possível buscar no banco de dados"
        conn.close()
        cursor.close()
        return jsonify({"erro" : err_msg}), 500 # erro do servidor

    imoveis = cursor.fetchall() # pega todos os imóveis
    if not imoveis: # verifica se não há imóveis
        cursor.close()
        conn.close()
        return jsonify({"erro": "Nenhum imóvel encontrado!"}), 200 # banco de dados vazio
    else:
        conn.close()
        cursor.close() # fecha o cursor 
        
        return jsonify(imoveis), 200   

#lista apenas um imóvel específico
@app.route('/imovel/<int:id>', methods=["GET"])
def lista_imovel(id):
    try:
        conn = conectar_banco()
    except Exception as e:
        err_msg = f"Não foi possível conectar ao banco de dados. Erro :{e}"
        return jsonify({"erro": err_msg}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT * FROM imoveis WHERE id = %s
        """, (id, ))
    except Exception as e:
        err_msg = f"Não foi possível fazer a seleção de apenas um imóvel. Erro: {e}"
        conn.close()
        cursor.close()
        return jsonify({"erro": err_msg}), 500

    imovel = cursor.fetchone()
    if not imovel:
        cursor.close()
        conn.close()
        return jsonify({"erro": "Nenhum imóvel encontrado!"}), 404 # banco de dados vazio
    else:
        cursor.close()
        conn.close()
        return jsonify(imovel), 200

@app.route('/imovel', methods=["POST"])
def adiciona_imovel():
    try:
        conn = conectar_banco()
    except Exception as e:
        err_msg = f"Não foi possível conectar ao banco de dados. Erro:{e}"
        return jsonify({"erro": err_msg}), 500
    req = request.get_json() # o imovel em questao da requisição. Retorna um dicionário
    cursor = conn.cursor(dictionary=True)

    if not all(k in req for k in ("logradouro", "tipo_logradouro", "bairro", "cidade", "cep", "tipo", "valor", "data_aquisicao")):
        cursor.close()
        conn.close()
        return jsonify({"erro": "Campos obrigatórios: logradouro, tipo_logradouro, bairro, cidade, cep tipo, valor, data_aquisicao"}), 400

    #faz o comando de execução
    try:
        cursor.execute("""INSERT into imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (
        req['logradouro'], req['tipo_logradouro'], req['bairro'], req['cidade'], 
        req['cep'], req['tipo'], req['valor'], req['data_aquisicao']
        ))
        conn.commit()
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"erro": "Falha ao adicionar imóvel"}), 500
    except Exception as e:
        err_msg = f"Não foi possível adicionar o imóvel. Erro: {e}"
        conn.close()
        cursor.close()
        return jsonify({"erro": err_msg}), 500 
    imovel = {
        "logradouro" : req['logradouro'],
        'tipo_logradouro': req['tipo_logradouro'],
        'bairro': req['bairro'],
        'cidade': req['cidade'],
        'cep': req['cep'],
        'tipo': req['tipo'],
        'valor': req['valor'],
        'data_aquisicao': req['data_aquisicao']
    }
    cursor.close()
    conn.close()
    return jsonify(imovel), 201

@app.route("/imovel/<int:id>", methods=["PUT"])
def atualiza_imovel(id):
    try:
        conn = conectar_banco()
    except Exception as e:
        err_msg = f"Não foi possível conectar ao banco de dados. Erro:{e}"
        return jsonify({"erro": err_msg}), 500
    
    req = request.get_json() # pega o imóvel da requisição
    
    if not all(k in req for k in ("logradouro", "tipo_logradouro", "bairro", "cidade", "cep", "tipo", "valor", "data_aquisicao")):
        conn.close()
        return jsonify({"erro": "Campos obrigatórios: logradouro, tipo_logradouro, bairro, cidade, cep tipo, valor, data_aquisicao"}), 400
    cursor = conn.cursor(dictionary=True)
    # cria a query sql
    try:
        cursor.execute("UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s",
        (
            req['logradouro'], req['tipo_logradouro'], req['bairro'], req['cidade'],
            req['cep'], req['tipo'], req['valor'], req['data_aquisicao'],
            id
        ))
        conn.commit()

        if cursor.rowcount == 0:
                cursor.close()
                conn.close()
                return jsonify({"erro": "Imóvel não encontrado"}), 404
    except Exception as e:
        err_msg = f"Não foi possível atualizar o imóvel"
        conn.close()
        cursor.close()
        return jsonify({"erro": err_msg}), 500 
 
    cursor.close()
    conn.close()
    imovel = {
        "logradouro" : req['logradouro'],
        'tipo_logradouro': req['tipo_logradouro'],
        'bairro': req['bairro'],
        'cidade': req['cidade'],
        'cep': req['cep'],
        'tipo': req['tipo'],
        'valor': req['valor'],
        'data_aquisicao': req['data_aquisicao']
    }
    return jsonify({"imóvel" : imovel, "id" : id}), 200

@app.route("/imovel/<int:id>", methods=["DELETE"])
def remove_imovel(id):
    try:
        conn = conectar_banco()
    except Exception as e:
        err_msg = f"Não foi possível conectar ao banco de dados. Erro:{e}"
        return jsonify({"erro": err_msg}), 500
    
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
        DELETE from imoveis
        WHERE id = %s
        """, (id,))
        conn.commit()
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({"erro": "O id não existe no banco de dados"}), 404
    except Exception as e:
        err_msg = f"Erro ao remover imóvel de id " + id + f"Erro: {e}"
        conn.close()
        cursor.close()
        return jsonify({erro: err_msg}), 500

    cursor.close()
    conn.close()
    return jsonify(f"Imóvel removido de id:{id}"), 200

@app.route("/imovel/tipo/<string:tipo>", methods=["GET"])
def lista_por_tipo(tipo):
    try:
        conn = conectar_banco()
    except Exception as e:
        err_msg = f"Não foi possível conectar ao banco de dados. Erro:{e}"
        return jsonify({"erro": err_msg}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
        SELECT * from imoveis
        WHERE tipo = %s
        """, (tipo,))
    except Exception as e:
        err_msg = "Erro ao listar imóveis"
        conn.close()
        cursor.close()
        return jsonify({"erro": err_msg}), 500
    
    imoveis = cursor.fetchall()
    if len(imoveis) > 0:
        conn.close()
        cursor.close()
        return jsonify(imoveis), 200
    else:
        conn.close()
        cursor.close()
        return jsonify({"mensagem": f"Não foram encontrados imóveis com tipo {tipo}"}), 200
    
@app.route("/imovel/cidade/<string:cidade>", methods=["GET"])
def lista_por_cidade(cidade):
    try:
        conn = conectar_banco()
    except Exception as e:
        err_msg = f"Não foi possível conectar ao banco de dados. Erro:{e}"
        return jsonify({"erro": err_msg}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
        SELECT * from imoveis
        WHERE cidade = %s
        """, (cidade,))
    except Exception as e:
        err_msg = "Erro ao listar imóveis"
        conn.close()
        cursor.close()
        return jsonify({"erro": err_msg}), 500
    
    imoveis = cursor.fetchall()
    if imoveis:
        conn.close()
        cursor.close()
        return jsonify(imoveis), 200
    else:
        conn.close()
        cursor.close()
        return jsonify({"mensagem": f"Não foram encontrados imóveis com cidade: {cidade}"}), 200
if __name__ == '__main__':
    app.run(debug=False)