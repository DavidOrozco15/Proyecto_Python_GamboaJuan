import os
import json

#Utils

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPresiona enter para continuar......")
    
def validacionOpcion():
    print("Error: Opción inválida. Intente nuevamente.")

def validadorCamper(IDcamper, campers):
    if IDcamper in campers:
        print("❌ Ya existe un camper con ese ID.")
        return False
    return True

#Validacion

def validadorCamperNoExiste(IDcamper, campers):
    if IDcamper not in campers:
        print("❌ No existe un camper con ese ID.")
        return False
    return True

def validadorTrainer(IDtrainer, trainers):
    if IDtrainer in trainers:
        print("❌ Ya existe un Trainer con ese ID.")
        return False
    return True

def validadorTrainerNoExiste(IDtrainer, trainers):
    if IDtrainer not in trainers:
        print("❌ No existe un Trainer con ese ID.")
        return False
    return True

def valFloat(mensaje):
    while True:
        try:
            nota = float(input(mensaje))  # intenta convertir a float
            if 0 <= nota <= 100:
                return nota
            else:
                print("❌ La nota debe estar entre 0 y 100.")
        except ValueError:
            print("❌ Debes ingresar un número válido (puede tener decimales).")

def val(mensaje):
    while True:
        dato = input(mensaje).strip()  
        if dato == "":
            print("⚠️ Este campo no puede estar vacío. Intenta de nuevo.")
        else:
            return dato
        

def validarEstado(estado, estados):
    """
    Valida que el estado ingresado sea uno de los estados válidos.
    Retorna True si es válido, False si no.
    """
    return estado in estados

#JSON


def cargar(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # si no existe el archivo, devuelve un diccionario vacío

def guardar(ruta, data):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)