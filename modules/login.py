from modules.utils import cargar, pausar, limpiar, val

def login():
    ruta = "data/trainers.json"
    trainers = cargar(ruta)
    ruta2 = "data/campers.json"
    campers = cargar(ruta2)

    while True:
        user = val("\nIngrese su usuario: ").lower()
        if user == "admin":
            limpiar()
            print("\nINICIASTE SESION COMO COORDINADOR")
            pausar()
            return "coordinador", user

        elif user in trainers:
            limpiar()
            print("\nACCESO CONCEDIDO")
            print(f"Bienvenido Trainer 🧍 {trainers[user]['nombres']}")
            pausar()
            return "trainer", user

        elif user in campers:
            limpiar()
            print("\nACCESO CONCEDIDO")
            print(f"\nBienvenido Camper 👤 {campers[user]['nombres']}")
            pausar()
            return "camper", user

        else:
            print("Usuario No Encontrado")
            pausar()
            limpiar()
        