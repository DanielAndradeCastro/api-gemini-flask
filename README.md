# API Flask com Gemini

API simples em Flask que recebe perguntas e responde usando a API do Gemini (Google).
Inclui um cliente para usar pelo terminal.

## Endpoints

- `GET /api/status`: mostra se a API está rodando e a data/hora do servidor.
- `POST /api/perguntar?type=gemini`: envia uma pergunta para o Gemini.

Exemplo de corpo da requisição:

```json
{"pergunta": "Explique em uma frase o que é uma API.", "model": "gemini-3.6-flash"}
```

O campo `model` é opcional.

## Como rodar

1. Clone o repositório e entre na pasta.
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Abra o `app.py` e preencha `GEMINI_API_KEY` com sua chave do Gemini
   (gerada no Google AI Studio).
5. Inicie a API:
   ```bash
   python app.py
   ```
6. Em outro terminal, use o cliente:
   ```bash
   python client.py "Explique em uma frase o que é uma API."
   ```
   Sem argumentos, ele abre um modo interativo.

## Observação

Nunca suba o arquivo `.env` para o GitHub. Ele já está no `.gitignore`.
