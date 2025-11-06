# Alvaro Freitas Miranda: RM565364
# João Victor Veronesi: RM565290
 
import os
import oracledb
import pandas as pd
import time

from datetime import datetime
os.system("cls")
 
# tabela sql
"""
CREATE TABLE carros (
    id_carro NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    modelo VARCHAR2(100) NOT NULL,
    marca VARCHAR2(50) NOT NULL,
    ano NUMBER(4) NOT NULL,            
    cor VARCHAR2(30),            
    proprietario VARCHAR2(100),
    data_cadastro VARCHAR2(16),
    data_ultima_modificacao VARCHAR2(16),
    ativo VARCHAR2(3)
);
"""
 
# ---------- CONEXÃO COM O BANCO ----------
def conectar_banco():
    try:
        conn = oracledb.connect(user="rm565364", password="100406", dsn="oracle.fiap.com.br:1521/ORCL")
 
        inst_cadastro = conn.cursor()
        inst_consulta = conn.cursor()
        inst_alteracao = conn.cursor()
        inst_exclusao = conn.cursor()
 
    except Exception as e:
        print(f"ERRO!! {e}")
        return None, None, None, None, None
    else:
        return conn, inst_cadastro, inst_consulta, inst_alteracao, inst_exclusao
 
 
# ---------- SUBALGORITMOS ----------

def hora_atual():
    agora = datetime.now()
    data_formatada = agora.strftime("%d/%m/%Y %H:%M")
    return data_formatada


#-------------------------------------------------------------------------------------------------------------------------


 
def cadastrar_carro(conn, inst_cadastro):
    try:
        os.system("cls")
        print("----- CADASTRAR CARROS -----\n")
        modelo = input("Digite o modelo....: ")
        marca = input("Digite a marca....: ")
        ano = int(input("Digite o ano...: "))
        cor = input("Digite a cor...: ")
        proprietario = input("Digite o proprietário...: ")

        data_atual = hora_atual()  # pega a data e hora formatadas

        cadastro = f"""
            INSERT INTO carros (modelo, marca, ano, cor, proprietario, data_cadastro, data_ultima_modificacao, ativo)
            VALUES ('{modelo}', '{marca}', {ano}, '{cor}', '{proprietario}', '{data_atual}', '{data_atual}', 'Sim')
        """

        inst_cadastro.execute(cadastro)
        conn.commit()

    except ValueError:
        print("Digite um número no ano!")
    except Exception as e:
        print("Erro na transação do BD:", e)
    else:
        print("\nDADOS GRAVADOS COM SUCESSO!")
 
 
 
 
#-------------------------------------------------------------------------------------------------------------------------
def pesquisar_carro_por_id(conn, inst_consulta):
    os.system("cls")
    print("----- PESQUISAR CARRO -----\n")
    id_carro = input("\nEscolha um Id: ")
 
    os.system("cls")
    print("DADOS ESCOLHIDOS POR ID\n")
 
    lista_carros2 = []
 
    if id_carro.isdigit():
        id_carro = int(id_carro)
        consulta = f""" SELECT * FROM carros WHERE id_carro = {id_carro}"""
        inst_consulta.execute(consulta)
        data = inst_consulta.fetchall()
 
        for dt in data:
            lista_carros2.append(dt)
 
        print("-" * 95)
        dados_df = pd.DataFrame.from_records(
            lista_carros2, columns=['Id', 'Modelo', 'Marca', 'Ano', 'Cor', 'Proprietário', 'data_cadastro', 'data_ultima_modificacao', 'ativo'], index='Id')
 
        if len(lista_carros2) == 0:
            print(f"Não há um carro cadastrado com o ID = {id_carro}")
        else:
            print(dados_df)
        print("-" * 95)
    else:
        print("O Id não é numérico!")
 
 
 
 
 
#-------------------------------------------------------------------------------------------------------------------------
def exportar_arquivo(dados_df):
    print("\033[33mGerar arquivo [E]xcel, [C]SV? Ou [ENTER] para voltar ao menu.\033[0m")

    escolha_exportar = input("Escolha: ").lower()

    if escolha_exportar in ("e", "c"):
        nome_do_arquivo = input("Nome do arquivo: ")

        if escolha_exportar == "e":
            dados_df.to_excel(f"{nome_do_arquivo}.xlsx")

            print(f"Arquivo '{nome_do_arquivo}.xlsx' gerado com sucesso!")

        elif escolha_exportar == "c":
            dados_df.to_csv(f"{nome_do_arquivo}.csv")

            print(f"Arquivo '{nome_do_arquivo}.csv' gerado com sucesso!")


 
 
#-------------------------------------------------------------------------------------------------------------------------
def listar_carros(conn, inst_consulta):
    os.system("cls")
    print("----- LISTAR REGISTROS -----")
    print("""
a - Listar todos os carros
b - Pesquisar carro por parte da String e listar
c - Pesquisar carro por um campo numérico e listar
d - Pesquisa genérica
""")
 
    alternativa = input("Escolha: ").lower()
 
    match alternativa:
        case "a":
            listar_todos_carros(inst_consulta)
        case "b":
            listar_por_string(inst_consulta)
        case "c":
            listar_por_numero(inst_consulta)
        case "d":
            pesquisa_generica(inst_consulta)
        case _:
            os.system("cls")
            print("Opção inválida!")


 
#-------------------------------------------------------------------------------------------------------------------------
def selecionar_colunas_padrao():
   
    todas_colunas = ['Id', 'Modelo', 'Marca', 'Ano', 'Cor', 'Proprietário', 'data_cadastro', 'data_ultima_modificacao', 'ativo']
 
    print("\nCampos disponíveis:")
    for i, col in enumerate(todas_colunas, start=1):
        print(f"{i} - {col}")
 
    print("\nDigite os números das colunas que deseja visualizar separados por vírgula.")
    print("Ou pressione [ENTER] para mostrar todas.\n")
 
    entrada = input("Colunas (ex: 1,3,5): ").strip()
 
    if entrada == "":
        return todas_colunas
 
    try:
        indices = [int(x.strip()) - 1 for x in entrada.split(",") if x.strip().isdigit()]
        colunas_escolhidas = [todas_colunas[i] for i in indices if 0 <= i < len(todas_colunas)]
    except ValueError:
        colunas_escolhidas = []
 
    if colunas_escolhidas:
        return colunas_escolhidas
    else:
        print("Nenhum índice válido selecionado. Mostrando todas.\n")
        return todas_colunas
    

 
#-------------------------------------------------------------------------------------------------------------------------
def listar_todos_carros(inst_consulta):
    os.system("cls")
    print("------ LISTANDO TODOS OS DADOS ------\n")
 
    colunas_escolhidas = selecionar_colunas_padrao()
 
    inst_consulta.execute('SELECT * FROM carros')
    data = inst_consulta.fetchall()
 
    if not data:
        print("Nenhum registro encontrado.")
        return
 
    dados_df = pd.DataFrame.from_records(
        data, columns=['Id', 'Modelo', 'Marca', 'Ano', 'Cor', 'Proprietário', 'data_cadastro', 'data_ultima_modificacao', 'ativo']
    )
 
    dados_df = dados_df[colunas_escolhidas]  
    print("-" * 98)
    print(dados_df)
    print("-" * 98)
 
    exportar_arquivo(dados_df)


 
#-------------------------------------------------------------------------------------------------------------------------
def listar_por_string(inst_consulta):
    os.system("cls")
    print("------ PESQUISA POR STRING ------\n")
 
   
    colunas_escolhidas = selecionar_colunas_padrao()
 
    campo = input("Digite o campo (marca, modelo, cor, proprietario): ")
    termo = input("Digite o texto que deseja buscar na tabela: ")
 
    sql = f"SELECT * FROM carros WHERE LOWER({campo}) LIKE '%{termo.lower()}%'"
    inst_consulta.execute(sql)
    data = inst_consulta.fetchall()
 
    if data:
        dados_df = pd.DataFrame.from_records(
            data, columns=['Id', 'Modelo', 'Marca', 'Ano', 'Cor', 'Proprietário', 'data_cadastro', 'data_ultima_modificacao', 'ativo']
        )
 
        dados_df = dados_df[colunas_escolhidas]
 
        print("-" * 95)
        print(dados_df)
        print("-" * 95)
        exportar_arquivo(dados_df)
    else:
        print("Nenhum registro encontrado com esse filtro.")


 
#-------------------------------------------------------------------------------------------------------------------------
def listar_por_numero(inst_consulta):
    os.system("cls")
    print("------ PESQUISA POR NÚMERO ------\n")
 
    colunas_escolhidas = selecionar_colunas_padrao()
 
    valor = int(input("Digite o ano: "))
    operador = input("Operador (>, >=, <, <=, = ou !=): ")
 
    sql = f"SELECT * FROM carros WHERE ano {operador} {valor}"
    inst_consulta.execute(sql)
    data = inst_consulta.fetchall()
 
    if data:
        dados_df = pd.DataFrame.from_records(
            data, columns=['Id', 'Modelo', 'Marca', 'Ano', 'Cor', 'Proprietário', 'data_cadastro', 'data_ultima_modificacao', 'ativo']
        )
 
        dados_df = dados_df[colunas_escolhidas]
 
        print("-" * 95)
        print(dados_df)
        print("-" * 95)
        exportar_arquivo(dados_df)
    else:
        print("Nenhum registro encontrado com esse filtro.")


 
#-------------------------------------------------------------------------------------------------------------------------
def pesquisa_generica(inst_consulta):
    os.system("cls")
    print("------ PESQUISA GENÉRICA ------\n")
 
    colunas_escolhidas = selecionar_colunas_padrao()
 
    termo = input("Digite parte do texto que deseja buscar: ").lower()
 
    sql = f"""
        SELECT * FROM carros
        WHERE LOWER(marca) LIKE '%{termo}%'
           OR LOWER(modelo) LIKE '%{termo}%'
           OR LOWER(cor) LIKE '%{termo}%'
           OR LOWER(proprietario) LIKE '%{termo}%'
    """
    inst_consulta.execute(sql)
    data = inst_consulta.fetchall()
 
    if data:
        dados_df = pd.DataFrame.from_records(
            data, columns=['Id', 'Modelo', 'Marca', 'Ano', 'Cor', 'Proprietário', 'data_cadastro', 'data_ultima_modificacao', 'ativo']
        )
 
        dados_df = dados_df[colunas_escolhidas]
 
        print("-" * 48)
        print(dados_df)
        print("-" * 48)
        exportar_arquivo(dados_df)
    else:
        print("Nenhum registro encontrado com esse filtro.")
 
 
 
#-------------------------------------------------------------------------------------------------------------------------
def editar_carro(conn, inst_consulta, inst_alteracao):
    os.system("cls")
    try:
        print("----- ALTERAR DADOS DO CARRO -----")
        print("\nDADOS JÁ GRAVADOS NA TABELA\n")

        inst_consulta.execute('SELECT * FROM carros')
        data = inst_consulta.fetchall()

        print('-' * 95)
        dados_df = pd.DataFrame.from_records(
            data, columns=['Id', 'Modelo', 'Marca', 'Ano', 'Cor', 'Proprietário', 
                           'Data Cadastro', 'Data Última Modificação', 'Ativo'], index='Id')
        print(dados_df)
        print('-' * 95)

        carro_id = int(input("\nEscolha o Id do carro que deseja editar: "))

        consulta = f"SELECT * FROM carros WHERE id_carro = {carro_id}"
        inst_consulta.execute(consulta)
        data = inst_consulta.fetchall()

        if not data:
            print(f"Nenhum carro encontrado com ID = {carro_id}")
            input("Pressione ENTER para voltar...")
            return

        novo_modelo = input("Novo modelo....: ")
        nova_marca = input("Nova marca....: ")
        novo_ano = int(input("Novo ano...: "))
        nova_cor = input("Nova cor...: ")
        novo_proprietario = input("Novo proprietário...: ")
        data_modificacao = hora_atual()  # atualiza a data/hora de modificação

        alteracao = f"""
            UPDATE carros
            SET modelo = '{novo_modelo}',
                marca = '{nova_marca}',
                ano = {novo_ano},
                cor = '{nova_cor}',
                proprietario = '{novo_proprietario}',
                data_ultima_modificacao = '{data_modificacao}'
            WHERE id_carro = {carro_id}
        """

        inst_alteracao.execute(alteracao)
        conn.commit()
        print("DADOS MODIFICADOS COM SUCESSO!")

    except ValueError:
        print("Digite um número válido no ano!")
    except Exception as e:
        print("Erro na transação do BD:", e)
 
 
 
 
#-------------------------------------------------------------------------------------------------------------------------
def excluir_carro(conn, inst_consulta, inst_exclusao):
    os.system("cls")
    print("----- EXCLUIR CARRO DA TABELA POR (ID) -----\n\n")
 
    print("DADOS JA GRAVADOS NA TABELA")
    lista_carros1 = []
 
    inst_consulta.execute('SELECT * FROM carros')
    data = inst_consulta.fetchall()
 
    for dt in data:
        lista_carros1.append(dt)
    lista_carros1 = sorted(lista_carros1)
 
    print("-" * 95)
    dados_df = pd.DataFrame.from_records(
        lista_carros1, columns=['Id', 'Modelo', 'Marca', 'Ano', 'Cor', 'Proprietário', 'data_cadastro', 'data_ultima_modificacao', 'ativo'], index='Id')
    print(dados_df)
    print("-" * 95)
 
    id_carro = input("\nEscolha um Id: ")
 
    os.system("cls")
    print("EXCLUIR DADOS POR (ID)\n")
 
    lista_carros = []
 
    if id_carro.isdigit():
        id_carro = int(id_carro)
        consulta = f""" SELECT * FROM carros WHERE id_carro = {id_carro}"""
        inst_consulta.execute(consulta)
        data = inst_consulta.fetchall()
 
        for dt in data:
            lista_carros.append(dt)
 
        if len(lista_carros) == 0:
            print(f"Não há um carro cadastrado com o ID = {id_carro}")
        else:
            exclusao = f"DELETE FROM carros WHERE id_carro = {id_carro}"
            inst_exclusao.execute(exclusao)
            conn.commit()
 
            print("-" * 95)
            dados_df = pd.DataFrame.from_records(
                lista_carros, columns=['Id', 'Modelo', 'Marca', 'Ano', 'Cor', 'Proprietário', 'data_cadastro', 'data_ultima_modificacao', 'ativo'], index='Id')
            print(dados_df)
            print("-" * 95)
    else:
        print("O Id não é numérico!")
       
 
 
# ---------- MENU PRINCIPAL ----------
def menu_principal():
    conn, inst_cadastro, inst_consulta, inst_alteracao, inst_exclusao = conectar_banco()
    if not conn:
        return
 
    conexao = True
 
    while conexao:
        os.system("cls")
        print("""Bem vindo a Company Cars! o que você desja ?
 
0 - SAIR                  
1- Cadastrar Carros
2- Pesquisar Carros
3- Listar registros Carros
4- Editar registro carro
5- Excluir registro carro por (ID)
""")
 
        opcao = input("Escolha: ")
 
        match opcao:
            case "1":
                cadastrar_carro(conn, inst_cadastro)
            case "2":
                pesquisar_carro_por_id(conn, inst_consulta)
            case "3":
                listar_carros(conn, inst_consulta)
            case "4":
                editar_carro(conn, inst_consulta, inst_alteracao)
            case "5":
                excluir_carro(conn, inst_consulta, inst_exclusao)
            case "0":
                os.system("cls")
                print("Programa sendo finalizado! Espere um instante...")
                time.sleep(3)
                os.system("cls")
                print("Programa finalizado!")
                break
            case _:
                print("Nenhuma alternativa encontrada! Tente novamente...")
 
        input("\n\nPressione enter para continuar...")
 
 
# ---------- EXECUÇÃO ----------
if __name__ == "__main__":
    menu_principal()
    
