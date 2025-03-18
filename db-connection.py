import os
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager

# Obtener cadena de conexión desde variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear un pool de conexiones para mejor rendimiento
pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=DATABASE_URL
)

@contextmanager
def get_connection():
    """
    Administra conexiones a la base de datos desde el pool.
    Utiliza un contextmanager para asegurar que las conexiones son devueltas al pool.
    """
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
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()

def close_pool():
    """
    Cierra el pool de conexiones cuando la aplicación se apaga.
    """
    if pool:
        pool.closeall()
