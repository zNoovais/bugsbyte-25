import sqlite3
import normalizar


def procuraBase(lista):
    out = []  # Lista para armazenar os resultados

    # Conectar ao banco de dados
    conexao = sqlite3.connect('baseDeDados.db')
    cursor = conexao.cursor()

    for artigo in lista:
        normalizar(artigo)  # Normalizar o texto do artigo
        print(artigo)
    # Iterar sobre os artigos na lista
    for artigo in lista:
        
        
        # Usar LIKE para procurar correspondências no banco de dados
        cursor.execute("SELECT * FROM produtos WHERE UPPER(product_dsc) LIKE ?", (f"%{artigo_upper}%",))
        
        resultados = cursor.fetchall()  # Obter todos os resultados da consulta
        print(resultados)
        # Adicionar os resultados à lista de saída
        out.extend(resultados)

    # Fechar a conexão
    conexao.close()

    return out  # Retornar os resultados encontrados


# Lista de artigos para procurar
artigos_mercado = [
    "lata de feijão preto",
    "feijão preto 1kg",
    "feijão preto orgânico",
    "feijão vermelho",
    "feijão carioca 500g",
    "feijão branco enlatado",
    "feijão fradinho",
    "arroz integral 5kg",
    "arroz branco pacote 1kg",
    "macarrão espaguete",
    "macarrão parafuso",
    "óleo de soja 900ml",
    "óleo de girassol lata",
    "açúcar refinado 1kg",
    "açúcar cristal",
    "café em pó 250g",
    "café torrado e moído",
    "leite em pó integral",
    "leite desnatado caixa",
    "farinha de trigo 1kg",
    "farinha de mandioca",
    "molho de tomate lata",
    "extrato de tomate",
    "sal refinado",
    "sal grosso",
    "azeite de oliva extravirgem",
    "vinagre de maçã",
    "sabão em pó 2kg",
    "amaciante de roupas",
    "papel higiênico 16 rolos",
    "água mineral 1,5L",
    "refrigerante lata",
    "suco de laranja caixa",
    "biscoito cream cracker",
    "bolacha recheada",
    "sabonete líquido",
    "shampoo anticaspa",
    "condicionador hidratante",
    "escova de dentes",
    "pasta de dente",
    "desinfetante pinho",
    "água sanitária",
    "esponja de aço",
    "detergente líquido",
    "lâmpada LED 9W",
    "pilhas alcalinas",
    "fita adesiva",
    "sacola plástica",
    "pão de forma integral",
    "pão francês",
    "queijo mussarela fatiado",
    "presunto cozido",
    "manteiga com sal",
    "margarina light",
    "iogurte natural",
    "requeijão cremoso",
    "ovo branco 12 unidades",
    "banana prata kg",
    "maçã argentina",
    "laranja bahia kg",
    "cenoura orgânica",
    "batata inglesa kg",
    "cebola roxa",
    "alho poró",
    "tomate cereja",
    "alface crespa",
    "rúcula orgânica",
    "limão tahiti kg",
    "melancia inteira",
    "abacaxi maduro",
    "peito de frango kg",
    "coxão mole kg",
    "carne moída",
    "salsicha hot dog",
    "mortadela",
    "sardinha enlatada",
    "atum em conserva",
    "aveia em flocos",
    "granola sem açúcar",
    "barra de cereal",
    "chocolate ao leite",
    "chocolate amargo 70%",
    "balas de goma",
    "pirulito",
    "água de coco",
    "energético lata",
    "cerveja long neck",
    "vinho tinto seco",
    "whisky nacional",
    "saco de lixo 50L",
    "vassoura",
    "rodo plástico",
    "pano de chão",
    "lustra móveis",
    "inseticida aerosol",
    "repelente elétrico",
    "ração para cães",
    "areia para gato",
    "coleira antipulgas"
]

# Executar a função e imprimir os resultados
resultados = procuraBase(artigos_mercado)
for resultado in resultados:
    print(resultado)