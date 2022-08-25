from fastapi import FastAPI
from decouple import config
import requests
from fastapi.middleware.cors import CORSMiddleware

app= FastAPI()

origins = [
    "*",
    "https://meicerto.com.br/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/")
def ROOT():
    return {'mensagem':'home'}


@app.get("/{cnpj}")
def CNPJ(cnpj:int):
    cnpj = cnpj
    url = 'https://api.infosimples.com/api/v2/consultas/receita-federal/simples-dasn'
    args = {
    "cnpj":    cnpj,
    "token":  config('token'),
    "timeout": 300
    }

    response = requests.post(url, args)
    response_json = response.json()
    response.close()

    if response_json['code'] == 200:
        print("Retorno com sucesso: ", response_json['data'])
        dados = response_json['data']

        cnpj = dados[0]['cnpj']
        razao_social = dados[0]['razao_social']
        anos =dados[0]['original']

        return {'cnpj':cnpj,
                'razao_social':razao_social,
                'ano':anos
                }
            
        


    elif response_json['code'] in range(600, 799):
        mensagem = "Resultado sem sucesso. Leia para saber mais: \n"
        mensagem += "Código: {} ({})\n".format(response_json['code'], response_json['code_message'])
        mensagem += "; ".join(response_json['errors'])
        print(mensagem)

    print("Cabeçalho da consulta: ", response_json['header'])
    print("URLs com comprovantes (HTML/PDF): ", response_json['site_receipts'])

    return {'mensagem':mensagem}
