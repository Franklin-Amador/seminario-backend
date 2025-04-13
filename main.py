from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Importar los controladores
import controllers.user_controller as user_controller
import controllers.courses_controller as courses_controller
import controllers.category_controller as category_controller
import controllers.assignments_controller as assignments_controller
import controllers.submission_controller as submission_controller
import controllers.grades_controller as grades_controller
import controllers.enrollments_controller as enrollments_controller
import controllers.forum_controller as forum_controller
import controllers.resources_controller as resources_controller
import controllers.role_controller as role_controller
import controllers.sections_controller as sections_controller
import controllers.file_controller as file_controller
import controllers.login_controller as login_controller

# Crear la aplicación FastAPI
app = FastAPI(
    title="Campus Virtual API",
    description="API para gestionar un campus virtual educativo",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manejador de errores personalizado
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": f"Error interno del servidor: {str(exc)}"}
    )

# Incluir los routers de los controladores
app.include_router(user_controller.router)
app.include_router(courses_controller.router)
app.include_router(category_controller.router)
app.include_router(assignments_controller.router)
app.include_router(submission_controller.router)
app.include_router(grades_controller.router)
app.include_router(enrollments_controller.router)
app.include_router(forum_controller.router)
app.include_router(resources_controller.router)
app.include_router(role_controller.router)
app.include_router(sections_controller.router)
app.include_router(file_controller.router, tags=["files"])
app.include_router(login_controller.router, tags=["login"])

# Endpoint de salud
@app.get("/")
async def root():
    return {"message": "Campus Virtual API está en funcionamiento"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}

# Ejecutar el servidor (si se ejecuta directamente)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)