Para criar um ambiente virtual execute:

```bash
python3 -m venv venv
```

Se for Windows, use o seguinte comando:

```bash
venv\Scripts\activate
```

Se for Linux ou macOS, use o seguinte comando:

```bash
source venv/bin/activate
```

Depois, instale as dependências:

```bash
pip install fastapi uvicorn
```


Para correr o backend execute:

```bash
uvicorn api:app --reload
```


Para sair do ambiente virtual, use o seguinte comando:

```bash
deactivate
```