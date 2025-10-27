# Alvaro Freitas Miranda: RM565364
# João Victor Veronesi: RM565290

import os
import oracledb
import pandas as pd
import time
os.system("cls")

# tabela sql
"""
CREATE TABLE carros (
    id_carro INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    modelo VARCHAR(100) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    ano DECIMAL(4) NOT NULL,            
    cor VARCHAR(30),            
    proprietario VARCHAR(100)   
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

def cadastrar_carro(conn, inst_cadastro):
    try:
        os.system("cls")
        print("----- CADASTRAR CARROS -----\n")
        modelo = input("Digite o modelo....: ")
        marca = input("Digite a marca....: ")
        ano = int(input("Digite o ano...: "))
        cor = input("Digite a cor...: ")
        propietario = input("Digite o proprietário...: ")

        cadastro = f""" INSERT INTO carros (modelo, marca, ano, cor, proprietario)
                        VALUES ('{modelo}', '{marca}', {ano}, '{cor}','{propietario}') """

        inst_cadastro.execute(cadastro)
        conn.commit()

    except ValueError:
        print("Digite um número na idade!")
    except:
        print("Erro na transação do BD")
    else:
        print("\nDADOS GRAVADOS COM SUCESSO!")


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

        print("-" * 45)
        dados_df = pd.DataFrame.from_records(
            lista_carros2, columns=['Id', 'Modelo', 'Marca', 'Ano', 'Cor', 'Proprietário'], index='Id')

        if len(lista_carros2) == 0:
            print(f"Não há um carro cadastrado com o ID = {id_carro}")
        else:
            print(dados_df)
            print("-" * 45)
    else:
        print("O Id não é numérico!")


def listar_carros(conn, inst_consulta):
    os.system("cls")
    print("----- LISTAR REGISTROS -----")
    print("""
a - Listar todos os carros
b - Pesquisar carro por parte da String e listar
c - Pesquisar carro por um campo numérico e listar
""")

    alternativa = input("Escolha: ").lower()

    match alternativa:
        case "a":
            listar_todos_carros(inst_consulta)
        case "b":
            listar_por_string(inst_consulta)
        case "c":
            listar_por_numero(inst_consulta)
        case _:
            os.system("cls")
            print("Opção inválida!")


def listar_todos_carros(inst_consulta):
    os.system("cls")
    print("------ LISTANDO TODOS OS DADOS ------\n")
    lista_carros1 = []

    inst_consulta.execute('SELECT * FROM carros')
    data = inst_consulta.fetchall()

    for dt in data:
        lista_carros1.append(dt)
    lista_carros1 = sorted(lista_carros1)

    print("-" * 48)
    dados_df = pd.DataFrame.from_records(
        lista_carros1, columns=['Id', 'Modelo', 'Marca', 'Ano', 'Cor', 'Proprietário'], index='Id')
    print(dados_df)
    print("-" * 48)

    exportar_arquivo(dados_df)


def listar_por_string(inst_consulta):
    os.system("cls")
    campo = input("Digite o campo (marca, modelo, cor, proprietario): ")
    termo = input("Digite o texto que deseja buscar na tabela: ")

    sql = f"SELECT * FROM carros WHERE LOWER({campo}) LIKE '%{termo}%'"
    inst_consulta.execute(sql)
    data = inst_consulta.fetchall()

    if data:
        lista_filtrada = sorted(data)
        print("-" * 48)
        dados_df = pd.DataFrame.from_records(
            lista_filtrada, columns=['Id', 'Modelo', 'Marca', 'Ano', 'Cor', 'Proprietário'], index='Id')
        print(dados_df)
        print("-" * 48)
        exportar_arquivo(dados_df)
    else:
        print("Nenhum registro encontrado com esse filtro.")


def listar_por_numero(inst_consulta):
    os.system("cls")
    valor = int(input("Digite o ano: "))
    operador = input("Operador (>, >=, <, <=, = ou !=): ")

    sql = f"SELECT * FROM carros WHERE ano {operador} {valor}"
    inst_consulta.execute(sql)
    data = inst_consulta.fetchall()

    if data:
        lista_filtrada = sorted(data)
        print("-" * 48)
        dados_df = pd.DataFrame.from_records(
            lista_filtrada, columns=['Id', 'Modelo', 'Marca', 'Ano', 'Cor', 'Proprietário'], index='Id')
        print(dados_df)
        print("-" * 48)
        exportar_arquivo(dados_df)
    else:
        print("Nenhum registro encontrado com esse filtro.")


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


def editar_carro(conn, inst_consulta, inst_alteracao):
    os.system("cls")
    try:
        print("----- ALTERARANDO DADOS DO CARRO -----")
        print("\n\nDADOS JA GRAVADOS NA TABELA")
        lista_carros1 = []

        inst_consulta.execute('SELECT * FROM carros')
        data = inst_consulta.fetchall()

        for dt in data:
            lista_carros1.append(dt)
        lista_carros1 = sorted(lista_carros1)

        print("-" * 45)
        dados_df = pd.DataFrame.from_records(
            lista_carros1, columns=['Id', 'Modelo', 'Marca', 'Ano', 'Cor', 'Proprietário'], index='Id')
        print(dados_df)
        print("-" * 45)

        carro_id = int(input("\nEscolha um Id: "))

        consulta = f""" SELECT * FROM carros WHERE id_carro = {carro_id}"""
        inst_consulta.execute(consulta)
        data = inst_consulta.fetchall()

        if len(data) == 0:
            print(f"Não há um carro cadastrado com o ID = {carro_id}")
            input("Pressione ENTER")
        else:
            os.system("cls")
            novo_modelo = input("Digite um novo modelo....: ")
            nova_marca = input("Digite uma nova marca....: ")
            novo_ano = int(input("Digite um novo ano...: "))
            nova_cor = input("Digite uma nova cor...: ")
            novo_propietario = input("Digite um novo proprietário...: ")

            alteracao = f"""
            UPDATE carros SET modelo='{novo_modelo}', marca='{nova_marca}', ano={novo_ano}, cor='{nova_cor}', proprietario='{novo_propietario}'
            WHERE id_carro={carro_id}
            """
            inst_alteracao.execute(alteracao)
            conn.commit()
    except ValueError:
        print("Digite um número no ano!")
    except:
        print("Erro na transação do BD")
    else:
        print("DADOS MODIFICADOS COM SUCESSO!!")


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

    print("-" * 45)
    dados_df = pd.DataFrame.from_records(
        lista_carros1, columns=['Id', 'Modelo', 'Marca', 'Ano', 'Cor', 'Proprietário'], index='Id')
    print(dados_df)
    print("-" * 45)

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

            print("-" * 45)
            dados_df = pd.DataFrame.from_records(
                lista_carros, columns=['Id', 'Modelo', 'Marca', 'Ano', 'Cor', 'Proprietário'], index='Id')
            print(dados_df)
            print("-" * 45)
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
