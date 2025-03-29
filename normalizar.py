import unicodedata

def normalizar_texto(texto):
    # Remove acentos, espaços extras e converte para minúsculas
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    texto = ' '.join(texto.lower().split())  # Remove espaços duplos
    return texto

# Exemplo:
normalizar_texto("Feijão Préto 1kg")  # Retorna: "feijao preto 1kg"