# main.py
import modules.utils as u
import modules.messages as m
import modules.login as l
import modules.coordinador as c
import modules.camper as cam
import modules.trainer as train

# MENÚ PRINCIPAL
def main():
    while True:
        opcion = m.menuLog()
        match opcion:
            case 1:
                rol, user = l.login()
                match rol:
                    case "coordinador":
                        mainCoordinador()  #llama al main del coordinador
                    case "trainer":
                        mainTrainer(user)
                    case "camper":
                        mainCamper(user)
            case 2:
                c.listarRutaCampersTrainers()
            case 0:
                print("¡Hasta luego! 👋")
                break
            case _:
                u.validacionOpcion()
                u.pausar()


# MENÚ COORDINADOR
def mainCoordinador():
    while True:
        opcion = m.menuCoordinador()
        match opcion:
            case 1:
                c.registrarCamper()
            case 2:
                c.registrarTrainer()
            case 3:
                c.crearRuta()
            case 4:
                c.crearGrupo()
            case 5:
                c.cambiarEstado()
            case 6:
                c.registrarNotas()
            case 7:
                c.registrarNotasCoordinador()
            case 8:
                c.asignarTrainerGrupo()
            case 9:
                c.matricularCamper()
            case 10:
                c.consultarCamperEnRiesgo()
            case 11:
                mainReportesMain()  # llama al menú de reportes
            case 0:
                print("Sesión cerrada.")
                break
            case _:
                u.validacionOpcion()
                u.pausar()


# MENÚ REPORTES
def mainReportesMain():
    while True:
        opcion = m.menuReportes()
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


# MENÚ TRAINER
def mainTrainer(user):
    while True:
        opcion = m.menuTrainer(user)
        match opcion:
            case 1:
                train.listarCampersAsignados(user)
            case 2:
                train.registrarNotasTrainer(user)
            case 3:
                train.consultarNotasCampers(user)
            case 4:
                train.generarReporteCampers(user)
            case 0:
                print("Sesión cerrada.")
                break
            case _:
                u.validacionOpcion()
                u.pausar()


# MENÚ CAMPER
def mainCamper(user):
    while True:
        opcion = m.menuCamper(user)
        match opcion:
            case 1:
                cam.consultarInfoCamper(user)
            case 2:
                cam.consultarNotasCamper(user)
            case 3:
                cam.consultarRutaCamper(user)
            case 0:
                print("Sesión cerrada.")
                break
            case _:
                u.validacionOpcion()
                u.pausar()
