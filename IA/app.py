from openai import OpenAI
import json

# Configuração fixa da API Key (substitua pelo seu valor real)
API_KEY = "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"  # ← Substituir esta string

def is_product_related(text):
    keywords = [
        'produto', 'quero', 'comprar', 'quero fazer', 'preciso de', 'necessito de',
        'sugira', 'recomende', 'lista de', 'material', 'ingrediente', 'ferramenta',
        'item', 'qual', 'quais', 'como fazer', 'para', 'limpar', 'cozinhar',
        'reparar', 'montar', 'fome', 'como se faz', 'limpar', 'tenho', 'buraco'
    ]
    return any(kw in text.lower() for kw in keywords)

def extract_products(response):
    produtos = []
    if "📋 Produtos Sugeridos:" in response:
        try:
            products_part = response.split("📋 Produtos Sugeridos:")[1].split("\n\n")[0]
            for line in products_part.split("\n"):
                line = line.strip()
                if line.startswith("-") and ":" in line:
                    produto = line.split(":", 1)[1].strip()
                    produtos.append(produto)
        except Exception:
            pass
    return produtos

def processar_consulta(user_input):
    client = OpenAI(api_key=API_KEY)  # Usa a chave fixa
    
    try:
        requires_products = is_product_related(user_input)
        
        prompt = (
            f"O utilizador perguntou: '{user_input}'\n"
            "Como assistente do Continente em Portugal:\n"
            "1. Responda em português europeu\n"
            "2. Seja natural e converse normalmente\n"
        )
        
        if requires_products:
            prompt += (
                "3. Sugira os produtos genéricos no formato:\n"
                "📋 Produtos Sugeridos:\n- [Categoria]: [Produto]\n"
                "4. Inclua uma dica prática breve\n"
                "5. Use apenas categorias existentes no Continente\n"
            )
        else:
            prompt += (
                "3. Responda de forma direta sem lista de produtos\n"
                "4. Mantenha a resposta curta e objetiva\n"
            )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        
        resposta = response.choices[0].message.content
        
        return {
            "pergunta": user_input,
            "resposta": resposta,
            "produtos_sugeridos": extract_products(resposta)
        }
        
    except Exception as e:
        return {
            "pergunta": user_input,
            "resposta": f"Erro na consulta: {str(e)}",
            "produtos_sugeridos": []
        }

# Exemplo de uso:
if __name__ == "__main__":
    resultado = processar_consulta("Quero fazer um cozido à portuguesa")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))