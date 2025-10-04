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

    camperInfo = campers.get(IDcamper, {})
    if not camperInfo:
        print("❌ Camper no encontrado.")
        pausar()
        return

    nota_inicial = camperInfo.get("notaInicial")
    if not nota_inicial:
        print(f"El camper {camperInfo.get('nombres', '')} {camperInfo.get('apellidos', '')} aún no tiene nota inicial registrada.")
        pausar()
        return

    print(f"\n📊 Nota inicial de {camperInfo.get('nombres','')} {camperInfo.get('apellidos','')}:")
    print(f"   - Teórica: {nota_inicial.get('teorica', 'N/A')}")
    print(f"   - Práctica: {nota_inicial.get('practica', 'N/A')}")
    print(f"   - Promedio: {nota_inicial.get('promedio', 'N/A')}")
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