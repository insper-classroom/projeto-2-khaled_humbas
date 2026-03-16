import pytest
from unittest.mock import patch, MagicMock
from api import app  

@pytest.fixture()
def client():
    app.config["TESTING"] = True 
    with app.test_client() as client:
        yield client

class Imovel:
    def __init__(self, id, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao):
        self.id = id
        self.logradouro = logradouro
        self.tipo_logradouro = tipo_logradouro
        self.bairro = bairro
        self.cidade = cidade 
        self.cep = cep
        self.tipo = tipo 
        self.valor = valor 
        self.data_aquisicao = data_aquisicao

@pytest.fixture()
def imovel_teste_1():
    return Imovel(id=1, logradouro = 'Nicole Common', tipo_logradouro='Travessa', 
    bairro='Lake Danielle', cidade='Judymouth', cep='85184', 
    tipo='casa em condominio', valor=488423.52, data_aquisicao='2017-07-29')

def imovel_teste_2():
    return Imovel(id=2, logradouro='Price Prairie', tipo_logradouro='Travessa', 
    bairr='Colonton', cidade='North Garyville', cep='93354', 
    tipo='casa em condominio', valor=260069.89, data_aquisicao='2021-11-30')

@patch("api.conectar_banco")
def test_lista_todos_ok(mock_conectar_banco, client, imovel_teste_1):
    # Testa a rota GET /list com sucesso
    imovel_teste = imovel_teste_1

    # Configura os mocks
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    # A função conectar_banco() deve retornar a conexão mockada
    mock_conectar_banco.return_value = mock_conn
    # A conexão, ao criar um cursor, retorna o cursor mockado
    mock_conn.cursor.return_value = mock_cursor
    
    # Simula o retorno do banco de dados 
    mock_cursor.fetchall.return_value = [
        {
            "id": 1,
            "logradouro": imovel_teste.logradouro,
            "tipo_logradouro": imovel_teste.tipo_logradouro,
            "bairro": imovel_teste.bairro,
            "cidade": imovel_teste.cidade,
            "cep": imovel_teste.cep,
            "tipo": imovel_teste.tipo,
            "valor": imovel_teste.valor,
            "data_aquisicao": imovel_teste.data_aquisicao
        }
    ]
    
    # Faz a requisição para a rota
    response = client.get("/imovel")
    
    # Verifica o status code
    assert response.status_code == 200
    
    # Verifica se a query SQL foi executada
    mock_cursor.execute.assert_called_once_with("""SELECT * from imoveis""")
    
    # Verifica se fetchall foi chamado
    mock_cursor.fetchall.assert_called_once()
    
    # Verifica se o cursor e a conexão foram fechados
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()
    
    # Verifica os dados retornados
    dados = response.get_json()
    imoveis = dados
    assert len(imoveis) == 1

    # olha se o imóvel retornado condiz
    imovel_retornado = imoveis[0]
    assert imovel_retornado["logradouro"] == imovel_teste.logradouro
    assert imovel_retornado["tipo_logradouro"] == imovel_teste.tipo_logradouro
    assert imovel_retornado["bairro"] == imovel_teste.bairro
    assert imovel_retornado["cidade"] == imovel_teste.cidade
    assert imovel_retornado["cep"] == imovel_teste.cep
    assert imovel_retornado["tipo"] == imovel_teste.tipo
    assert imovel_retornado["valor"] == imovel_teste.valor
    assert imovel_retornado["data_aquisicao"] == imovel_teste.data_aquisicao

@patch("api.conectar_banco")
def test_lista_todos_vazio(mock_conectar_banco, client):
    # testa a rota GET /list com erro

    #configura os mocks
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    # olha se todas as variáveis estão setadas
    mock_conectar_banco.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [] # retorna uma lista vazia
    # pega a lista      
    response = client.get("/imovel")
    # verifica o status code 200
    assert response.status_code == 200

    # Verifica se a query SQL foi executada
    mock_cursor.execute.assert_called_once_with("""SELECT * from imoveis""")

    assert response.get_json() == {"erro": "Nenhum imóvel encontrado!"}

    # Verifica se fetchall foi chamado
    mock_cursor.fetchall.assert_called_once()
    
    # Verifica se o cursor e a conexão foram fechados
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("api.conectar_banco")
def test_lista_todos_erro_cursor(mock_conectar_banco, client):
    #configura os mocks
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    # olha se todas as variáveis estão setadas
    mock_conectar_banco.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    with pytest.raises(Exception):
        response = client.get("/imovei")
        mock_cursor.execute.assert_called_once_with("""SELECT * from imoveis""")
        err_msg = f"Não foi possível buscar no banco de dados"
        mock_conn.close.assert_called_once_with()
        mock_cursor.close.assert_called_once_with()
        assert response.status_code == 500
        assert response.geet_json["erro"] == err_msg
       
@patch("api.conectar_banco")
def test_lista_imovel_especifico_ok(mock_conectar_banco, client, imovel_teste_1):
    # mocka o imovel teste
    imovel_teste = imovel_teste_1
    # mocka a conexão e cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    # mocka a conexão e conectar banco
    mock_conn.cursor.return_value = mock_cursor
    mock_conectar_banco.return_value = mock_conn 
    #mocka o retorno do valor
    mock_cursor.fetchone.return_value = {
        "id": imovel_teste.id,
        "logradouro": imovel_teste.logradouro,
        "tipo_logradouro": imovel_teste.tipo_logradouro,
        "bairro": imovel_teste.bairro,
        "cidade": imovel_teste.cidade,
        "cep": imovel_teste.cep,
        "tipo": imovel_teste.tipo,
        "valor": imovel_teste.valor,
        "data_aquisicao": imovel_teste.data_aquisicao
    }

    # mocka o teste do imovel
    response = client.get(f"/imovel/{imovel_teste.id}") # lista o imóvel 1

    assert response.status_code == 200

    dados = response.get_json()

    assert dados["id"] == imovel_teste.id
    assert dados["logradouro"] == imovel_teste.logradouro
    assert dados["tipo_logradouro"] == imovel_teste.tipo_logradouro
    assert dados["bairro"] == imovel_teste.bairro
    assert dados["cidade"] == imovel_teste.cidade
    assert dados["cep"] == imovel_teste.cep
    assert dados["tipo"] == imovel_teste.tipo
    assert dados["valor"] == imovel_teste.valor
    assert dados["data_aquisicao"] == imovel_teste.data_aquisicao

    mock_cursor.execute.assert_called_once_with(
        """
            SELECT * FROM imoveis WHERE id = %s
        """, (imovel_teste.id, )
    )
    # todas as chamdas ocorreram apenas uma vez
    mock_cursor.fetchone.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("api.conectar_banco")
def test_lista_imovel_especifico_erro(mock_conectar_banco, client):
    # inicializa a conexão e cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_conectar_banco.return_value = mock_conn

    mock_cursor.fetchone.return_value = {} # não retorna nada 

    response = client.get("/imovel/9999") # testa pra um id bem grande
    mock_cursor.execute.assert_called_once_with(
        """
            SELECT * FROM imoveis WHERE id = %s
        """, (9999, )
    ) # fez a query com o id 9999
    # status de código e json
    assert response.status_code == 404
    assert response.get_json() == {"erro": "Nenhum imóvel encontrado!"}
    # todas as chamadas só ocorreram uma vez
    mock_cursor.fetchone.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("api.conectar_banco")
def test_adiciona_imovel_ok(mock_conectar_banco, client, imovel_teste_1):
    imovel_teste = imovel_teste_1
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_conectar_banco.return_value = mock_conn

    mock_cursor.fetchone.return_value = {
        "id": imovel_teste.id,
        "logradouro": imovel_teste.logradouro,
        "tipo_logradouro": imovel_teste.tipo_logradouro,
        "bairro": imovel_teste.bairro,
        "cidade": imovel_teste.cidade,
        "cep": imovel_teste.cep,
        "tipo": imovel_teste.tipo,
        "valor": imovel_teste.valor,
        "data_aquisicao": imovel_teste.data_aquisicao
    }

    response = client.post("/imovel", json={
    "logradouro": imovel_teste.logradouro,
    "tipo_logradouro": imovel_teste.tipo_logradouro,
    "bairro": imovel_teste.bairro,
    "cidade": imovel_teste.cidade,
    "cep": imovel_teste.cep,
    "tipo": imovel_teste.tipo,
    "valor": imovel_teste.valor,
    "data_aquisicao": imovel_teste.data_aquisicao
    })
    
    mock_cursor.execute.assert_called_once_with("""INSERT into imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
    (
    imovel_teste.logradouro, imovel_teste.tipo_logradouro, imovel_teste.bairro, imovel_teste.cidade, 
    imovel_teste.cep, imovel_teste.tipo, imovel_teste.valor, imovel_teste.data_aquisicao
    ))

    assert response.status_code == 201
    dados = response.get_json()
    assert dados["logradouro"] == imovel_teste.logradouro
    assert dados["tipo_logradouro"] == imovel_teste.tipo_logradouro
    assert dados["bairro"] == imovel_teste.bairro
    assert dados["cidade"] == imovel_teste.cidade
    assert dados["cep"] == imovel_teste.cep
    assert dados["tipo"] == imovel_teste.tipo
    assert dados["valor"] == imovel_teste.valor
    assert dados["data_aquisicao"] == imovel_teste.data_aquisicao
    # 5. Verificar outras chamadas
    mock_cursor.close.assert_called_once()
    mock_conn.commit.assert_called_once()  # Se houver commit no código real
    mock_conn.close.assert_called_once()

@patch("api.conectar_banco")
def test_adiciona_imovel_sem_campos_corretos(mock_conectar_banco, client, imovel_teste_1):
    imovel_teste = imovel_teste_1
    # inicializa a conexão e cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    # olhe se o valor de retorno é igual
    mock_conn.cursor.return_value = mock_cursor
    mock_conectar_banco.return_value = mock_conn
    response = client.post("/imovel", json={
    "logradouro": imovel_teste.logradouro,
    "tipo_logradouro": imovel_teste.tipo_logradouro,
    "bairro": imovel_teste.bairro,
    "cidade": imovel_teste.cidade,
    "cep": imovel_teste.cep,
    "tipo": imovel_teste.tipo,
    "valor": imovel_teste.valor,
    "skibidi": imovel_teste.data_aquisicao
    })
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

    assert response.status_code == 400
    err_msg = response.get_json()
    err_msg = err_msg['erro']
    assert err_msg == "Campos obrigatórios: logradouro, tipo_logradouro, bairro, cidade, cep tipo, valor, data_aquisicao"

@patch("api.conectar_banco")
def test_adiciona_imovel_erro_cursor(mock_conectar_banco, client, imovel_teste_1):
    imovel_teste = imovel_teste_1
    # Inicializa a conexão e o cursor como Mocks
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    # Configura o mock de conectar_banco para retornar mock_conn
    mock_conectar_banco.return_value = mock_conn
    # Configura o mock_conn.cursor() para retornar mock_cursor
    mock_conn.cursor.return_value = mock_cursor

    with pytest.raises(Exception):
        
        response = client.post("/add", json={
            "logradouro": imovel_teste.logradouro,
            "tipo_logradouro": imovel_teste.tipo_logradouro,
            "bairro": imovel_teste.bairro,
            "cidade": imovel_teste.cidade,
            "cep": imovel_teste.cep,
            "tipo": imovel_teste.tipo,
            "valor": imovel_teste.valor,
            "data_aquisicao": imovel_teste.data_aquisicao
        })

        # Verifica chamadas
        mock_conectar_banco.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
        """INSERT into imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (
            imovel_teste.logradouro, imovel_teste.tipo_logradouro,
            imovel_teste.bairro, imovel_teste.cidade,
            imovel_teste.cep, imovel_teste.tipo,
            imovel_teste.valor, imovel_teste.data_aquisicao
        )
        )
        # verifica se o cursor e conexão foram fechadas
        mock_cursor.close.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        # vê o status code
        assert response.status_code == 500
        # vê mensagem de erro
        err_msg = response.get_json()['erro']
        assert err_msg == "Falha ao adicionar imóvel"

@patch("api.conectar_banco")
def test_atualiza_imovel_ok(mock_conectar_banco, client, imovel_teste_1):
    imovel_teste = imovel_teste_1
    # mocka a conexão e cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conectar_banco.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    # mocka o json
    response = client.put(f"/imovel/{imovel_teste.id}", json={
    "logradouro": imovel_teste.logradouro,
    "tipo_logradouro": imovel_teste.tipo_logradouro,
    "bairro": imovel_teste.bairro,
    "cidade": imovel_teste.cidade,
    "cep": imovel_teste.cep,
    "tipo": imovel_teste.tipo,
    "valor": imovel_teste.valor,
    "data_aquisicao": imovel_teste.data_aquisicao
    })
    # mocka o cursor
    mock_cursor.execute.assert_called_once_with(
        "UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s",
        (
            imovel_teste.logradouro, imovel_teste.tipo_logradouro,
            imovel_teste.bairro, imovel_teste.cidade,
            imovel_teste.cep, imovel_teste.tipo,
            imovel_teste.valor, imovel_teste.data_aquisicao,
            imovel_teste.id
        )
    )

    assert response.status_code == 200
    # cria o imovel
    imovel = {"logradouro": imovel_teste.logradouro,
    "tipo_logradouro": imovel_teste.tipo_logradouro,
    "bairro": imovel_teste.bairro,
    "cidade": imovel_teste.cidade,
    "cep": imovel_teste.cep,
    "tipo": imovel_teste.tipo,
    "valor": imovel_teste.valor,
    "data_aquisicao": imovel_teste.data_aquisicao
    }

    dados = response.get_json()
    assert dados["id"] == imovel_teste.id
    dados = dados["imóvel"]
    # verifica os campos
    assert dados["logradouro"] == imovel_teste.logradouro
    assert dados["tipo_logradouro"] == imovel_teste.tipo_logradouro
    assert dados["bairro"] == imovel_teste.bairro
    assert dados["cidade"] == imovel_teste.cidade
    assert dados["cep"] == imovel_teste.cep
    assert dados["tipo"] == imovel_teste.tipo
    assert dados["valor"] == imovel_teste.valor
    assert dados["data_aquisicao"] == imovel_teste.data_aquisicao

@patch("api.conectar_banco")
def teste_atualiza_imovel_sem_campos_corretos(mock_conectar_banco, client, imovel_teste_1):
    imovel_teste = imovel_teste_1
    # inicializa a conexão e cursor
    mock_conn = MagicMock()
    # olhe se o valor de retorno é igual
    mock_conectar_banco.return_value = mock_conn
    response = client.put(f"/imovel/{imovel_teste.id}", json={
        "logradouro": imovel_teste.logradouro,
        "tipo_logradouro": imovel_teste.tipo_logradouro,
        "bairro": imovel_teste.bairro,
        "cidade": imovel_teste.cidade,
        "cep": imovel_teste.cep,
        "tipo": imovel_teste.tipo,
        "valor": imovel_teste.valor,
        "skibidi": imovel_teste.data_aquisicao
    })
    mock_conn.close.assert_called_once()

    assert response.status_code == 400
    err_msg = response.get_json()
    err_msg = err_msg['erro']
    assert err_msg == "Campos obrigatórios: logradouro, tipo_logradouro, bairro, cidade, cep tipo, valor, data_aquisicao"

@patch("api.conectar_banco")
def test_atualiza_imovel_erro_cursor(mock_conectar_banco, client, imovel_teste_1):
    imovel_teste = imovel_teste_1
    # Inicializa a conexão e o cursor como Mocks
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    # Configura o mock de conectar_banco para retornar mock_conn
    mock_conectar_banco.return_value = mock_conn
    # Configura o mock_conn.cursor() para retornar mock_cursor
    mock_conn.cursor.return_value = mock_cursor
    json_imovel={
        "logradouro": imovel_teste.logradouro,
        "tipo_logradouro": imovel_teste.tipo_logradouro,
        "bairro": imovel_teste.bairro,
        "cidade": imovel_teste.cidade,
        "cep": imovel_teste.cep,
        "tipo": imovel_teste.tipo,
        "valor": imovel_teste.valor,
        "data_aquisicao": imovel_teste.data_aquisicao
    }
    response = client.put(f"/imovel/{imovel_teste.id}", json=json_imovel)

    # mocka o cursor
    mock_cursor.execute.assert_called_once_with(
        "UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s",
        (
            imovel_teste.logradouro, imovel_teste.tipo_logradouro,
            imovel_teste.bairro, imovel_teste.cidade,
            imovel_teste.cep, imovel_teste.tipo,
            imovel_teste.valor, imovel_teste.data_aquisicao,
            imovel_teste.id
        )
    )
    with pytest.raises(Exception):
        # verifica se o cursor e conexão foram fechadas
        mock_cursor.close.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        # vê o status code
        assert response.status_code == 500
        # vê mensagem de erro
        err_msg_test = f"Não foi possível atualizar o imóvel"
        err_msg = response.get_json()['erro']
        assert err_msg == err_msg_test

@patch("api.conectar_banco")
def test_remove_imovel_ok(mock_conectar_banco, client):
    # mocka as coisas
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conectar_banco.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 1  # simula que uma linha foi afetada
        # Faz requisição DELETE
    response = client.delete("/imovel/1")

    # Verifica chamadas
    mock_conectar_banco.assert_called_once()
    mock_conn.cursor.assert_called_once_with(dictionary=True)
    mock_cursor.execute.assert_called_once_with("""
        DELETE from imoveis
        WHERE id = %s
        """, (1,))
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

    # Verifica resposta
    assert response.status_code == 200
    assert response.get_json() == "Imóvel removido de id:1"

@patch("api.conectar_banco")
def test_remove_imovel_imovel_nao_existe(mock_conectar_banco, client):
    # mocka as coisas
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conectar_banco.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 0
    # Faz a requisição
    response = client.delete("/imovel/9999")
    # Verificações
    mock_cursor.execute.assert_called_once_with("""
        DELETE from imoveis
        WHERE id = %s
        """, (9999,))
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()
    
    assert response.status_code == 404
    
    # CORREÇÃO: get_json() é um método, não um atributo
    assert response.get_json()["erro"] == "O id não existe no banco de dados"

@patch("api.conectar_banco")
def test_remove_imovel_erro_cursor(mock_conectar_banco, client):
    # mocka a coneexão e cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conectar_banco.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    # faz a requisição
    response = client.delete("/imovel/9999")
    with pytest.raises(Exception):
        mock_cursor.execute.assert_called_once_with("""
        DELETE from imoveis
        WHERE id = %s
        """, (1,))
        err_msg = f"Erro ao remover imóvel de id:" + str(9999) 
        mock_conn.close()
        mock_cursor.close()
        
        assert response.status_code == 500
        assert response.get_json()["erro"] == err_msg

@patch("api.conectar_banco")
def test_lista_por_tipo_ok(mock_conectar_banco, client, imovel_teste_1):
    # mocka a coneexão e cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conectar_banco.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    imovel_teste = imovel_teste_1
    imovel_dict = {
        "id": 1,
        "logradouro": imovel_teste.logradouro,
        "tipo_logradouro": imovel_teste.tipo_logradouro,
        "bairro": imovel_teste.bairro,
        "cidade": imovel_teste.cidade,
        "cep": imovel_teste.cep,
        "tipo": imovel_teste.tipo,
        "valor": imovel_teste.valor,
        "data_aquisicao": imovel_teste.data_aquisicao
    }
    mock_cursor.fetchall.return_value = [imovel_dict]
    response = client.get(f"/imovel/tipo/{imovel_teste.tipo}")

    mock_cursor.execute.assert_called_once_with("""
        SELECT * from imoveis
        WHERE tipo = %s
        """, (imovel_teste.tipo,))


    mock_cursor.fetchall.return_value = [
        {
            "id": 1,
            "logradouro": imovel_teste.logradouro,
            "tipo_logradouro": imovel_teste.tipo_logradouro,
            "bairro": imovel_teste.bairro,
            "cidade": imovel_teste.cidade,
            "cep": imovel_teste.cep,
            "tipo": imovel_teste.tipo,
            "valor": imovel_teste.valor,
            "data_aquisicao": imovel_teste.data_aquisicao
        }
    ]

    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()
    assert response.status_code == 200
    dados = response.get_json()
    assert dados == [imovel_dict]

@patch("api.conectar_banco")
def test_lista_por_tipo_erro(mock_conectar_banco, client, imovel_teste_1):
    # mocka a coneexão e cursor
    imovel_teste = imovel_teste_1
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conectar_banco.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    imovel_teste = imovel_teste_1
    imovel_dict = {
            "id": 1,
            "logradouro": imovel_teste.logradouro,
            "tipo_logradouro": imovel_teste.tipo_logradouro,
            "bairro": imovel_teste.bairro,
            "cidade": imovel_teste.cidade,
            "cep": imovel_teste.cep,
            "tipo": imovel_teste.tipo,
            "valor": imovel_teste.valor,
            "data_aquisicao": imovel_teste.data_aquisicao
    }
    mock_cursor.fetchall.return_value = [imovel_dict]
    response = client.get(f"/imovel/tipo/{imovel_teste.tipo}")
    with pytest.raises(Exception):

        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
        assert response.status_code == 500
        err_msg = "Erro ao listar imóveis"
        assert response.get_json()["erro"] == err_msg

@patch("api.conectar_banco")
def test_lista_por_tipo_nenhum_imovel(mock_conectar_banco, client, imovel_teste_1):
    imovel_teste = imovel_teste_1
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conectar_banco.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor 

    mock_cursor.fetchall.return_value = [] # retorna uma lista vazia

    response = client.get(f"/imovel/tipo/{imovel_teste.tipo}")
    mock_cursor.execute.assert_called_once_with("""
        SELECT * from imoveis
        WHERE tipo = %s
        """, (imovel_teste.tipo,))

    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

    assert response.status_code == 200
    assert response.get_json()["mensagem"] == f"Não foram encontrados imóveis com tipo {imovel_teste.tipo}"

@patch("api.conectar_banco")
def test_lista_por_cidade_ok(mock_conectar_banco, client, imovel_teste_1):
    # mocka a coneexão e cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conectar_banco.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    imovel_teste = imovel_teste_1
    imovel_dict = {
        "id": 1,
        "logradouro": imovel_teste.logradouro,
        "tipo_logradouro": imovel_teste.tipo_logradouro,
        "bairro": imovel_teste.bairro,
        "cidade": imovel_teste.cidade,
        "cep": imovel_teste.cep,
        "tipo": imovel_teste.tipo,
        "valor": imovel_teste.valor,
        "data_aquisicao": imovel_teste.data_aquisicao
    }
    mock_cursor.fetchall.return_value = [imovel_dict]
    response = client.get(f"/imovel/cidade/{imovel_teste.cidade}")

    mock_cursor.execute.assert_called_once_with("""
        SELECT * from imoveis
        WHERE cidade = %s
        """, (imovel_teste.cidade,))


    mock_cursor.fetchall.return_value = [
        {
            "id": 1,
            "logradouro": imovel_teste.logradouro,
            "tipo_logradouro": imovel_teste.tipo_logradouro,
            "bairro": imovel_teste.bairro,
            "cidade": imovel_teste.cidade,
            "cep": imovel_teste.cep,
            "tipo": imovel_teste.tipo,
            "valor": imovel_teste.valor,
            "data_aquisicao": imovel_teste.data_aquisicao
        }
    ]

    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()
    assert response.status_code == 200
    dados = response.get_json()
    assert dados == [imovel_dict]

@patch("api.conectar_banco")
def test_lista_por_cidade_erro(mock_conectar_banco, client, imovel_teste_1):
    # mocka a coneexão e cursor
    imovel_teste = imovel_teste_1
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conectar_banco.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    imovel_teste = imovel_teste_1
    imovel_dict = {
            "id": 1,
            "logradouro": imovel_teste.logradouro,
            "tipo_logradouro": imovel_teste.tipo_logradouro,
            "bairro": imovel_teste.bairro,
            "cidade": imovel_teste.cidade,
            "cep": imovel_teste.cep,
            "tipo": imovel_teste.tipo,
            "valor": imovel_teste.valor,
            "data_aquisicao": imovel_teste.data_aquisicao
    }
    mock_cursor.fetchall.return_value = [imovel_dict]
    response = client.get(f"/imovel/cidade/{imovel_teste.cidade}")
    with pytest.raises(Exception):

        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
        assert response.status_code == 500
        err_msg = "Erro ao listar imóveis"
        assert response.get_json()["erro"] == err_msg

@patch("api.conectar_banco")
def test_lista_por_cidade_nenhum_imovel(mock_conectar_banco, client, imovel_teste_1):
    imovel_teste = imovel_teste_1
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conectar_banco.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor 

    mock_cursor.fetchall.return_value = [] # retorna uma lista vazia

    response = client.get(f"/imovel/cidade/{imovel_teste.cidade}")
    mock_cursor.execute.assert_called_once_with("""
        SELECT * from imoveis
        WHERE cidade = %s
        """, (imovel_teste.cidade,))

    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

    assert response.status_code == 200
    assert response.get_json()["mensagem"] == f"Não foram encontrados imóveis com cidade: {imovel_teste.cidade}"