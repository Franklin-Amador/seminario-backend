# Campus Virtual API

Backend API para un Campus Virtual educativo utilizando FastAPI, GraphQL (Strawberry) y PostgreSQL con Prisma ORM.

## Características

- **Doble API**: REST y GraphQL para máxima flexibilidad
- **Base de datos**: PostgreSQL gestionada con Prisma ORM
- **Sin autenticación restrictiva**: Login simple para identificación de usuarios
- **Manejo de archivos**: Soporte para subida y descarga de recursos y entregas
- **Operaciones CRUD completas** para todas las entidades principales

## Estructura del Proyecto

```
campus-virtual/
│
├── .env                       # Variables de entorno (DB_URL, etc.)
│
├── main.py                    # Punto de entrada de la aplicación
├── schema.py                  # Definiciones GraphQL (Strawberry)
│
├── models/                    # Modelos Pydantic
│   └── base.py                # Definiciones de modelos
│
├── controllers/               # Controladores por funcionalidad
│   ├── login_controller.py    # Gestión de login simple
│   ├── file_controller.py     # Manejo de archivos
│   └── rest_controller.py     # Endpoints REST API
│
├── prisma/                    # Configuración Prisma ORM
│   ├── schema.prisma          # Esquema de la BD
│   └── migrations/            # Migraciones automáticas
│       └── migration.sql      # Migración inicial
│
├── uploads/                   # Almacenamiento de archivos (creado automáticamente)
│   ├── assignments/           # Entregas de tareas
│   ├── resources/             # Recursos de cursos
│   └── profiles/              # Imágenes de perfil
│
└── requirements.txt           # Dependencias del proyecto
```

## Requisitos

- Python 3.8+
- PostgreSQL 12+
- Node.js 14+ (para Prisma CLI)

## Instalación

1. Clonar el repositorio:

   ```bash
   git clone <url-del-repositorio>
   cd campus-virtual
   ```

2. Crear un entorno virtual e instalar dependencias:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configurar variables de entorno:
   - Crear archivo `.env` con:

   ```
   DATABASE_URL="postgresql://usuario:contraseña@localhost:5432/campus_virtual"
   ```

4. Generar el cliente Prisma:

   ```bash
   prisma generate
   ```

5. Ejecutar migraciones:

   ```bash
   prisma migrate deploy
   ```

## Ejecución

Iniciar el servidor de desarrollo:

```bash
uvicorn main:app --reload
```

El servidor estará disponible en:

- API: <http://localhost:8000>
- Documentación: <http://localhost:8000/docs>
- GraphQL Playground: <http://localhost:8000/graphql>

## Endpoints Principales

### REST API

- **Roles**: `/api/roles`
- **Usuarios**: `/api/users`
- **Cursos**: `/api/courses`
- **Categorías**: `/api/categories`
- **Asignaciones**: `/api/courses/{course_id}/assignments`
- **Foros**: `/api/courses/{course_id}/forums`
- **Matrículas**: `/api/enrollments`
- **Calificaciones**: `/api/courses/{course_id}/grades`

### GraphQL

Accesible en `/graphql` con operaciones para todas las entidades principales:

- Queries para consulta de datos
- Mutations para creación, actualización y eliminación

### Login

```
POST /login
```

Cuerpo:

```json
{
  "username": "usuario",
  "password": "contraseña"
}
```

### Manejo de Archivos

- **Subir entregas**: `POST /files/assignment/{assignment_id}`
- **Descargar entregas**: `GET /files/assignment/{assignment_id}/{submission_id}`
- **Subir recursos**: `POST /files/resource/{course_id}`
- **Descargar recursos**: `GET /files/resource/{resource_id}`
- **Subir avatar**: `POST /files/profile/{user_id}`
- **Obtener avatar**: `GET /files/profile/{user_id}`

## Ejemplos de Uso

### Ejemplo de Login

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

### Ejemplo de consulta GraphQL

```graphql
query GetAllRoles {
  roles {
    id
    name
    shortname
    description
    sortorder
    archetype
  }
}
```

### Ejemplo de petición REST

```bash
# Obtener todos los cursos
curl -X GET http://localhost:8000/api/courses

# Crear un nuevo rol
curl -X POST http://localhost:8000/api/roles \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tutor",
    "shortname": "tutor",
    "description": "Rol para tutores académicos",
    "sortorder": 4,
    "archetype": "tutor"
  }'
```

## Notas de Desarrollo

### Base de Datos

El sistema utiliza PostgreSQL con Prisma ORM para la gestión de datos. El esquema completo está definido en `prisma/schema.prisma`.

### Sistema de Login

El sistema implementa un login simple sin verificación de tokens para facilitar el desarrollo. Para entornos de producción, se recomienda implementar autenticación JWT y protección de rutas.

### Manejo de Archivos

Los archivos se almacenan en el sistema de archivos local. Para entornos de producción, considerar usar servicios como S3 u otros proveedores de almacenamiento en la nube.

## Consideraciones para Producción

- Implementar autenticación JWT completa
- Hashear contraseñas (actualmente se almacenan en texto plano)
- Mover almacenamiento de archivos a servicios cloud
- Configurar CORS adecuadamente para dominios específicos
- Implementar rate limiting y otros mecanismos de seguridad

## Licencia

[MIT](LICENSE)
