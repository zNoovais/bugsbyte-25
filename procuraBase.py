import sqlite3
from rapidfuzz import fuzz, process
import normalizar

def procuraBase(lista):
    out = []  # Lista para armazenar os resultados

    # Conectar ao banco de dados
    conexao = sqlite3.connect('baseDeDados.db')
    cursor = conexao.cursor()

    # Obter todos os valores da coluna 'product_dsc_normalizado' da tabela 'produtos'
    cursor.execute("SELECT product_dsc_normalizado, * FROM produtos")
    produtos = cursor.fetchall()  # Lista de todos os produtos no banco de dados

    # Iterar sobre os artigos na lista
    for artigo in lista:
        artigo_normalizado = normalizar.normalizar_texto(artigo)  # Normalizar o artigo
        print(f"Procurando por: {artigo_normalizado}")

        # Usar correspondência aproximada para encontrar o melhor resultado
        best_match = process.extractOne(
            artigo_normalizado,  # Texto a ser comparado
            [produto[0] for produto in produtos],  # Lista de descrições normalizadas
            scorer=fuzz.partial_ratio  # Algoritmo de similaridade
        )

        # Adicionar o melhor resultado à lista de saída, se a similaridade for alta
        if best_match:
            produto_desc, score, index = best_match
            print(f"Melhor produto encontrado: {produto_desc} (similaridade: {score})")
            if score >= 90:  # Apenas adicionar correspondências com similaridade >= 70%
                print(f"Adicionando produto: {produtos[index]}")
                out.append(produtos[index][0])

    # Fechar a conexão
    conexao.close()

    return out  # Retornar os resultados encontrados


# Lista de artigos para procurar
artigos2 = [
    "feijao preto",
    "joao henrique",
    "massa linguine",
    "fiambre",
    "pasta de amendoim",
    "carne moida",
    "vinho",
    "diogo alves",
    "pedro mo",
    "jose pedro",
    "andreia alves cardoso",
    "filipa cangueiro gonçalves",
    "Guilherme Vaz",
    "Ines Trovisco"
]

# Executar a função e imprimir os resultados
resultados = procuraBase(artigos2)
print("Resultados encontrados:")
print(resultados)