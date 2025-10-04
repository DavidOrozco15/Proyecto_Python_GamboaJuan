import json
from modules.utils import cargar, guardar, val, validadorCamper, validadorTrainer, validadorCamperNoExiste, validarEstado, validadorRuta, validadorTrainerNoExiste, ValidadorRutaNoExiste, pedirEntero, pedirFloat, pausar, limpiar
import modules.messages as msg

#Tuplas
estados = (
        "en proceso de ingreso",
        "inscrito",
        "aprobado",
        "cursando",
        "graduado",
        "expulsado",
        "retirado"
    )

riesgos = (
        "bajo",
        "alto"
    )


def registrarCamper():
    limpiar()
    ruta = "data/campers.json"
    campers = cargar(ruta)
    
    IDcamper = val("Ingrese el numero de identificacion: ") #valida que la entrada no este vacia
    validadorCamper(IDcamper, campers) #Valida que no este en campers

    nombres = val("Ingrese los nombres: ")
    apellidos = val("Ingrese apellidos: ")
    direccion = val("Ingrese direccion: ")
    acudiente = val("Ingrese el nombre del acudiente: ")

    celular = val("Ingrese el telefono celular: ")
    fijo = val("Ingrese telefono fijo: ")

    estado = "en proceso de ingreso"
    riesgo = "bajo"

    camper = {
        "nombres": nombres,
        "apellidos": apellidos,
        "direccion": direccion,
        "acudiente": acudiente,
        "telefonos": {
            "celular": celular,
            "fijo": fijo
        },
        "estado": estado,
        "riesgo": riesgo,
        "ruta": None,
        "notas": {}
    }

    #guardar en campers.json
    campers[IDcamper] = camper
    guardar(ruta, campers)

    print(f"✅ Camper {nombres} {apellidos} registrado con éxito.")
    pausar()

def registrarTrainer():
    limpiar()
    ruta = "data/trainers.json"
    trainers = cargar(ruta)

    IDtrainer = val("Ingrese el numero de identificacion del trainer: ")
    validadorTrainer(IDtrainer, trainers)

    nombre = val("Ingrese el nombre: ")
    apellido = val("Ingrese el apellido: ")
    telefono = val("Ingrese el telefono: ")
    correo = val("Ingrese el correo: ")
    estado = "activo"

    trainer = {
        "nombres": nombre,
        "apellidos": apellido,
        "telefono": telefono,
        "correo": correo,
        "estado": estado,
        "rutasAsignadas": []
    }

    trainers[IDtrainer] = trainer
    guardar(ruta, trainers)
    pausar()

def registrarNotas():
    limpiar()
    ruta = "data/campers.json"
    campers = cargar(ruta)

    IDcamper = val("Ingrese el numero de identificacion: ") #valida que la entrada no este vacia
    validadorCamperNoExiste(IDcamper, campers)

    if IDcamper in campers:
        Id = campers[IDcamper]
        print(f"\n Camper ID:{IDcamper} | Nombre: {Id['nombres']} Estado: {Id['estado']}")

    notaT = pedirFloat("Ingresa el valor de la Nota Teorica (0-100)")
    notaP = pedirFloat("Ingresa el valor de la Nota Practica (0-100)")

    promedio = (notaT + notaP)/2

    if promedio >= 60:
        campers[IDcamper]["estado"] = "aprobado"
        print("El Camper aprobo exitosamente.")
    elif promedio < 60:
        print("El Camper debe volver a intentarlo.")
        campers[IDcamper]["estado"] = "en proceso de ingreso"
    

    campers[IDcamper]["notaInicial"] = {
        "teorica": notaT,
        "practica": notaP,
        "promedio": promedio
    }
    guardar(ruta, campers)

    print(f"Promedio final: {promedio:.2f} | Estado: {campers[IDcamper]['estado']}")
    pausar()

def crearRuta():
    limpiar()
    horarios = ["08:00-12:00", "12:00-16:00", "16:00-20:00"]
    salones = ["salon 1", "salon 2", "salon 3"]

    modulosRuta = {
        "Fundamentos de programación": ["Introducción a la algoritmia", "PSeInt", "Python"],
        "Programación Web": ["HTML", "CSS", "Bootstrap"],
        "Bases de datos": ["MySQL", "MongoDB", "PostgreSQL"]
    }

    ruta = "data/rutas.json"
    rutas = cargar(ruta)

    
    nombreRuta = val("Ingrese el nombre de la ruta: ")
    # si muestras rutas fijas
    msg.rutasFijas()
    # Elegir Programación Formal
    print("Programación Formal: ")
    print("1. Java | 2. JavaScript | 3. C#")
    formal = pedirEntero("Seleccione una: ")
    if formal == 1:
        formal = "Java"
    elif formal == 2:
        formal = "JavaScript"
    elif formal == 3:
        formal = "C#"

    # Elegir Backend
    print("Backend: ")
    print("1. NodeJS | 2. SpringBoot | 3. Netcore | 4. Express")
    backend = pedirEntero("Seleccione una: ")
    if backend == 1:
        backend = "NodeJS"
    elif backend == 2:
        backend = "SpringBoot"
    elif backend == 3:
        backend = "Netcore"
    elif backend == 4:
        backend = "Express"

    # Elegir Bases de Datos (opcional, se pueden escoger dos)
    print("\nBases de datos disponibles (escoge hasta 2, separados por coma):")
    for i, db in enumerate(modulosRuta["Bases de datos"], 1):
        print(f"{i}. {db}")
    db_input = pedirEntero("Ingrese números separados por coma (Enter para ninguna): ")
    basesSeleccionadas = []
    if db_input.strip():
        indices = db_input.split(",")
        for ind in indices[:2]:  # máximo 2
            if ind.strip().isdigit() and 1 <= int(ind.strip()) <= len(modulosRuta["Bases de datos"]):
                basesSeleccionadas.append(modulosRuta["Bases de datos"][int(ind.strip())-1])

    # Capacidad
    capacidad = pedirEntero("Ingrese la capacidad máxima de la ruta (Enter para 33): ")
    capacidad = int(capacidad) if capacidad.strip() else 33

    # Selección de salón
    print("\nSalones de entrenamiento disponibles:")
    for i, salon in enumerate(salones, 1):
        print(f"{i}. {salon}")
    while True:
        seleccion = pedirEntero("Seleccione un salon de entrenamiento (1-3): ")
        if 1 <= seleccion <= len(salones):
            salonSeleccionado = salones[seleccion - 1]
            break

    # Horarios disponibles según salón
    ocupados_por_salon = {}
    for r in rutas.values():
        s = r["salon"]
        for h in r["horarios"]:
            if s not in ocupados_por_salon:
                ocupados_por_salon[s] = []
            ocupados_por_salon[s].append(h)

    disponibles = [h for h in horarios if h not in ocupados_por_salon.get(salonSeleccionado, [])]
    if not disponibles:
        print(f"❌ No hay horarios disponibles para {salonSeleccionado}.")
        pausar()
        return

    print(f"\nHorarios disponibles para {salonSeleccionado}:")
    for i, h in enumerate(disponibles, 1):
        print(f"{i}. {h}")
    while True:
        seleccion_horario = pedirEntero("Seleccione un horario: ")
        if 1 <= seleccion_horario <= len(disponibles):
            horarioSeleccionado = [disponibles[seleccion_horario - 1]]  # se guarda como lista
            break

    # Crear la ruta
    nuevaRuta = {
        "modulos": {
            **modulosRuta,
            "Programación formal": [formal],
            "Backend": [backend],
            "Bases de datos": basesSeleccionadas
        },
        "capacidadMax": capacidad,
        "campersAsignados": [],
        "salon": salonSeleccionado,
        "horarios": horarioSeleccionado,
        "trainerEncargado": "No asignado",
        "matriculas": {}
    }

    rutas[nombreRuta] = nuevaRuta
    guardar(ruta, rutas)
    print(f"✅ Ruta '{nombreRuta}' creada correctamente en {salonSeleccionado} con horario {horarioSeleccionado[0]}.")
    pausar()

def cambiarEstado():
    limpiar()
    ruta = "data/campers.json"
    campers = cargar(ruta)

    IDcamper = val("Ingrese el numero de identificacion: ") #valida que la entrada no este vacia
    validadorCamperNoExiste(IDcamper, campers)

    Id = campers[IDcamper]
    print(f"\nCamper ID:{IDcamper} | Nombre: {Id['nombres']} Estado: {Id['estado']}")
    print()

    for i, estado in enumerate(estados, start=1):
        print(f"{i}. {estado}")

    while True:
        nuevoEstado = val("\nIngrese el nuevo estado de los mostrados: ")
        if validarEstado(nuevoEstado, estados):
            break  # estado válido, salimos del bucle
        else:
            print("❌ Estado inválido. Debe ser uno de:", ", ".join(estados))
    
    campers[IDcamper]["estado"] = nuevoEstado
    guardar(ruta, campers)
    pausar()

def asignarTrainerRuta():
    limpiar()
    rutaTrainers = "data/trainers.json"
    rutaRutas = "data/rutas.json"
    trainers = cargar(rutaTrainers)
    rutas = cargar(rutaRutas)

    print("----RUTAS DISPONIBLES----")
    for i, (nombreRuta, info) in enumerate(rutas.items(), start=1):
        print(f"\n{i}. {nombreRuta} | Capacidad: {info['capacidadMax']} | Salón: {info['salon']} | Trainer: {info.get('trainer_encargado', 'No asignado')}")
    
    while True:
        opcion = pedirEntero("\nSeleccione una ruta: ")
        if 1 <= opcion <= len(rutas):
            rutaSeleccionada = list(rutas.keys())[opcion - 1]
            break
        
    print("\n----TRAINERS DISPONIBLES----")
    for i, (IDtrainer, info) in enumerate(trainers.items(), start=1):
        print(f"\n{i}. {info['nombres']} {info['apellidos']} | ID: {IDtrainer}")

    while True:
        opcion = pedirEntero("\nSeleccione un trainer: ")
        if 1 <= opcion <= len(trainers):
            trainerSeleccionado = list(trainers.keys())[opcion - 1]
            break

    rutas[rutaSeleccionada]["trainerEncargado"] = trainerSeleccionado
    guardar(rutaRutas, rutas)

    print(f"\n✅ Trainer '{trainers[trainerSeleccionado]['nombres']} {trainers[trainerSeleccionado]['apellidos']}' asignado correctamente a la ruta '{rutaSeleccionada}'.")
    pausar()

def matricularCamper():
    limpiar()
    rutaCampers = "data/campers.json"
    rutaRutas = "data/rutas.json"
    campers = cargar(rutaCampers)
    rutas = cargar(rutaRutas)

    campersAprobados = {IDcamper : info for IDcamper, info in campers.items() if info["estado"] == "aprobado"}

    print("----CAMPERS APROBADOS----")
    for IDcamper, info in campersAprobados.items():
        print(f"[ID: {IDcamper}]: 👤 {info['nombres']} {info['apellidos']}")

    while True:
        opcion = pedirEntero("\nSeleccione un camper: ")
        if 1 <= opcion <= len(campersAprobados):
            camperSeleccionado = list(campersAprobados.keys())[opcion - 1]
            break

    print("\n---- RUTAS DISPONIBLES ----")

    rutasDisponibles = {}
    contador = 1

    for nombreRuta, info in rutas.items():
        ocupados = len(info.get("campersAsignados", [])) #para mirar cuantos campers ya estan asignados
        disponible = ocupados < info["capacidadMax"] # mirar si aun hay espacio
        trainer = info.get("trainerEncargado", "no asignado") #trainer asignado o no
        estado = "disponible" if disponible else "lleno"
        print(f"\n{contador}. {nombreRuta} | Capacidad: {ocupados}/{info['capacidadMax']} | Trainer: {trainer} | Estado: {estado}")
    
        if disponible:
            rutasDisponibles[contador] = nombreRuta

        contador += 1

    while True:
        opcion = pedirEntero("\nSeleccione una ruta disponible: ")
        if opcion in rutasDisponibles:
            rutaSeleccionada = rutasDisponibles[opcion]
            break

    fechaInicio = val("Ingrese fecha de inicio (YYYY-MM-DD): ")
    fechaFin = val("Ingrese fecha de fin (YYYY-MM-DD): ")
                            #revisa si existe, si no la crea
    rutas[rutaSeleccionada].setdefault("campersAsignados", []).append(camperSeleccionado)

    rutas[rutaSeleccionada].setdefault("matriculas", {})[camperSeleccionado] = {
        "fechaInicio": fechaInicio,
        "fechaFin": fechaFin,
        "trainer": rutas[rutaSeleccionada].get("trainerEncargado", "no asignado")
    }

    campers[camperSeleccionado]["estado"] = "cursando"

    guardar(rutaCampers, campers)
    guardar(rutaRutas, rutas)
    print(f"\n✅ Camper '{campers[camperSeleccionado]['nombres']} {campers[camperSeleccionado]['apellidos']}' matriculado en la ruta '{rutaSeleccionada}' con éxito.")
    pausar()

def consultarCamperEnRiesgo():
    limpiar()
    rutaCampers = "data/campers.json"
    rutaRutas = "data/rutas.json"
    campers = cargar(rutaCampers)
    rutas = cargar(rutaRutas)

    # Mostrar todos los campers inscritos
    campersInscritos = {ID: info for ID, info in campers.items() if info["estado"] == "inscrito"}
    print("\n----CAMPERS INSCRITOS----")
    for ID, info in campersInscritos.items():
        print(f"{ID}: {info['nombres']} {info['apellidos']}")

    # Recorrer rutas y matriculas
    for nombreRuta, infoRuta in rutas.items():
        matriculas = infoRuta.get("matriculas", {})

        for IDcamper, infoMatricula in matriculas.items():
            if campers.get(IDcamper, {}).get("estado") != "inscrito":
                continue

            modulos = infoMatricula.get("modulos", {})

            for nombreModulo, notas in modulos.items():
                # Saltar módulos sin notas
                if notas.get("teorica") is None and notas.get("practica") is None and notas.get("quiz") is None:
                    continue

                # Calcular promedio ponderado
                notaT = notas.get("teorica", 0)
                notaP = notas.get("practica", 0)
                notaQ = notas.get("quiz", 0)

                promedio = notaT*0.3 + notaP*0.6 + notaQ*0.1

                # Actualizar riesgo según promedio
                if promedio < 60:
                    campers[IDcamper]["riesgo"] = "alto"
                else:
                    campers[IDcamper]["riesgo"] = "bajo"

    guardar(rutaCampers, campers)
    print("\n✅ Se ha actualizado el riesgo de todos los campers inscritos según sus notas.")
    pausar()
    
def listarCampersInscritos():
    limpiar()
    ruta = "data/campers.json"
    campers = cargar(ruta)
    
    campersInscritos = {IDcamper : info for IDcamper, info in campers.items() if info["estado"] == "inscrito"}

    print("\n----CAMPERS INSCRITOS----")
    for IDcamper, info in campersInscritos.items():
        print(f"ID: {IDcamper}: | Nombre :{info['nombres']} | Apellido :  {info['apellidos']} | Estado : {info['estado']}").strip()
        print("-"*20)
    pausar()

def listarCampersAprobados():
    limpiar()
    ruta = "data/campers.json"
    campers = cargar(ruta)
    
    campersAprobados = {IDcamper : info for IDcamper, info in campers.items() if info["estado"] == "aprobado"}

    print("\n----CAMPERS APROBADOS----")
    for IDcamper, info in campersAprobados.items():
        print(f"ID: {IDcamper}: | Nombre :{info['nombres']} | Apellido :  {info['apellidos']} | Estado : {info['estado']}").strip()
        print("-"*20)
    pausar()

def listarTrainers():
    limpiar()
    ruta = "data/trainers.json"
    trainers = cargar(ruta)
    
    trainersActivos = {IDtrainer : info for IDcamper, info in trainers.items() if info["estado"] == "activo"}

    print("\n----LISTA DE TRAINERS----")
    for IDtrainer, info in trainersActivos.items():
        print(f"ID: {IDtrainer}: | Nombre :{info['nombres']} | Apellido :  {info['apellidos']} | Estado : {info['estado']}").strip()
        print("-"*20)
    pausar()
    
def listarCampersBajoRendimiento():
    limpiar()
    ruta = "data/campers.json"
    campers = cargar(ruta)
    
    campersRiesgo = {IDcamper : info for IDcamper, info in campers.items() if info["riesgo"] == "alto"}

    print("\n----CAMPERS APROBADOS----")
    for IDcamper, info in campersRiesgo.items():
        print(f"ID: {IDcamper}: | Nombre :{info['nombres']} | Apellido :  {info['apellidos']} | Riesgo : {info['riesgo']}").strip()
        print("-"*20)
    pausar()

def listarRutaCampersTrainers():
    limpiar()
    ruta = "data/rutas.json"
    rutaRutas = cargar(ruta)
    ruta = "data/campers.json"
    campers = cargar(ruta)
    ruta = "data/trainers.json"
    trainers = cargar(ruta)
    
    for nombreRuta, infoRuta in rutaRutas.items():
        # Obtener el ID del trainer encargado
        IDtrainer = infoRuta.get("trainerEncargado", None)
        if IDtrainer and IDtrainer in trainers:
            trainerNombre = f"{trainers[IDtrainer]['nombres']} {trainers[IDtrainer]['apellidos']}"
        else:
            trainerNombre = "No asignado"

        # Obtener campers asignados
        campersAsignados = infoRuta.get("campersAsignados", [])

        print(f"\n---- RUTA: {nombreRuta} | Trainer: {trainerNombre} ----")
        
        if not campersAsignados:
            print("No hay campers asignados.")
        else:
            for IDcamper in campersAsignados:
                info = campers.get(IDcamper, {})
                print(f"ID: {IDcamper} | Nombre: {info.get('nombres','')} {info.get('apellidos','')} | "f"Estado: {info.get('estado','')} | Riesgo: {info.get('riesgo','')}")
        print("-"*40)
    pausar()
    
def mostrarResultadosModulos():
    limpiar()
    ruta = "data/rutas.json"
    rutaRutas = cargar(ruta)
    ruta = "data/campers.json"
    campers = cargar(ruta)
    ruta = "data/trainers.json"
    trainers = cargar(ruta)
    
    for nombreRuta, infoRuta in rutaRutas.items():
        # Obtener el ID del trainer encargado
        IDtrainer = infoRuta.get("trainerEncargado", None)
        if IDtrainer and IDtrainer in trainers:
            trainerNombre = f"{trainers[IDtrainer]['nombres']} {trainers[IDtrainer]['apellidos']}"
        else:
            trainerNombre = "No asignado"
            
        print(f"\n---- RUTA: {nombreRuta} | Trainer: {trainerNombre} ----")
        
        matriculas = infoRuta.get("matricula", {})
        
        modulosResumen = {}
        
    for IDcamper, infoMatricula in matriculas.items():
        camperInfo = campers.get(IDcamper, {})
        modulos = infoMatricula.get("modulos", {})

        for nombreModulo, notas in modulos.items():
            # Calcular promedio ponderado
            notaT = notas.get("teorica", 0)
            notaP = notas.get("practica", 0)
            notaQ = notas.get("quiz", 0)
            promedio = notaT*0.3 + notaP*0.6 + notaQ*0.1

            # Inicializar diccionario del módulo si no existe
            if nombreModulo not in modulosResumen:
                modulosResumen[nombreModulo] = {'aprobados': [], 'reprobados': []}

            # Nombre completo del camper
            nombreCompleto = camperInfo.get('nombres','') + " " + camperInfo.get('apellidos','')

            # Clasificar según promedio
            if promedio >= 60:
                modulosResumen[nombreModulo]['aprobados'].append(nombreCompleto)
            else:
                modulosResumen[nombreModulo]['reprobados'].append(nombreCompleto)

# Imprimir resumen por módulo
    for nombreModulo, datos in modulosResumen.items():
        aprobados = datos['aprobados']
        reprobados = datos['reprobados']

        print(f"\nMódulo: {nombreModulo}")
        print(f"Aprobados ({len(aprobados)}): {', '.join(aprobados) if aprobados else 'Ninguno'}")
        print(f"Reprobados ({len(reprobados)}): {', '.join(reprobados) if reprobados else 'Ninguno'}")
        print("-"*50)
    pausar()