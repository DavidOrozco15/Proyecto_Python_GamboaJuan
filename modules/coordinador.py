import json
from modules.utils import cargar, guardar, val, validadorCamper, validadorTrainer, validadorRuta, validadorGrupo, validadorCamperNoExiste, validarEstado, pedirEntero, pedirFloat, pausar, limpiar, pedirFecha
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
    # Carga los campers existentes desde el archivo JSON.
    ruta = "data/campers.json"
    campers = cargar(ruta)
    print("----REGISTRO DE CAMPERS----")
    IDcamper = val("Ingrese el numero de identificacion: ") #valida que la entrada no este vacia
    if not validadorCamper(IDcamper, campers): # Verifica que el ID no esté ya registrado en la base de datos
        pausar()
        return

    nombres = val("Ingrese los nombres: ")
    apellidos = val("Ingrese apellidos: ")
    direccion = val("Ingrese direccion: ")
    acudiente = val("Ingrese el nombre del acudiente: ")

    celular = val("Ingrese el telefono celular: ")
    fijo = val("Ingrese telefono fijo: ")

    # Estado inicial y nivel de riesgo por defecto
    estado = "en proceso de ingreso"
    riesgo = "bajo"

    # Estructura estandarizada del camper
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
        "ruta": None, # Aún no asignado a una ruta formativa
        "notas": {} # Diccionario vacío para futuras notas o calificaciones
    }

    #guardar en campers.json
    campers[IDcamper] = camper
    guardar(ruta, campers)

    print(f"✅ Camper {nombres} {apellidos} registrado con éxito.")
    pausar()

def registrarTrainer():
    limpiar()
    ruta = "data/trainers.json" # Ruta del archivo JSON donde se almacenarán los trainers.
    trainers = cargar(ruta)  # Esta variable será un DICCIONARIO que contiene todos los trainers guardados hasta el momento.

    print("----REGISTRO DE TRAINERS----")
    IDtrainer = val("Ingrese el numero de identificacion del trainer: ")
    if not validadorTrainer(IDtrainer, trainers): # Se verifica que este ID no exista ya en el archivo JSON.
        pausar()
        return

    nombre = val("Ingrese el nombre: ")
    apellido = val("Ingrese el apellido: ")
    telefono = val("Ingrese el telefono: ")
    correo = val("Ingrese el correo: ")
    estado = "activo" # El estado por defecto de un trainer nuevo es "activo".

    # Se crea un DICCIONARIO llamado "trainer" que almacena toda la información del nuevo trainer.
    # 🔹 Un diccionario en Python se compone de pares clave:valor
    # 🔹 Las claves ("nombres", "telefono", etc.) permiten identificar cada dato.
    trainer = {
        "nombres": nombre,
        "apellidos": apellido,
        "telefono": telefono,
        "correo": correo,
        "estado": estado,
        "rutasAsignadas": [] # Lista vacía → aquí se guardarán las rutas que el trainer tendrá asignadas
    }

    # Se añade el nuevo trainer al diccionario "trainers" usando como clave su número de identificación.
    # Esto significa que cada trainer queda guardado con su ID como clave principal.
    # Ejemplo: trainers["123"] = {datos del trainer 123}
    trainers[IDtrainer] = trainer
    guardar(ruta, trainers)
    pausar()

def registrarNotas():
    limpiar()
    ruta = "data/campers.json"
    campers = cargar(ruta)
    print("----REGISTRO DE NOTAS INICIALES----")
    IDcamper = val("Ingrese el numero de identificacion: ") #valida que la entrada no este vacia
    if not validadorCamperNoExiste(IDcamper, campers):  # Se valida que el camper exista en la base de datos.
        pausar()
        return

    # Si el camper existe, se obtiene su información para mostrarla al usuario.
    Id = campers[IDcamper] # Se extrae la información del camper mediante su ID.
    print(f"\n Camper ID:{IDcamper} | Nombre: {Id['nombres']} Estado: {Id['estado']}") # Se imprime información básica del camper: ID, nombre y estado actual.

    # Solo pedir una nota para la prueba inicial
    notaInicial = pedirFloat("Ingrese nota de la prueba inicial (0-100): ")

    if notaInicial >= 60:
        campers[IDcamper]["estado"] = "aprobado"
        print("El Camper aprobo exitosamente.")
    else:
        print("El Camper debe volver a intentarlo.")
        campers[IDcamper]["estado"] = "inscrito"

    # Se guarda la información de notas dentro del diccionario del camper.
    # Se crea una nueva clave "notaInicial" donde se almacenan las notas y el promedio.
    campers[IDcamper]["notaInicial"] = {
        "teorica": notaInicial,
        "practica": notaInicial,
        "quiz": notaInicial,
        "promedio": notaInicial
    }
    guardar(ruta, campers)

    print(f"Nota final: {notaInicial:.2f} | Estado: {campers[IDcamper]['estado']}") # Se muestra la nota final y el nuevo estado del camper en consola.
    pausar()

def crearRuta():
    limpiar()
    # Diccionario que contiene los módulos base de todas las rutas.
    # Cada clave es un área (por ejemplo "Bases de datos") y su valor es una lista de tecnologías.
    modulosRuta = {
        "Fundamentos de programación": ["Introducción a la algoritmia", "PSeInt", "Python"],
        "Programación Web": ["HTML", "CSS", "Bootstrap"],
        "Bases de datos": ["MySQL", "MongoDB", "PostgreSQL"]
    }

    ruta = "data/rutas.json"
    rutas = cargar(ruta)

    print("----CREAR UNA RUTA----")
    nombreRuta = val("Ingrese el nombre de la ruta: ")

    # Verificar si ya existe
    if "rutas" not in rutas:
        rutas["rutas"] = {}
    if not validadorRuta(nombreRuta, rutas["rutas"]):
        pausar()
        return

    # Mensaje o menú fijo con rutas predefinidas.
    msg.rutasFijas()

    # Elegir Programación Formal
    print("\nProgramación Formal: ")
    print("1. Java | 2. JavaScript | 3. C#")
    formal = pedirEntero("Seleccione una: ")
    if formal == 1:
        formal = "Java"
    elif formal == 2:
        formal = "JavaScript"
    elif formal == 3:
        formal = "C#"

    # Elegir Backend
    print("\nBackend: ")
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

    while True:
        dbInput = input("Ingrese números separados por coma (Enter para ninguna): ").strip()
        if not dbInput:
            basesSeleccionadas = []
            break
        indicesStr = dbInput.split(",")
        indices = []
        for idx in indicesStr:
            idx = idx.strip()
            if not idx.isdigit():
                print("❌ Entrada inválida. Solo números separados por coma.")
                break
            num = int(idx)
            if num < 1 or num > len(modulosRuta["Bases de datos"]):
                print("❌ Número fuera de rango.")
                break
            indices.append(num)
        else:
            if len(indices) > 2:
                print("❌ Máximo dos opciones.")
            else:
                basesSeleccionadas = [modulosRuta["Bases de datos"][i-1] for i in indices]
                break

    # Crear la ruta (solo template)
    nuevaRuta = {
        "modulos": {
            **modulosRuta,
            "Programación formal": [formal],
            "Backend": [backend],
            "Bases de datos": basesSeleccionadas
        }
    }

    rutas["rutas"][nombreRuta] = nuevaRuta
    guardar(ruta, rutas)
    print(f"✅ Ruta '{nombreRuta}' creada correctamente.")
    pausar()

def crearGrupo():
    limpiar()
    horarios = ["08:00-12:00", "12:00-16:00", "16:00-20:00"]
    salones = ["salon 1", "salon 2", "salon 3"]

    ruta = "data/rutas.json"
    rutas = cargar(ruta)

    print("----CREAR UN GRUPO----")

    # Listar rutas disponibles
    if "rutas" not in rutas or not rutas["rutas"]:
        print("❌ No hay rutas disponibles. Crea una ruta primero.")
        pausar()
        return

    print("\n----RUTAS DISPONIBLES----")
    for i, (nombreRuta, info) in enumerate(rutas["rutas"].items(), start=1):
        print(f"{i}. {nombreRuta}")

    while True:
        opcion = pedirEntero("\nSeleccione una ruta: ")
        if 1 <= opcion <= len(rutas["rutas"]):
            rutaSeleccionada = list(rutas["rutas"].keys())[opcion - 1]
            break

    nombreGrupo = val("Ingrese el nombre del grupo: ")

    # Verificar si ya existe
    if "grupos" not in rutas:
        rutas["grupos"] = {}
    if not validadorGrupo(nombreGrupo, rutas["grupos"]):
        pausar()
        return

    # Capacidad
    while True:
        capacidadInput = input("Ingrese la capacidad máxima del grupo (Enter para 33): ").strip()
        if not capacidadInput:
            capacidad = 33
            break
        if capacidadInput.isdigit() and int(capacidadInput) > 0:
            capacidad = int(capacidadInput)
            break
        else:
            print("❌ Ingrese un número entero positivo o deje vacío para el valor por defecto (33).")

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
    ocupadosPorSalon = {}
    if "grupos" in rutas:
        for g in rutas["grupos"].values():
            s = g["salon"]
            for h in g["horarios"]:
                if s not in ocupadosPorSalon:
                    ocupadosPorSalon[s] = []
                ocupadosPorSalon[s].append(h)

    disponibles = [h for h in horarios if h not in ocupadosPorSalon.get(salonSeleccionado, [])]
    if not disponibles:
        print(f"❌ No hay horarios disponibles para {salonSeleccionado}.")
        pausar()
        return

    print(f"\nHorarios disponibles para {salonSeleccionado}:")
    for i, h in enumerate(disponibles, 1):
        print(f"{i}. {h}")
    while True:
        seleccionHorario = pedirEntero("Seleccione un horario: ")
        if 1 <= seleccionHorario <= len(disponibles):
            horarioSeleccionado = [disponibles[seleccionHorario - 1]]
            break

    # Crear el grupo
    nuevoGrupo = {
        "ruta": rutaSeleccionada,
        "capacidadMax": capacidad,
        "campersAsignados": [],
        "salon": salonSeleccionado,
        "horarios": horarioSeleccionado,
        "trainerEncargado": "No asignado",
        "matriculas": {}
    }

    rutas["grupos"][nombreGrupo] = nuevoGrupo
    guardar(ruta, rutas)
    print(f"✅ Grupo '{nombreGrupo}' creado correctamente en {salonSeleccionado} con horario {horarioSeleccionado[0]}.")
    pausar()

def cambiarEstado():
    limpiar()
    ruta = "data/campers.json"
    campers = cargar(ruta)
    print("----CAMBIAR ESTADO MANUAL----")
    IDcamper = val("Ingrese el numero de identificacion: ") #valida que la entrada no este vacia
    if not validadorCamperNoExiste(IDcamper, campers):
        pausar()
        return

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
            print("❌ Estado inválido. Debe ser uno de:", ", ".join(estados)) # join transforma la lista de estados en una sola cadena.
    
    campers[IDcamper]["estado"] = nuevoEstado # Actualiza directamente el valor de la clave estado del camper seleccionado dentro del diccionario campers.
    guardar(ruta, campers)
    pausar()

def asignarTrainerGrupo():
    limpiar()
    rutaTrainers = "data/trainers.json"
    rutaRutas = "data/rutas.json"
    trainers = cargar(rutaTrainers)
    rutas = cargar(rutaRutas)

    print("----ASIGNACION DE TRAINER A GRUPO----")
    print("\n----GRUPOS DISPONIBLES----")

    grupos = rutas.get("grupos", {})
    if not grupos:
        print("❌ No hay grupos disponibles.")
        pausar()
        return

    for i, (nombreGrupo, info) in enumerate(grupos.items(), start=1):
        print(f"\n{i}. {nombreGrupo} | Ruta: {info['ruta']} | Capacidad: {info['capacidadMax']} | Salón: {info['salon']} | Trainer: {info.get('trainerEncargado', 'No asignado')}")

    while True:
        opcion = pedirEntero("\nSeleccione un grupo: ")
        if 1 <= opcion <= len(grupos):
            grupoSeleccionado = list(grupos.keys())[opcion - 1]
            break

    print("\n----TRAINERS DISPONIBLES----")
    for i, (IDtrainer, info) in enumerate(trainers.items(), start=1):
        print(f"\n{i}. {info['nombres']} {info['apellidos']} | ID: {IDtrainer}")

    while True:
        opcion = pedirEntero("\nSeleccione un trainer: ")
        if 1 <= opcion <= len(trainers):
            trainerSeleccionado = list(trainers.keys())[opcion - 1]
            break

    rutas["grupos"][grupoSeleccionado]["trainerEncargado"] = trainerSeleccionado
    if grupoSeleccionado not in trainers[trainerSeleccionado]["rutasAsignadas"]:
        trainers[trainerSeleccionado]["rutasAsignadas"].append(grupoSeleccionado)

    guardar(rutaTrainers, trainers)
    guardar(rutaRutas, rutas)

    print(f"\n✅ Trainer '{trainers[trainerSeleccionado]['nombres']} {trainers[trainerSeleccionado]['apellidos']}' asignado correctamente al grupo '{grupoSeleccionado}'.")
    pausar()

def matricularCamper():
    limpiar()
    rutaCampers = "data/campers.json"
    rutaRutas = "data/rutas.json"
    campers = cargar(rutaCampers)
    rutas = cargar(rutaRutas)

    # Se crea un nuevo diccionario por comprensión que filtra únicamente los campers cuyo estado es "aprobado".
    campersAprobados = {IDcamper : info for IDcamper, info in campers.items() if info["estado"] == "aprobado"}

    print("----MATRICULAR CAMPER----")
    print("\n----CAMPERS APROBADOS----")
    for IDcamper, info in campersAprobados.items():
        print(f"[ID: {IDcamper}]: 👤 {info['nombres']} {info['apellidos']}")

    while True:
        opcion = pedirEntero("\nSeleccione un camper: ")
        if 1 <= opcion <= len(campersAprobados):
            camperSeleccionado = list(campersAprobados.keys())[opcion - 1] # convierte las claves (IDs) en una lista
            break

    if campers[camperSeleccionado].get("ruta"): # devuelve el valor de la clave "ruta" (si existe) o None (si no).
        print("❌ Este camper ya está asignado a un grupo.")
        pausar()
        return

    print("\n---- GRUPOS DISPONIBLES ----")

    gruposDisponibles = {} # Diccionario vacío donde se guardarán grupos disponibles asociados a un número.
    contador = 1 # variable tipo int usada para numerar los grupos en pantalla.

    for nombreGrupo, info in rutas.get("grupos", {}).items():
        ocupados = len(info.get("campersAsignados", [])) # cantidad actual de campers asignados (usa .get() para evitar error si no existe).
        disponible = ocupados < info["capacidadMax"] # True si hay cupos (ocupados < capacidadMax), False si está llena.
        trainer = info.get("trainerEncargado", "no asignado") # nombre o ID del trainer asignado (si no hay, muestra "no asignado").
        rutaNombre = info.get("ruta", "desconocida")
        estado = "disponible" if disponible else "lleno"
        print(f"\n{contador}. {nombreGrupo} | Ruta: {rutaNombre} | Capacidad: {ocupados}/{info['capacidadMax']} | Trainer: {trainer} | Estado: {estado}")

        if disponible:
            gruposDisponibles[contador] = nombreGrupo

        contador += 1

    while True:
        opcion = pedirEntero("\nSeleccione un grupo disponible: ")
        if opcion in gruposDisponibles:
            grupoSeleccionado = gruposDisponibles[opcion]
            break

    fechaInicio = pedirFecha("Ingrese fecha de inicio (YYYY-MM-DD): ")
    fechaFin = pedirFecha("Ingrese fecha de fin (YYYY-MM-DD): ")
    #revisa si existe, si no la crea
    #setdefault() verifica si existe la clave "campersAsignados":
    #Si existe, devuelve su lista actual.
    #Si no existe, la crea vacía [] y luego la devuelve
    campersAsignados = rutas["grupos"][grupoSeleccionado].setdefault("campersAsignados", [])

    # Añade el ID del camper a la lista campersAsignados si no está ya incluido.
    if camperSeleccionado not in campersAsignados:
        campersAsignados.append(camperSeleccionado)

    #Obtiene la nota inicial del camper (si existe) y la añade al diccionario modulos.
    #Si el camper tiene nota, modulos = {"Nota Inicial": {...}}
    #Si no tiene, modulos = {}
    notaInicial = campers[camperSeleccionado].get("notaInicial")
    modulos = {"Nota Inicial": notaInicial} if notaInicial else {}

    #Itera sobre los módulos de la ruta del grupo y crea un espacio vacío {} en modulos para cada uno, garantizando que todos los módulos existan.
    rutaTemplate = rutas["grupos"][grupoSeleccionado]["ruta"]
    for moduloNombre in rutas["rutas"][rutaTemplate]["modulos"]:
        if moduloNombre not in modulos:
            modulos[moduloNombre] = {}

    # Aquí se crea una entrada dentro del diccionario matriculas del grupo:
    #setdefault("matriculas", {}) crea la clave "matriculas" si no existe.
    #Luego se añade una nueva matrícula para el camper seleccionado, donde:
    #Clave = ID del camper.
    #Valor = diccionario con fechas, trainer y módulos.
    rutas["grupos"][grupoSeleccionado].setdefault("matriculas", {})[camperSeleccionado] = {
        "fechaInicio": fechaInicio,
        "fechaFin": fechaFin,
        "trainer": rutas["grupos"][grupoSeleccionado].get("trainerEncargado", "no asignado"),
        "modulos": modulos
    }

    campers[camperSeleccionado]["estado"] = "cursando"
    campers[camperSeleccionado]["ruta"] = grupoSeleccionado

    guardar(rutaCampers, campers)
    guardar(rutaRutas, rutas)
    print(f"\n✅ Camper '{campers[camperSeleccionado]['nombres']} {campers[camperSeleccionado]['apellidos']}' matriculado en el grupo '{grupoSeleccionado}' con éxito.")
    pausar()

def consultarCamperEnRiesgo():
    limpiar()
    rutaCampers = "data/campers.json"
    rutaRutas = "data/rutas.json"
    campers = cargar(rutaCampers)
    rutas = cargar(rutaRutas)

    # Mostrar todos los campers inscritos
    campersInscritos = {ID: info for ID, info in campers.items() if info["estado"] == "inscrito"}
    print("----RIESGO DE LOS CAMPERS----")
    print("\n----CAMPERS INSCRITOS----")
    for ID, info in campersInscritos.items():
        print(f"{ID}: {info['nombres']} {info['apellidos']}")

    # Recorre todos los grupos existentes.
    #Para cada grupo (nombreGrupo), se obtiene el campo "matriculas" que contiene los campers inscritos en ese grupo.
    #Si no existe el campo "matriculas", se usa {} como valor por defecto para evitar errores.
    for nombreGrupo, infoGrupo in rutas.get("grupos", {}).items():
        matriculas = infoGrupo.get("matriculas", {})

        # Se recorre cada matrícula (camper inscrito en ese grupo).
        #Con campers.get(IDcamper, {}) se busca la información del camper.
        #Si el camper no está en estado "inscrito", se omite (continue) y no se evalúa.
        #Esto garantiza que solo los campers en estado "inscrito" sean analizados.
        for IDcamper, infoMatricula in matriculas.items():
            if campers.get(IDcamper, {}).get("estado") != "inscrito":
                continue

            modulos = infoMatricula.get("modulos", {}) # Extrae el campo "modulos" del camper dentro de ese grupo.Cada módulo puede contener notas teóricas, prácticas y quiz.

            for nombreModulo, notas in modulos.items():
                # Saltar módulos sin notas
                if notas.get("teorica") is None and notas.get("practica") is None and notas.get("quiz") is None:
                    continue

                # Calcular promedio ponderado Si alguna no existe, se toma 0 por defecto.
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

    # Mostrar campers en riesgo alto
    campersRiesgo = {ID: info for ID, info in campers.items() if info.get("riesgo") == "alto"}
    if campersRiesgo:
        print("\n---- CAMPERS EN RIESGO ALTO ----")
        for IDcamper, info in campersRiesgo.items():
            print(f"ID: {IDcamper} | Nombre: {info['nombres']} {info['apellidos']} | Riesgo: {info['riesgo']}")
    else:
        print("\n✅ No hay campers en riesgo alto actualmente.")

    print("\n✅ Se ha actualizado el riesgo de todos los campers inscritos según sus notas.")
    pausar()
    
def listarCampersInscritos():
    limpiar()
    ruta = "data/campers.json"
    campers = cargar(ruta)
    
    campersInscritos = {IDcamper : info for IDcamper, info in campers.items() if info["estado"] == "inscrito"}

    print("\n----CAMPERS INSCRITOS----")
    for IDcamper, info in campersInscritos.items():
        print(f"👤 ID: {IDcamper}: | Nombre :{info['nombres']} | Apellido :  {info['apellidos']} | Estado : {info['estado']}")
        print("-"*80)
    pausar()

def listarCampersAprobados():
    limpiar()
    ruta = "data/campers.json"
    campers = cargar(ruta)

    campersAprobados = {IDcamper : info for IDcamper, info in campers.items() if "notaInicial" in info and info["notaInicial"]["promedio"] >= 60}

    print("\n--------------------CAMPERS QUE APROBARON LA PRUEBA INICIAL-----------------------")
    for IDcamper, info in campersAprobados.items():
        print(f"👤 ID: {IDcamper}: | Nombre :{info['nombres']} | Apellido :  {info['apellidos']} | Estado : {info['estado']}")
        print("-"*80)
    pausar()

def listarTrainers():
    limpiar()
    ruta = "data/trainers.json"
    trainers = cargar(ruta)
    
    trainersActivos = {IDtrainer : info for IDtrainer, info in trainers.items() if info["estado"] == "activo"}

    print("\n---------------------------------------LISTA DE TRAINERS-----------------------------------------")
    for IDtrainer, info in trainersActivos.items():
        print(f"👤 ID: {IDtrainer}: | Nombre :{info['nombres']} | Apellido :  {info['apellidos']} | Estado : {info['estado']}")
        print("-"*80)
    pausar()
    
def listarCampersBajoRendimiento():
    limpiar()
    ruta = "data/campers.json"
    campers = cargar(ruta)
    
    campersRiesgo = {IDcamper : info for IDcamper, info in campers.items() if info["riesgo"] == "alto"}

    print("\n-------------------------------------CAMPERS BAJO RENDIMIENTO--------------------------------------------")
    for IDcamper, info in campersRiesgo.items():
        print(f"👤 ID: {IDcamper}: | Nombre :{info['nombres']} | Apellido :  {info['apellidos']} | Riesgo : {info['riesgo']}")
        print("-"*80)
    pausar()

def listarRutaCampersTrainers():
    limpiar()
    ruta = "data/rutas.json"
    rutaRutas = cargar(ruta)
    ruta = "data/campers.json"
    campers = cargar(ruta)
    ruta = "data/trainers.json"
    trainers = cargar(ruta)

    #nombreGrupo = nombre del grupo (ej: "Grupo1", "Grupo2").
    #infoGrupo = información completa del grupo (trainer, campers asignados, capacidad, etc.)
    for nombreGrupo, infoGrupo in rutaRutas.get("grupos", {}).items():
        # Obtener el ID del trainer encargado
        IDtrainer = infoGrupo.get("trainerEncargado", None)
        # Se verifica si el IDtrainer existe y está en el diccionario trainers:
        # Si existe, se obtiene su nombre completo (nombres + apellidos).
        # Si no existe o es None, se asigna "No asignado".
        if IDtrainer and IDtrainer in trainers:
            trainerNombre = f"{trainers[IDtrainer]['nombres']} {trainers[IDtrainer]['apellidos']}"
        else:
            trainerNombre = "No asignado"

        # Extrae la lista de campers asignados a ese grupo. Si el campo no existe, devuelve una lista vacía [].
        campersAsignados = infoGrupo.get("campersAsignados", [])

        rutaNombre = infoGrupo.get("ruta", "desconocida")
        print(f"\n---------------------------------- GRUPO: {nombreGrupo} | Ruta: {rutaNombre} | 👤 Trainer: {trainerNombre} -----------------------------------------------------------")

        if not campersAsignados:
            print("No hay campers asignados.")
        else:
            for IDcamper in campersAsignados:
                info = campers.get(IDcamper, {})
                print(f"👤 ID: {IDcamper} | Nombre: {info.get('nombres','')} {info.get('apellidos','')} | "f"Estado: {info.get('estado','')} | Riesgo: {info.get('riesgo','')}")
        print("-"*80)
    pausar()
    
def registrarNotasCoordinador():
    limpiar()
    rutaRutas = "data/rutas.json"
    rutaCampers = "data/campers.json"

    rutas = cargar(rutaRutas)
    campers = cargar(rutaCampers)

    print("----REGISTRAR NOTAS DE LOS MODULOS----")

    # Listar grupos disponibles
    grupos = rutas.get("grupos", {})
    if not grupos:
        print("❌ No hay grupos disponibles.")
        pausar()
        return

    print("\n---- GRUPOS DISPONIBLES ----")
    for i, (nombreGrupo, infoGrupo) in enumerate(grupos.items(), start=1):
        rutaNombre = infoGrupo.get("ruta", "desconocida")
        print(f"{i}. {nombreGrupo} | Ruta: {rutaNombre}")

    # Seleccionar grupo
    opcion = pedirEntero("\nSeleccione un grupo: ")
    grupoSeleccionado = list(grupos.keys())[opcion - 1]

    matriculas = rutas["grupos"][grupoSeleccionado].get("matriculas", {})

    if not matriculas:
        print("⚠️ No hay campers matriculados en este grupo todavía.")
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
    rutas["grupos"][grupoSeleccionado]["matriculas"][IDcamperSeleccionado]["modulos"][nombreModulo] = {
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

def mostrarResultadosModulos():
    limpiar()
    ruta = "data/rutas.json"
    rutaRutas = cargar(ruta)
    ruta = "data/campers.json"
    campers = cargar(ruta)
    ruta = "data/trainers.json"
    trainers = cargar(ruta)

    for nombreGrupo, infoGrupo in rutaRutas.get("grupos", {}).items():
        # Obtener el ID del trainer encargado
        IDtrainer = infoGrupo.get("trainerEncargado", None) # Se obtiene el ID del trainer encargado del grupo actual. Si no existe, devuelve None por defecto.
        if IDtrainer and IDtrainer in trainers:
            trainerNombre = f"{trainers[IDtrainer]['nombres']} {trainers[IDtrainer]['apellidos']}"
        else:
            trainerNombre = "No asignado"

        rutaNombre = infoGrupo.get("ruta", "desconocida")
        print(f"\n---- GRUPO: {nombreGrupo} | Ruta: {rutaNombre} | Trainer: {trainerNombre} ----")

        #Obtiene el diccionario matriculas del grupo actual, donde se almacenan los campers matriculados y sus notas por módulo.
        #Si no existe, devuelve un diccionario vacío {}.
        matriculas = infoGrupo.get("matriculas", {})

        # Crea un diccionario vacío donde se irán almacenando los resultados agrupados por módulo:
        #Cada clave será el nombre del módulo y su valor contendrá dos listas:
        modulosResumen = {}

        for IDcamper, infoMatricula in matriculas.items():
            camperInfo = campers.get(IDcamper, {}) # Obtiene la información personal del camper (nombre, apellidos, etc.) a partir del diccionario campers. Si no existe, devuelve {} para evitar errores.
            modulos = infoMatricula.get("modulos", {}) # Extrae los módulos cursados por ese camper dentro del grupo. Cada módulo incluye notas teóricas, prácticas y de quiz.

            # Recorre todos los módulos cursados por el camper.
            #nombreModulo: nombre del módulo (por ejemplo, "Python", "Bases de Datos").
            #notas: diccionario con las calificaciones de ese módul
            for nombreModulo, notas in modulos.items():
                # Calcular promedio ponderado
                notaT = notas.get("teorica", 0)
                notaP = notas.get("practica", 0)
                notaQ = notas.get("quiz", 0)
                promedio = notaT*0.3 + notaP*0.6 + notaQ*0.1

                # Si el módulo aún no existe en modulosResumen, se inicializa con las listas vacías 'aprobados' y 'reprobados'. Esto permite agrupar campers por módulo.
                if nombreModulo not in modulosResumen:
                    modulosResumen[nombreModulo] = {'aprobados': [], 'reprobados': []}

                # Nombre completo del camper
                nombreCompleto = camperInfo.get('nombres','') + " " + camperInfo.get('apellidos','')

                # Clasificar según promedio
                if promedio >= 60:
                    modulosResumen[nombreModulo]['aprobados'].append(nombreCompleto)
                else:
                    modulosResumen[nombreModulo]['reprobados'].append(nombreCompleto)

        # Luego de procesar todos los campers, se recorre el resumen para mostrar los resultados agrupados por módulo.
        for nombreModulo, datos in modulosResumen.items():
            aprobados = datos['aprobados']
            reprobados = datos['reprobados']

            print(f"\nMódulo: {nombreModulo}")
            print(f"✔️ Aprobados ({len(aprobados)}): {', '.join(aprobados) if aprobados else 'Ninguno'}")
            print(f"❌ Reprobados ({len(reprobados)}): {', '.join(reprobados) if reprobados else 'Ninguno'}")
            print("-"*80)
    pausar()

# [Comentarios con "colores" - ROJO para datos de campers, AZUL para trainers, VERDE para rutas/grupos]
# ROJO: Relacionado con campers.json (ID, nombres, apellidos, estado, riesgo, ruta, notas, historialEstados)
# def eliminarCamper():
#     limpiar()
#     ruta = "data/campers.json"
#     rutasRuta = "data/rutas.json"
#     campers = cargar(ruta)
#     rutas = cargar(rutasRuta)
#     print("----ELIMINAR CAMPER----")
#     IDcamper = val("Ingrese el numero de identificacion: ")
#     if not validadorCamperNoExiste(IDcamper, campers):
#         pausar()
#         return
#     # Confirmar eliminación
#     confirm = input(f"¿Está seguro de eliminar al camper {campers[IDcamper]['nombres']} {campers[IDcamper]['apellidos']}? (s/n): ").lower()
#     if confirm != 's':
#         print("Eliminación cancelada.")
#         pausar()
#         return
#     # Remover de grupo si asignado
#     grupo = campers[IDcamper].get("ruta")
#     if grupo and grupo in rutas.get("grupos", {}):
#         rutas["grupos"][grupo]["campersAsignados"] = [c for c in rutas["grupos"][grupo]["campersAsignados"] if c != IDcamper]
#         if IDcamper in rutas["grupos"][grupo].get("matriculas", {}):
#             del rutas["grupos"][grupo]["matriculas"][IDcamper]
#         guardar(rutasRuta, rutas)
#     # Eliminar del diccionario
#     del campers[IDcamper]
#     guardar(ruta, campers)
#     print("✅ Camper eliminado exitosamente.")
#     pausar()

# AZUL: Relacionado con trainers.json (ID, nombres, apellidos, telefono, correo, estado, rutasAsignadas)
# def eliminarTrainer():
#     limpiar()
#     ruta = "data/trainers.json"
#     rutasRuta = "data/rutas.json"
#     trainers = cargar(ruta)
#     rutas = cargar(rutasRuta)
#     print("----ELIMINAR TRAINER----")
#     IDtrainer = val("Ingrese el numero de identificacion del trainer: ")
#     if not validadorTrainer(IDtrainer, trainers):
#         pausar()
#         return
#     # Confirmar eliminación
#     confirm = input(f"¿Está seguro de eliminar al trainer {trainers[IDtrainer]['nombres']} {trainers[IDtrainer]['apellidos']}? (s/n): ").lower()
#     if confirm != 's':
#         print("Eliminación cancelada.")
#         pausar()
#         return
#     # Remover asignaciones de grupos
#     for grupo, info in rutas.get("grupos", {}).items():
#         if info.get("trainerEncargado") == IDtrainer:
#             rutas["grupos"][grupo]["trainerEncargado"] = "No asignado"
#     guardar(rutasRuta, rutas)
#     # Cambiar estado a inactivo en lugar de eliminar
#     trainers[IDtrainer]["estado"] = "inactivo"
#     guardar(ruta, trainers)
#     print("✅ Trainer marcado como inactivo exitosamente.")
#     pausar()

# VERDE: Relacionado con rutas.json (grupos: ruta, capacidadMax, campersAsignados, salon, horarios, trainerEncargado, matriculas)
# def eliminarGrupo():
#     limpiar()
#     ruta = "data/rutas.json"
#     rutas = cargar(ruta)
#     print("----ELIMINAR GRUPO----")
#     grupos = rutas.get("grupos", {})
#     if not grupos:
#         print("❌ No hay grupos disponibles.")
#         pausar()
#         return
#     print("\n----GRUPOS DISPONIBLES----")
#     for i, (nombreGrupo, info) in enumerate(grupos.items(), start=1):
#         print(f"{i}. {nombreGrupo}")
#     opcion = pedirEntero("\nSeleccione un grupo: ")
#     grupoSeleccionado = list(grupos.keys())[opcion - 1]
#     # Verificar si tiene campers asignados
#     if rutas["grupos"][grupoSeleccionado]["campersAsignados"]:
#         print("❌ No se puede eliminar un grupo con campers asignados.")
#         pausar()
#         return
#     # Confirmar
#     confirm = input(f"¿Está seguro de eliminar el grupo {grupoSeleccionado}? (s/n): ").lower()
#     if confirm != 's':
#         print("Eliminación cancelada.")
#         pausar()
#         return
#     del rutas["grupos"][grupoSeleccionado]
#     guardar(ruta, rutas)
#     print("✅ Grupo eliminado exitosamente.")
#     pausar()

# ROJO: Relacionado con campers.json (nombres, apellidos, direccion, telefonos)
# def editarInfoCamper():
#     limpiar()
#     ruta = "data/campers.json"
#     campers = cargar(ruta)
#     print("----EDITAR INFORMACIÓN DE CAMPER----")
#     IDcamper = val("Ingrese el numero de identificacion: ")
#     if not validadorCamperNoExiste(IDcamper, campers):
#         pausar()
#         return
#     camper = campers[IDcamper]
#     print(f"Información actual: {camper['nombres']} {camper['apellidos']}, Dirección: {camper['direccion']}, Celular: {camper['telefonos']['celular']}, Fijo: {camper['telefonos']['fijo']}")
#     # Editar
#     camper['nombres'] = val("Nuevos nombres: ")
#     camper['apellidos'] = val("Nuevos apellidos: ")
#     camper['direccion'] = val("Nueva dirección: ")
#     camper['telefonos']['celular'] = val("Nuevo celular: ")
#     camper['telefonos']['fijo'] = val("Nuevo fijo: ")
#     guardar(ruta, campers)
#     print("✅ Información actualizada.")
#     pausar()

# AZUL: Relacionado con trainers.json (nombres, apellidos, telefono, correo)
# def editarInfoTrainer():
#     limpiar()
#     ruta = "data/trainers.json"
#     trainers = cargar(ruta)
#     print("----EDITAR INFORMACIÓN DE TRAINER----")
#     IDtrainer = val("Ingrese el numero de identificacion del trainer: ")
#     if not validadorTrainer(IDtrainer, trainers):
#         pausar()
#         return
#     trainer = trainers[IDtrainer]
#     print(f"Información actual: {trainer['nombres']} {trainer['apellidos']}, Teléfono: {trainer['telefono']}, Correo: {trainer['correo']}")
#     # Editar
#     trainer['nombres'] = val("Nuevos nombres: ")
#     trainer['apellidos'] = val("Nuevos apellidos: ")
#     trainer['telefono'] = val("Nuevo teléfono: ")
#     trainer['correo'] = val("Nuevo correo: ")
#     guardar(ruta, trainers)
#     print("✅ Información actualizada.")
#     pausar()

def listarGruposDisponibles():
    limpiar()
    ruta = "data/rutas.json"
    rutas = cargar(ruta)
    print("----GRUPOS DISPONIBLES----")
    grupos = rutas.get("grupos", {})
    if not grupos:
        print("No hay grupos.")
        pausar()
        return
    for nombreGrupo, info in grupos.items():
        ocupados = len(info.get("campersAsignados", []))
        disponible = ocupados < info["capacidadMax"]
        estado = "Disponible" if disponible else "Lleno"
        print(f"{nombreGrupo}: {ocupados}/{info['capacidadMax']} - {estado}")
    pausar()

def listarCampersPorGrupo():
    limpiar()
    rutaRutas = "data/rutas.json"
    rutaCampers = "data/campers.json"
    rutas = cargar(rutaRutas)
    campers = cargar(rutaCampers)
    print("----LISTAR CAMPERS POR GRUPO----")
    grupos = rutas.get("grupos", {})
    if not grupos:
        print("No hay grupos.")
        pausar()
        return
    print("\n----GRUPOS----")
    for i, nombreGrupo in enumerate(grupos.keys(), start=1):
        print(f"{i}. {nombreGrupo}")
    opcion = pedirEntero("Seleccione un grupo: ")
    grupoSeleccionado = list(grupos.keys())[opcion - 1]
    print(f"\nCampers en {grupoSeleccionado}:")
    for IDcamper in rutas["grupos"][grupoSeleccionado].get("campersAsignados", []):
        info = campers.get(IDcamper, {})
        print(f"ID: {IDcamper} | {info.get('nombres','')} {info.get('apellidos','')} | Estado: {info.get('estado','')} | Riesgo: {info.get('riesgo','')}")
    pausar()

def consultarHistorialEstados():
    limpiar()
    ruta = "data/campers.json"
    campers = cargar(ruta)
    print("----HISTORIAL DE CAMBIOS DE ESTADO----")
    IDcamper = val("Ingrese el numero de identificacion: ")
    if not validadorCamperNoExiste(IDcamper, campers):
        pausar()
        return
    camper = campers[IDcamper]
    historial = camper.get("historialEstados", [])
    if not historial:
        print("No hay historial disponible.")
    else:
        for cambio in historial:
            print(f"Fecha: {cambio['fecha']} | Estado: {cambio['estado']} | Cambiado por: {cambio['cambiadoPor']}")
    pausar()

# def reasignarCamperGrupo():
#     """
#     Reasigna un camper a otro grupo disponible.
#     """
#     limpiar()
#     rutaCampers = "data/campers.json"
#     rutaRutas = "data/rutas.json"
#     campers = cargar(rutaCampers)
#     rutas = cargar(rutaRutas)

#     print("----REASIGNAR CAMPER A OTRO GRUPO----")

#     # Listar campers con grupo asignado
#     campersConGrupo = {ID: info for ID, info in campers.items() if info.get("ruta")}
#     if not campersConGrupo:
#         print("No hay campers asignados a grupos.")
#         pausar()
#         return

#     print("\n----CAMPERS CON GRUPO ASIGNADO----")
#     for i, (IDcamper, info) in enumerate(campersConGrupo.items(), start=1):
#         print(f"{i}. ID: {IDcamper} | Nombre: {info['nombres']} {info['apellidos']} | Grupo actual: {info['ruta']}")

#     opcion = pedirEntero("\nSeleccione un camper para reasignar: ")
#     if opcion < 1 or opcion > len(campersConGrupo):
#         print("Opción inválida.")
#         pausar()
#         return

#     camperSeleccionado = list(campersConGrupo.keys())[opcion - 1]
#     grupoActual = campers[camperSeleccionado].get("ruta")

#     # Listar grupos disponibles (con capacidad)
#     gruposDisponibles = {}
#     contador = 1
#     for nombreGrupo, info in rutas.get("grupos", {}).items():
#         ocupados = len(info.get("campersAsignados", []))
#         disponible = ocupados < info["capacidadMax"]
#         if disponible and nombreGrupo != grupoActual:
#             gruposDisponibles[contador] = nombreGrupo
#             print(f"{contador}. {nombreGrupo} (Capacidad: {ocupados}/{info['capacidadMax']})")
#             contador += 1

#     if not gruposDisponibles:
#         print("No hay grupos disponibles para reasignar.")
#         pausar()
#         return

#     opcionGrupo = pedirEntero("\nSeleccione el nuevo grupo: ")
#     if opcionGrupo not in gruposDisponibles:
#         print("Opción inválida.")
#         pausar()
#         return

#     nuevoGrupo = gruposDisponibles[opcionGrupo]

#     # Remover camper del grupo actual
#     if grupoActual and grupoActual in rutas.get("grupos", {}):
#         campersAsignados = rutas["grupos"][grupoActual].get("campersAsignados", [])
#         if camperSeleccionado in campersAsignados:
#             campersAsignados.remove(camperSeleccionado)
#         matriculas = rutas["grupos"][grupoActual].get("matriculas", {})
#         if camperSeleccionado in matriculas:
#             del matriculas[camperSeleccionado]

#     # Añadir camper al nuevo grupo
#     rutas["grupos"][nuevoGrupo].setdefault("campersAsignados", []).append(camperSeleccionado)
#     rutas["grupos"][nuevoGrupo].setdefault("matriculas", {})[camperSeleccionado] = {
#         "fechaInicio": None,
#         "fechaFin": None,
#         "trainer": rutas["grupos"][nuevoGrupo].get("trainerEncargado", "no asignado"),
#         "modulos": {}
#     }

#     # Actualizar ruta en campers.json
#     campers[camperSeleccionado]["ruta"] = nuevoGrupo

#     guardar(rutaCampers, campers)
#     guardar(rutaRutas, rutas)

#     print(f"\n✅ Camper '{campers[camperSeleccionado]['nombres']} {campers[camperSeleccionado]['apellidos']}' reasignado al grupo '{nuevoGrupo}'.")
#     pausar()

# def reasignarTrainerGrupo():
#     """
#     Reasigna un trainer a otro grupo disponible.
#     """
#     limpiar()
#     rutaTrainers = "data/trainers.json"
#     rutaRutas = "data/rutas.json"
#     trainers = cargar(rutaTrainers)
#     rutas = cargar(rutaRutas)

#     print("----REASIGNAR TRAINER A OTRO GRUPO----")

#     grupos = rutas.get("grupos", {})
#     if not grupos:
#         print("No hay grupos disponibles.")
#         pausar()
#         return

#     print("\n----GRUPOS----")
#     for i, (nombreGrupo, info) in enumerate(grupos.items(), start=1):
#         trainerID = info.get("trainerEncargado", "No asignado")
#         print(f"{i}. {nombreGrupo} | Trainer actual: {trainerID}")

#     opcionGrupo = pedirEntero("\nSeleccione un grupo para reasignar trainer: ")
#     if opcionGrupo < 1 or opcionGrupo > len(grupos):
#         print("Opción inválida.")
#         pausar()
#         return

#     grupoSeleccionado = list(grupos.keys())[opcionGrupo - 1]

#     print("\n----TRAINERS DISPONIBLES----")
#     trainersActivos = {ID: info for ID, info in trainers.items() if info.get("estado") == "activo"}
#     for i, (IDtrainer, info) in enumerate(trainersActivos.items(), start=1):
#         print(f"{i}. {info['nombres']} {info['apellidos']} | ID: {IDtrainer}")

#     opcionTrainer = pedirEntero("\nSeleccione un nuevo trainer: ")
#     if opcionTrainer < 1 or opcionTrainer > len(trainersActivos):
#         print("Opción inválida.")
#         pausar()
#         return

#     nuevoTrainerID = list(trainersActivos.keys())[opcionTrainer - 1]
#     trainerActualID = rutas["grupos"][grupoSeleccionado].get("trainerEncargado", None)

#     # Actualizar trainer en grupo
#     rutas["grupos"][grupoSeleccionado]["trainerEncargado"] = nuevoTrainerID

#     # Actualizar rutasAsignadas en trainers.json
#     if trainerActualID and trainerActualID in trainers:
#         if grupoSeleccionado in trainers[trainerActualID].get("rutasAsignadas", []):
#            trainers[trainerActualID]["rutasAsignadas"].remove(grupoSeleccionado)

#     if nuevoTrainerID in trainers:
#         if grupoSeleccionado not in trainers[nuevoTrainerID].get("rutasAsignadas", []):
#             trainers[nuevoTrainerID]["rutasAsignadas"].append(grupoSeleccionado)

#     guardar(rutaTrainers, trainers)
#     guardar(rutaRutas, rutas)

#     print(f"\n✅ Trainer reasignado al grupo '{grupoSeleccionado}'.")
#     pausar()

# ROJO/AZUL: Relacionado con campers.json y trainers.json (nombres, apellidos)
# def buscarUsuario():
#     limpiar()
#     print("----BUSCAR USUARIO----")
#     print("1. Buscar Camper")
#     print("2. Buscar Trainer")
#     opcion = pedirEntero("Seleccione una opción: ")
#     if opcion not in [1, 2]:
#         print("❌ Opción inválida.")
#         pausar()
#         return

#     termino = val("Ingrese el nombre o parte del nombre a buscar: ").lower()

#     if opcion == 1:
#         ruta = "data/campers.json"
#         usuarios = cargar(ruta)
#         tipo = "Camper"
#     else:
#         ruta = "data/trainers.json"
#         usuarios = cargar(ruta)
#         tipo = "Trainer"

#     resultados = []
#     for IDusuario, info in usuarios.items():
#         nombreCompleto = f"{info.get('nombres', '')} {info.get('apellidos', '')}".lower()
#         if termino in nombreCompleto:
#             resultados.append((IDusuario, info))

#     if not resultados:
#         print(f"❌ No se encontraron {tipo.lower()}s que coincidan con '{termino}'.")
#         pausar()
#         return

#     print(f"\n---- RESULTADOS DE BÚSQUEDA PARA '{termino.upper()}' ----")
#     for i, (IDusuario, info) in enumerate(resultados, start=1):
#         print(f"{i}. ID: {IDusuario} | Nombre: {info.get('nombres', '')} {info.get('apellidos', '')}")

#     # Opcional: seleccionar uno para ver detalles
#     verDetalles = input("\n¿Desea ver detalles de alguno? (s/n): ").lower()
#     if verDetalles == 's':
#         seleccion = pedirEntero("Seleccione el número: ")
#         if 1 <= seleccion <= len(resultados):
#             IDseleccionado, infoSeleccionado = resultados[seleccion - 1]
#             print(f"\n---- DETALLES DE {tipo.upper()} ----")
#             print(f"ID: {IDseleccionado}")
#             for clave, valor in infoSeleccionado.items():
#                 print(f"{clave.capitalize()}: {valor}")
#         else:
#             print("❌ Selección inválida.")
#     pausar()
