import modules.utils as u
import modules.messages as mgs
import modules.login as l
import modules.coordinador as c

def main():
    while True:
        opcion = mgs.menuLog()
        match opcion:
            case 1:
                rol, user = l.login()
                match rol:
                    case "coordinador":
                        menuCoordinador()
                    case "trainer":
                        menuTrainer()
                    case "camper":
                        menuCamper()
            case 0:
                print("¡Hasta luego! 👋")
                break
            case _:
                u.validacionOpcion()
                u.pausar()
                u.limpiar()

def menuCoordinador():
    while True:
        opcion = mgs.menuCoordinador()
        match opcion:
            case 1:
                # Registrar Camper
                c.registrarCamper()
            case 2:
                # Registrar Trainer
                c.registrarTrainer()
            case 3:
                # Crear Ruta de entrenamiento
                c.crearRuta()
            case 4:
                # Cambiar estados
                c.cambiarEstado()
            case 5:
                c.registrarNotas()
            case 6:
                c.asignarTrainerRuta()
            case 7:
                c.matricularCamper()
            case 8:
                c.consultarCamperEnRiesgo()
            case 9:
                mgs.menuReportes()
            case 0:
                print("Sesión cerrada.")
                mgs.menuLog()
            case _:
                u.validacionOpcion()
                u.pausar()
                u.limpiar()

def menuReportes():
    while True:
        opcion = mgs.menuReportes()
        match opcion:
            case 1:
                c.listarCampersInscritos()
                pass
            case 2:
                c.listarCampersAprobados()
                pass
            case 3:
                c.listarTrainers()
                pass
            case 4:
                c.listarCampersBajoRendimiento()
                pass
            case 5:
                c.listarRutaCampersTrainers()
                pass
            case 6:
                c.mostrarResultadosModulos()
                pass
            case 0:
                break
            case _:
                u.validacionOpcion()
                u.pausar()
                u.limpiar()

def menuTrainer():
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

def menuCamper():
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

