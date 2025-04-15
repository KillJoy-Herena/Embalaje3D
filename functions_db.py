import sqlite3
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def conectar_db():
    return sqlite3.connect("data/carga_contenedores.db")

def obtener_paquetes():
    """Obtiene todos los paquetes de la base de datos."""
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM paquetes")
            return cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"Error al obtener paquetes: {e}")
        return []

def insertar_paquete(nombre, peso, volumen):
    """Inserta un paquete en la base de datos."""
    if not nombre or peso <= 0 or volumen <= 0:
        raise ValueError("Los datos proporcionados no son válidos.")
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO paquetes (nombre, peso, volumen) VALUES (?, ?, ?)", 
                           (nombre, peso, volumen))
            conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Error al insertar paquete: {e}")

def editar_paquete(id, nombre, peso, volumen):
    """Edita un paquete existente."""
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE paquetes SET nombre=?, peso=?, volumen=? WHERE id=?", 
                           (nombre, peso, volumen, id))
            conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Error al editar paquete: {e}")

def eliminar_paquete(id):
    """Elimina un paquete por ID."""
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM paquetes WHERE id=?", (id,))
            conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Error al eliminar paquete: {e}")