from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenido a la API del Campus Virtual"}
    
    
def test_login_success():
    response = client.post("/api/login", json={"username": "admin", "password": "1234"})
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "user_id": 1,
        "username": "admin",
        "firstname": "Administrador",
        "lastname": "Sistema",
        "email": "admin@unah.edu.hn",
        "roles": [
            {
                "id": 1,
                "name": "Administrador",
                "shortname": "admin"
            }
        ],
        "message": "Login exitoso"
    }
    
# Prueba para un inicio de sesión fallido
def test_login_failure():
    response = client.post("/api/login", json={"username": "admin", "password": "wrong"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Credenciales incorrectas"}

def test_login_empty_credentials():
    response = client.post("/api/login", json={"username": "", "password": ""})
    assert response.status_code == 422  # Unprocessable Entity
    assert "String should have at least 1 character" in response.json()["detail"][0]["msg"]
    
def test_login_invalid_data_types():
    response = client.post("/api/login", json={"username": 123, "password": 456})
    assert response.status_code == 422  # Unprocessable Entity
    assert "Input should be a valid string" in response.json()["detail"][0]["msg"]


def test_login_long_credentials():
    long_username = "a" * 101 
    long_password = "b" * 101 
    response = client.post("/api/login", json={"username": long_username, "password": long_password})
    assert response.status_code == 422 # Unprocessable Entity
    assert "String should have at most 100 characters" in response.json()["detail"][0]["msg"]