import json
import asyncio
import time
from playwright.async_api import async_playwright
import random
import argparse
import matplotlib.pyplot as plt

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
    def plot_results(self):
        summary = self.get_summary()
        
        # Crear un gráfico de barras para las solicitudes exitosas y fallidas
        labels = ['Successful Requests', 'Failed Requests']
        values = [self.successful_requests, self.failed_requests]

        plt.figure(figsize=(10, 6))
        
        plt.subplot(2, 2, 1)
        plt.bar(labels, values, color=['green', 'red'])
        plt.title('Requests Summary')
        plt.ylabel('Number of Requests')

        # Crear un gráfico de líneas para los tiempos de respuesta
        plt.subplot(2, 2, 2)
        plt.plot(self.response_times, label='Response Time')
        plt.title('Response Times')
        plt.xlabel('Request Number')
        plt.ylabel('Response Time (seconds)')
        plt.legend()

        # Crear un gráfico de líneas para el tiempo de respuesta promedio
        plt.subplot(2, 2, 3)
        plt.axhline(y=summary['avg_response_time'], color='blue', linestyle='-', label='Avg Response Time')
        plt.title('Average Response Time')
        plt.xlabel('Requests')
        plt.ylabel('Response Time (seconds)')
        plt.legend()

        # Crear un gráfico de líneas para el tiempo de respuesta mínimo y máximo
        plt.subplot(2, 2, 4)
        plt.axhline(y=summary['min_response_time'], color='green', linestyle='-', label='Min Response Time')
        plt.axhline(y=summary['max_response_time'], color='red', linestyle='-', label='Max Response Time')
        plt.title('Min and Max Response Times')
        plt.xlabel('Requests')
        plt.ylabel('Response Time (seconds)')
        plt.legend()

        plt.tight_layout()
        plt.show()

# funcion para probar endpoint de cursos
async def get_cursos(playwright, stats, context):
    start_time = time.time()
    try:
        page = await context.new_page()  # Usar el context proporcionado
        page.set_default_timeout(10000)
        response = await page.goto(f'{BASE_URL}/api/courses')
        if response and response.status == 200:
            content = await page.text_content('pre')
            cursos = json.loads(content)
            if isinstance(cursos, list) and len(cursos) > 0:
                stats.add_success(time.time() - start_time)
                print("✓ GET /api/courses exitoso")
                return
            else:
                print("x GET /api/courses: respuesta vacía o formato incorrecto")
        else:
            print(f"x GET /api/courses: estado {response.status if response else 'desconocido'}")
    except Exception as e:
        print(f"Error en get_cursos: {str(e)}")
        stats.add_failure()
    finally:
        await page.close()

# funcion para probar endpoint de usuarios
async def get_usuarios(playwright, stats, context):
    start_time = time.time()
    try:
        page = await context.new_page()  # Usar el context proporcionado
        page.set_default_timeout(10000)
        response = await page.goto(f'{BASE_URL}/api/users')
        if response and response.status == 200:
            content = await page.text_content('pre')
            usuarios = json.loads(content)
            if isinstance(usuarios, list) and len(usuarios) > 0:
                stats.add_success(time.time() - start_time)
                print("✓ GET /api/users exitoso")
                return
            else:
                print("x GET /api/users: respuesta vacía o formato incorrecto")
        else:
            print(f"x GET /api/users: estado {response.status if response else 'desconocido'}")
    except Exception as e:
        print(f"Error en get_usuarios: {str(e)}")
        stats.add_failure()
    finally:
        await page.close()
        
# funcios para endpoint de categorias
async def get_categorias(playwright, stats, context):
    start_time = time.time()
    try:
        page = await context.new_page()  # Usar el context proporcionado
        page.set_default_timeout(10000)
        response = await page.goto(f'{BASE_URL}/api/categories')
        if response and response.status == 200:
            content = await page.text_content('pre')
            categorias = json.loads(content)
            if isinstance(categorias, list) and len(categorias) > 0:
                stats.add_success(time.time() - start_time)
                print("✓ GET /api/categories exitoso")
                return
            else:
                print("x GET /api/categories: respuesta vacía o formato incorrecto")
        else:
            print(f"x GET /api/categories: estado {response.status if response else 'desconocido'}")
    except Exception as e:
        print(f"Error en get_categorias: {str(e)}")
        stats.add_failure()
    finally:
        await page.close()

# funcion para probar endpoint de login
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

        # Hacer una solicitud POST a la ruta /login usando fetch en el navegador
        response = await page.evaluate('''async ({ url, data }) => {
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                return {
                    status: response.status,
                    body: await response.text()
                };
            } catch (error) {
                return {
                    status: 0,  // Indica un error de red o de fetch
                    body: error.toString()
                };
            }
        }''', { "url": f'{BASE_URL}/login', "data": login_data })  # Pasar un solo objeto

        if response['status'] == 200:
            # Verificar el contenido de la respuesta
            response_data = json.loads(response['body'])

            if valid:
                if response_data.get("message") == "Login exitoso":
                    stats.add_success(time.time() - start_time)
                    print("✓ POST /login (válido) exitoso")
                    return
                else:
                    print(f"× POST /login (válido): respuesta inesperada: {response_data}")
            else:
                print(f"× POST /login (inválido): estado {response['status']}, error: {response['body']}")
                stats.add_failure()
        elif response['status'] == 401:
            # Verificar el contenido de la respuesta
            response_data = json.loads(response['body'])
            if response_data.get("detail") == "Credenciales incorrectas":
                stats.add_success(time.time() - start_time)
                print("✓ POST /login (inválido) exitoso")
                return
            else:
                print(f"× POST /login (inválido): respuesta inesperada: {response_data}")
                stats.add_failure()
        else:
            print(f"× POST /login: estado {response['status']}, error: {response['body']}")
            stats.add_failure()
    except Exception as e:
        print(f"Error en login: {str(e)}")
        stats.add_failure()
    finally:
        await page.close()


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
                await login(playwright, stats, context, valid=True)  # Pasar context a login
            else:
                test_name = "login (inválido)"
                await login(playwright, stats, context, valid=False)  # Pasar context a login
        except Exception as e:
            print(f"Error en la prueba {test_name}: {str(e)}")
            stats.add_failure()
        else:
            print(f"Prueba {test_name} exitosa")

async def run_stress_test(concurrent_users, test_duration, ramp_up=0, max_concurrent_requests=3):  # Reducir max_concurrent_requests
    stats = Stats()
    semaphore = asyncio.Semaphore(max_concurrent_requests)
    
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()  # Crear un solo context para reutilizar
        
        stats.start()
        
        if ramp_up > 0:
            batch_delay = ramp_up / concurrent_users
            for i in range(concurrent_users):
                print(f"Iniciando usuario {i+1} de {concurrent_users}")
                asyncio.create_task(run_random_test(playwright, stats, semaphore, context))
                await asyncio.sleep(batch_delay)
        else:
            print(f"Iniciando {concurrent_users} usuarios simultáneamente")
            for _ in range(concurrent_users):
                asyncio.create_task(run_random_test(playwright, stats, semaphore, context))
        
        end_time = time.time() + test_duration - (ramp_up if ramp_up > 0 else 0)
        
        while time.time() < end_time:
            for _ in range(concurrent_users):
                asyncio.create_task(run_random_test(playwright, stats, semaphore, context))
            await asyncio.sleep(2)
        
        print("Finalizando pruebas, esperando tareas pendientes...")
        await asyncio.sleep(5)
        
        stats.stop()
        await browser.close()
        
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
            
        # Mostrar gráficos
        stats.plot_results()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ejecutar prueba de estrés en la API')
    parser.add_argument('--users', type=int, default=10, help='Número de usuarios concurrentes')
    parser.add_argument('--duration', type=int, default=30, help='Duración de la prueba en segundos')
    parser.add_argument('--ramp-up', type=int, default=5, help='Tiempo de ramp-up en segundos (0 para iniciar todos a la vez)')
    parser.add_argument('--max-concurrent', type=int, default=5, help='Máximo número de solicitudes concurrentes')
    args = parser.parse_args()
    
    print(f"Iniciando prueba de estrés con {args.users} usuarios concurrentes durante {args.duration} segundos (ramp-up: {args.ramp_up} segundos)")
    
    asyncio.run(run_stress_test(args.users, args.duration, args.ramp_up, args.max_concurrent))