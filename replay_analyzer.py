import json
import subprocess
import os


RRROCKET = os.environ.get("RRROCKET_PATH", "rrrocket")


def analizar_replay(ruta_replay):
    try:
        resultado = subprocess.run(
            [RRROCKET, ruta_replay],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        if resultado.returncode != 0:
            return {
                "ok": False,
                "error": resultado.stderr or "rrrocket produjo un error."
            }

        try:
            datos = json.loads(resultado.stdout)
        except json.JSONDecodeError:
            return {
                "ok": False,
                "error": "rrrocket no devolvió JSON válido."
            }

        return {
            "ok": True,
            "data": datos
        }

    except FileNotFoundError:
        return {
            "ok": False,
            "error": "No se encontró rrrocket en el servidor."
        }

    except Exception as e:
        return {
            "ok": False,
            "error": str(e)
        }
