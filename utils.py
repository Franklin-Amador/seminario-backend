import bcrypt
from datetime import datetime
from typing import Any, Dict, List

def hash_password(password: str) -> str:
    """
    Hashea una contraseña utilizando bcrypt.
    
    Args:
        password (str): Contraseña en texto plano
        
    Returns:
        str: Contraseña hasheada
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña coincide con su hash.
    
    Args:
        password (str): Contraseña en texto plano
        hashed_password (str): Contraseña hasheada
        
    Returns:
        bool: True si la contraseña coincide con el hash
    """
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def get_current_timestamp() -> datetime:
    """
    Devuelve el timestamp actual en UTC.
    
    Returns:
        datetime: Timestamp actual en UTC
    """
    return datetime.utcnow()

def format_db_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Formatea un resultado de la base de datos para convertir fechas y otros
    tipos de datos especiales a formatos serializables.
    
    Args:
        result (Dict[str, Any]): Resultado de la base de datos
        
    Returns:
        Dict[str, Any]: Resultado formateado
    """
    formatted = {}
    for key, value in result.items():
        if isinstance(value, datetime):
            formatted[key] = value.isoformat()
        else:
            formatted[key] = value
    return formatted

def format_db_results(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Formatea una lista de resultados de la base de datos.
    
    Args:
        results (List[Dict[str, Any]]): Lista de resultados
        
    Returns:
        List[Dict[str, Any]]: Lista de resultados formateados
    """
    return [format_db_result(result) for result in results]

def to_camel_case(snake_str: str) -> str:
    """
    Convierte una cadena en snake_case a camelCase.
    
    Args:
        snake_str (str): Cadena en snake_case
        
    Returns:
        str: Cadena en camelCase
    """
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def convert_keys_to_camel_case(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convierte todas las claves de un diccionario de snake_case a camelCase.
    
    Args:
        data (Dict[str, Any]): Diccionario con claves en snake_case
        
    Returns:
        Dict[str, Any]: Diccionario con claves en camelCase
    """
    if not isinstance(data, dict):
        return data
    
    return {to_camel_case(key): convert_keys_to_camel_case(value) if isinstance(value, dict) else value 
            for key, value in data.items()}

def convert_list_keys_to_camel_case(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convierte todas las claves de una lista de diccionarios de snake_case a camelCase.
    
    Args:
        data (List[Dict[str, Any]]): Lista de diccionarios con claves en snake_case
        
    Returns:
        List[Dict[str, Any]]: Lista de diccionarios con claves en camelCase
    """
    return [convert_keys_to_camel_case(item) for item in data]