import pymongo
from datetime import datetime
import random

# Conexión a MongoDB Local
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["clinica_veterinaria"]
coleccion = db["mascotas"]

#--- FUNCIONES AUXILIARES ---
def mostrar_mascota(m):
    print(f"\n--- Mascota: {m['nombre'].upper()} ---")
    print(f"ID: {m['_id']}")
    print(f"Especie: {m['especie']} | Edad: {m['edad']} años")
    print(f"Dueño: {m['propietario']['nombre']} | Tel: {m['propietario']['telefono']}")
    print(f"Última visita registrada: {m['ultima_visita'].strftime('%d/%m/%Y')}")
    if m.get('historial_medico'):
        print("Historial Médico:")
        for h in m['historial_medico']:
            print(f"  - {h['fecha'].strftime('%Y-%m-%d')}: {h['diagnostico']} (${h['costo']})")
    else:
        print("Historial Médico: Sin registros previos.")
    print("-" * 40)

#--- MENÚ PRINCIPAL ---
def menu():
    print("\n==== GESTIÓN DE CLÍNICA VETERINARIA ====")
    print("1. Registrar nueva mascota")
    print("2. Ver todas las mascotas")
    print("3. Buscar por edad (Mayores a X años)")
    print("4. Buscar por nombre (Texto parcial)")
    print("5. Buscar por rango de fechas de visita")
    print("6. Buscar por nombre de dueño")
    print("7. Actualizar edad de una mascota")
    print("8. Registrar nueva atención (Agregar al historial)")
    print("9. Eliminar mascota por nombre")
    print("0. Salir")
    return input("Seleccione una opción: ")

# --- FUNCIONALIDADES CRUD ---

def crear():
    try:
        # Generar ID de 4 dígitos único
        nuevo_id = random.randint(1000, 9999)
        while coleccion.find_one({"_id": nuevo_id}):
            nuevo_id = random.randint(1000, 9999)

        nombre = input("Nombre: ")
        especie = input("Especie: ")
        edad = int(input("Edad: "))
        p_nom = input("Dueño: ")
        p_tel = input("Teléfono: ")
        
        nuevo = {
            "_id": nuevo_id,
            "nombre": nombre,
            "especie": especie,
            "edad": edad,
            "propietario": {"nombre": p_nom, "telefono": p_tel},
            "historial_medico": [],
            "ultima_visita": datetime.now()
        }
        coleccion.insert_one(nuevo)
        print(f">>> Registro creado con ID {nuevo_id} exitosamente.")
    except Exception as e:
        print(f"Error al crear: {e}")

# Listar todas las mascotas registradas
def listar():
    cursor = coleccion.find()
    for m in cursor:
        mostrar_mascota(m)

# Buscar mascotas con edad mayor o igual a un valor dado
def buscar_comparacion():
    edad_min = int(input("Mostrar mascotas con edad mayor o igual a: "))
    query = {"edad": {"$gte": edad_min}}
    for m in coleccion.find(query):
        mostrar_mascota(m)

# Buscar mascotas por nombre usando regex (texto parcial, ignorando mayúsculas o minúsculas)
def buscar_regex():
    texto = input("Ingrese el nombre (o parte de él) a buscar: ")
    # Buscamos usando regex con la opción 'i' (case-insensitive)
    query = {"nombre": {"$regex": f"^{texto}$", "$options": "i"}}
    # Si quieres que sea parcial, quita los símbolos ^ y $ del f-string
    for m in coleccion.find(query):
        mostrar_mascota(m)

# Buscar mascotas que hayan tenido una visita entre dos fechas dadas
def buscar_por_fechas():
    try:
        print("Use formato AAAA-MM-DD")
        inicio = datetime.strptime(input("Fecha Inicio: "), "%Y-%m-%d")
        fin = datetime.strptime(input("Fecha Fin: "), "%Y-%m-%d")
        query = {"ultima_visita": {"$gte": inicio, "$lte": fin}}
        for m in coleccion.find(query):
            mostrar_mascota(m)
    except ValueError:
        print("Formato de fecha incorrecto.")

# Buscar mascotas por el nombre del dueño usando regex (ignorando mayúsculas o minúsculas)
def buscar_en_subdoc():
    dueño = input("Nombre del dueño a buscar: ")
    query = {"propietario.nombre": {"$regex": dueño, "$options": "i"}}
    for m in coleccion.find(query):
        mostrar_mascota(m)

# Actualizar la edad de una mascota por su nombre (ignorando mayúsculas o minúsculas)
def actualizar_campo_raiz():
    nom = input("Nombre de la mascota: ")
    nueva_edad = int(input("Nueva edad: "))
    
# Usamos regex para encontrar el nombre, ignorando mayúsculas o minúsculas
    res = coleccion.update_one(
        {"nombre": {"$regex": f"^{nom}$", "$options": "i"}}, 
        {"$set": {"edad": nueva_edad}}
    )
    if res.modified_count > 0:
        print(">>> Edad actualizada correctamente.")
    else:
        print("No se encontró la mascota.")

#   Actualizar el historial médico de una mascota agregando un nuevo evento (diagnóstico, fecha y costo)
def actualizar_array():
    nom = input("Nombre de la mascota: ")
    diag = input("Nuevo diagnóstico: ")
    precio = int(input("Costo consulta: "))
    
    nuevo_evento = {
        "fecha": datetime.now(),
        "diagnostico": diag,
        "costo": precio
    }
    
# Usamos regex para encontrar el nombre, ignorando mayúsculas o minúsculas y actualizamos el historial médico y la última visita
    res = coleccion.update_one(
        {"nombre": {"$regex": f"^{nom}$", "$options": "i"}},
        {"$push": {"historial_medico": nuevo_evento}, "$set": {"ultima_visita": datetime.now()}}
    )
    if res.modified_count > 0:
        print(">>> Historial médico actualizado.")
    else:
        print("No se encontró la mascota.")

# Eliminar una mascota por su nombre (ignorando mayúsculas o minúsculas)
def eliminar():
    nom = input("Nombre de la mascota a eliminar: ")


    # Usamos regex para eliminar ignorando mayúsculas o minúsculas
    res = coleccion.delete_one({"nombre": {"$regex": f"^{nom}$", "$options": "i"}})
    if res.deleted_count > 0:
        print(">>> Registro eliminado exitosamente.")
    else:
        print("No se encontró el registro.")

# --- BUCLE PRINCIPAL ---
if __name__ == "__main__":
    while True:
        opcion = menu()
        if opcion == "1": crear()
        elif opcion == "2": listar()
        elif opcion == "3": buscar_comparacion()
        elif opcion == "4": buscar_regex()
        elif opcion == "5": buscar_por_fechas()
        elif opcion == "6": buscar_en_subdoc()
        elif opcion == "7": actualizar_campo_raiz()
        elif opcion == "8": actualizar_array()
        elif opcion == "9": eliminar()
        elif opcion == "0": 
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")
