from modules.utils import cargar, guardar

def listarCampersAsignados():
    ruta = "data/rutas.json"
    rutaRutas = cargar(ruta)
    ruta = "data/campers.json"
    campers = cargar(ruta)
    
    encontrado = False
    
    for nombreRuta, infoRuta in rutaRutas.items():
        if infoRuta.get("trainerEncargado") == IDtrainer:
            encontrado = True
            print(f"\n Ruta: {nombreRuta}")
            campersAsignados = infoRuta.get("campersAsignados", [])
            
            if not campersAsignados:
                print("No hay campers Asignados aun")
            else:
                for IDcamper in campersAsignados:
                    info = campers.get(IDcamper, {})
                    print(f" ID: {IDcamper} | Nombres: {info.get('nombres','')} | Apellidos: {info.get('apellidos','')} | Estado: {info.get('estado','')} | Riesgo: {info.get('riesgo','')}")
    if not encontrado:
        print("No tienes rutas asignadas Actualmente")