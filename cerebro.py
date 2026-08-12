
import requests
import json
import os


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODELO = "qwen2.5:7b"
REPLAY_FILE = "replay.json"


# ============================================================
# CARGAR REPLAY
# ============================================================

def cargar_replay():

    if not os.path.exists(REPLAY_FILE):
        print("❌ No se encontró replay.json")
        return None

    try:
        with open(REPLAY_FILE, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    except Exception as e:
        print("❌ Error leyendo replay.json:")
        print(e)
        return None


# ============================================================
# INSPECCIÓN DEL REPLAY
# ============================================================

def inspeccionar_replay(replay):

    print("🎮 WAShed AI - INSPECCIÓN PROFUNDA")
    print("================================")
    print()

    nombres = replay.get("names", [])
    objetos = replay.get("objects", [])
    net_cache = replay.get("net_cache", [])

    print("📦 Objetos:", len(objetos))
    print("🏷️ Nombres:", len(nombres))
    print("🧠 Net Cache:", len(net_cache))
    print()

    print("🔎 PROPIEDADES DEL NET CACHE")
    print()

    for i, entrada in enumerate(net_cache):

        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"Entrada #{i}")
        print(f"object_ind: {entrada.get('object_ind')}")
        print(f"parent_id: {entrada.get('parent_id')}")
        print(f"cache_id: {entrada.get('cache_id')}")

        propiedades = entrada.get("properties", [])

        print(f"propiedades: {len(propiedades)}")

        for propiedad in propiedades[:10]:

            object_ind = propiedad.get("object_ind")
            stream_id = propiedad.get("stream_id")

            nombre = "DESCONOCIDO"

            if (
                isinstance(object_ind, int)
                and 0 <= object_ind < len(objetos)
            ):
                nombre = str(objetos[object_ind])

            print(
                f"   object #{object_ind} "
                f"| stream {stream_id} "
                f"| {nombre}"
            )

    print()
    print("✅ Inspección terminada.")


# ============================================================
# BUSCAR PROPIEDADES IMPORTANTES
# ============================================================

def buscar_propiedades_importantes(replay):

    importantes = [
        "RelativeLocation",
        "RelativeRotation",
        "Velocity",
        "CurrentBoostAmount",
        "ReplicatedBoostAmount",
        "ReplicatedThrottle",
        "ReplicatedSteer",
        "bDriving",
        "AirActivateCount",
        "DoubleJumpImpulse",
        "DodgeTorque",
        "PlayerReplicationInfo",
        "UniqueId",
        "AnonymizedName"
    ]

    print("\n🔎 PROPIEDADES IMPORTANTES ENCONTRADAS")
    print("=" * 50)

    encontrados = set()

    objetos = replay.get("objects", [])

    for entrada in replay.get("net_cache", []):

        for propiedad in entrada.get("properties", []):

            objeto_id = propiedad.get("object_ind")

            if not isinstance(objeto_id, int):
                continue

            if 0 <= objeto_id < len(objetos):

                nombre = objetos[objeto_id]

                for importante in importantes:

                    if importante.lower() in str(nombre).lower():
                        encontrados.add(str(nombre))

    for nombre in sorted(encontrados):
        print("✅", nombre)

    print("\nTotal:", len(encontrados))


# ============================================================
# INSPECCIÓN DE OBJETOS DE MOVIMIENTO
# ============================================================

def inspeccionar_objetos_movimiento(replay):

    print("\n🔬 INSPECCIÓN DE OBJETOS DE MOVIMIENTO")
    print("=" * 60)

    objetos = replay.get("objects", [])

    propiedades_interesantes = [
        "RelativeLocation",
        "RelativeRotation",
        "Velocity",
        "CurrentBoostAmount",
        "ReplicatedBoostAmount",
        "ReplicatedThrottle",
        "ReplicatedSteer",
        "PlayerReplicationInfo"
    ]

    encontrados = 0

    for i, objeto in enumerate(objetos):

        texto = str(objeto)

        if any(
            prop.lower() in texto.lower()
            for prop in propiedades_interesantes
        ):

            print(f"\nOBJETO #{i}")
            print("Tipo:", type(objeto).__name__)
            print("Valor:", objeto)

            encontrados += 1

            if encontrados >= 30:
                break

    print("\nTotal inspeccionados:", encontrados)


# ============================================================
# INSPECCIÓN DE ESTRUCTURA PROFUNDA
# ============================================================

def inspeccionar_estructura_profunda(replay):

    print("\n🧬 INSPECCIÓN DE ESTRUCTURA PROFUNDA")
    print("=" * 60)

    # --------------------------------------------------------
    # ESTRUCTURAS PRINCIPALES
    # --------------------------------------------------------

    for nombre in [
        "levels",
        "keyframes",
        "tick_marks",
        "packages"
    ]:

        datos = replay.get(nombre)

        print(f"\n📦 {nombre}")

        if datos is None:
            print("No existe en el replay")
            continue

        print("Tipo:", type(datos).__name__)

        if isinstance(datos, list):

            print("Cantidad:", len(datos))

            if len(datos) > 0:

                print("Primer elemento:")
                print(repr(datos[0])[:2000])

        else:

            print("Valor:")
            print(repr(datos)[:2000])

    # --------------------------------------------------------
    # OBJECTS
    # --------------------------------------------------------

    print("\n📦 OBJECTS")

    objetos = replay.get("objects", [])

    print("Cantidad:", len(objetos))

    for i in range(min(10, len(objetos))):

        print(f"\nObjeto {i}:")
        print("Tipo:", type(objetos[i]).__name__)
        print("Valor:", repr(objetos[i])[:1000])

    # --------------------------------------------------------
    # NET CACHE
    # --------------------------------------------------------

    print("\n🧠 NET CACHE")

    cache = replay.get("net_cache", [])

    print("Cantidad:", len(cache))

    for i in range(min(3, len(cache))):

        print(f"\nEntrada {i}:")
        print(repr(cache[i])[:3000])


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================


def inspeccionar_datos_temporales(replay):

    print("\n⏱️ INSPECCIÓN DE DATOS TEMPORALES")
    print("=" * 60)

    keyframes = replay.get("keyframes", [])
    tick_marks = replay.get("tick_marks", [])

    print("\n🎞️ KEYFRAMES")
    print("Cantidad:", len(keyframes))

    if keyframes:
        print("\nPrimeros keyframes:")

        for i, keyframe in enumerate(keyframes[:10]):
            print(f"\nKeyframe #{i}")
            print("Tiempo:", keyframe.get("time"))
            print("Frame:", keyframe.get("frame"))
            print("Posición:", keyframe.get("position"))

    print("\n🏷️ TICK MARKS")
    print("Cantidad:", len(tick_marks))

    for i, tick in enumerate(tick_marks):

        print(f"\nEvento #{i}")
        print("Descripción:", tick.get("description"))
        print("Frame:", tick.get("frame"))

    print("\n🔍 TODOS LOS CAMPOS DEL REPLAY")

    for clave, valor in replay.items():

        if isinstance(valor, list):
            print(
                f"📦 {clave}: lista con {len(valor)} elementos"
            )

        elif isinstance(valor, dict):
            print(
                f"🧠 {clave}: diccionario con {len(valor)} campos"
            )

        else:
            print(
                f"📄 {clave}: {type(valor).__name__} = {valor}"
            )

    print("\n✅ Inspección temporal terminada.")

def inspeccionar_contenido_replay(replay):

    print("\n🔬 INSPECCIÓN DEL CONTENIDO DEL REPLAY")
    print("=" * 60)

    print("\n📦 TIPOS DE DATOS DISPONIBLES")

    for clave, valor in replay.items():

        print(f"\n🔹 {clave}")
        print("   Tipo:", type(valor).__name__)

        if isinstance(valor, bytes):
            print("   Bytes:", len(valor))
            print("   Primeros 32 bytes:", valor[:32].hex())

        elif isinstance(valor, bytearray):
            print("   Bytes:", len(valor))
            print("   Primeros 32 bytes:", bytes(valor[:32]).hex())

        elif isinstance(valor, list):
            print("   Elementos:", len(valor))

            if valor:
                print(
                    "   Tipo primer elemento:",
                    type(valor[0]).__name__
                )

        elif isinstance(valor, dict):
            print("   Campos:", len(valor))

    print("\n🔍 BUSCANDO DATOS BINARIOS")

    encontrados = 0

    def buscar_binarios(obj, ruta="replay"):

        nonlocal encontrados

        if isinstance(obj, (bytes, bytearray)):

            encontrados += 1

            print(
                f"\n💾 DATOS BINARIOS EN: {ruta}"
            )

            print(
                "   Tamaño:",
                len(obj),
                "bytes"
            )

            print(
                "   HEX:",
                bytes(obj[:64]).hex()
            )

        elif isinstance(obj, dict):

            for clave, valor in obj.items():

                buscar_binarios(
                    valor,
                    f"{ruta}.{clave}"
                )

        elif isinstance(obj, list):

            for i, valor in enumerate(obj):

                buscar_binarios(
                    valor,
                    f"{ruta}[{i}]"
                )

    buscar_binarios(replay)

    print("\n📊 RESULTADO")

    print(
        "Bloques binarios encontrados:",
        encontrados
    )

    if encontrados == 0:

        print(
            "\n⚠️ No se encontraron bytes "
            "dentro de la estructura actual."
        )

    print("\n✅ Inspección de contenido terminada.")

if __name__ == "__main__":

    print("🧠 Washed AI")
    print("💻 IA local:", MODELO)
    print("🎮 Analizador de Rocket League")
    print()

    replay = cargar_replay()

    if replay:

        inspeccionar_replay(replay)

        buscar_propiedades_importantes(replay)

        inspeccionar_objetos_movimiento(replay)

        inspeccionar_estructura_profunda(replay)

        inspeccionar_datos_temporales(replay)

        inspeccionar_contenido_replay(replay)

        print()
        print("================================")
        print("✅ ANÁLISIS COMPLETO TERMINADO")
        print("================================")

    def inspeccionar(nombre, datos, nivel=0):

        indent = "  " * nivel

        if nivel > 3:
            return

        if isinstance(datos, dict):

            for clave, valor in list(datos.items())[:20]:

                if isinstance(valor, (int, float)):
                    print(
                        f"{indent}📊 {nombre}.{clave} = {valor}"
                    )

                elif isinstance(valor, (list, dict)):
                    inspeccionar(
                        f"{nombre}.{clave}",
                        valor,
                        nivel + 1
                    )

        elif isinstance(datos, list):

            print(
                f"{indent}📦 {nombre} -> "
                f"lista de {len(datos)} elementos"
            )

            for i, elemento in enumerate(datos[:3]):

                if isinstance(elemento, (dict, list)):
                    inspeccionar(
                        f"{nombre}[{i}]",
                        elemento,
                        nivel + 1
                    )

                elif isinstance(elemento, (int, float)):
                    print(
                        f"{indent}  🔢 [{i}] = {elemento}"
                    )

    for clave, valor in replay.items():

        if isinstance(valor, (list, dict)):

            print(f"\n🔎 ANALIZANDO: {clave}")

            inspeccionar(
                clave,
                valor
            )

    print("\n" + "=" * 60)
    print("✅ INSPECCIÓN TEMPORAL TERMINADA")
    print("=" * 60)