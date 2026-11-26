import json
from pathlib import Path

RUTA_ARCHIVO = Path(__file__).with_name("datos.json")


def buscar_agente(agentes):
    """Busca agentes por nombres o apellidos."""
    print("\n--- BUSCAR AGENTE ---")
    if not agentes:
        print("No hay agentes registrados para buscar.")
        return

    while True:
        consulta = " ".join(input("Nombres o apellidos a buscar: ").strip().lower().split())
        palabras = consulta.split()
        if not palabras:
            print("Error: escribe al menos un nombre o apellido para buscar.")
        else:
            break

    encontrados = 0
    for agente in agentes:
        nombre_completo = f"{agente['nombres']} {agente['apellidos']}".lower()
        if all(palabra in nombre_completo for palabra in palabras):
            print(
                f"Código: {agente['codigo']} | "
                f"Agente: {agente['nombres']} {agente['apellidos']} | "
                f"F. Nac.: {agente['fecha_nacimiento']} | "
                f"Edad: {agente['edad']} años"
            )
            encontrados += 1

    if encontrados == 0:
        print("No se encontraron agentes con ese criterio.")


def contar_sin_cobertura_recursivo(turnos, indice=0):
    """Función recursiva que cuenta turnos sin agente asignado."""
    if indice >= len(turnos):
        return 0
    pendiente = 1 if turnos[indice]["codigo_agente"] == "" else 0
    return pendiente + contar_sin_cobertura_recursivo(turnos, indice + 1)


def consultar_cobertura(turnos):
    """Lista los turnos sin agente asignado y muestra el total mediante recursividad."""
    print("\n--- TURNOS SIN COBERTURA ---")
    total_pendientes = contar_sin_cobertura_recursivo(turnos)

    if total_pendientes == 0:
        print("No hay turnos pendientes de cobertura.")
        return

    for turno in turnos:
        if turno["codigo_agente"] == "":
            print(
                f"Turno: {turno['codigo']} | Puesto: {turno['codigo_puesto']} | "
                f"Horario: {turno['inicio']} - {turno['fin']}"
            )
    print(f"Total de turnos pendientes de cobertura: {total_pendientes}")


def guardar_datos(datos):
    """Persiste las listas de agentes, puestos y turnos en formato JSON."""
    try:
        with open(RUTA_ARCHIVO, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
        print("Información guardada correctamente.")
        return True
    except OSError as error:
        print("No se pudo guardar la información:", error)
        return False


def cargar_datos():
    """Carga los datos desde datos.json o inicializa estructuras vacías."""
    datos_vacios = {"agentes": [], "puestos": [], "turnos": []}

    if not RUTA_ARCHIVO.exists():
        return datos_vacios

    try:
        with open(RUTA_ARCHIVO, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        if not isinstance(datos, dict):
            raise ValueError("El archivo no tiene la estructura esperada.")
        if not all(isinstance(datos.get(clave), list) for clave in datos_vacios):
            raise ValueError("Faltan listas de agentes, puestos o turnos.")
        return datos
    except (OSError, ValueError) as error:
        print("No se pudo cargar la información:", error)
        return datos_vacios
