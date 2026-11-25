def registrar_agente(agentes):
    print("\n--- REGISTRAR AGENTE ---")
    
    # PASO 1: No avanza al nombre hasta que el código sea correcto
    while True:
        codigo = input("Código del agente: ").strip().upper()
        
        if not codigo:
            print("Error: el código es obligatorio.")
        elif any(agente["codigo"] == codigo for agente in agentes):
            print("Error: ya existe un agente con ese código.")
        else:
            break  

    # PASO 2: No guarda hasta que el nombre sea correcto
    while True:
        nombre = " ".join(input("Nombre completo: ").strip().split())
        
        if not nombre:
            print("Error: el nombre es obligatorio.")
        else:
            break 

    # PASO 3: Se ejecuta solo cuando ambos campos pasaron la prueba
    agentes.append({"codigo": codigo, "nombre": nombre})
    print("Agente registrado correctamente.")

def registrar_puesto(puestos):
    print("\n--- REGISTRAR PUESTO ---")
    codigo = input("Código del puesto: ").strip().upper()
    nombre = " ".join(input("Nombre del puesto: ").strip().split())

    if not codigo or not nombre:
        print("Error: el código y el nombre son obligatorios.")
        return

    for puesto in puestos:
        if puesto["codigo"] == codigo:
            print("Error: ya existe un puesto con ese código.")
            return

    puestos.append({"codigo": codigo, "nombre": nombre})
    print("Puesto registrado correctamente.")
