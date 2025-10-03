from modules.utils import cargar, pausar
import modules.messages as m

def login():
    ruta = "data/trainers.json"
    trainers = cargar(ruta)
    ruta2 = "data/campers.json"
    campers = cargar(ruta2)
    
    user = input("Ingrese su usuario: ").lower()
    if user == "admin":
        print("INICIASTE SESION COMO COORDINADOR")
        pausar()
        return "coordinador", user
    
    elif user in trainers:
        print("ACCESO CONCEDIDO")
        print(f"Bienvenido Trainer {trainers[user]['nombre']}")
        pausar()
        return "trainer", user
    
    elif user in campers:
        print("ACCESO CONCEDIDO")
        print(f"Bienvenido Camper {campers[user]['nombres']}")
        pausar()
        return "camper", user
    
    else:
        print("Usuario No Encontrado")
        pausar()
        return None