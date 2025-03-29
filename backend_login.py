from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["login.html"],  # Em produção, troque pelo domínio do seu frontend
    allow_methods=["POST"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    accountNumber: str

class LoginResponse(BaseModel):
    exists: bool
    user: Optional[dict] = None

def get_db():
    conn = sqlite3.connect('baseDeDados.db')
    conn.row_factory = sqlite3.Row  # Retorna dicionários
    return conn

# Rota principal
@app.post("/api/check-user", response_model=LoginResponse)
async def check_user(request: LoginRequest):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM usuarios WHERE account_no = ?", 
            (request.accountNumber,)
        )
        user = cursor.fetchone()
        
        if user:
            return {
                "exists": True,
                "user": dict(user)
            }
        return {"exists": False}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro no servidor: {str(e)}"
        )
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)