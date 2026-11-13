import sys

import requests

BASE_URL = "http://127.0.0.1:5001"


def checar_status():
    resposta = requests.get(f"{BASE_URL}/api/status")
    print(resposta.status_code, resposta.json())


def perguntar(pergunta, modelo=None):
    corpo = {"pergunta": pergunta}
    if modelo:
        corpo["model"] = modelo

    resposta = requests.post(f"{BASE_URL}/api/perguntar?type=gemini", json=corpo)
    dados = resposta.json()

    if resposta.status_code != 200:
        print("Erro:", dados)
        return

    print(dados["resposta"].strip())


if __name__ == "__main__":
    if len(sys.argv) > 1:
        perguntar(" ".join(sys.argv[1:]))
    else:
        checar_status()
        while True:
            pergunta = input("\nPergunta (ou 'sair'): ").strip()
            if pergunta.lower() == "sair":
                break
            if pergunta:
                perguntar(pergunta)
