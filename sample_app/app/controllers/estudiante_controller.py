import psycopg2
import psycopg2.extras
from app.db import get_connection

def get_estudiantes():
    """Recupera la lista completa de estudiantes desde la tabla 'estudiantes'."""
    conn = get_connection()
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("""
            SELECT id, nombre, apellido, dni, codigo_estudiante, carrera 
            FROM public.estudiantes
            ORDER BY id;
        """)
        estudiantes = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return estudiantes

def add_estudiante(post_data):
    """
    Inserta un nuevo estudiante en la tabla 'estudiantes'.
    Se esperan las claves: nombre, apellido, dni, codigo_estudiante y carrera.
    """
    required_fields = ['nombre', 'apellido', 'dni', 'codigo_estudiante', 'carrera']
    missing = [field for field in required_fields if field not in post_data]
    if missing:
        return {"error": f"Los siguientes campos son requeridos: {', '.join(missing)}"}, "400 Bad Request"

    conn = get_connection()
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        insert_query = """
            INSERT INTO public.estudiantes (nombre, apellido, dni, codigo_estudiante, carrera)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, nombre, apellido, dni, codigo_estudiante, carrera;
        """
        cursor.execute(insert_query, (
            post_data['nombre'],
            post_data['apellido'],
            post_data['dni'],
            post_data['codigo_estudiante'],
            post_data['carrera']
        ))
        conn.commit()
        nuevo_estudiante = cursor.fetchone()
    except Exception as e:
        conn.rollback()
        return {"error": f"Error al insertar el estudiante: {str(e)}"}, "500 Internal Server Error"
    finally:
        cursor.close()
        conn.close()
    return nuevo_estudiante, "201 Created"