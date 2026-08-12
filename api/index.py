from flask import Flask, request, jsonify
import subprocess
import tempfile
import os
import json

app = Flask(__name__)

RRROCKET = os.environ.get("RRROCKET_PATH", "./rrrocket")


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        return analyze()

    return jsonify({
        "ok": True,
        "service": "Washed AI Replay Analyzer",
        "status": "online"
    })


@app.route("/analyze", methods=["POST"])
def analyze():

    if "replay" not in request.files:
        return jsonify({
            "ok": False,
            "error": "No se recibió ninguna replay."
        }), 400

    replay = request.files["replay"]

    if not replay.filename:
        return jsonify({
            "ok": False,
            "error": "La replay no tiene nombre."
        }), 400

    if not replay.filename.lower().endswith(".replay"):
        return jsonify({
            "ok": False,
            "error": "El archivo debe ser .replay."
        }), 400

    temp_path = None
    json_path = None

    try:

        with tempfile.NamedTemporaryFile(
            suffix=".replay",
            delete=False
        ) as temp:

            replay.save(temp.name)
            temp_path = temp.name

       resultado = subprocess.run(
    [
        RRROCKET,
        temp_path
    ],
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace"
)

if resultado.returncode != 0:
    return jsonify({
        "ok": False,
        "error": resultado.stderr
        or "rrrocket produjo un error."
    }), 500

try:
    datos = json.loads(
        resultado.stdout
    )

except json.JSONDecodeError:

    return jsonify({
        "ok": False,
        "error": "rrrocket no devolvió JSON válido.",
        "stdout": resultado.stdout[:2000],
        "stderr": resultado.stderr[:2000]
    }), 500

return jsonify({
    "ok": True,
    "data": datos
})

    except Exception as e:

        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

    finally:

        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

        if json_path and os.path.exists(json_path):
            try:
                os.remove(json_path)
            except Exception:
                pass
