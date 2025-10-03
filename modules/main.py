import modules.utils as u
import modules.messages as mgs
import modules.login as l
import modules.coordinador as c
import modules.camper as cam
import modules.trainer as train

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
                        menuTrainer(user)
                    case "camper":
                        menuCamper(user)
            case 0:
                print("¡Hasta luego! 👋")
                break
            case _:
                u.validacionOpcion()
                u.pausar()
                

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
                

def menuReportes():
    while True:
        opcion = mgs.menuReportes()
        match opcion:
            case 1:
                c.listarCampersInscritos()
            case 2:
                c.listarCampersAprobados()
            case 3:
                c.listarTrainers()
            case 4:
                c.listarCampersBajoRendimiento()
            case 5:
                c.listarRutaCampersTrainers()
            case 6:
                c.mostrarResultadosModulos()
            case 0:
                break
            case _:
                u.validacionOpcion()
                u.pausar()
                

def menuTrainer():
    while True:
        opcion = mgs.menuTrainer()
        match opcion:
            case 1:
                train.listarCampersAsignados()
            case 2:
                train.registrarNotasTrainer()
            case 3:
                train.consultarNotasCampers()
            case 4:
                train.generarReporteCampers()
            case 0:
                print("Sesión cerrada.")
                break
            case _:
                u.validacionOpcion()
                u.pausar()
                

def menuCamper():
    while True:
        opcion = mgs.menuCamper()
        match opcion:
            case 1:
                cam.consultarInfoCamper()
            case 2:
                cam.consultarNotasCamper()
            case 3:
                cam.consultarRutaCamper()
            case 0:
                print("Sesión cerrada.")
                break
            case _:
                u.validacionOpcion()
                u.pausar()
                

