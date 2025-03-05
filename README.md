# Campus Virtual API

Backend completo para un Campus Virtual educativo utilizando FastAPI, GraphQL (Strawberry) y PostgreSQL con Prisma ORM.

## Características

- **API Dual**: Endpoints REST y GraphQL para máxima flexibilidad
- **Base de datos**: PostgreSQL con Prisma ORM para gestión eficiente de datos
- **Login Simple**: Sistema de login sin autenticación restrictiva
- **Manejo de archivos**: Soporte para subida y descarga de recursos, tareas y perfiles
- **Operaciones CRUD completas** para todas las entidades principales
- **Containerización**: Configuración completa con Docker y Docker Compose

## Estructura del Proyecto

```
campus-virtual/
│
├── .env                       # Variables de entorno (DATABASE_URL, etc.)
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
├── uploads/                   # Almacenamiento de archivos
│   ├── assignments/           # Entregas de tareas
│   ├── resources/             # Recursos de cursos
│   └── profiles/              # Imágenes de perfil
│
├── Dockerfile                 # Configuración de Docker
├── docker-compose.yml         # Configuración de Docker Compose
└── requirements.txt           # Dependencias del proyecto
```

## Requisitos

Para ejecución local (sin Docker):

- Python 3.8+
- PostgreSQL 12+
- Node.js 14+ (para Prisma CLI)

Con Docker (recomendado):

- Docker y Docker Compose

## Instalación y Ejecución

### Usando Docker (Recomendado)

1. Clonar el repositorio:

   ```bash
   git clone <url-del-repositorio>
   cd seminario-backend
   ```

2. Iniciar los contenedores:

   ```bash
   docker-compose up -d
   ```

3. La API estará disponible en:
   - API: <http://localhost:8000>
   - Documentación: <http://localhost:8000/docs>
   - GraphQL Playground: <http://localhost:8000/graphql>

### Instalación Local (Alternativa)

1. Clonar el repositorio:

   ```bash
   git clone <url-del-repositorio>
   cd seminario-backend
   ```

2. Crear un entorno virtual e instalar dependencias:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configurar variables de entorno:
   - Crear un archivo `.env` con:

   ```
   DATABASE_URL="postgresql://usuario:contraseña@localhost:5432/dbname"
   ```

4. Generar el cliente Prisma:

   ```bash
   prisma generate
   ```

5. Ejecutar migraciones:

   ```bash
   prisma migrate deploy
   ```

6. Iniciar el servidor:

   ```bash
   uvicorn main:app --reload
   ```

## Uso de la API

### Documentación Automática

La documentación completa de la API REST está disponible en `/docs` una vez que el servidor está corriendo.

### Sistema de Login

El sistema implementa un endpoint de login simple sin verificación de tokens:

```
POST /login
```

Cuerpo de la solicitud:

```json
{
  "username": "usuario",
  "password": "contraseña"
}
```

Respuesta exitosa:

```json
{
  "success": true,
  "user_id": 1,
  "username": "admin",
  "firstname": "Admin",
  "lastname": "User",
  "email": "admin@example.com",
  "roles": [
    {
      "id": 1,
      "name": "Administrador",
      "shortname": "admin"
    }
  ],
  "message": "Login exitoso"
}
```

### REST API

#### Roles

```
GET /api/roles             # Obtener todos los roles
GET /api/roles/{id}        # Obtener rol por ID
POST /api/roles            # Crear nuevo rol
PUT /api/roles/{id}        # Actualizar rol
DELETE /api/roles/{id}     # Eliminar rol
```

#### Usuarios

```
GET /api/users             # Obtener todos los usuarios
GET /api/users/{id}        # Obtener usuario por ID
POST /api/users            # Crear nuevo usuario
PUT /api/users/{id}        # Actualizar usuario
DELETE /api/users/{id}     # Eliminar usuario (marca como eliminado)
```

#### Cursos

```
GET /api/courses                          # Obtener todos los cursos
GET /api/courses/{id}                     # Obtener curso por ID
POST /api/courses                         # Crear nuevo curso
PUT /api/courses/{id}                     # Actualizar curso
DELETE /api/courses/{id}                  # Eliminar curso (marca como no visible)
GET /api/courses/{id}/assignments         # Obtener tareas de un curso
POST /api/courses/{id}/assignments        # Crear tarea en un curso
GET /api/courses/{id}/forums              # Obtener foros de un curso
POST /api/courses/{id}/forums             # Crear foro en un curso
GET /api/courses/{id}/enrollments         # Obtener matrículas de un curso
GET /api/courses/{id}/grades              # Obtener elementos de calificación de un curso
GET /api/courses/{id}/user/{user_id}/grades # Obtener calificaciones de un usuario en un curso
GET /api/courses/{id}/resources           # Obtener recursos de un curso
POST /api/courses/{id}/resources          # Crear recurso en un curso
```

#### Manejo de Archivos

```
POST /files/assignment/{assignment_id}           # Subir entrega de tarea
GET /files/assignment/{assignment_id}/{submission_id} # Descargar entrega
POST /files/resource/{course_id}                 # Subir recurso
GET /files/resource/{resource_id}                # Descargar recurso
POST /files/profile/{user_id}                    # Subir imagen de perfil
GET /files/profile/{user_id}                     # Obtener imagen de perfil
```

### GraphQL

El endpoint GraphQL está disponible en `/graphql` con un playground para pruebas interactivas.

#### Ejemplos de consultas GraphQL

Consultar todos los roles:

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

Crear un nuevo rol:

```graphql
mutation CreateRole {
  createRole(
    input: {
      name: "Estudiante",
      shortname: "student",
      description: "Rol para estudiantes del campus",
      sortorder: 5,
      archetype: "student"
    }
  ) {
    id
    name
    shortname
    description
    sortorder
    archetype
  }
}
```

## Mantenimiento

### Gestión de Contenedores

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Reiniciar los servicios
docker-compose restart

# Detener los contenedores
docker-compose down

# Reconstruir las imágenes
docker-compose build --no-cache

# Iniciar los contenedores reconstruidos
docker-compose up -d
```

### Backups de Base de Datos

```bash
# Crear backup de la base de datos
docker-compose exec db pg_dump -U postgres campus_virtual > backup_$(date +%Y%m%d).sql

# Restaurar backup
cat backup_20250305.sql | docker-compose exec -T db psql -U postgres campus_virtual
```

## Notas de Desarrollo

### Base de Datos

El sistema utiliza PostgreSQL con Prisma ORM. El esquema completo está definido en `prisma/schema.prisma`.

Para modificar el esquema:

1. Editar `schema.prisma`
2. Generar la migración: `prisma migrate dev --name <nombre_del_cambio>`

### Sistema de Login

El sistema implementa un login simple sin verificación de tokens para facilitar el desarrollo. Para entornos de producción, se recomienda implementar autenticación JWT y protección de rutas.

### Manejo de Archivos

Los archivos se almacenan dentro del contenedor y se persisten usando volúmenes Docker. Para entornos de producción, considerar usar servicios como S3 u otros proveedores de almacenamiento en la nube.

## Consideraciones para Producción

- Implementar autenticación JWT completa
- Hashear contraseñas (actualmente se almacenan en texto plano)
- Mover almacenamiento de archivos a servicios cloud
- Configurar CORS adecuadamente para dominios específicos
- Implementar rate limiting y otros mecanismos de seguridad
- Utilizar un proxy inverso como Nginx para servir la aplicación
- Configurar HTTPS

## Licencia

[MIT](LICENSE)
