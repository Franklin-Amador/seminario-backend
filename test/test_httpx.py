import json
import asyncio
import time
import httpx
import random
import argparse

# URL base de tu API FastAPI
BASE_URL = 'http://127.0.0.1:8000'

# Contador de solicitudes exitosas y fallidas
class Stats:
    def __init__(self):
        self.successful_requests = 0
        self.failed_requests = 0
        self.response_times = []
        self.start_time = None
        self.end_time = None
    
    def start(self):
        self.start_time = time.time()
    
    def stop(self):
        self.end_time = time.time()
    
    def add_success(self, response_time):
        self.successful_requests += 1
        self.response_times.append(response_time)
    
    def add_failure(self):
        self.failed_requests += 1
    
    def get_summary(self):
        elapsed = self.end_time - self.start_time if self.end_time else time.time() - self.start_time
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        
        return {
            "duration_seconds": elapsed,
            "requests_per_second": (self.successful_requests + self.failed_requests) / elapsed if elapsed > 0 else 0,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": (self.successful_requests / (self.successful_requests + self.failed_requests)) * 100 if (self.successful_requests + self.failed_requests) > 0 else 0,
            "avg_response_time": avg_response_time,
            "min_response_time": min(self.response_times) if self.response_times else 0,
            "max_response_time": max(self.response_times) if self.response_times else 0
        }

# Funciones de prueba asíncronas
async def get_cursos(client, stats):
    start_time = time.time()
    try:
        # Hacer una solicitud GET a la ruta /api/courses
        response = await client.get(f'{BASE_URL}/api/courses', timeout=10.0)
        
        if response.status_code == 200:
            # Verificar el contenido de la respuesta
            cursos = response.json()
            if isinstance(cursos, list) and len(cursos) > 0:
                stats.add_success(time.time() - start_time)
                print("✓ GET /api/courses exitoso")
            else:
                print("× GET /api/courses: respuesta vacía o formato incorrecto")
                stats.add_failure()
        else:
            print(f"× GET /api/courses: estado {response.status_code}")
            stats.add_failure()
    except Exception as e:
        print(f"Error en get_cursos: {str(e)}")
        stats.add_failure()

async def get_usuarios(client, stats):
    start_time = time.time()
    try:
        # Hacer una solicitud GET a la ruta /api/users
        response = await client.get(f'{BASE_URL}/api/users', timeout=10.0)
        
        if response.status_code == 200:
            # Verificar el contenido de la respuesta
            usuarios = response.json()
            if isinstance(usuarios, list) and len(usuarios) > 0:
                stats.add_success(time.time() - start_time)
                print("✓ GET /api/users exitoso")
            else:
                print("× GET /api/users: respuesta vacía o formato incorrecto")
                stats.add_failure()
        else:
            print(f"× GET /api/users: estado {response.status_code}")
            stats.add_failure()
    except Exception as e:
        print(f"Error en get_usuarios: {str(e)}")
        stats.add_failure()

# async def login(playwright, stats, valid=True, max_retries=2):
#     start_time = time.time()
#     browser = None

#     for attempt in range(max_retries + 1):
#         try:
#             browser = await playwright.chromium.launch(headless=True)
#             context = await browser.new_context()
#             page = await context.new_page()

#             # Configurar timeout más largo
#             page.set_default_timeout(10000)  # 10 segundos

#             # Datos de login
#             login_data = {
#                 "username": "frank",
#                 "password": "1234" if valid else f"wrong{random.randint(1000, 9999)}"
#             }

#             # Hacer una solicitud POST a la ruta /login
#             response = await page.goto(f'{BASE_URL}/login', method="POST", headers={'Content-Type': 'application/json'}, postData=json.dumps(login_data))

#             if response and response.status == 200:
#                 # Verificar el contenido de la respuesta
#                 content = await page.text_content('pre')
#                 response_data = json.loads(content)

#                 if valid:
#                     if response_data.get("message") == "Login exitoso":
#                         stats.add_success(time.time() - start_time)
#                         print("✓ POST /login (válido) exitoso")
#                         return
#                     else:
#                         print(f"× POST /login (válido): respuesta inesperada: {response_data}")
#                 else:
#                     if response_data.get("detail") == "Credenciales incorrectas":
#                         stats.add_success(time.time() - start_time)
#                         print("✓ POST /login (inválido) exitoso")
#                         return
#                     else:
#                         print(f"× POST /login (inválido): respuesta inesperada: {response_data}")
#             else:
#                 print(f"× POST /login: estado {response.status if response else 'desconocido'}")

#             # Si llegamos aquí y no es el último intento, reintentamos
#             if attempt < max_retries:
#                 print(f"Reintentando POST /login ({attempt+1}/{max_retries})")
#                 await asyncio.sleep(1)  # Esperar antes de reintentar

#         except Exception as e:
#             print(f"Error en login (intento {attempt+1}): {str(e)}")
#             if attempt < max_retries:
#                 print(f"Reintentando en 1 segundo...")
#                 await asyncio.sleep(1)
#             else:
#                 stats.add_failure()
#         finally:
#             if browser:
#                 await browser.close()

#     # Si llegamos aquí, es porque fallaron todos los intentos
#     stats.add_failure()

async def login(playwright, stats, context, valid=True, max_retries=2):
    start_time = time.time()
    try:
        page = await context.new_page()  # Usar el context proporcionado
        page.set_default_timeout(10000)

        # Datos de login
        login_data = {
            "username": "frank",
            "password": "1234" if valid else f"wrong{random.randint(1000, 9999)}"
        }

        # Hacer una solicitud POST a la ruta /login
        response = await page.goto(f'{BASE_URL}/login', method="POST", headers={'Content-Type': 'application/json'}, postData=json.dumps(login_data))

        if response and response.status == 200:
            content = await page.text_content('pre')
            response_data = json.loads(content)

            if valid:
                if response_data.get("message") == "Login exitoso":
                    stats.add_success(time.time() - start_time)
                    print("✓ POST /login (válido) exitoso")
                    return
                else:
                    print(f"× POST /login (válido): respuesta inesperada: {response_data}")
            else:
                if response_data.get("detail") == "Credenciales incorrectas":
                    stats.add_success(time.time() - start_time)
                    print("✓ POST /login (inválido) exitoso")
                    return
                else:
                    print(f"× POST /login (inválido): respuesta inesperada: {response_data}")
        else:
            print(f"× POST /login: estado {response.status if response else 'desconocido'}")
    except Exception as e:
        print(f"Error en login: {str(e)}")
        stats.add_failure()
    finally:
        await page.close()


# Ejecutar una prueba aleatoria
async def run_random_test(playwright, stats, semaphore, context):
    async with semaphore:
        test_type = random.randint(0, 3)
        test_name = ""
        try:
            if test_type == 0:
                test_name = "get_cursos"
                await get_cursos(playwright, stats, context)
            elif test_type == 1:
                test_name = "get_usuarios"
                await get_usuarios(playwright, stats, context)
            elif test_type == 2:
                test_name = "login (válido)"
                await login(playwright, stats, valid=True)  # Llamada a login con Playwright
            else:
                test_name = "login (inválido)"
                await login(playwright, stats, valid=False)  # Llamada a login con Playwright
        except Exception as e:
            print(f"Error en la prueba {test_name}: {str(e)}")
            stats.add_failure()
        else:
            print(f"Prueba {test_name} exitosa")

# Función principal para ejecutar pruebas de estrés
async def run_stress_test(concurrent_users, test_duration, ramp_up=0):
    stats = Stats()
    
    # Límites para evitar sobrecargar el cliente
    limits = httpx.Limits(max_keepalive_connections=100, max_connections=100)
    
    async with httpx.AsyncClient(limits=limits, timeout=20.0) as client:
        stats.start()
        
        # Si hay tiempo de ramp-up, incrementamos gradualmente los usuarios
        if ramp_up > 0:
            batch_delay = ramp_up / concurrent_users
            
            for i in range(concurrent_users):
                print(f"Iniciando usuario {i+1} de {concurrent_users}")
                asyncio.create_task(run_random_test(client, stats))
                await asyncio.sleep(batch_delay)
        else:
            # Si no hay ramp-up, iniciar todos los usuarios a la vez
            print(f"Iniciando {concurrent_users} usuarios simultáneamente")
            tasks = []
            for _ in range(concurrent_users):
                tasks.append(asyncio.create_task(run_random_test(client, stats)))
        
        # Crear bucle de pruebas para el resto de la duración
        end_time = time.time() + test_duration - (ramp_up if ramp_up > 0 else 0)
        
        print(f"Ejecutando pruebas hasta {time.ctime(end_time)}")
        
        while time.time() < end_time:
            # Crear tareas para todos los usuarios concurrentes
            tasks = []
            for _ in range(concurrent_users):
                tasks.append(asyncio.create_task(run_random_test(client, stats)))
            
            # Esperar a que se completen las tareas
            await asyncio.sleep(1)
        
        # Esperar un tiempo adicional para que terminen las tareas pendientes
        print("Finalizando pruebas, esperando tareas pendientes...")
        await asyncio.sleep(5)
        
        stats.stop()
        
        # Mostrar resultados
        summary = stats.get_summary()
        print("\n--- Resultados de la Prueba de Estrés ---")
        print(f"Duración: {summary['duration_seconds']:.2f} segundos")
        print(f"Solicitudes por segundo: {summary['requests_per_second']:.2f}")
        print(f"Solicitudes exitosas: {summary['successful_requests']}")
        print(f"Solicitudes fallidas: {summary['failed_requests']}")
        print(f"Tasa de éxito: {summary['success_rate']:.2f}%")
        print(f"Tiempo de respuesta promedio: {summary['avg_response_time']:.4f} segundos")
        if summary['min_response_time'] > 0:
            print(f"Tiempo de respuesta mínimo: {summary['min_response_time']:.4f} segundos")
        if summary['max_response_time'] > 0:
            print(f"Tiempo de respuesta máximo: {summary['max_response_time']:.4f} segundos")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ejecutar prueba de estrés en la API')
    parser.add_argument('--users', type=int, default=10, help='Número de usuarios concurrentes')
    parser.add_argument('--duration', type=int, default=30, help='Duración de la prueba en segundos')
    parser.add_argument('--ramp-up', type=int, default=5, help='Tiempo de ramp-up en segundos (0 para iniciar todos a la vez)')
    args = parser.parse_args()
    
    print(f"Iniciando prueba de estrés con {args.users} usuarios concurrentes durante {args.duration} segundos (ramp-up: {args.ramp_up} segundos)")
    
    asyncio.run(run_stress_test(args.users, args.duration, args.ramp_up))