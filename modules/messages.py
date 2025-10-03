from modules.utils import pausar, limpiar

def menuLog():
    limpiar()
    print("----CAMPUSLANDS ERP----")
    print("\n1. Iniciar Sesion👤")
    print("0. Salir 👋")
    try:
            opcion = int(input("\nSeleccione una opcion: "))
            if opcion in {0, 1}:
                return opcion
            else:
                print("\nError: Opción inválida. Intente nuevamente.")
                pausar()
    except ValueError:
            print("\nError: Debe ingresar un número entero.")
            pausar()

def menuCoordinador():
    limpiar()
    print("----BIENVENIDO COORDINADOR 🙍‍♂️----")
    print("\n1. Registrar Camper 👨‍🎓")
    print("2. Registrar Trainer 👨‍⚕️")
    print("3. Crear Ruta de entrenamiento 💪")
    print("4. Cambiar Estados Manuales 🔴🟡🟢")
    print("5. Registrar Notas 📔")
    print("6. Asignar Trainer Ruta 🙆")
    print("7. Asignar Matricula 📚")
    print("8. Consultar Riesgo Camper 📉")
    print("9. Reportes 📝")
    print("0. Cerrar Sesion 👋")
    try:
            opcion = int(input("\nSeleccione una opcion: "))
            if opcion in {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}:
                return opcion
            else:
                print("Error: Opción inválida. Intente nuevamente.")
                pausar()
    except ValueError:
            print("Error: Debe ingresar un número entero.")
            pausar()

def menuReportes():
    limpiar()
    print("\n----MENÚ DE REPORTES 📊----")
    print("1. Listar campers en estado 'Inscrito'")
    print("2. Listar campers que aprobaron examen inicial")
    print("3. Listar entrenadores activos")
    print("4. Listar campers con bajo rendimiento")
    print("5. Listar campers y trainers asociados a rutas")
    print("6. Mostrar aprobados y perdidos por módulo, ruta y trainer")
    print("0. Volver al menú anterior")
    try:
        opcion = int(input("Seleccione una opcion: "))
        if opcion in {1, 2, 3, 4, 5, 6, 0}:
            return opcion
        else:
            print("Error: Opción inválida. Intente nuevamente.")
            pausar()
    except ValueError:
        print("Error: Debe ingresar un número entero.")
        pausar()

def menuTrainer():
    limpiar()
    print("\n--- BIENVENIDO TRAINER ---")
    print("1. Listar Campers asignados")
    print("2. Registrar Notas de Campers")
    print("3. Consultar Notas de Campers")
    print("4. Generar Reportes")
    print("0. Cerrar sesión")
    try:
        opcion = int(input("Seleccione una opcion: "))
        if opcion in {1, 2, 3, 4, 0}:
            return opcion
        else:
            print("Error: Opción inválida. Intente nuevamente.")
            pausar()
    except ValueError:
        print("Error: Debe ingresar un número entero.")
        pausar()

def menuCamper():
    limpiar()
    print("\n--- MENÚ CAMPER ---")
    print("1. Consultar mi informacion")
    print("2. Consultar mis notas")
    print("3. Consultar mi ruta")
    print("0. Cerrar sesión")
    try:
        opcion = int(input("Seleccione una opcion: "))
        if opcion in {1, 2, 3, 0}:
            return opcion
        else:
            print("Error: Opción inválida. Intente nuevamente.")
            pausar()
    except ValueError:
        print("Error: Debe ingresar un número entero.")
        pausar()

def rutasFijas():
    limpiar()
    print("\n---MODULOS FIJOS---")
    print("Fundamentos de Programacion: Introduccion a la algoritmia | PSeint | Python")
    print("Programacion Web: HTML | CSS | Bootstrap")
    

