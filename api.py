from fastapi import FastAPI
from fastapi.responses import FileResponse  
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

app = FastAPI()

# Servir arquivos estáticos (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Servir o arquivo index.html na raiz
@app.get("/")
def read_root():
    return FileResponse(os.path.join("static", "index.html"))

# Modelo para definir o input esperado do frontend
class InputData(BaseModel):
    text: str

# Função que processa a string e devolve um JSON
def processar_string(texto: str):
    #TODO chamar a função "chatbot" que recebe o texto e devolve um JSON
    return {"processed": texto.upper()}  # Exemplo simples

# Função que transforma o JSON numa string
def json_para_string(dados: dict):
    return f"Resultado: {dados['processed']}"

# Endpoint da API
@app.post("/process")
def processar(input_data: InputData):
    json_resultado = processar_string(input_data.text)
    resposta = json_para_string(json_resultado)
    return {"response": resposta}