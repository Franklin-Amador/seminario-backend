from locust import HttpUser, task, between
import random
import json

class LoginUser(HttpUser):
    wait_time = between(1, 3)  # Tiempo entre solicitudes (1-3 segundos)
    
    # Lista de usuarios de prueba (asume que están en la BD)
    test_users = [
        {"username": f"user{i}", "password": "1234"} 
        for i in range(1, 11)  # 10 usuarios de prueba
    ]
    
    @task(10)  # Mayor peso para el endpoint principal de login
    def login(self):
        # Seleccionar un usuario aleatorio de nuestra lista
        user = random.choice(self.test_users)
        
        # Realizar solicitud de login
        response = self.client.post(
            "/login",
            json=user,
            headers={"Content-Type": "application/json"}
        )
        
        # Registrar éxito/fracaso basado en el código de respuesta
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("success", False):
                # Login exitoso
                pass
            else:
                # Respuesta 200 pero login falló
                response.failure(f"Login falló: {response_data.get('message', 'No message')}")
        else:
            # Error en la solicitud
            response.failure(f"Login request failed with status code: {response.status_code}")
    
    @task(1)  # Menor frecuencia para actualización de contraseña
    def update_password(self):
        # Seleccionar un usuario aleatorio
        user_index = random.randint(1, 10)
        
        # Datos para actualizar contraseña
        update_data = {
            "email": f"user{user_index}@example.com",
            "new_password": "1234"  # Nueva contraseña (simple para pruebas)
        }
        
        # Realizar solicitud
        response = self.client.put(
            "/login/update-password",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        
        # Registrar resultado
        if response.status_code != 200:
            response.failure(f"Password update failed with status code: {response.status_code}")

    @task(1)  # Simulación ocasional de reset de contraseñas (admin)
    def reset_all_passwords(self):
        # Datos para reset masivo (con clave de admin)
        reset_data = {
            "admin_key": "papi_claude",
            "new_password": "1234"
        }
        
        # Realizar solicitud
        response = self.client.put(
            "/login/reset-all-passwords",
            json=reset_data,
            headers={"Content-Type": "application/json"}
        )
        
        # Registrar resultado
        if response.status_code != 200:
            response.failure(f"Bulk password reset failed: {response.status_code}")

# Para ejecutar:
# locust -f locustfile.py --host=http://localhost:8000
