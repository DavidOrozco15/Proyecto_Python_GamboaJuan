from modules.utils import cargar, limpiar, pausar, validadorCamperNoExiste

def consultarInfoCamper(IDcamper):
    limpiar()
    ruta = "data/campers.json"
    campers = cargar(ruta)

    validadorCamperNoExiste(IDcamper, campers)

    info = campers[IDcamper]
    print("👤 Información Personal del Camper:")
    print(f"\n 💹 ID: {IDcamper}")
    print(f"Nombres: {info.get('nombres', '')}")
    print(f"Apellidos: {info.get('apellidos', '')}")
    print(f"Estado: {info.get('estado', '')}")
    print(f"Riesgo: {info.get('riesgo', '')}")

    grupoAsignado = info.get('ruta', 'No asignado')
    print(f"Grupo asignado: {grupoAsignado}")

    if grupoAsignado != 'No asignado':
        rutaRutas = "data/rutas.json"
        rutas = cargar(rutaRutas)
        if grupoAsignado in rutas.get("grupos", {}):
            rutaNombre = rutas["grupos"][grupoAsignado].get("ruta", "Desconocida")
            print(f"Ruta: {rutaNombre}")
        else:
            print("Ruta: No asignada")
    else:
        print("Ruta: No asignada")

    pausar()
    
def consultarNotasCamper(IDcamper):
    limpiar()
    rutaCampers = "data/campers.json"
    campers = cargar(rutaCampers)
    rutaRutas = "data/rutas.json"
    rutas = cargar(rutaRutas)

    print("----CONSULTAR NOTAS----")
    camperInfo = campers.get(IDcamper, {})
    if not camperInfo:
        print("❌ Camper no encontrado.")
        pausar()
        return

    rutaAsignada = camperInfo.get("ruta")
    if not rutaAsignada or rutaAsignada not in rutas.get("grupos", {}):
        print("❌ No tienes grupo asignado o notas registradas.")
        pausar()
        return

    matricula = rutas["grupos"][rutaAsignada].get("matriculas", {}).get(IDcamper, {})
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
        print(f"\n📚 Módulo: {mod_name}")
        print(f"  📑 - Teórica: {teorica}")
        print(f"  📑 - Práctica: {practica}")
        print(f"  📑 - Quiz: {quiz}")
        print(f"  📑 - Promedio: {promedio}")
    pausar()
    
def consultarRutaCamper(IDcamper):
    limpiar()
    rutaRutas = "data/rutas.json"
    rutas = cargar(rutaRutas)

    rutaTrainers = "data/trainers.json"
    trainers = cargar(rutaTrainers)

    print("----CONSULTAR RUTA----")
    encontrado = False

    for nombreGrupo, infoGrupo in rutas.get("grupos", {}).items():
        if IDcamper in infoGrupo.get("campersAsignados", []):
            encontrado = True
            trainerID = infoGrupo.get("trainerEncargado", None)
            trainerNombre = (
                f"{trainers[trainerID]['nombres']} {trainers[trainerID]['apellidos']}" # se hace de esta manera, es un if ternario, se hace asi para no tener errores de sintaxis
                if trainerID and trainerID in trainers else "No asignado"
            )

            rutaNombre = infoGrupo.get("ruta", "desconocida")
            print(f"\n📚 Grupo: {nombreGrupo} | Ruta: {rutaNombre}")
            print(f"👨‍🏫 Trainer: {trainerNombre}")
            print(f"🏫 Salón: {infoGrupo.get('salon','No definido')}")
            print(f"⏰ Horarios: {infoGrupo.get('horarios','No definido')}")

            print("\n📌 Módulos de la ruta:")
            rutaTemplate = rutas.get("rutas", {}).get(rutaNombre, {})
            for modulo, temas in rutaTemplate.get("modulos", {}).items():
                print(f"  - {modulo}: {', '.join(temas)}")
        
    pausar()

    if not encontrado:
        print("❌ No estás asignado a ninguna ruta actualmente.")
        pausar()

# def consultarNotas(IDcamper):
#     limpiar()
#     rutaCampers = "data/campers.json"
#     campers = cargar(rutaCampers)
#     rutaRutas = "data/rutas.json"
#     rutas = cargar(rutaRutas)

#     print("----CONSULTAR NOTAS----")
#     camperInfo = campers.get(IDcamper, {})
#     if not camperInfo:
#         print("❌ Camper no encontrado.")
#         pausar()
#         return

#     rutaAsignada = camperInfo.get("ruta")
#     if not rutaAsignada or rutaAsignada not in rutas.get("grupos", {}):
#         print("❌ No tienes grupo asignado o notas registradas.")
#         pausar()
#         return

#     matricula = rutas["grupos"][rutaAsignada].get("matriculas", {}).get(IDcamper, {})
#     modulos = matricula.get("modulos", {})

#     if not modulos:
#         print("❌ No tienes notas registradas aún.")
#         pausar()
#         return

#     print(f"\n📊 Notas de {camperInfo.get('nombres','')} {camperInfo.get('apellidos','')}:")
#     for mod_name, notas in modulos.items():
#         teorica = notas.get("teorica", "No registrada")
#         practica = notas.get("practica", "No registrada")
#         quiz = notas.get("quiz", "No registrada")
#         promedio = notas.get("promedio", "No calculado")
#         print(f"\n📚 Módulo: {mod_name}")
#         print(f"  📑 - Teórica: {teorica}")
#         print(f"  📑 - Práctica: {practica}")
#         print(f"  📑 - Quiz: {quiz}")
#         print(f"  📑 - Promedio: {promedio}")
#     pausar()

# def consultarEstado(IDcamper):
#     limpiar()
#     ruta = "data/campers.json"
#     campers = cargar(ruta)

#     validadorCamperNoExiste(IDcamper, campers)

#     info = campers[IDcamper]
#     print("👤 Información Personal del Camper:")
#     print(f"\n 💹 ID: {IDcamper}")
#     print(f"Nombres: {info.get('nombres', '')}")
#     print(f"Apellidos: {info.get('apellidos', '')}")
#     print(f"Estado: {info.get('estado', '')}")
#     print(f"Riesgo: {info.get('riesgo', '')}")

#     grupoAsignado = info.get('ruta', 'No asignado')
#     print(f"Grupo asignado: {grupoAsignado}")

#     if grupoAsignado != 'No asignado':
#         rutaRutas = "data/rutas.json"
#         rutas = cargar(rutaRutas)
#         if grupoAsignado in rutas.get("grupos", {}):
#             rutaNombre = rutas["grupos"][grupoAsignado].get("ruta", "Desconocida")
#             print(f"Ruta: {rutaNombre}")
#         else:
#             print("Ruta: No asignada")
#     else:
#         print("Ruta: No asignada")

#     pausar()

# def consultarHorarioSemanal(IDcamper):
#     limpiar()
#     rutaCampers = "data/campers.json"
#     campers = cargar(rutaCampers)
#     rutaRutas = "data/rutas.json"
#     rutas = cargar(rutaRutas)

#     print("----CONSULTAR HORARIO SEMANAL----")
#     camperInfo = campers.get(IDcamper, {})
#     if not camperInfo:
#         print("❌ Camper no encontrado.")
#         pausar()
#         return

#     grupoAsignado = camperInfo.get("ruta")
#     if not grupoAsignado or grupoAsignado not in rutas.get("grupos", {}):
#         print("❌ No tienes grupo asignado.")
#         pausar()
#         return

#     grupoInfo = rutas["grupos"][grupoAsignado]
#     horario = grupoInfo.get("horarios", "No definido")

#     print(f"\n📅 Horario Semanal del Grupo: {grupoAsignado}")
#     print(f"🏫 Salón: {grupoInfo.get('salon', 'No definido')}")
#     print(f"⏰ Horarios: {horario}")

#     # Mostrar módulos de la ruta con días si están definidos
#     rutaNombre = grupoInfo.get("ruta", "")
#     if rutaNombre:
#         rutaTemplate = rutas.get("rutas", {}).get(rutaNombre, {})
#         modulos = rutaTemplate.get("modulos", {})
#         if modulos:
#             print("\n📚 Módulos de la Ruta:")
#             for modulo, temas in modulos.items():
#                 print(f"  - {modulo}: {', '.join(temas)}")
#         else:
#             print("\n📚 No hay módulos definidos para esta ruta.")
#     else:
#         print("\n📚 Ruta no especificada.")

#     pausar()
