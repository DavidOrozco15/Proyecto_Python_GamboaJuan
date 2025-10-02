import json
from utils import cargar, guardar, val, validadorCamper, validadorTrainer, valFloat, validadorCamperNoExiste, validarEstado
import modules.messages as m

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
        "medio",
        "alto"
    )


def registrarCamper():
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

def registrarTrainer():
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
        "nombre": nombre,
        "apellido": apellido,
        "telefono": telefono,
        "correo": correo,
        "estado": estado,
        "rutasAsignadas": []
    }

    trainers[IDtrainer] = trainer
    guardar(ruta, trainers)

def registrarNotas():
    ruta = "data/campers.json"
    campers = cargar(ruta)

    IDcamper = val("Ingrese el numero de identificacion: ") #valida que la entrada no este vacia
    validadorCamper(IDcamper, campers) #Valida que no este en campers
    validadorCamperNoExiste(IDcamper, campers)

    if IDcamper in campers:
        Id = campers[IDcamper]
        print(f"\n Camper ID:{IDcamper} | Nombre: {Id['nombre']} Estado: {Id['estado']}")

    notaT = valFloat("Ingresa el valor de la Nota Teorica (0-100)")
    notaP = valFloat("Ingresa el valor de la Nota Practica (0-100)")

    promedio = (notaT + notaP)/2

    if promedio >= 60:
        campers[IDcamper]["estado"] = "aprobado"
        print("El Camper aprobo exitosamente.")
    elif promedio < 60:
        print("El Camper debe volver a intentarlo.")
        campers[IDcamper]["estado"] = "en proceso de ingreso"
    else:
        None


    campers[IDcamper]["notaInicial"] = {
        "teorica": notaT,
        "practica": notaP,
        "promedio": promedio
    }
    guardar(ruta, campers)

    print(f"Promedio final: {promedio:.2f} | Estado: {campers[IDcamper]['estado']}")

def crearRuta():

    horarios = ["08:00-12:00", "12:00-16:00", "16:00-20:00"]
    salones = ["salon 1", "salon 2", "salon 3"]
    modulosRuta = {
        "Fundamentos de programación": ["Introducción a la algoritmia", "PSeInt", "Python"],
        "Programación Web": ["HTML", "CSS", "Bootstrap"],
        "Bases de datos": ["MySQL", "MongoDB", "PostgreSQL"]
    }

    ruta = "data/rutas.json"
    rutas = cargar(ruta)

    nombreRuta = input("Ingrese el nombre de la ruta: ")
    m.rutasFijas()

    print("Programacion Formal (escoge una opcion): ")
    print("1. Java | 2. JavaScript | 3. C#")
    formal = input()
    if formal == 1:
        formal = "java"
    elif formal == 2:
        formal = "javascript"
    elif formal == 3:
        formal = "c#"
    
    print("Backend (escoge una opcion): ")
    print("1. NodeJS | 2. SpringBoot | 3. Netcore | 4. Express")
    backend = input()
    if backend == 1:
        backend = "nodejs"
    elif backend == 2:
        backend = "springboot"
    elif backend == 3:
        backend = "netcore"
    elif backend == 4:
        backend = "express"

    capacidad = input("Ingrese la capacidad máxima de la ruta (Enter para 33): ")
    if capacidad.strip() == "":
        capacidad = 33
    else:
        capacidad = int(capacidad)
    
    print("\Salones de entrenamiento disponibles:")
    for i, salon in enumerate(salones, 1):
        print(f"{i}. {salon}")
    while True:
        seleccion = int(input("Seleccione un salon de entrenamiento (1-3): "))
        if 1 <= seleccion <= len(salones):
            salonSeleccionado = salones[seleccion - 1]
            break
        else:
            print("❌ Selección inválida. Intente nuevamente.")
    
    nuevaRuta = {
    "modulos": {
        **modulosRuta,
        "Programación formal": [formal],
        "Backend": [backend]
    },
    "capacidadMax": capacidad,
    "campersAsignados": [],
    "salon": salonSeleccionado,
    "horarios": horarios
    }
    rutas[nombreRuta] = nuevaRuta
    guardar(ruta, rutas)
    print(f"✅ Ruta '{nombreRuta}' creada correctamente.")

def cambiarEstado():
    ruta = "data/campers.json"
    campers = cargar(ruta)

    IDcamper = val("Ingrese el numero de identificacion: ") #valida que la entrada no este vacia
    validadorCamper(IDcamper, campers) #Valida que no este en campers
    validadorCamperNoExiste(IDcamper, campers)

    Id = campers[IDcamper]
    print(f"\n Camper ID:{IDcamper} | Nombre: {Id['nombre']} Estado: {Id['estado']}")

    print(estados).strip
    while True:
        nuevoEstado = input("Ingrese el nuevo estado de los mostrados: ")
        if validarEstado(nuevoEstado):
            break  # estado válido, salimos del bucle
        else:
            print("❌ Estado inválido. Debe ser uno de:", ", ".join(estados))
    
    campers[IDcamper]["estado"] = nuevoEstado
    guardar(ruta, campers)

def asignarTrainerRuta():
    rutaTrainers = "data/trainers.json"
    rutaRutas = "data/rutas.json"
    trainers = cargar(rutaTrainers)
    rutas = cargar(rutaRutas)

    print("\n----RUTAS DISPONIBLES----")
    for i, (nombreRuta, info) in enumerate(rutaRutas.items(), start=1):
        print(f"{i}. {nombreRuta} | Capacidad: {info['capacidad_max']} | Salón: {info['salon']} | Trainer: {info.get('trainer_encargado', 'No asignado')}")
    
    while True:
        opcion = int(input("Seleccione una ruta: "))
        if 1 <= opcion <= len(rutas):
            rutaSeleccionada = list(rutas.keys())[opcion - 1]
            break
        else:
            print("❌ Selección inválida. Intente nuevamente.")

    print("\n----TRAINERS DISPONIBLES----")
    for i, (IDtrainer, info) in enumerate(trainers.items(), start=1):
        print(f"{i}. {info['nombre']} {info['apellido']} | ID: {IDtrainer}")

    while True:
        opcion = int(input("Seleccione un trainer: "))
        if 1 <= opcion <= len(trainers):
            trainerSeleccionado = list(trainers.keys())[opcion - 1]
            break
        else:
            print("❌ Selección inválida. Intente nuevamente.")

    rutas[rutaSeleccionada]["trainerEncargado"] = trainerSeleccionado
    guardar(rutaRutas, rutas)

    print(f"\n✅ Trainer '{trainers[trainerSeleccionado]['nombre']} {trainers[trainerSeleccionado]['apellido']}' asignado correctamente a la ruta '{rutaSeleccionada}'.")

def matricularCamper():
    rutaCampers = "data/campers.json"
    rutaRutas = "data/rutas.json"
    campers = cargar(rutaCampers)
    rutas = cargar(rutaRutas)

    campersAprobados = {IDcamper : info for IDcamper, info in campers.items() if info["estado"] == "aprobado"}

    print("\n----CAMPERS APROBADOS----")
    for IDcamper, info in campersAprobados.items():
        print(f"{IDcamper}: {info['nombre']} {info['apellido']}")

    while True:
        opcion = int(input("Seleccione un camper: "))
        if 1 <= opcion <= len(campersAprobados):
            camperSeleccionado = list(campersAprobados.keys())[opcion - 1]
            break
        else:
            print("❌ Selección inválida. Intente nuevamente.")

    print("\n---- RUTAS DISPONIBLES ----")

    rutasDisponibles = {}
    contador = 1

    for nombreRuta, info in rutas.items():
        ocupados = len(info.get("campersAsignados", [])) #para mirar cuantos campers ya estan asignados
        disponible = ocupados < info["capacidadMax"] # mirar si aun hay espacio
        trainer = info.get("trainerEncargado", "no asignado") #trainer asignado o no
        estado = "disponible" if disponible else "lleno"
        print(f"{contador}. {nombreRuta} | Capacidad: {ocupados}/{info['capacidadMax']} | Trainer: {trainer} | Estado: {estado}")
    
        if disponible:
            rutasDisponibles[contador] = nombreRuta

        contador += 1

    while True:
        opcion = int(input("Seleccione una ruta disponible: "))
        if opcion in rutasDisponibles:
            rutaSeleccionada = rutasDisponibles[opcion]
            break
        else:
            print("❌ Selección inválida o ruta llena. Intente nuevamente.")

    fechaInicio = input("Ingrese fecha de inicio (YYYY-MM-DD): ")
    fechaFin = input("Ingrese fecha de fin (YYYY-MM-DD): ")
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
    print(f"\n✅ Camper '{campers[camperSeleccionado]['nombre']} {campers[camperSeleccionado]['apellido']}' matriculado en la ruta '{rutaSeleccionada}' con éxito.")

def consultarCamperEnRiesgo():
    rutaCampers = "data/campers.json"
    rutaRutas = "data/rutas.json"
    campers = cargar(rutaCampers)
    rutas = cargar(rutaRutas)

    # Mostrar todos los campers inscritos
    campersInscritos = {ID: info for ID, info in campers.items() if info["estado"] == "inscrito"}
    print("\n----CAMPERS INSCRITOS----")
    for ID, info in campersInscritos.items():
        print(f"{ID}: {info['nombre']} {info['apellido']}")

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

    # Guardar cambios una sola vez al final
    guardar(rutaCampers, campers)
    print("\n✅ Se ha actualizado el riesgo de todos los campers inscritos según sus notas.")

