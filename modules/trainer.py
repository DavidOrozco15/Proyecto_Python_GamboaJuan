from modules.utils import cargar, guardar, pedirEntero, pedirFloat, limpiar, pausar

def listarCampersAsignados(IDtrainer):
    limpiar()
    ruta = "data/rutas.json"
    rutaRutas = cargar(ruta)
    ruta = "data/campers.json"
    campers = cargar(ruta)
    
    encontrado = False
    
    for nombreRuta, infoRuta in rutaRutas.items():
        if infoRuta.get("trainerEncargado") == IDtrainer:
            encontrado = True
            print(f"\n📖 Ruta: {nombreRuta}")
            campersAsignados = infoRuta.get("campersAsignados", [])
            
            if not campersAsignados:
                print("No hay campers Asignados aun")
                pausar()
            else:
                for IDcamper in campersAsignados:
                    info = campers.get(IDcamper, {})
                    print(f"\n👤 ID: {IDcamper} | Nombres: {info.get('nombres','')} | Apellidos: {info.get('apellidos','')} | Estado: {info.get('estado','')} ")
    if not encontrado:
        print("\nNo tienes rutas asignadas Actualmente")
        pausar()
    
    pausar()
        
def registrarNotasTrainer(IDtrainer):
    limpiar()
    rutaRutas = "data/rutas.json"
    rutaCampers = "data/campers.json"

    rutas = cargar(rutaRutas)
    campers = cargar(rutaCampers)

    print("----REGISTRAR NOTAS DE LOS MODULOS----")
    # Buscar la ruta asignada al trainer
    rutaAsignada = None
    for nombreRuta, infoRuta in rutas.items():
        if infoRuta.get("trainerEncargado") == IDtrainer:
            rutaAsignada = nombreRuta
            break

    if not rutaAsignada:
        print("❌ No tienes ninguna ruta asignada actualmente.")
        pausar()
        return

    print(f"\n📚 Ruta asignada: {rutaAsignada}")
    matriculas = rutas[rutaAsignada].get("matriculas", {})

    if not matriculas:
        print("⚠️ No hay campers matriculados en esta ruta todavía.")
        pausar()
        return

    # Mostrar campers asignados
    print("\n---- CAMPERS DISPONIBLES ----")
    for i, (IDcamper, infoMatricula) in enumerate(matriculas.items(), start=1):
        camperInfo = campers.get(IDcamper, {})
        print(f"{i}. 👤 {IDcamper} | {camperInfo.get('nombres','')} {camperInfo.get('apellidos','')}")

    # Seleccionar camper
    opcion = pedirEntero("Seleccione un camper: ")
    IDcamperSeleccionado = list(matriculas.keys())[opcion - 1]

    # Seleccionar módulo
    modulos = matriculas[IDcamperSeleccionado].get("modulos", {})
    modulosDisponibles = {k: v for k, v in modulos.items() if k != "Nota Inicial"}
    if not modulosDisponibles:
        print("⚠️ Este camper no tiene módulos disponibles para calificar.")
        pausar()
        return

    print("\n---- MÓDULOS DISPONIBLES ----")
    for i, modulo in enumerate(modulosDisponibles.keys(), start=1):
        print(f"{i}. {modulo}")

    opcionModulo = pedirEntero("Seleccione un módulo: ")
    nombreModulo = list(modulosDisponibles.keys())[opcionModulo - 1]

    # Ingresar notas
    notaT = pedirFloat("Ingrese nota teórica (0-100): ")
    notaP = pedirFloat("Ingrese nota práctica (0-100): ")
    notaQ = pedirFloat("Ingrese nota quiz (0-100): ")

    promedio = notaT * 0.3 + notaP * 0.6 + notaQ * 0.1

    # Guardar notas en rutas.json
    rutas[rutaAsignada]["matriculas"][IDcamperSeleccionado]["modulos"][nombreModulo] = {
        "teorica": notaT,
        "practica": notaP,
        "quiz": notaQ,
        "promedio": promedio
    }

    # Actualizar riesgo en campers.json
    if promedio < 60:
        campers[IDcamperSeleccionado]["riesgo"] = "alto"
    else:
        campers[IDcamperSeleccionado]["riesgo"] = "bajo"

    guardar(rutaRutas, rutas)
    guardar(rutaCampers, campers)

    print(f"✅ Notas registradas para {campers[IDcamperSeleccionado]['nombres']} en {nombreModulo}.")
    print(f"📊 Promedio: {promedio:.2f} | Riesgo actualizado: {campers[IDcamperSeleccionado]['riesgo']}")
    pausar()
    
def consultarNotasCampers(IDtrainer):
    limpiar()
    rutaRutas = "data/rutas.json"
    rutaCampers = "data/campers.json"

    rutas = cargar(rutaRutas)
    campers = cargar(rutaCampers)
    print("----CONSULTAR NOTAS----")
    # Buscar la ruta asignada al trainer
    rutaAsignada = None
    for nombreRuta, infoRuta in rutas.items():
        if infoRuta.get("trainerEncargado") == IDtrainer:
            rutaAsignada = nombreRuta
            break

    if not rutaAsignada:
        print("❌ No tienes ninguna ruta asignada actualmente.")
        pausar()
        return

    print(f"\n📚 Ruta asignada: {rutaAsignada}")
    matriculas = rutas[rutaAsignada].get("matriculas", {})

    if not matriculas:
        print("⚠️ No hay campers matriculados en esta ruta todavía.")
        pausar()
        return

    print("\n---- NOTAS DE CAMPERS ----")
    for IDcamper, infoMatricula in matriculas.items():
        camperInfo = campers.get(IDcamper, {})
        nombreCamper = f"{camperInfo.get('nombres','')} {camperInfo.get('apellidos','')}"
        print(f"\n👤 Camper: {nombreCamper} (ID: {IDcamper})")

        modulos = infoMatricula.get("modulos", {})
        if not modulos:
            print("   ⚠️ Este camper no tiene notas registradas aún.")
            pausar()
            continue

        for nombreModulo, notas in modulos.items():
            teorica = notas.get("teorica", "No registrada")
            practica = notas.get("practica", "No registrada")
            quiz = notas.get("quiz", "No registrada")
            promedio = notas.get("promedio", "No calculado")
            
            print(f"   📘 Módulo: {nombreModulo}")
            print(f"      - Teórica: {teorica}")
            print(f"      - Práctica: {practica}")
            print(f"      - Quiz: {quiz}")
            print(f"      - Promedio: {promedio}")
    print("\n✅ Consulta finalizada.")
    pausar()

def generarReporteCampers(IDtrainer):
    limpiar()
    rutaRutas = "data/rutas.json"
    rutaCampers = "data/campers.json"
    
    rutas = cargar(rutaRutas)
    campers = cargar(rutaCampers)
    
    encontrado = False
    
    for nombreRuta, infoRuta in rutas.items():
        if infoRuta.get("trainerEncargado") == IDtrainer:
            encontrado = True
            print(f"\n📊 Reporte de la Ruta: {nombreRuta}")
            print("-"*50)
            
            campersAsignados = infoRuta.get("campersAsignados", [])
            
            if not campersAsignados:
                print("⚠ No hay campers asignados todavía.")
                pausar()
            else:
                for IDcamper in campersAsignados:
                    info = campers.get(IDcamper, {})
                    infoMatricula = infoRuta.get("matriculas", {}).get(IDcamper, {})
                    modulos = infoMatricula.get("modulos", {})

                    print(f"\n🧑 ID: {IDcamper}")
                    print(f"   Nombres : {info.get('nombres','')}")
                    print(f"   Apellidos : {info.get('apellidos','')}")
                    print(f"   Estado : {info.get('estado','')}")
                    print(f"   Riesgo : {info.get('riesgo','')}")
            
                    if modulos:
                        print("   📑 Notas:")
                        for modulo, notas in modulos.items():
                            print(f"\n    📚  {modulo}:")
                            print(f"         Teórica: {notas.get('teorica', 'No registrada')}")
                            print(f"         Práctica: {notas.get('practica', 'No registrada')}")
                            print(f"         Quiz: {notas.get('quiz', 'No registrada')}")
                            print(f"         Promedio: {notas.get('promedio', 'No calculado')}")
                        
                    else:
                        print("   📘 Notas: Sin registrar")
                    
                    print("-"*50)
            pausar()
    if not encontrado:
        print("❌ No tienes rutas asignadas actualmente.")
        pausar()
        
