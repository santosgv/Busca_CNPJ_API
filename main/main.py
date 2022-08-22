from fastapi import fastapi

app= fastapi()

@app.get("/")
def root():
    return {'mensagem':'teste'}