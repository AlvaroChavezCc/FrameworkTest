import psycopg2
import psycopg2.extras
from app.db import get_connection  # Importamos la función de conexión desde el módulo central

def get_cursos():
    conn = get_connection()
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("""
            SELECT id, codigo_curso, nombre_curso, ciclo
            FROM public.cursos
            ORDER BY id;
        """)
        cursos = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return cursos
