import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from contextlib import contextmanager

# Cargar variables de entorno
load_dotenv()

# Obtener la URL de conexión desde variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

@contextmanager
def get_db_connection():
    """
    Contexto para gestionar la conexión a la base de datos.
    Abre la conexión, ejecuta las operaciones y la cierra automáticamente.
    """
    conn = None
    try:
        # Establecer la conexión
        conn = psycopg2.connect(DATABASE_URL)
        # Devolver la conexión para uso dentro del bloque with
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

@contextmanager
def get_db_cursor(commit=False):
    """
    Contexto para gestionar el cursor de la base de datos.
    Permite ejecutar consultas SQL y obtener los resultados.
    
    Args:
        commit (bool): Si es True, hace commit de la transacción al finalizar.
    """
    with get_db_connection() as conn:
        # Crear un cursor que devuelva resultados como diccionarios
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            # Devolver el cursor para uso dentro del bloque with
            yield cursor
            if commit:
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

# Función para ejecutar una consulta que devuelve resultados
def fetch_data(query, params=None):
    """
    Ejecuta una consulta SQL y devuelve los resultados.
    
    Args:
        query (str): Consulta SQL a ejecutar
        params (tuple, optional): Parámetros para la consulta
        
    Returns:
        list: Lista de diccionarios con los resultados
    """
    with get_db_cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()

# Función para ejecutar una consulta que devuelve un solo resultado
def fetch_one(query, params=None):
    """
    Ejecuta una consulta SQL y devuelve un solo resultado.
    
    Args:
        query (str): Consulta SQL a ejecutar
        params (tuple, optional): Parámetros para la consulta
        
    Returns:
        dict: Diccionario con el resultado o None si no hay resultados
    """
    with get_db_cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchone()

# Función para ejecutar una consulta que no devuelve resultados (INSERT, UPDATE, DELETE)
def execute_query(query, params=None):
    """
    Ejecuta una consulta SQL que modifica datos.
    
    Args:
        query (str): Consulta SQL a ejecutar
        params (tuple, optional): Parámetros para la consulta
        
    Returns:
        int: Número de filas afectadas
    """
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(query, params)
        return cursor.rowcount

# Función para ejecutar una consulta que devuelve el ID del registro insertado
def execute_query_returning_id(query, params=None):
    """
    Ejecuta una consulta SQL INSERT que devuelve el ID del registro insertado.
    
    Args:
        query (str): Consulta SQL a ejecutar (debe incluir RETURNING id)
        params (tuple, optional): Parámetros para la consulta
        
    Returns:
        int: ID del registro insertado
    """
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result:
            return result.get('id')
        return None

# Función para ejecutar una función almacenada que devuelve resultados
def call_function_returning_rows(function_name, params=None):
    """
    Ejecuta una función almacenada que devuelve resultados.
    
    Args:
        function_name (str): Nombre de la función almacenada
        params (tuple, optional): Parámetros para la función
        
    Returns:
        list: Lista de diccionarios con los resultados
    """
    with get_db_cursor() as cursor:
        # Construir la consulta para llamar a la función
        query = f"SELECT * FROM {function_name}("
        if params:
            placeholders = ", ".join(["%s" for _ in range(len(params))])
            query += placeholders
        query += ")"
        
        cursor.execute(query, params)
        return cursor.fetchall()

# Función para ejecutar una función almacenada que devuelve un solo registro
def call_function_returning_one(function_name, params=None):
    """
    Ejecuta una función almacenada que devuelve un solo registro.
    
    Args:
        function_name (str): Nombre de la función almacenada
        params (tuple, optional): Parámetros para la función
        
    Returns:
        dict: Diccionario con el resultado o None si no hay resultados
    """
    with get_db_cursor() as cursor:
        # Construir la consulta para llamar a la función
        query = f"SELECT * FROM {function_name}("
        if params:
            placeholders = ", ".join(["%s" for _ in range(len(params))])
            query += placeholders
        query += ")"
        
        cursor.execute(query, params)
        return cursor.fetchone()

# Función para convertir resultados de RealDictCursor a un formato serializable
def clean_db_results(results):
    """
    Convierte los resultados de la base de datos a un formato serializable.
    Maneja tipos de datos como datetime, UUID, etc.
    
    Args:
        results: Resultados de la base de datos (dict o list de dicts)
        
    Returns:
        dict o list: Resultados en formato serializable
    """
    import json
    from datetime import datetime, date
    
    class CustomJSONEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (datetime, date)):
                return obj.isoformat()
            return super().default(obj)
    
    # Convertir a JSON y luego de vuelta a dict para asegurar serialización
    if isinstance(results, list):
        serializable = json.loads(json.dumps(results, cls=CustomJSONEncoder))
    else:
        serializable = json.loads(json.dumps(dict(results), cls=CustomJSONEncoder))
    
    return serializable