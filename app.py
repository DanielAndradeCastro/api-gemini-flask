import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from google import genai
from google.genai import errors

load_dotenv()

GEMINI_API_KEY = ""
if not GEMINI_API_KEY:
    raise RuntimeError("Coloque sua GEMINI_API_KEY na variável GEMINI_API_KEY em app.py")

MODELO_PADRAO = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
MODELO_RESERVA = os.environ.get("GEMINI_MODEL_RESERVA", "gemini-2.5-flash")

app = Flask(__name__)
cliente_gemini = genai.Client(api_key=GEMINI_API_KEY)


@app.route("/api/status", methods=["GET"])
def status_servidor():
    dados = {
        "status": "API rodando",
        "data-hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }
    return jsonify(dados), 200


@app.route("/api/perguntar", methods=["POST"])
def perguntar_para_ia():
    tipo_ia = request.args.get("type", "gemini")

    corpo_requisicao = request.get_json(silent=True)

    if not corpo_requisicao or "pergunta" not in corpo_requisicao:
        return jsonify({"Erro": "Você precisa passar uma chave pergunta"}), 400

    pergunta = corpo_requisicao["pergunta"]

    if tipo_ia != "gemini":
        return jsonify({"Erro": "Você precisa escolher gemini"}), 400

    modelo = corpo_requisicao.get("model", MODELO_PADRAO)
    modelos_para_tentar = [modelo]
    if MODELO_RESERVA != modelo:
        modelos_para_tentar.append(MODELO_RESERVA)

    resultado = None
    modelo_usado = None
    ultimo_erro = None

    for m in modelos_para_tentar:
        try:
            resultado = cliente_gemini.models.generate_content(model=m, contents=pergunta)
            modelo_usado = m
            break
        except errors.ServerError as e:
            ultimo_erro = e  # 5xx (ex.: 503): tenta o próximo modelo
        except Exception as e:
            return jsonify({"Erro": f"Falha ao chamar o Gemini: {e}"}), 502

    if resultado is None:
        return jsonify({"Erro": f"Gemini indisponível no momento: {ultimo_erro}"}), 503

    return jsonify({
        "tipo_ia": tipo_ia,
        "pergunta": pergunta,
        "model": modelo_usado,
        "resposta": resultado.text,
    }), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)