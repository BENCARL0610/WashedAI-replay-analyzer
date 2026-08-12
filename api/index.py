from flask import Flask, request, jsonify
import subprocess
import tempfile
import os
import json

app = Flask(__name__)

RRROCKET = os.environ.get(
    "RRROCKET_PATH",
    "./rrrocket"
)


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

    try:

        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(
            suffix=".replay",
            delete=False
        ) as temp:

            replay.save(temp.name)
            temp_path = temp.name

        # Ejecutar rrrocket
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

        # Comprobar error de rrrocket
        if resultado.returncode != 0:

            return jsonify({
                "ok": False,
                "error": (
                    resultado.stderr
                    or "rrrocket produjo un error."
                ),
                "stdout": resultado.stdout[:2000]
            }), 500

        # Intentar interpretar el resultado como JSON
        try:

            datos = json.loads(
                resultado.stdout
            )

        except json.JSONDecodeError:

            return jsonify({
                "ok": False,
                "error": "rrrocket no devolvió JSON válido.",
                "stdout": resultado.stdout[:5000],
                "stderr": resultado.stderr[:5000]
            }), 500

        # Respuesta correcta
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

        if temp_path:

            try:

                if os.path.exists(temp_path):
                    os.remove(temp_path)

            except Exception:
                pass


if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
