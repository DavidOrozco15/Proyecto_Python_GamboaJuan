import json
from modules.utils import cargar, guardar, val, validadorCamper, validadorTrainer, validadorCamperNoExiste, validarEstado, pedirEntero, pedirFloat, pausar, limpiar, pedirFecha
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
    validadorCamper(IDcamper, campers) # Verifica que el ID no esté ya registrado en la base de datos

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
    validadorTrainer(IDtrainer, trainers) # Se verifica que este ID no exista ya en el archivo JSON.

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
    print("----REGISTRO DE NOTAS----")
    IDcamper = val("Ingrese el numero de identificacion: ") #valida que la entrada no este vacia
    validadorCamperNoExiste(IDcamper, campers)  # Se valida que el camper exista en la base de datos.

    # Si el camper existe, se obtiene su información para mostrarla al usuario.
    if IDcamper in campers:
        Id = campers[IDcamper] # Se extrae la información del camper mediante su ID.
        print(f"\n Camper ID:{IDcamper} | Nombre: {Id['nombres']} Estado: {Id['estado']}") # Se imprime información básica del camper: ID, nombre y estado actual.

    # "pedirFloat()" asegura que se ingrese un número decimal válido entre 0 y 100.
    notaT = pedirFloat("Ingresa el valor de la Nota Teorica (0-100)")
    notaP = pedirFloat("Ingresa el valor de la Nota Practica (0-100)")

    promedio = (notaT + notaP)/2

    if promedio >= 60:
        campers[IDcamper]["estado"] = "aprobado"
        print("El Camper aprobo exitosamente.")
    elif promedio < 60:
        print("El Camper debe volver a intentarlo.")
        campers[IDcamper]["estado"] = "inscrito"
    
    # Se guarda la información de notas dentro del diccionario del camper.
    # Se crea una nueva clave "notaInicial" donde se almacenan las notas y el promedio.
    campers[IDcamper]["notaInicial"] = {
        "teorica": notaT,
        "practica": notaP,
        "promedio": promedio
    }
    guardar(ruta, campers)

    print(f"Promedio final: {promedio:.2f} | Estado: {campers[IDcamper]['estado']}") # Se muestra el promedio final y el nuevo estado del camper en consola.
    pausar()

def crearRuta():
    limpiar()
    # Lista de horarios disponibles para asignar a las rutas.
    # 🔹 Tipo: list (lista de strings)
    horarios = ["08:00-12:00", "12:00-16:00", "16:00-20:00"]
    # Lista de salones disponibles para las clases.
    # 🔹 Tipo: list (lista de strings)
    salones = ["salon 1", "salon 2", "salon 3"]

    # Diccionario que contiene los módulos base de todas las rutas.
    # Cada clave es un área (por ejemplo "Bases de datos") y su valor es una lista de tecnologías.
    # 🔹 Tipo: dict que contiene listas
    modulosRuta = {
        "Fundamentos de programación": ["Introducción a la algoritmia", "PSeInt", "Python"],
        "Programación Web": ["HTML", "CSS", "Bootstrap"],
        "Bases de datos": ["MySQL", "MongoDB", "PostgreSQL"]
    }

    ruta = "data/rutas.json"
    rutas = cargar(ruta)

    print("----CREAR UNA RUTA----")
    nombreRuta = val("Ingrese el nombre de la ruta: ")

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
    # Se muestran las opciones numeradas usando enumerate()
    for i, db in enumerate(modulosRuta["Bases de datos"], 1): #db en el for nombre de la base de datos en cada iteración (ej. "MySQL").
        print(f"{i}. {db}")

    # Bucle para validar la selección del usuario
    while True:
        dbInput = input("Ingrese números separados por coma (Enter para ninguna): ").strip()

        # Si no ingresa nada, no se seleccionan bases de datos, Si el usuario presiona Enter sin escribir nada: se interpreta como "no quiero ninguna base de datos". Se asigna basesSeleccionadas = [] y se sale del while.
        if not dbInput:
            basesSeleccionadas = []
            break
        # Separar por coma y limpiar espacios
        indicesStr = dbInput.split(",") # indicesStr — list[str] Resultado de dbInput.split(","). Cada elemento es una subcadena separada por comas (aún sin limpiar).
        indices = [] # indices — list[int] Lista que acumula los números válidos convertidos a int. Ej: [1, 3].
        for idx in indicesStr: # idx (en el for idx in indicesStr) — str Cada elemento de indicesStr, tras idx.strip() contiene el texto limpio de cada número introducido por el usuario.
            idx = idx.strip() # Limpia espacios alrededor del número. Si venía " 3 ", ahora es "3".

            # Validar que cada elemento sea un número
            if not idx.isdigit():
                print("❌ Entrada inválida. Solo números separados por coma.")
                break
            num = int(idx) # num — int Conversión a entero de idx. Usado para validar rango y para añadir a indices.

            # Validar que esté dentro del rango
            if num < 1 or num > len(modulosRuta["Bases de datos"]): # Valida que el número esté entre 1 y la cantidad de bases disponibles. Si no, muestra error y break del for (se pedirá la entrada otra vez).
                print("❌ Número fuera de rango.")
                break
            indices.append(num) # Si pasó las validaciones, guarda el entero en indices.
        else:
            if len(indices) > 2: # Verifica que el usuario no haya seleccionado más de 2 opciones. Si son más, muestra mensaje de error y el while se repite (no se ejecuta el break final).
                print("❌ Máximo dos opciones.")
            else:
                #Si hay 0, 1 o 2 índices válidos: convierte cada índice (1-based) en el nombre real tomando la lista modulosRuta["Bases de datos"] con i-1 (para pasar a índice 0-based).
                # — Asigna la lista resultante a basesSeleccionadas y sale del while con break (entrada aceptada).
                basesSeleccionadas = [modulosRuta["Bases de datos"][i-1] for i in indices] # basesSeleccionadas — list[str] (resultado final) Lista con nombres exactos de las bases de datos elegidas. Ej: ["MySQL", "PostgreSQL"]. Si el usuario no selecciona nada, será [].
                break

    # 🔹 Capacidad máxima de la ruta
    while True:
        capacidadInput = input("Ingrese la capacidad máxima de la ruta (Enter para 33): ").strip()
        if not capacidadInput:
            capacidad = 33 # Valor por defecto
            break
        if capacidadInput.isdigit() and int(capacidadInput) > 0:
            capacidad = int(capacidadInput)
            break
        else:
            print("❌ Ingrese un número entero positivo o deje vacío para el valor por defecto (33).")

    # Selección de salón
    print("\nSalones de entrenamiento disponibles:")
    # (índice, elemento)
    for i, salon in enumerate(salones, 1):
        print(f"{i}. {salon}")
    while True:
        seleccion = pedirEntero("Seleccione un salon de entrenamiento (1-3): ")
        if 1 <= seleccion <= len(salones): # Debe ser mayor o igual a 1 (la primera opción),Y menor o igual a len(salones) (el número total de opciones disponibles).
            # Accede a la lista salones usando índices basados en 0.
            #Como el usuario eligió un número entre 1 y N, se resta 1 para convertirlo al índice correcto de la lista (que comienza en 0).
            #Ejemplo:
            #Si seleccion = 1 → salonSeleccionado = salones[0] = "salon 1"
            #Si seleccion = 3 → salonSeleccionado = salones[2] = "salon 3"
            #Guarda el nombre del salón escogido (tipo str) en salonSeleccionado.
            salonSeleccionado = salones[seleccion - 1]
            break

    # Horarios disponibles según salón
    ocupadosPorSalon = {} # Un diccionario vacío que servirá para agrupar horarios ocupados por cada salón.
    for r in rutas.values(): # Recorre todos los valores del diccionario rutas
        s = r["salon"] # Extrae de cada ruta el nombre del salón donde se dicta.
        for h in r["horarios"]: # Recorre la lista de horarios asociados a esa ruta.
            if s not in ocupadosPorSalon: # Verifica si el salón s ya tiene una entrada en el diccionario ocupadosPorSalon.
                ocupadosPorSalon[s] = [] # Inicializa una lista vacía para ese salón si no existía antes.
            ocupadosPorSalon[s].append(h) # Agrega el horario actual (h) a la lista de horarios ocupados del salón s.

    # Crea una lista por comprensión con los horarios que están disponibles (no ocupados) en el salón seleccionado.
    #horarios es una lista general de todos los horarios posibles (por ejemplo ["8:00-10:00", "10:00-12:00", "14:00-16:00"])
    #ocupadosPorSalon.get(salonSeleccionado, []) obtiene la lista de horarios ocupados en ese salón.
    #Si el salón no aparece en el diccionario (porque está vacío), devuelve una lista vacía [].
    #if h not in ... filtra y deja solo los horarios que no están ocupados.
    disponibles = [h for h in horarios if h not in ocupadosPorSalon.get(salonSeleccionado, [])]
    if not disponibles:
        print(f"❌ No hay horarios disponibles para {salonSeleccionado}.")
        pausar()
        return


    print(f"\nHorarios disponibles para {salonSeleccionado}:")

    #Recorre la lista de horarios disponibles (disponibles), generando un índice numérico que inicia en 1.
    # i → número de opción (1, 2, 3, …)
    # h → horario (cadena de texto)
    for i, h in enumerate(disponibles, 1):
        print(f"{i}. {h}")
    while True:
        seleccionHorario = pedirEntero("Seleccione un horario: ")
        if 1 <= seleccionHorario <= len(disponibles): # Verifica si la opción seleccionada está dentro del rango válido.
            horarioSeleccionado = [disponibles[seleccionHorario - 1]]  # Toma el horario seleccionado (restando 1 porque los índices en listas empiezan en 0) y lo guarda como una lista con un solo elemento.
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
        "trainerEncargado": "No asignado", # str → campo pendiente de asignar
        "matriculas": {} # dict → registro de inscripciones futuras
    }

    # Se añade la nueva ruta al diccionario de rutas existentes, usando el nombre como clave
    rutas[nombreRuta] = nuevaRuta
    guardar(ruta, rutas)
    print(f"✅ Ruta '{nombreRuta}' creada correctamente en {salonSeleccionado} con horario {horarioSeleccionado[0]}.")
    pausar()

def cambiarEstado():
    limpiar()
    ruta = "data/campers.json"
    campers = cargar(ruta)
    print("----CAMBIAR ESTADO MANUAL----")
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
            print("❌ Estado inválido. Debe ser uno de:", ", ".join(estados)) # join transforma la lista de estados en una sola cadena.
    
    campers[IDcamper]["estado"] = nuevoEstado # Actualiza directamente el valor de la clave estado del camper seleccionado dentro del diccionario campers.
    guardar(ruta, campers)
    pausar()

def asignarTrainerRuta():
    limpiar()
    rutaTrainers = "data/trainers.json"
    rutaRutas = "data/rutas.json"
    trainers = cargar(rutaTrainers)
    rutas = cargar(rutaRutas)

    print("----ASIGNACION DE RUTA A TRAINER----")
    print("\n----RUTAS DISPONIBLES----")

    #Recorre el diccionario rutas con enumerate, lo que devuelve:
    #i: número de índice (desde 1),
    #nombreRuta: nombre de la ruta (clave del diccionario),
    #info: subdiccionario con los datos de esa ruta.
    #rutas.items() devuelve tuplas:
    for i, (nombreRuta, info) in enumerate(rutas.items(), start=1):
        print(f"\n{i}. {nombreRuta} | Capacidad: {info['capacidadMax']} | Salón: {info['salon']} | Trainer: {info.get('trainerEncargado', 'No asignado')}")
    
    while True:
        opcion = pedirEntero("\nSeleccione una ruta: ")
        if 1 <= opcion <= len(rutas): # Verifica que el número ingresado esté dentro del rango válido (entre 1 y la cantidad de rutas existentes).
            rutaSeleccionada = list(rutas.keys())[opcion - 1] # Convierte las claves del diccionario rutas en una lista y selecciona la ruta elegida. Se usa opcion - 1 porque los índices en listas comienzan en 0.
            break
        
    print("\n----TRAINERS DISPONIBLES----")
    for i, (IDtrainer, info) in enumerate(trainers.items(), start=1):
        print(f"\n{i}. {info['nombres']} {info['apellidos']} | ID: {IDtrainer}")

    while True:
        opcion = pedirEntero("\nSeleccione un trainer: ")
        if 1 <= opcion <= len(trainers):
            trainerSeleccionado = list(trainers.keys())[opcion - 1]
            # Validar si el trainer ya tiene una ruta asignada
            if trainers[trainerSeleccionado]["rutasAsignadas"]: # Verifica si el trainer ya tiene rutas asignadas (si su lista rutasAsignadas no está vacía). Si la lista tiene al menos un elemento, significa que ya está asignado a una ruta.
                print("❌ Este trainer ya está asignado a una ruta. Seleccione otro trainer.")
                continue # Vuelve al inicio del bucle para forzar al usuario a elegir otro trainer.
            break

    rutas[rutaSeleccionada]["trainerEncargado"] = trainerSeleccionado # Asigna el ID del trainer dentro de la ruta seleccionada.
    if rutaSeleccionada not in trainers[trainerSeleccionado]["rutasAsignadas"]: # Verifica que la ruta no esté ya en la lista de rutas del trainer.
        trainers[trainerSeleccionado]["rutasAsignadas"].append(rutaSeleccionada) # Agrega el nombre de la ruta a la lista rutasAsignadas del trainer.

    guardar(rutaTrainers, trainers)
    guardar(rutaRutas, rutas)

    print(f"\n✅ Trainer '{trainers[trainerSeleccionado]['nombres']} {trainers[trainerSeleccionado]['apellidos']}' asignado correctamente a la ruta '{rutaSeleccionada}'.")
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
        print("❌ Este camper ya está asignado a una ruta.")
        pausar()
        return

    print("\n---- RUTAS DISPONIBLES ----")

    rutasDisponibles = {} # Diccionario vacío donde se guardarán rutas disponibles asociadas a un número.
    contador = 1 # variable tipo int usada para numerar las rutas en pantalla.

    for nombreRuta, info in rutas.items():
        ocupados = len(info.get("campersAsignados", [])) # cantidad actual de campers asignados (usa .get() para evitar error si no existe).
        disponible = ocupados < info["capacidadMax"] # True si hay cupos (ocupados < capacidadMax), False si está llena.
        trainer = info.get("trainerEncargado", "no asignado") # nombre o ID del trainer asignado (si no hay, muestra "no asignado").
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

    fechaInicio = pedirFecha("Ingrese fecha de inicio (YYYY-MM-DD): ")
    fechaFin = pedirFecha("Ingrese fecha de fin (YYYY-MM-DD): ")
    #revisa si existe, si no la crea
    #setdefault() verifica si existe la clave "campersAsignados":
    #Si existe, devuelve su lista actual.
    #Si no existe, la crea vacía [] y luego la devuelve
    campersAsignados = rutas[rutaSeleccionada].setdefault("campersAsignados", [])

    # Añade el ID del camper a la lista campersAsignados si no está ya incluido.
    if camperSeleccionado not in campersAsignados:
        campersAsignados.append(camperSeleccionado)

    #Obtiene la nota inicial del camper (si existe) y la añade al diccionario modulos.
    #Si el camper tiene nota, modulos = {"Nota Inicial": {...}}
    #Si no tiene, modulos = {}
    notaInicial = campers[camperSeleccionado].get("notaInicial")
    modulos = {"Nota Inicial": notaInicial} if notaInicial else {}

    #Itera sobre los módulos de la ruta y crea un espacio vacío {} en modulos para cada uno, garantizando que todos los módulos existan.
    for moduloNombre in rutas[rutaSeleccionada]["modulos"]:
        if moduloNombre not in modulos:
            modulos[moduloNombre] = {}

    # Aquí se crea una entrada dentro del diccionario matriculas de la ruta:
    #setdefault("matriculas", {}) crea la clave "matriculas" si no existe.
    #Luego se añade una nueva matrícula para el camper seleccionado, donde:
    #Clave = ID del camper.
    #Valor = diccionario con fechas, trainer y módulos.
    rutas[rutaSeleccionada].setdefault("matriculas", {})[camperSeleccionado] = {
        "fechaInicio": fechaInicio,
        "fechaFin": fechaFin,
        "trainer": rutas[rutaSeleccionada].get("trainerEncargado", "no asignado"),
        "modulos": modulos
    }

    campers[camperSeleccionado]["estado"] = "cursando"
    campers[camperSeleccionado]["ruta"] = rutaSeleccionada

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
    print("----RIESGO DE LOS CAMPERS----")
    print("\n----CAMPERS INSCRITOS----")
    for ID, info in campersInscritos.items():
        print(f"{ID}: {info['nombres']} {info['apellidos']}")

    # Recorre todas las rutas existentes.
    #Para cada ruta (nombreRuta), se obtiene el campo "matriculas" que contiene los campers inscritos en esa ruta.
    #Si no existe el campo "matriculas", se usa {} como valor por defecto para evitar errores.
    for nombreRuta, infoRuta in rutas.items():
        matriculas = infoRuta.get("matriculas", {})

        # Se recorre cada matrícula (camper inscrito en esa ruta).
        #Con campers.get(IDcamper, {}) se busca la información del camper.
        #Si el camper no está en estado "inscrito", se omite (continue) y no se evalúa.
        #Esto garantiza que solo los campers en estado "inscrito" sean analizados.
        for IDcamper, infoMatricula in matriculas.items():
            if campers.get(IDcamper, {}).get("estado") != "inscrito":
                continue

            modulos = infoMatricula.get("modulos", {}) # Extrae el campo "modulos" del camper dentro de esa ruta.Cada módulo puede contener notas teóricas, prácticas y quiz.

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
    
    #nombreRuta = nombre de la ruta (ej: "Python", "Java").
    #infoRuta = información completa de esa ruta (trainer, campers asignados, capacidad, etc.)
    for nombreRuta, infoRuta in rutaRutas.items():
        # Obtener el ID del trainer encargado
        IDtrainer = infoRuta.get("trainerEncargado", None)
        # Se verifica si el IDtrainer existe y está en el diccionario trainers:
        # Si existe, se obtiene su nombre completo (nombres + apellidos).
        # Si no existe o es None, se asigna "No asignado".
        if IDtrainer and IDtrainer in trainers:
            trainerNombre = f"{trainers[IDtrainer]['nombres']} {trainers[IDtrainer]['apellidos']}"
        else:
            trainerNombre = "No asignado"

        # Extrae la lista de campers asignados a esa ruta. Si el campo no existe, devuelve una lista vacía [].
        campersAsignados = infoRuta.get("campersAsignados", [])

        print(f"\n---------------------------------- RUTA: {nombreRuta} | 👤 Trainer: {trainerNombre} -----------------------------------------------------------")
        
        if not campersAsignados:
            print("No hay campers asignados.")
        else:
            for IDcamper in campersAsignados:
                info = campers.get(IDcamper, {})
                print(f"👤 ID: {IDcamper} | Nombre: {info.get('nombres','')} {info.get('apellidos','')} | "f"Estado: {info.get('estado','')} | Riesgo: {info.get('riesgo','')}")
        print("-"*80)
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
        IDtrainer = infoRuta.get("trainerEncargado", None) # Se obtiene el ID del trainer encargado de la ruta actual. Si no existe, devuelve None por defecto.
        if IDtrainer and IDtrainer in trainers:
            trainerNombre = f"{trainers[IDtrainer]['nombres']} {trainers[IDtrainer]['apellidos']}"
        else:
            trainerNombre = "No asignado"
            
        print(f"\n---- RUTA: {nombreRuta} | Trainer: {trainerNombre} ----")
        
        #Obtiene el diccionario matriculas de la ruta actual, donde se almacenan los campers matriculados y sus notas por módulo.
        #Si no existe, devuelve un diccionario vacío {}.
        matriculas = infoRuta.get("matriculas", {})
        
        # Crea un diccionario vacío donde se irán almacenando los resultados agrupados por módulo:
        #Cada clave será el nombre del módulo y su valor contendrá dos listas:
        modulosResumen = {}
        
        for IDcamper, infoMatricula in matriculas.items():
            camperInfo = campers.get(IDcamper, {}) # Obtiene la información personal del camper (nombre, apellidos, etc.) a partir del diccionario campers. Si no existe, devuelve {} para evitar errores.
            modulos = infoMatricula.get("modulos", {}) # Extrae los módulos cursados por ese camper dentro de la ruta. Cada módulo incluye notas teóricas, prácticas y de quiz.

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