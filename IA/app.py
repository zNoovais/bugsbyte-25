from openai import OpenAI
import json

# Configuração fixa da API Key (substitua pelo seu valor real)
API_KEY = "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"  # ← Substituir esta string

def is_product_related(text):
    keywords = [
        'produto', 'quero', 'comprar', 'quero fazer', 'preciso de', 'necessito de',
        'sugira', 'recomende', 'lista de', 'material', 'ingrediente', 'ferramenta',
        'item', 'qual', 'quais', 'como fazer', 'para', 'limpar', 'cozinhar',
        'reparar', 'montar', 'fome', 'como se faz', 'limpar', 'tenho', 'buraco','como',
        'quais', 'onde', 'encontrar', 'ajuda', 'dicas', 'sugestões'
    ]
    return any(kw in text.lower() for kw in keywords)

def extract_products(response):
    produtos = []
    


    for letra in range(len(response)):
        if response[letra] == ":":
            produtos = response[(letra + 4):].split("\n")

    return produtos

def extract_pergunta(response):
    pergunta = []
    
    print(response)

    for letra in range(len(response)):
        pergunta.append(response[letra])
        if response[letra] == ":":
            break
    
    return ''.join(pergunta)

def processar_consulta(user_input):
    client = OpenAI(api_key=API_KEY)  # Usa a chave fixa
    
    try:
        requires_products = is_product_related(user_input)
        
        prompt = (
            f"O utilizador perguntou: '{user_input}'"
            "Como assistente do Continente em Portugal:"
            "1. Responda em português europeu"
            "2. Seja natural e converse normalmente"
        )
        
        if requires_products:
            prompt += (
                "diga o problema e depois coloque dois pontos e faça o (5.)"
                "5. escreva os produtos em uma lista separada por \n sem espaço nem -"
                "4. Não use emojis"
                "6. so coloque produtos de supermercado"
                "depois da lista nao escreva mais nada"
            )
        else:
            prompt += (
                "3. Responda de forma direta sem lista de produtos"
                "4. Mantenha a resposta curta e objetiva"
            )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        
        resposta = response.choices[0].message.content
        
        return {
            "pergunta": user_input,
            "resposta": extract_pergunta(resposta),
            "detalhes": {
                "produtos_sugeridos": extract_products(resposta)
            }
        }
        
    except Exception as e:
        return {
            "pergunta": user_input,
            "resposta": f"Erro na consulta: {str(e)}",
            "detalhes": {
                "produtos_sugeridos": []
            }
        }
    
# Função para salvar os dados em um arquivo JSON
def salvar_em_json(dados, arquivo="resultado.json"):
    try:
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
        print(f"Dados salvos com sucesso em {arquivo}")
    except Exception as e:
        print(f"Erro ao salvar os dados: {e}")

# Exemplo de uso
if __name__ == "__main__":
    consulta = "Quais produtos preciso para fazer uma feijoada?"
    resultado = processar_consulta(consulta)
    salvar_em_json(resultado, "resultado.json")