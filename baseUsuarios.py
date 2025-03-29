import pandas as pd
import sqlite3

# Tabela 1: Carregar o primeiro arquivo CSV
try:
    df1 = pd.read_csv('DataSet_MCSonae/sample_prod_info.csv', sep=';', encoding='utf-8')
    print("Primeiro arquivo CSV carregado com sucesso!")
    print("Colunas disponíveis no primeiro CSV:", df1.columns.tolist())  # Verificar colunas
    df1.columns = df1.columns.str.strip()  # Remover espaços extras
except FileNotFoundError:
    print("Erro: Primeiro arquivo não encontrado. Verifique o caminho.")
    exit()

# Selecionar apenas as colunas desejadas para a primeira tabela
colunas_desejadas1 = ['sku', 'product_dsc', 'cat_cd', 'cat_dsc_ext', 'product_short_dsc', '20231226']
df1 = df1[colunas_desejadas1]

# Tabela 2: Carregar o segundo arquivo CSV
try:
    df2 = pd.read_csv('DataSet_MCSonae/sample_account_info_encripted.csv', sep=',', encoding='utf-8')
    print("Segundo arquivo CSV carregado com sucesso!")
    print("Colunas disponíveis no segundo CSV:", df2.columns.tolist())  # Verificar colunas
    df2.columns = df2.columns.str.strip()  # Remover espaços extras
except FileNotFoundError:
    print("Erro: Segundo arquivo não encontrado. Verifique o caminho.")
    exit()

# Selecionar apenas as colunas desejadas para a segunda tabela
colunas_desejadas2 = ['account_no', 'family_members', 'segment_gender_f', 'segment_gender_m', 'age_group', 'district', 'region', 'segment_cd_lifestyle', 'segment_dsc_lifestyle']
df2 = df2[colunas_desejadas2]

# Conectar ao banco de dados SQLite
try:
    connection = sqlite3.connect('baseDeDados.db')  # Nome do banco de dados
    cursor = connection.cursor()
    print("Conexão com o banco de dados estabelecida!")
except sqlite3.Error as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
    exit()

# Criar a primeira tabela
try:
    cursor.execute("DROP TABLE IF EXISTS produtos")  # Apagar a tabela se já existir
    colunas1 = ', '.join([f"[{col}] TEXT" for col in colunas_desejadas1])
    cursor.execute(f"CREATE TABLE produtos ({colunas1});")
    print("Tabela 'produtos' criada/verificada com sucesso!")
    for _, row in df1.iterrows():
        valores = tuple(row)
        placeholders = ', '.join(['?'] * len(row))
        cursor.execute(f"INSERT INTO produtos VALUES ({placeholders});", valores)
    connection.commit()
    print("Dados inseridos com sucesso na tabela 'produtos'!")
except sqlite3.Error as e:
    print(f"Erro ao criar/inserir dados na tabela 'produtos': {e}")
    connection.rollback()

# Criar a segunda tabela
try:
    cursor.execute("DROP TABLE IF EXISTS usuarios")  # Apagar a tabela se já existir
    colunas2 = ', '.join([f"[{col}] TEXT" for col in colunas_desejadas2])
    cursor.execute(f"CREATE TABLE usuarios ({colunas2});")
    print("Tabela 'usuarios' criada/verificada com sucesso!")
    for _, row in df2.iterrows():
        valores = tuple(row)
        placeholders = ', '.join(['?'] * len(row))
        cursor.execute(f"INSERT INTO usuarios VALUES ({placeholders});", valores)
    connection.commit()
    print("Dados inseridos com sucesso na tabela 'usuarios'!")
except sqlite3.Error as e:
    print(f"Erro ao criar/inserir dados na tabela 'usuarios': {e}")
    connection.rollback()
finally:
    # Fechar a conexão
    connection.close()
    print("Conexão com o banco de dados fechada.")

