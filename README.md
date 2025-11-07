# 🚗 Conectando Python com Banco de Dados Oracle

Projeto desenvolvido por **Álvaro Freitas Miranda** e **João Victor Veronesi** Com mentoria do Nosso professor de python [Edson de Oliveira](https://www.linkedin.com/in/edson-de-oliveira-338343148/).  
O sistema tem como objetivo **gerenciar o cadastro de carros** utilizando **Python** com **conexão ao banco de dados Oracle**.

---

## 🧩 Descrição do Projeto

Este projeto implementa um sistema em Python que permite realizar operações completas de **CRUD** (Create, Read, Update, Delete) sobre registros de veículos armazenados em uma tabela Oracle.  
Também é possível **exportar os dados para arquivos Excel (.xlsx)** ou **CSV (.csv)**.

O sistema conta com um **menu interativo no terminal**, permitindo ao usuário realizar ações como cadastrar, listar, pesquisar, editar e excluir registros de forma simples e eficiente.

---

## 🗄️ Estrutura da Tabela (Oracle)

```sql
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
```

---

## ⚙️ Funcionalidades

✅ **Cadastrar carros** com informações detalhadas.  
✅ **Pesquisar veículos** por ID ou por diferentes critérios (texto, número, genérico).  
✅ **Listar registros** com seleção de colunas personalizadas.  
✅ **Editar dados** de carros existentes.  
✅ **Excluir carros** por ID.  
✅ **Exportar resultados** para Excel ou CSV.  
✅ **Registrar data e hora de cadastro e última modificação** automaticamente.

---

## 🧠 Tecnologias Utilizadas

- **Python 3.x**
- **Oracle Database (FIAP ORCL)**
- **oracledb** → Conexão com o banco de dados Oracle.  
- **pandas** → Manipulação de dados e exportação para Excel/CSV.  
- **datetime** → Controle de datas e horários.  
- **os e time** → Operações no sistema e pausas no terminal.

---

## 🚀 Execução do Projeto

### 1️⃣ Pré-requisitos

- Ter o **Python 3** instalado.
- Instalar as bibliotecas necessárias:

```bash
pip install oracledb pandas
```

- Ter acesso ao banco **Oracle da FIAP** (ou um banco Oracle equivalente) e criar a tabela `carros` com o script SQL fornecido acima.

---

### 2️⃣ Executar o programa

```bash
python conexao_BD.py
```

O menu principal será exibido no terminal, permitindo navegar entre as opções disponíveis:

```
Bem vindo a Company Cars! o que você deseja?

0 - SAIR
1 - Cadastrar Carros
2 - Pesquisar Carros
3 - Listar Registros
4 - Editar Registro
5 - Excluir Registro por ID
```

---

## 📤 Exportação de Dados

Durante as listagens e pesquisas, o sistema permite gerar relatórios:
- **Excel (.xlsx)**
- **CSV (.csv)**

Basta escolher a opção `[E]xcel` ou `[C]SV` ao final da consulta.

---

## 👨‍💻 Autores

| Nome
|------
| Álvaro Freitas Miranda
| João Victor Veronesi

---

## 🧾 Licença

Este projeto é de uso **acadêmico** e foi desenvolvido como parte das atividades da **FIAP**.  
Fique à vontade para estudar e adaptar o código conforme suas necessidades.

---

### 💡 Dica

Para adaptar o sistema a outro banco de dados (ex: MySQL ou SQLite), basta ajustar a função de conexão e as queries SQL.
