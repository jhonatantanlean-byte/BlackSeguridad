from datetime import datetime, date


def generar_codigo(registros, prefijo):
    """Genera un código automático correlativo con formato PREFIJO-001."""
    mayor = 0
    for item in registros:
        codigo_actual = item.get("codigo", "")
        if "-" in codigo_actual:
            partes = codigo_actual.split("-")
            if partes[0] == prefijo and partes[1].isdigit():
                numero = int(partes[1])
                if numero > mayor:
                    mayor = numero
    return f"{prefijo}-{mayor + 1:03d}"


def calcular_edad(fecha_nacimiento_str):
    """Calcula la edad exacta en años a partir de una fecha 'DD-MM-AAAA'."""
    fecha_nac = datetime.strptime(fecha_nacimiento_str, "%d-%m-%Y").date()
    hoy = date.today()
    edad = hoy.year - fecha_nac.year
    if (hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day):
        edad -= 1
    return edad


def validar_fecha_nacimiento(fecha_texto):
    """Valida formato DD-MM-AAAA, fecha real, no futura y mayoría de edad (>= 18)."""
    try:
        fecha_nac = datetime.strptime(fecha_texto, "%d-%m-%Y").date()
    except ValueError:
        return False, "Formato inválido o fecha inexistente. Use DD-MM-AAAA (ej. 15-08-1998)."

    if fecha_nac > date.today():
        return False, "La fecha de nacimiento no puede ser futura."

    if calcular_edad(fecha_texto) < 18:
        return False, "El agente debe ser mayor de edad (18 años o más)."

    return True, "Fecha válida."


def normalizar_texto(texto):
    """Elimina espacios múltiples y convierte a formato Título."""
    return " ".join(texto.strip().split()).title()


def es_texto_alfabetico(texto):
    """Verifica que el texto tenga contenido y solo contenga letras y espacios."""
    if not texto:
        return False
    return all(palabra.isalpha() for palabra in texto.split())


def registrar_agente(agentes):
    """Registra un agente validando cada dato inmediatamente después de ingresarlo."""
    print("\n--- REGISTRAR AGENTE ---")
    codigo = generar_codigo(agentes, "AG")
    print(f"Código asignado automáticamente: {codigo}")

    while True:
        nombres = normalizar_texto(input("Nombres: "))
        if not es_texto_alfabetico(nombres):
            print("Error: ingrese nombres válidos (solo letras, campo obligatorio).")
        else:
            break

    while True:
        apellidos = normalizar_texto(input("Apellidos: "))
        if not es_texto_alfabetico(apellidos):
            print("Error: ingrese apellidos válidos (solo letras, campo obligatorio).")
        else:
            break

    while True:
        fecha_nacimiento = input("Fecha de nacimiento (DD-MM-AAAA): ").strip()
        es_valida, mensaje = validar_fecha_nacimiento(fecha_nacimiento)
        if not es_valida:
            print(f"Error: {mensaje}")
        else:
            break

    edad = calcular_edad(fecha_nacimiento)

    agentes.append({
        "codigo": codigo,
        "nombres": nombres,
        "apellidos": apellidos,
        "fecha_nacimiento": fecha_nacimiento,
        "edad": edad
    })
    print(f"Agente {nombres} {apellidos} ({edad} años) registrado con código {codigo}.")


def registrar_puesto(puestos):
    """Registra un puesto validando inmediatamente que el nombre no esté vacío ni repetido."""
    print("\n--- REGISTRAR PUESTO ---")
    codigo = generar_codigo(puestos, "PU")
    print(f"Código asignado automáticamente: {codigo}")

    while True:
        nombre = normalizar_texto(input("Nombre del puesto: "))
        if not nombre:
            print("Error: el nombre del puesto es obligatorio.")
        elif any(puesto["nombre"].lower() == nombre.lower() for puesto in puestos):
            print(f"Error: ya existe un puesto registrado con el nombre '{nombre}'.")
        else:
            break

    puestos.append({"codigo": codigo, "nombre": nombre})
    print(f"Puesto '{nombre}' registrado correctamente con código {codigo}.")