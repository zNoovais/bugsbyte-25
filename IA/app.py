import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog, filedialog
import json
import os
from openai import OpenAI

# Configurações
client = OpenAI(api_key="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")  # Substitua pela sua chave

class SmartAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Assistente Inteligente 2.0")
        
        self.data_file = "solutions.json"
        self.cart_file = "carrinho.json"
        self.solutions = self.load_data()
        self.cart = self.load_cart()
        
        self.create_interface()
        
    def load_data(self):
        """Carrega as soluções salvas do arquivo JSON"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def create_interface(self):
        # Área de conversa principal
        self.chat_area = scrolledtext.ScrolledText(
            self.root, 
            width=80, 
            height=25,
            wrap=tk.WORD,
            state='disabled'
        )
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Frame de entrada
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=5, fill=tk.X)
        
        self.user_input = tk.Entry(input_frame, width=60)
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.user_input.bind("<Return>", lambda e: self.process_input())
        
        btn_send = tk.Button(input_frame, text="Enviar", command=self.process_input)
        btn_send.pack(side=tk.RIGHT)
        
        # Botões de ação
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=5)
        
        ttk.Button(action_frame, text="🛒 Ver Carrinho", command=self.show_cart).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="💾 Salvar Tudo", command=self.save_all).pack(side=tk.LEFT, padx=5)
        
        self.show_message("Assistente: Olá! Como posso ajudar hoje? (Digite 'ajuda' para opções)")

    def process_input(self):
        user_text = self.user_input.get().strip().lower()
        self.user_input.delete(0, tk.END)
        
        if not user_text:
            return
            
        if user_text == "sair":
            self.root.destroy()
            return
            
        if user_text == "ajuda":
            self.show_help()
            return
            
        if user_text.startswith("listar"):
            self.list_solutions(user_text)
            return
            
        if user_text.startswith("detalhes"):
            self.show_details(user_text)
            return
            
        self.generate_solution(user_text)

    def show_help(self):
        help_text = """
        Comandos disponíveis:
        - listar [tipo]: Mostra soluções salvas
        - detalhes X: Mostra detalhes da solução X
        - salvar tudo: Guarda todos os dados
        - ajuda: Mostra esta mensagem
        - sair: Encerra o programa
        """
        self.show_message(help_text)

    def list_solutions(self, command):
        filter_type = command[7:].strip() if len(command) > 7 else None
        filtered = [s for s in self.solutions if not filter_type or s["tipo"] == filter_type]
        
        if not filtered:
            self.show_message("Nenhuma solução encontrada")
            return
            
        for idx, solution in enumerate(filtered, 1):
            self.show_message(f"{idx}. [{solution['tipo'].upper()}] {solution['problema']}")

    def show_details(self, command):
        try:
            index = int(command.split()[1]) - 1
            solution = self.solutions[index]
            self.show_message(f"Detalhes:\n{solution['display']}")
        except:
            self.show_message("Comando inválido. Use 'detalhes X'")

    def show_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + "\n\n")
        self.chat_area.yview(tk.END)
        self.chat_area.config(state='disabled')

    def generate_solution(self, problem):
        try:
            prompt = (
                f"Para: '{problem}'\n"
                "1. Solução prática\n"
                "2. Lista de materiais/ingredientes\n"
                "Formato:\n"
                "SOLUÇÃO: [texto]\n"
                "MATERIAIS: item1 (opcional), item2, item3 (opcional)..."
            )
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400
            )
            
            result = self.parse_response(response.choices[0].message.content)
            
            if result:
                entry = {
                    "problema": problem,
                    "tipo": self.detect_problem_type(problem),
                    "solucao": result["solucao"],
                    "materiais": result["materiais"]
                }
                self.solutions.append(entry)
                self.show_materials_window(entry)
                
        except Exception as e:
            self.show_message(f"Erro: {str(e)}")

    def parse_response(self, text):
        try:
            parts = text.split("MATERIAIS:")
            if len(parts) < 2:
                return None
                
            solution = parts[0].replace("SOLUÇÃO:", "").strip()
            materials = []
            
            for item in parts[1].split(","):
                item = item.strip()
                optional = "(opcional)" in item.lower()
                name = item.replace("(opcional)", "").strip()
                materials.append({"nome": name, "opcional": optional, "selecionado": not optional})
            
            return {
                "solucao": solution,
                "materiais": materials,
                "display": f"Solução:\n{solution}\n\nMateriais:\n" + 
                           "\n".join([f"- {m['nome']} {'(opcional)' if m['opcional'] else ''}" for m in materials])
            }
        except Exception as e:
            self.show_message(f"Erro ao processar resposta: {str(e)}")
            return None

    def show_materials_window(self, solution):
        window = tk.Toplevel(self.root)
        window.title(f"Lista de Materiais: {solution['problema']}")
        
        # Frame da lista
        list_frame = ttk.Frame(window)
        list_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Treeview para lista editável
        columns = ('selecionado', 'nome', 'opcional', 'acoes')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        
        # Configurar colunas
        self.tree.heading('selecionado', text='✓')
        self.tree.heading('nome', text='Item')
        self.tree.heading('opcional', text='Opcional')
        self.tree.heading('acoes', text='Ações')
        
        self.tree.column('selecionado', width=50, anchor='center')
        self.tree.column('nome', width=200)
        self.tree.column('opcional', width=80, anchor='center')
        self.tree.column('acoes', width=100, anchor='center')
        
        # Adicionar itens
        for idx, item in enumerate(solution['materiais']):
            self.tree.insert('', 'end', values=(
                '✓' if item['selecionado'] else '',
                item['nome'],
                'Sim' if item['opcional'] else 'Não',
                '🗑️ Remover'
            ))
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Controles
        control_frame = ttk.Frame(window)
        control_frame.pack(pady=10)
        
        ttk.Button(control_frame, text="➕ Adicionar Item", 
                  command=lambda: self.add_item(solution, window)).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🛒 Adicionar ao Carrinho", 
                  command=lambda: self.add_to_cart(solution, window)).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="💾 Salvar Lista", 
                  command=lambda: self.save_list(solution, window)).pack(side=tk.LEFT, padx=5)

    def add_to_cart(self, solution, window):
        selected_items = []
        for child in self.tree.get_children():
            values = self.tree.item(child)['values']
            if values[0] == '✓':
                selected_items.append({
                    'nome': values[1],
                    'opcional': values[2] == 'Sim'
                })
        
        self.cart.append({
            'problema': solution['problema'],
            'itens': selected_items,
            'prioridade': 'normal'
        })
        self.save_cart()
        messagebox.showinfo("Carrinho", "Itens adicionados ao carrinho com sucesso!")
        window.destroy()

    def show_cart(self):
        cart_window = tk.Toplevel(self.root)
        cart_window.title("🛒 Carrinho de Compras")
        
        # Treeview para o carrinho
        tree = ttk.Treeview(cart_window, columns=('item', 'projeto', 'prioridade'), show='headings')
        tree.heading('item', text='Item')
        tree.heading('projeto', text='Projeto')
        tree.heading('prioridade', text='Prioridade')
        
        for item in self.cart:
            for subitem in item['itens']:
                tree.insert('', 'end', values=(subitem['nome'], item['problema'], item['prioridade']))
        
        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Botões de gestão
        btn_frame = ttk.Frame(cart_window)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Exportar Lista", command=self.export_cart).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar Carrinho", command=self.clear_cart).pack(side=tk.LEFT, padx=5)

    def save_all(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.solutions, f, ensure_ascii=False, indent=2)
        self.save_cart()
        messagebox.showinfo("Salvar", "Todos os dados foram salvos!")

    def load_cart(self):
        if os.path.exists(self.cart_file):
            with open(self.cart_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_cart(self):
        with open(self.cart_file, 'w', encoding='utf-8') as f:
            json.dump(self.cart, f, ensure_ascii=False, indent=2)

    def detect_problem_type(self, text):
        """Detecta o tipo de problema com base em palavras-chave"""
        keywords = {
            "culinária": ["fazer", "receita", "cozinhar", "comida"],
            "reparo": ["buraco", "vazamento", "consertar", "quebrado"],
            "tecnologia": ["computador", "internet", "celular", "wi-fi"]
        }
        
        for category, words in keywords.items():
            if any(word in text.lower() for word in words):
                return category
        return "geral"

    def add_item(self, solution, window):
        """Adiciona novo item à lista de materiais"""
        new_item = simpledialog.askstring("Novo Item", "Digite o nome do item:")
        if new_item:
            solution['materiais'].append({
                'nome': new_item,
                'opcional': False,
                'selecionado': True
            })
            window.destroy()
            self.show_materials_window(solution)

    def save_list(self, solution, window):
        """Salva alterações na lista de materiais"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.solutions, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Sucesso", "Lista atualizada com sucesso!")
        window.destroy()

    def clear_cart(self):
        """Limpa o carrinho de compras"""
        self.cart = []
        self.save_cart()
        messagebox.showinfo("Carrinho", "Carrinho limpo com sucesso!")

    def export_cart(self):
        """Exporta o carrinho para um arquivo de texto"""
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                for item in self.cart:
                    f.write(f"Projeto: {item['problema']}\n")
                    f.write("Itens:\n")
                    for subitem in item['itens']:
                        f.write(f"- {subitem['nome']}\n")
                    f.write("\n")
            messagebox.showinfo("Exportar", "Lista exportada com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartAssistant(root)
    root.mainloop()