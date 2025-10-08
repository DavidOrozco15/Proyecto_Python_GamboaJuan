from modules.utils import cargar, guardar, pedirEntero, pedirFloat, limpiar, pausar

def listarCampersAsignados(IDtrainer):
    limpiar()
    ruta = "data/rutas.json"
    rutaRutas = cargar(ruta)
    ruta = "data/campers.json"
    campers = cargar(ruta)

    encontrado = False # Si al final del recorrido sigue siendo False, significa que el trainer no tiene grupos asignadas.
    print("----LISTAR CAMPERS ASIGNADOS A MI----")
    for nombreGrupo, infoGrupo in rutaRutas.get("grupos", {}).items():
        if infoGrupo.get("trainerEncargado") == IDtrainer: # Comprueba si el entrenador encargado de este grupo es el mismo que el IDtrainer actual.
            encontrado = True # Actualiza la bandera a True, indicando que sí tiene grupos asignadas.
            print(f"\n📖 Grupo: {nombreGrupo}")
            campersAsignados = infoGrupo.get("campersAsignados", [])

            if not campersAsignados:
                print("No hay campers Asignados aun")
                pausar()
            else:
                for IDcamper in campersAsignados:
                    info = campers.get(IDcamper, {})
                    print(f"\n👤 ID: {IDcamper} | Nombres: {info.get('nombres','')} | Apellidos: {info.get('apellidos','')} | Estado: {info.get('estado','')} ")
    if not encontrado:
        print("\nNo tienes grupos asignadas Actualmente")
        pausar()

    pausar()
        
def registrarNotasTrainer(IDtrainer):
    limpiar()
    rutaRutas = "data/rutas.json"
    rutaCampers = "data/campers.json"

    rutas = cargar(rutaRutas)
    campers = cargar(rutaCampers)

    print("----REGISTRAR NOTAS DE LOS MODULOS----")
    # Buscar el grupo asignado al trainer
    grupoAsignado = None
    for nombreGrupo, infoGrupo in rutas.get("grupos", {}).items():
        if infoGrupo.get("trainerEncargado") == IDtrainer:
            grupoAsignado = nombreGrupo
            break

    if not grupoAsignado:
        print("❌ No tienes ningún grupo asignado actualmente.")
        pausar()
        return

    print(f"\n📚 Grupo asignado: {grupoAsignado}")
    matriculas = rutas["grupos"][grupoAsignado].get("matriculas", {})

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
    rutas["grupos"][grupoAsignado]["matriculas"][IDcamperSeleccionado]["modulos"][nombreModulo] = {
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
    # Buscar el grupo asignado al trainer
    grupoAsignado = None
    for nombreGrupo, infoGrupo in rutas.get("grupos", {}).items():
        if infoGrupo.get("trainerEncargado") == IDtrainer:
            grupoAsignado = nombreGrupo
            break

    if not grupoAsignado:
        print("❌ No tienes ningún grupo asignado actualmente.")
        pausar()
        return

    print(f"\n📚 Grupo asignado: {grupoAsignado}")
    matriculas = rutas["grupos"][grupoAsignado].get("matriculas", {})

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

    for nombreGrupo, infoGrupo in rutas.get("grupos", {}).items():
        if infoGrupo.get("trainerEncargado") == IDtrainer:
            encontrado = True
            print(f"\n📊 Reporte del Grupo: {nombreGrupo}")
            print("-"*50)

            campersAsignados = infoGrupo.get("campersAsignados", [])

            if not campersAsignados:
                print("⚠ No hay campers asignados todavía.")
                pausar()
            else:
                for IDcamper in campersAsignados:
                    info = campers.get(IDcamper, {})
                    infoMatricula = infoGrupo.get("matriculas", {}).get(IDcamper, {})
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
        print("❌ No tienes grupos asignados actualmente.")
        pausar()

# def corregirNotasModulo(IDtrainer):
#     limpiar()
#     rutaRutas = "data/rutas.json"
#     rutaCampers = "data/campers.json"

#     rutas = cargar(rutaRutas)
#     campers = cargar(rutaCampers)

#     print("----CORREGIR NOTAS DE MÓDULO----")
#     # Buscar el grupo asignado al trainer
#     grupoAsignado = None
#     for nombreGrupo, infoGrupo in rutas.get("grupos", {}).items():
#         if infoGrupo.get("trainerEncargado") == IDtrainer:
#             grupoAsignado = nombreGrupo
#             break

#     if not grupoAsignado:
#         print("❌ No tienes ningún grupo asignado actualmente.")
#         pausar()
#         return

#     print(f"\n📚 Grupo asignado: {grupoAsignado}")
#     matriculas = rutas["grupos"][grupoAsignado].get("matriculas", {})

#     if not matriculas:
#         print("⚠️ No hay campers matriculados en esta ruta todavía.")
#         pausar()
#         return

#     # Mostrar campers asignados
#     print("\n---- CAMPERS DISPONIBLES ----")
#     for i, (IDcamper, infoMatricula) in enumerate(matriculas.items(), start=1):
#         camperInfo = campers.get(IDcamper, {})
#         print(f"{i}. 👤 {IDcamper} | {camperInfo.get('nombres','')} {camperInfo.get('apellidos','')}")

#     # Seleccionar camper
#     opcion = pedirEntero("Seleccione un camper: ")
#     IDcamperSeleccionado = list(matriculas.keys())[opcion - 1]

#     # Seleccionar módulo
#     modulos = matriculas[IDcamperSeleccionado].get("modulos", {})
#     modulosDisponibles = {k: v for k, v in modulos.items() if k != "Nota Inicial" and v}
#     if not modulosDisponibles:
#         print("⚠️ Este camper no tiene módulos con notas para corregir.")
#         pausar()
#         return

#     print("\n---- MÓDULOS CON NOTAS ----")
#     for i, modulo in enumerate(modulosDisponibles.keys(), start=1):
#         print(f"{i}. {modulo}")

#     opcionModulo = pedirEntero("Seleccione un módulo para corregir: ")
#     nombreModulo = list(modulosDisponibles.keys())[opcionModulo - 1]

#     # Confirmar corrección
#     confirm = input(f"¿Está seguro de corregir las notas de {nombreModulo} para {campers[IDcamperSeleccionado]['nombres']} {campers[IDcamperSeleccionado]['apellidos']}? (s/n): ").lower()
#     if confirm != 's':
#         print("Corrección cancelada.")
#         pausar()
#         return

#     # Eliminar notas anteriores
#     del rutas["grupos"][grupoAsignado]["matriculas"][IDcamperSeleccionado]["modulos"][nombreModulo]

#     # Ingresar nuevas notas
#     notaT = pedirFloat("Ingrese nueva nota teórica (0-100): ")
#     notaP = pedirFloat("Ingrese nueva nota práctica (0-100): ")
#     notaQ = pedirFloat("Ingrese nueva nota quiz (0-100): ")

#     promedio = notaT * 0.3 + notaP * 0.6 + notaQ * 0.1

#     # Guardar nuevas notas
#     rutas["grupos"][grupoAsignado]["matriculas"][IDcamperSeleccionado]["modulos"][nombreModulo] = {
#         "teorica": notaT,
#         "practica": notaP,
#         "quiz": notaQ,
#         "promedio": promedio
#     }

#     # Actualizar riesgo
#     if promedio < 60:
#         campers[IDcamperSeleccionado]["riesgo"] = "alto"
#     else:
#         campers[IDcamperSeleccionado]["riesgo"] = "bajo"

#     guardar(rutaRutas, rutas)
#     guardar(rutaCampers, campers)

#     print(f"✅ Notas corregidas para {campers[IDcamperSeleccionado]['nombres']} en {nombreModulo}.")
#     print(f"📊 Nuevo promedio: {promedio:.2f} | Riesgo actualizado: {campers[IDcamperSeleccionado]['riesgo']}")
#     pausar()

# def consultarEstadisticasGrupo(IDtrainer):
#     limpiar()
#     rutaRutas = "data/rutas.json"
#     rutaCampers = "data/campers.json"

#     rutas = cargar(rutaRutas)
#     campers = cargar(rutaCampers)

#     print("----ESTADÍSTICAS DEL GRUPO----")
#     # Buscar el grupo asignado al trainer
#     grupoAsignado = None
#     for nombreGrupo, infoGrupo in rutas.get("grupos", {}).items():
#         if infoGrupo.get("trainerEncargado") == IDtrainer:
#             grupoAsignado = nombreGrupo
#             break

#     if not grupoAsignado:
#         print("❌ No tienes ningún grupo asignado actualmente.")
#         pausar()
#         return

#     print(f"\n📚 Grupo asignado: {grupoAsignado}")
#     matriculas = rutas["grupos"][grupoAsignado].get("matriculas", {})

#     if not matriculas:
#         print("⚠️ No hay campers matriculados en esta ruta todavía.")
#         pausar()
#         return

#     totalCampers = len(matriculas)
#     campersRiesgoAlto = 0
#     campersRiesgoBajo = 0
#     campersAprobados = 0
#     campersReprobados = 0

#     for IDcamper, infoMatricula in matriculas.items():
#         camperInfo = campers.get(IDcamper, {})
#         riesgo = camperInfo.get("riesgo", "bajo")
#         if riesgo == "alto":
#             campersRiesgoAlto += 1
#         else:
#             campersRiesgoBajo += 1

#         modulos = infoMatricula.get("modulos", {})
#         for nombreModulo, notas in modulos.items():
#             if nombreModulo == "Nota Inicial":
#                 continue
#             promedio = notas.get("promedio", 0)
#             if promedio >= 60:
#                 campersAprobados += 1
#             else:
#                 campersReprobados += 1

#     print(f"\n📊 Estadísticas del Grupo {grupoAsignado}:")
#     print(f"   Total de Campers: {totalCampers}")
#     print(f"   Campers en Riesgo Alto: {campersRiesgoAlto}")
#     print(f"   Campers en Riesgo Bajo: {campersRiesgoBajo}")
#     print(f"   Módulos Aprobados: {campersAprobados}")
#     print(f"   Módulos Reprobados: {campersReprobados}")

#     # Porcentaje de aprobación
#     if campersAprobados + campersReprobados > 0:
#         porcentajeAprobacion = (campersAprobados / (campersAprobados + campersReprobados)) * 100
#         print(f"   Porcentaje de Aprobación: {porcentajeAprobacion:.2f}%")
#     else:
#         print("   Porcentaje de Aprobación: No hay módulos evaluados aún.")

#     pausar()
        
