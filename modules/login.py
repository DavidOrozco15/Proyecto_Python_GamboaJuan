from modules.utils import cargar, pausar, limpiar, val
import modules.messages as m

def login():
    ruta = "data/trainers.json"
    trainers = cargar(ruta)
    ruta2 = "data/campers.json"
    campers = cargar(ruta2)
    
    user = val("\nIngrese su usuario: ").lower()
    if user == "admin":
        limpiar()
        print("\nINICIASTE SESION COMO COORDINADOR")
        pausar()
        return "coordinador", user
    
    elif user in trainers:
        limpiar()
        print("\nACCESO CONCEDIDO")
        print(f"Bienvenido Trainer {trainers[user]['nombre']}")
        pausar()
        return "trainer", user
    
    elif user in campers:
        limpiar()
        print("\nACCESO CONCEDIDO")
        print(f"Bienvenido Camper {campers[user]['nombres']}")
        pausar()
        return "camper", user
    
    
    print("Usuario No Encontrado")
    pausar()
        