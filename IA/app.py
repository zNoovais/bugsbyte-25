import tkinter as tk
from tkinter import scrolledtext
import json
import os
from openai import OpenAI

class SmartAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Assistente Continente")
        
        self.data_file = "historico_conversas.json"
        self.chat_history = self.load_data()
        
        self.main_categories = [
            "Frescos", "Lacticínios e Ovos", "Congelados", "Mercearia",
            "Bebidas", "Limpeza", "Beleza e Higiene", "Bebé",
            "Animais", "Casa e Jardim", "Electrodomésticos", "Tecnologia"
        ]
        
        self.create_interface()

    def create_interface(self):
        self.chat_area = scrolledtext.ScrolledText(
            self.root, 
            width=70, 
            height=25,
            wrap=tk.WORD,
            state='disabled'
        )
        self.chat_area.pack(padx=10, pady=10)
        
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=5, fill=tk.X)
        
        self.user_input = tk.Entry(input_frame, width=60)
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.user_input.bind("<Return>", lambda e: self.process_input())
        
        btn_send = tk.Button(input_frame, text="Enviar", command=self.process_input)
        btn_send.pack(side=tk.RIGHT)
        
        self.show_message("Assistente", "Bem-vindo ao Continente! Como posso ajudar? (Escreva 'ajuda' para opções)")

    def show_message(self, sender, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_area.yview(tk.END)
        self.chat_area.config(state='disabled')

    def process_input(self):
        user_text = self.user_input.get().strip()
        self.user_input.delete(0, tk.END)
        
        if not user_text:
            return
            
        self.show_message("Utilizador", user_text)
        
        if user_text.lower() == "sair":
            self.root.destroy()
            return
            
        try:
            if user_text.lower() == "ajuda":
                response = self.get_help()
            else:
                response = self.generate_response(user_text)
            
            self.show_message("Assistente", response)
            self.save_interaction(user_text, response)
            
        except Exception as e:
            error_msg = f"Erro: {str(e)}"
            self.show_message("Assistente", error_msg)
            self.save_interaction(user_text, error_msg)

    def generate_response(self, problem):
        try:
            requires_products = self.is_product_related(problem)
            
            prompt = (
                f"O utilizador perguntou: '{problem}'\n"
                "Como assistente do Continente em Portugal:\n"
                "1. Responda em português europeu\n"
                "2. Seja natural e converse normalmente\n"
            )
            
            if requires_products:
                prompt += (
                    "3. Sugira até 5 produtos genéricos no formato:\n"
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
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Erro na API: {str(e)}")

    def is_product_related(self, text):
        keywords = [
            'produto', 'quero', 'comprar', 'quero fazer','preciso de', 'necessito de',
            'sugira', 'recomende', 'lista de', 'material',
            'ingrediente', 'ferramenta', 'item', 'qual',
            'quais', 'como fazer', 'para', 'limpar',
            'cozinhar', 'reparar', 'montar', 'fome', 'como se faz'
        ]
        text_lower = text.lower()
        return any(kw in text_lower for kw in keywords)

    def extract_products(self, response):
        produtos = []
        try:
            if "📋 Produtos Sugeridos:" in response:
                parte_produtos = response.split("📋 Produtos Sugeridos:")[1].split("\n\n")[0]
                for linha in parte_produtos.split("\n"):
                    if linha.startswith("-") and ":" in linha:
                        produto = linha.split(":", 1)[1].strip()
                        produtos.append(produto)
        except:
            pass
        return produtos

    def save_interaction(self, pergunta, resposta):
        interacao = {
            "pergunta": pergunta,
            "resposta": resposta,
            "produtos_sugeridos": self.extract_products(resposta)
        }
        
        self.chat_history.append(interacao)
        self.save_data()

    def save_data(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.chat_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao guardar: {str(e)}")

    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar: {str(e)}")
        return []

    def get_help(self):
        return (
            "Comandos disponíveis:\n"
            "- Escreva normalmente para fazer perguntas\n"
            "- 'sair' para terminar o programa\n"
            "- Peça sugestões de produtos (ex: 'Preciso de materiais de limpeza')\n"
            "- Faça perguntas sobre produtos disponíveis no Continente\n"
            "- Use termos comuns em português de Portugal"
        )

if __name__ == "__main__":
    client = OpenAI(api_key="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")  # Substituir pela chave real
    root = tk.Tk()
    app = SmartAssistant(root)
    root.mainloop()