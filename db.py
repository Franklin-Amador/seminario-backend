import os
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# Obtener cadena de conexión directamente
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/campus_virtual")

# Verificar la conexión al inicio
try:
    # Conexión de prueba para verificar
    conn = psycopg2.connect(DATABASE_URL)
    conn.close()
    logger.info("Conexión a la base de datos verificada correctamente")
except Exception as e:
    logger.error(f"Error al conectar a la base de datos: {str(e)}")
    # No raise para permitir que la aplicación inicie aunque la BD no esté disponible inicialmente

# Crear un pool de conexiones para mejor rendimiento
pool = None
try:
    pool = SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        dsn=DATABASE_URL
    )
    logger.info("Pool de conexiones creado correctamente")
except Exception as e:
    logger.error(f"Error al crear el pool de conexiones: {str(e)}")

@contextmanager
def get_connection():
    """
    Administra conexiones a la base de datos desde el pool.
    Utiliza un contextmanager para asegurar que las conexiones son devueltas al pool.
    """
    global pool
    if pool is None:
        try:
            pool = SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                dsn=DATABASE_URL
            )
            logger.info("Pool de conexiones creado correctamente (reintentar)")
        except Exception as e:
            logger.error(f"Error al crear el pool de conexiones (reintentar): {str(e)}")
            raise

    conn = pool.getconn()
    try:
        # Configurar la conexión para usar RealDictCursor por defecto
        conn.cursor_factory = RealDictCursor
        yield conn
    finally:
        pool.putconn(conn)

@contextmanager
def get_cursor():
    """
    Proporciona un cursor con manejo automático de la conexión.
    """
    with get_connection() as conn:
        # Configurar autocommit en False para manejar transacciones manualmente
        conn.autocommit = False
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Error en transacción: {str(e)}")
            raise
        finally:
            cursor.close()

def close_pool():
    """
    Cierra el pool de conexiones cuando la aplicación se apaga.
    """
    global pool
    if pool:
        pool.closeall()
        pool = None
        logger.info("Pool de conexiones cerrado")

class Database:
    """
    Clase que proporciona métodos para interactuar con la base de datos.
    """
    
    @classmethod
    def execute(cls, query: str, *args, fetch=False):
        """
        Ejecuta una consulta SQL y opcionalmente devuelve resultados.
        
        Args:
            query (str): La consulta SQL a ejecutar
            *args: Parámetros posicionales para la consulta
            fetch (bool): Si es True, devuelve los resultados
            
        Returns:
            List[Dict] o None: Resultados de la consulta o None
        """
        try:
            with get_cursor() as cursor:
                cursor.execute(query, args)
                if fetch:
                    return cursor.fetchall()
                return None
        except Exception as e:
            logger.error(f"Error ejecutando query: {query}, error: {str(e)}")
            raise

    @classmethod
    def execute_proc(cls, proc_name: str, *args):
        """
        Ejecuta un procedimiento almacenado y devuelve los resultados.
        
        Args:
            proc_name (str): Nombre del procedimiento almacenado
            *args: Parámetros posicionales para el procedimiento
            
        Returns:
            List[Dict]: Resultados del procedimiento
        """
        try:
            # Construir la llamada al procedimiento
            placeholders = ", ".join(["%s" for _ in range(len(args))])
            query = f"SELECT * FROM {proc_name}({placeholders})"
            
            logger.info(f"Ejecutando procedimiento: {query}")
            
            with get_cursor() as cursor:
                cursor.execute(query, args)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error ejecutando procedimiento {proc_name}: {str(e)}")
            raise

    @classmethod
    def execute_proc_transaction(cls, proc_name: str, *args):
        """
        Ejecuta un procedimiento almacenado dentro de una transacción explícita.
        
        Args:
            proc_name (str): Nombre del procedimiento almacenado
            *args: Parámetros posicionales para el procedimiento
            
        Returns:
            List[Dict]: Resultados del procedimiento
        """
        try:
            # Construir la llamada al procedimiento
            placeholders = ", ".join(["%s" for _ in range(len(args))])
            query = f"SELECT * FROM {proc_name}({placeholders})"
            
            logger.info(f"Ejecutando procedimiento en transacción: {query}")
            
            with get_connection() as conn:
                conn.autocommit = False
                with conn.cursor() as cursor:
                    cursor.execute(query, args)
                    result = cursor.fetchall()
                    conn.commit()
                    return result
        except Exception as e:
            logger.error(f"Error ejecutando procedimiento {proc_name} en transacción: {str(e)}")
            raise

    @classmethod
    def get_pool(cls):
        """
        Devuelve el pool existente.
        """
        global pool
        return pool

# Función de ayuda para convertir filas a diccionarios
def row_to_dict(row):
    """
    Convierte una fila de psycopg2 (ya es un diccionario con RealDictCursor) a un diccionario.
    Esta función se mantiene por compatibilidad, pero con RealDictCursor es redundante.
    """
    if row is None:
        return None
    
    return dict(row)

def rows_to_list(rows):
    """
    Convierte múltiples filas a una lista de diccionarios.
    Esta función se mantiene por compatibilidad, pero con RealDictCursor es casi redundante.
    """
    if rows is None:
        return []
    
    return [row_to_dict(row) for row in rows]
