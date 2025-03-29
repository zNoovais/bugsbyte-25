from flask import Flask, request, jsonify, make_response
import csv

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response

def load_users():
    users = {}
    try:
        with open('sample_account_info_encripted.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[row['account_no']] = row
        return users
    except Exception as e:
        print(f"Erro ao carregar CSV: {e}")
        return {}
# DeekSeek deitou e rolou aqui, não tenho a menor ideia do que ele fez

@app.route('/api/check-user', methods=['POST', 'OPTIONS'])
def check_user():
    if request.method == 'OPTIONS':
        return make_response(jsonify({}), 200)
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados inválidos."}), 400
        
    account_number = data.get('accountNumber')
    
    if not account_number:
        return jsonify({"error": "Número de conta é obrigatório."}), 400
    
    users = load_users()
    user = users.get(str(account_number)) # Tô convertendo pra string pra ter certeza que essa brincadeira funciona
    
    if user:
        return jsonify({"exists": True, "user": user})
    return jsonify({"exists": False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)