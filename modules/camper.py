from modules.utils import cargar, limpiar, pausar, validadorCamperNoExiste

def consultarInfoCamper(IDcamper):
    limpiar()
    ruta = "data/campers.json"
    campers = cargar(ruta)

    validadorCamperNoExiste(IDcamper, campers)

    info = campers[IDcamper]
    print("Información Personal del Camper:")
    print(f"\nID: {IDcamper}")
    print(f"Nombres: {info.get('nombres', '')}")
    print(f"Apellidos: {info.get('apellidos', '')}")
    print(f"Estado: {info.get('estado', '')}")
    print(f"Riesgo: {info.get('riesgo', '')}")
    print(f"Ruta asignada: {info.get('ruta', 'No asignada')}")
    pausar()
    
def consultarNotasCamper(IDcamper):
    limpiar()
    rutaCampers = "data/campers.json"
    campers = cargar(rutaCampers)
    rutaRutas = "data/rutas.json"
    rutas = cargar(rutaRutas)

    camperInfo = campers.get(IDcamper, {})
    if not camperInfo:
        print("❌ Camper no encontrado.")
        pausar()
        return

    ruta_asignada = camperInfo.get("ruta")
    if not ruta_asignada or ruta_asignada not in rutas:
        print("❌ No tienes ruta asignada o notas registradas.")
        pausar()
        return

    matricula = rutas[ruta_asignada].get("matriculas", {}).get(IDcamper, {})
    modulos = matricula.get("modulos", {})

    if not modulos:
        print("❌ No tienes notas registradas aún.")
        pausar()
        return

    print(f"\n📊 Notas de {camperInfo.get('nombres','')} {camperInfo.get('apellidos','')}:")
    for mod_name, notas in modulos.items():
        teorica = notas.get("teorica", "No registrada")
        practica = notas.get("practica", "No registrada")
        quiz = notas.get("quiz", "No registrada")
        promedio = notas.get("promedio", "No calculado")
        print(f"\nMódulo: {mod_name}")
        print(f"   - Teórica: {teorica}")
        print(f"   - Práctica: {practica}")
        print(f"   - Quiz: {quiz}")
        print(f"   - Promedio: {promedio}")
    pausar()
    
def consultarRutaCamper(IDcamper):
    limpiar()
    rutaRutas = "data/rutas.json"
    rutas = cargar(rutaRutas)

    rutaTrainers = "data/trainers.json"
    trainers = cargar(rutaTrainers)

    encontrado = False

    for nombreRuta, infoRuta in rutas.items():
        if IDcamper in infoRuta.get("campersAsignados", []):
            encontrado = True
            trainerID = infoRuta.get("trainerEncargado", None)
            trainerNombre = (
                f"{trainers[trainerID]['nombres']} {trainers[trainerID]['apellidos']}"
                if trainerID and trainerID in trainers else "No asignado"
            )

            print(f"\n📚 Ruta: {nombreRuta}")
            print(f"👨‍🏫 Trainer: {trainerNombre}")
            print(f"🏫 Salón: {infoRuta.get('salon','No definido')}")
            print(f"⏰ Horarios: {infoRuta.get('horarios','No definido')}")

            print("\n📌 Módulos de la ruta:")
            for modulo, temas in infoRuta.get("modulos", {}).items():
                print(f"  - {modulo}: {', '.join(temas)}")
        
    pausar()

    if not encontrado:
        print("❌ No estás asignado a ninguna ruta actualmente.")
        pausar()