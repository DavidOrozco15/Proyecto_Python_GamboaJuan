import modules.utils as u
import modules.messages as mgs

def login():
    while True:
        opcion = mgs.menuLog()
        match opcion:
            case 1:
                # Aquí iría la lógica para iniciar sesión
                pass
            case 0:
                print("¡Hasta luego! 👋")
                break
            case _:
                u.validacionOpcion()
                u.pausar()
                u.limpiar()

def menu_coordinador():
    while True:
        opcion = mgs.menuCoordinador()
        match opcion:
            case 1:
                # Registrar Camper
                pass
            case 2:
                # Registrar Trainer
                pass
            case 3:
                # Crear Ruta de entrenamiento
                pass
            case 4:
                # Crear área de entrenamiento
                pass
            case 5:
                # Asignar Matrícula
                pass
            case 6:
                menu_reportes()
            case 0:
                print("Sesión cerrada.")
                break
            case _:
                u.validacionOpcion()
                u.pausar()
                u.limpiar()

def menu_reportes():
    while True:
        opcion = mgs.menuReportes()
        match opcion:
            case 1:
                # Listar campers en estado "Inscrito"
                pass
            case 2:
                # Listar campers que aprobaron examen inicial
                pass
            case 3:
                # Listar entrenadores activos
                pass
            case 4:
                # Listar campers con bajo rendimiento
                pass
            case 5:
                # Listar campers y trainers asociados a rutas
                pass
            case 6:
                # Mostrar aprobados y perdidos por módulo, ruta y trainer
                pass
            case 0:
                break
            case _:
                u.validacionOpcion()
                u.pausar()
                u.limpiar()

def menu_trainer():
    while True:
        opcion = mgs.menuTrainer()
        match opcion:
            case 1:
                # Registrar notas de campers
                pass
            case 2:
                # Consultar campers de mis rutas
                pass
            case 0:
                print("Sesión cerrada.")
                break
            case _:
                u.validacionOpcion()
                u.pausar()
                u.limpiar()

def menu_camper():
    while True:
        opcion = mgs.menuCamper()
        match opcion:
            case 1:
                # Consultar mi ruta asignada
                pass
            case 2:
                # Consultar mis notas
                pass
            case 0:
                print("Sesión cerrada.")
                break
            case _:
                u.validacionOpcion()
                u.pausar()
                u.limpiar()

