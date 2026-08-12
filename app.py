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


@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "ok": True,
        "service": "Washed AI Replay Analyzer",
        "status": "online"
    })


@app.route("/test-rrrocket", methods=["GET"])
def test_rrrocket():

    try:

        resultado = subprocess.run(
            [RRROCKET, "--help"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        return jsonify({
            "ok": resultado.returncode == 0,
            "returncode": resultado.returncode,
            "stdout": resultado.stdout[:2000],
            "stderr": resultado.stderr[:2000]
        })

    except Exception as e:

        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500


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

        # =====================================================
        # GUARDAR REPLAY TEMPORAL
        # =====================================================

        with tempfile.NamedTemporaryFile(
            suffix=".replay",
            delete=False
        ) as temp:

            replay.save(temp.name)

            temp_path = temp.name


        # =====================================================
        # EJECUTAR RRROCKET
        # =====================================================

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
                "error":
                    resultado.stderr
                    or "rrrocket produjo un error."
            }), 500


        # =====================================================
        # RRROCKET CREA UN JSON AL LADO DE LA REPLAY
        # =====================================================

        json_path = os.path.splitext(
            temp_path
        )[0] + ".json"


        if not os.path.exists(json_path):

            return jsonify({
                "ok": False,
                "error":
                    "rrrocket terminó correctamente, "
                    "pero no creó el archivo JSON."
            }), 500


        # =====================================================
        # LEER JSON
        # =====================================================

        with open(
            json_path,
            "r",
            encoding="utf-8"
        ) as archivo:

            datos = json.load(
                archivo
            )


        # =====================================================
        # RESPUESTA
        # =====================================================

        return jsonify({
            "ok": True,
            "data": datos
        })


    except json.JSONDecodeError:

        return jsonify({
            "ok": False,
            "error": "El JSON generado por rrrocket no es válido."
        }), 500


    except Exception as e:

        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500


    finally:

        # =====================================================
        # BORRAR ARCHIVOS TEMPORALES
        # =====================================================

        if temp_path:

            try:

                if os.path.exists(temp_path):

                    os.remove(temp_path)

            except Exception:

                pass


        if json_path:

            try:

                if os.path.exists(json_path):

                    os.remove(json_path)

            except Exception:

                pass


# =========================================================
# EJECUCIÓN
# =========================================================

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
