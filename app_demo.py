import os
import threading
import time

import requests as http_req
from bs4 import BeautifulSoup, Comment
from flask import Flask, Response, jsonify, render_template, request
from google import genai
from google.genai import types
from vulnerable_analysis import vulnerable_analysis
from secure_analysis import secure_analysis
app = Flask(__name__)

secure_analizer = secure_analysis()
vulnerable_analizer = vulnerable_analysis()


UTENTE = {
        "nome":            "Marco Bianchi",
        "email":           "m.bianchi@aziendademo.it",
        "ruolo":           "Responsabile IT",
        "reparto":         "Operations",
        "codice_cliente":  "CUST-4471-B",
    }
    



def get_client() -> genai.Client:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Imposta la variabile d'ambiente GEMINI_API_KEY")
    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=90_000),
    )


def fetch_page(url: str) -> str:
    resp = http_req.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    comments = "\n".join(
        str(c) for c in soup.find_all(string=lambda t: isinstance(t, Comment))
    )
    return soup.get_text(separator="\n", strip=True) + "\n" + comments



@app.route("/")
def index():
    return render_template("index.html", utente=UTENTE)


@app.route("/api/summarize", methods=["POST"])
def api_summarize():
    data = request.get_json(silent=True) or {}
    url  = data.get("url", "").strip()
    security = data.get("security", [])
    print(f"Security options: {security}")

    if security:
        return secure_analizer.api_summarize(url, security)
    else:
        return vulnerable_analizer.api_summarize(url)



if __name__ == "__main__":
    print("=" * 58)
    print("  IPI Demo Flask App")
    print("  Apri: http://localhost:5000")
    print("  Richiede local_server.py su porta 8000")
    print("=" * 58)
    app.run(debug=False, port=5000, threaded=True)