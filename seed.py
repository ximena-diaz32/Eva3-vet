import pymongo
from datetime import datetime

# Conexión
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["clinica_veterinaria"]
coleccion = db["mascotas"]

# Limpiar base de datos para asegurar que queden exactamente 10
coleccion.delete_many({})

datos_iniciales = [
    {
        "nombre": "Thor",
        "especie": "Perro",
        "edad": 5,
        "propietario": {"nombre": "Carlos Ruiz", "telefono": "+569111111"},
        "historial_medico": [{"fecha": datetime(2025, 10, 5), "diagnostico": "Vacuna Antirrábica", "costo": 15000}],
        "ultima_visita": datetime(2025, 10, 5)
    },
    {
        "nombre": "Luna",
        "especie": "Gato",
        "edad": 2,
        "propietario": {"nombre": "Maria Soto", "telefono": "+569222222"},
        "historial_medico": [{"fecha": datetime(2026, 1, 20), "diagnostico": "Control sano", "costo": 12000}],
        "ultima_visita": datetime(2026, 1, 20)
    },
    {
        "nombre": "Rocky",
        "especie": "Perro",
        "edad": 8,
        "propietario": {"nombre": "Juan Perez", "telefono": "+569333333"},
        "historial_medico": [{"fecha": datetime(2025, 12, 1), "diagnostico": "Limpieza dental", "costo": 45000}],
        "ultima_visita": datetime(2025, 12, 1)
    },
    {
        "nombre": "Simba",
        "especie": "Gato",
        "edad": 1,
        "propietario": {"nombre": "Lucia Diaz", "telefono": "+569444444"},
        "historial_medico": [],
        "ultima_visita": datetime(2026, 3, 10)
    },
    {
        "nombre": "Rex",
        "especie": "Iguana",
        "edad": 4,
        "propietario": {"nombre": "Pedro Arce", "telefono": "+569555555"},
        "historial_medico": [{"fecha": datetime(2025, 11, 15), "diagnostico": "Suplemento calcio", "costo": 8000}],
        "ultima_visita": datetime(2025, 11, 15)
    },
    {
        "nombre": "Bella",
        "especie": "Perro",
        "edad": 3,
        "propietario": {"nombre": "Sofia Rojas", "telefono": "+569666666"},
        "historial_medico": [{"fecha": datetime(2026, 4, 5), "diagnostico": "Desparasitación", "costo": 10000}],
        "ultima_visita": datetime(2026, 4, 5)
    },
    {
        "nombre": "Toby",
        "especie": "Perro",
        "edad": 10,
        "propietario": {"nombre": "Andres Vera", "telefono": "+569777777"},
        "historial_medico": [{"fecha": datetime(2024, 5, 20), "diagnostico": "Cirugía de cadera", "costo": 250000}],
        "ultima_visita": datetime(2024, 5, 20)
    },
    {
        "nombre": "Mora",
        "especie": "Hamster",
        "edad": 1,
        "propietario": {"nombre": "Elena Paz", "telefono": "+569888888"},
        "historial_medico": [],
        "ultima_visita": datetime(2026, 2, 28)
    },
    {
        "nombre": "Cooper",
        "especie": "Perro",
        "edad": 6,
        "propietario": {"nombre": "Roberto Jara", "telefono": "+569999999"},
        "historial_medico": [{"fecha": datetime(2025, 8, 14), "diagnostico": "Control de peso", "costo": 5000}],
        "ultima_visita": datetime(2025, 8, 14)
    },
    {
        "nombre": "Nina",
        "especie": "Conejo",
        "edad": 2,
        "propietario": {"nombre": "Valeria Monte", "telefono": "+569000000"},
        "historial_medico": [{"fecha": datetime(2026, 5, 1), "diagnostico": "Corte de uñas", "costo": 7500}],
        "ultima_visita": datetime(2026, 5, 1)
    }
]

coleccion.insert_many(datos_iniciales)
print(f"Éxito: Se han cargado {coleccion.count_documents({})} documentos en la colección.")