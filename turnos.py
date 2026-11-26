rom datetime import datetime
from registro import generar_codigo


def mostrar_puestos_disponibles(puestos):
    """Muestra todos los puestos registrados."""
    print("\nPuestos registrados disponibles:")
    for puesto in puestos:
        print(f"  - {puesto['codigo']}: {puesto['nombre']}")


def mostrar_turnos_por_puesto(turnos, codigo_puesto):
    """Muestra los turnos ya creados para un puesto específico."""
    turnos_puesto = [t for t in turnos if t["codigo_puesto"] == codigo_puesto]
    if turnos_puesto:
        print(f"\nTurnos actuales en el puesto {codigo_puesto}:")
        for t in turnos_puesto:
            estado = f"Agente: {t['codigo_agente']}" if t["codigo_agente"] else "Sin asignar"
            print(f"  - {t['codigo']} | Horario: {t['inicio']} - {t['fin']} ({estado})")
    else:
        print(f"\nEl puesto {codigo_puesto} aún no tiene turnos registrados.")


def mostrar_agentes_disponibles(agentes):
    """Muestra todos los agentes registrados."""
    print("\nAgentes registrados disponibles:")
    for agente in agentes:
        print(f"  - {agente['codigo']}: {agente['nombres']} {agente['apellidos']}")


def mostrar_turnos_disponibles(turnos):
    """Muestra únicamente los turnos que aún no tienen agente asignado."""
    disponibles = [t for t in turnos if t["codigo_agente"] == ""]
    print("\nTurnos disponibles (sin agente asignado):")
    if not disponibles:
        print("  (Ninguno disponible)")
    else:
        for turno in disponibles:
            print(
                f"  - {turno['codigo']} | Puesto: {turno['codigo_puesto']} | "
                f"Horario: {turno['inicio']} - {turno['fin']}"
            )
    return disponibles


def convertir_a_minutos(hora_str):
    """Valida formato HH:MM y convierte la hora a minutos desde medianoche."""
    hora_dt = datetime.strptime(hora_str, "%H:%M")
    return hora_dt.hour * 60 + hora_dt.minute


def horarios_se_cruzan(inicio1, fin1, inicio2, fin2):
    """Detecta cruce entre dos horarios HH:MM, incluyendo turnos nocturnos."""
    a1 = convertir_a_minutos(inicio1)
    a2 = convertir_a_minutos(fin1)
    if a2 <= a1:
        a2 += 1440

    b1 = convertir_a_minutos(inicio2)
    b2 = convertir_a_minutos(fin2)
    if b2 <= b1:
        b2 += 1440

    return (
        (a1 < b2 and b1 < a2)
        or (a1 + 1440 < b2 and b1 < a2 + 1440)
        or (a1 < b2 + 1440 and b1 + 1440 < a2)
    )


def crear_turno(turnos, puestos):
    """Crea un turno permitiendo que un mismo puesto tenga múltiples turnos."""
    print("\n--- CREAR TURNO ---")
    if not puestos:
        print("Error: debe registrar al menos un puesto antes de crear turnos.")
        return

    codigo = generar_codigo(turnos, "TU")
    print(f"Código de turno asignado automáticamente: {codigo}")

    mostrar_puestos_disponibles(puestos)
    while True:
        codigo_puesto = input("\nIngrese el código del puesto: ").strip().upper()
        if not codigo_puesto:
            print("Error: el código del puesto es obligatorio.")
            mostrar_puestos_disponibles(puestos)
        elif not any(puesto["codigo"] == codigo_puesto for puesto in puestos):
            print(f"Error: el código '{codigo_puesto}' no está registrado.")
            mostrar_puestos_disponibles(puestos)
        else:
            break

    mostrar_turnos_por_puesto(turnos, codigo_puesto)

    while True:
        inicio = input("\nHora de inicio (HH:MM, ej. 08:30): ").strip()
        try:
            convertir_a_minutos(inicio)
            break
        except ValueError:
            print("Error: hora de inicio inválida. Use el formato HH:MM (00:00 a 23:59).")

    while True:
        fin = input("Hora de fin (HH:MM, ej. 17:45): ").strip()
        try:
            convertir_a_minutos(fin)
        except ValueError:
            print("Error: hora de fin inválida. Use el formato HH:MM (00:00 a 23:59).")
            continue

        if fin == inicio:
            print("Error: la hora de fin no puede ser igual a la hora de inicio.")
            continue

        break

    turnos.append({
        "codigo": codigo,
        "codigo_puesto": codigo_puesto,
        "inicio": inicio,
        "fin": fin,
        "codigo_agente": ""
    })
    print(f"Turno {codigo} creado correctamente para el puesto {codigo_puesto} ({inicio} - {fin}).")


def asignar_agente(agentes, turnos):
    """Asigna un agente a un turno disponible evitando cruces horarios en el mismo agente."""
    print("\n--- ASIGNAR AGENTE ---")
    if not agentes:
        print("Error: no hay agentes registrados en el sistema.")
        return

    disponibles = mostrar_turnos_disponibles(turnos)
    if not disponibles:
        print("Error: todos los turnos registrados ya tienen un agente asignado.")
        return

    mostrar_agentes_disponibles(agentes)

    while True:
        codigo_agente = input("\nIngrese el código del agente: ").strip().upper()
        if not codigo_agente:
            print("Error: debe ingresar un código de agente.")
            mostrar_agentes_disponibles(agentes)
        elif not any(agente["codigo"] == codigo_agente for agente in agentes):
            print(f"Error: el agente '{codigo_agente}' no está registrado.")
            mostrar_agentes_disponibles(agentes)
        else:
            break

    while True:
        codigo_turno = input("\nIngrese el código del turno disponible: ").strip().upper()
        turno_elegido = None
        for turno in turnos:
            if turno["codigo"] == codigo_turno:
                turno_elegido = turno
                break

        if not codigo_turno:
            print("Error: debe ingresar un código de turno.")
            mostrar_turnos_disponibles(turnos)
        elif turno_elegido is None:
            print(f"Error: el turno '{codigo_turno}' no existe.")
            mostrar_turnos_disponibles(turnos)
        elif turno_elegido["codigo_agente"] != "":
            print(
                f"Error: el turno '{codigo_turno}' ya está registrado con el agente "
                f"{turno_elegido['codigo_agente']}."
            )
            mostrar_turnos_disponibles(turnos)
        else:
            cruce_agente = None
            for turno in turnos:
                if turno["codigo_agente"] == codigo_agente and horarios_se_cruzan(
                    turno_elegido["inicio"],
                    turno_elegido["fin"],
                    turno["inicio"],
                    turno["fin"]
                ):
                    cruce_agente = turno
                    break

            if cruce_agente is not None:
                print(
                    f"Error: el agente {codigo_agente} ya cubre el turno {cruce_agente['codigo']} "
                    f"({cruce_agente['inicio']} - {cruce_agente['fin']}) en ese horario."
                )
                mostrar_turnos_disponibles(turnos)
            else:
                break

    turno_elegido["codigo_agente"] = codigo_agente
    print(f"Agente {codigo_agente} asignado correctamente al turno {codigo_turno}.")
