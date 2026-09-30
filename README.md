# IPI Demo - Security demo for LLM web summarization

Questa demo mostra come un assistente AI che riassume pagine web possa essere esposto a prompt injection e exfiltration di dati attraverso contenuti nascosti o istruzioni inserite nella pagina target.

## Obiettivo

Il progetto combina due casi di studio:

- un server "attaccante" che raccoglie dati exfiltrati tramite richieste GET invisibili dal browser
- un'applicazione Flask che invoca Gemini per riassumere una pagina web, con una versione vulnerabile e una versione protetta

## Struttura del progetto

- `app_demo.py`: demo di exfiltration, con endpoint `/log`, `/received`, `/clear` e pagina di controllo
- `attacker_server_demo.py`: app principale con interfaccia web per analizzare un URL
- `vulnerable_analysis.py`: recupera il contenuto della pagina senza filtrare hidden text o prompt injection
- `secure_analysis.py`: applica rimozione degli elementi nascosti, sanitizzazione e prompt strengthening
- `templates/`: template HTML per il frontend della demo
- `static/`: CSS dedicato delle pagine

## Come eseguire

1. Entra nella cartella del progetto:

```bash
cd /home/ab/Documenti/uni/cyber/prog/ipi_project/ipi_project/application_demo
```

2. (Opzionale ma consigliato) crea e attiva un ambiente virtuale:

```bash
python3 -m venv Poc_Env
source Poc_Env/bin/activate
```

3. Installa le dipendenze:

```bash
pip install flask requests beautifulsoup4 google-genai
```

4. Imposta la chiave API Gemini:

```bash
export GEMINI_API_KEY="la-tua-api-key"
```

5. Avvia il server di exfiltration:

```bash
python app_demo.py
```

6. In un secondo terminale, avvia l'applicazione di demo:

```bash
python attacker_server_demo.py
```

## URL utili

- `http://localhost:9000` -> dashboard di controllo e server di exfiltration
- `http://localhost:9000/poc` -> pagina "malicious" usata per dimostrare il caso di exfiltration
- `http://localhost:5000` -> interfaccia principale per testare la demo sul riassunto di pagine

## Modalità demo

Nella pagina principale dell'app (`http://localhost:5000`):

- lascia il checkbox "Attiva sicurezza" disattivato per usare la versione vulnerabile
- attivalo per usare `secure_analysis.py`, che elimina testo nascosto, rimuove pattern di injection e rafforza il system prompt


## Requisiti

- Python 3.10+
- Flask
- requests
- BeautifulSoup4
- Google GenAI SDK
