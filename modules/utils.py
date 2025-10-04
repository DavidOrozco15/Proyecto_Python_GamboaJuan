import os
import json
from datetime import datetime

#Utils

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPresiona enter para continuar......")
    
def validacionOpcion():
    print("Error: Opción inválida. Intente nuevamente.")

#Validacion de existencias

def validadorCamper(IDcamper, campers):
    if IDcamper in campers:
        print("❌ Ya existe un camper con ese ID.")
        return False
    return True

def validadorTrainer(IDtrainer, trainers):
    if IDtrainer in trainers:
        print("❌ Ya existe un trainer con ese ID.")
        return False
    return True

def validadorRuta(nombreRuta, rutas):
    if nombreRuta in rutas:
        print("❌ Ya existe una ruta con ese nombre.")
        return False
    return True

def validadorCamperNoExiste(IDcamper, campers):
    if IDcamper not in campers:
        print("❌ No existe un camper con ese ID.")
        return False
    return True

def validadorTrainerNoExiste(IDtrainer, trainers):
    if IDtrainer not in trainers:
        print("❌ No existe un Trainer con ese ID.")
        return False
    return True

def ValidadorRutaNoExiste(nombreRuta, rutaRutas):
    if nombreRuta not in rutaRutas:
        print("❌ No existe la ruta.")
        return False
    return True

#Validacion de tipos de datos

def pedirFloat(mensaje):
    while True:
        dato = input(mensaje).strip()
        
        if not dato:  # si está vacío
            print("❌ El campo no puede estar vacío. Intente de nuevo.")
            continue

        try:
            valor = float(dato)  # intenta convertir a float
            return valor
        except ValueError:
            print("❌ Debe ingresar un número válido (ej: 12.5).")

def val(mensaje):
    while True:
        dato = input(mensaje).strip()  
        if dato == "":
            print("⚠️ Este campo no puede estar vacío. Intenta de nuevo.")
        else:
            return dato
        
def pedirEntero(mensaje):
    while True:
        dato = input(mensaje).strip()
        if not dato:
            print("❌ El campo no puede estar vacío. Intente de nuevo.")
            continue
        try:
            return int(dato)
        except ValueError:
            print("❌ Debe ingresar un número entero válido.")
        
 
 # Validacion de estado
  
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

#datatime

def pedirFecha(mensaje):
    while True:
        fecha = input(mensaje).strip()
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return fecha
        except ValueError:
            print("❌ Formato de fecha inválido. Debe ser YYYY-MM-DD.")