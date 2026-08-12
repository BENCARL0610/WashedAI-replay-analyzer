import subprocess
import tempfile
import os
import json


RRROCKET = os.environ.get(
    "RRROCKET_PATH",
    "./rrrocket"
)


def analizar_replay(ruta_replay):

    carpeta = os.path.dirname(ruta_replay)

    try:

        resultado = subprocess.run(
            [
                RRROCKET,
                ruta_replay
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        if resultado.returncode != 0:

            return {
                "ok": False,
                "error": (
                    resultado.stderr
                    or "rrrocket produjo un error."
                )
            }


        ruta_json = os.path.splitext(
            ruta_replay
        )[0] + ".json"


        if not os.path.exists(ruta_json):

            return {
                "ok": False,
                "error": (
                    "rrrocket terminó correctamente, "
                    "pero no creó el archivo JSON."
                )
            }


        with open(
            ruta_json,
            "r",
            encoding="utf-8"
        ) as archivo:

            datos = json.load(
                archivo
            )


        return {
            "ok": True,
            "data": datos
        }


    except Exception as e:

        return {
            "ok": False,
            "error": str(e)
        }


    finally:

        if 'ruta_json' in locals():

            try:

                if os.path.exists(ruta_json):
                    os.remove(ruta_json)

            except Exception:
                pass
