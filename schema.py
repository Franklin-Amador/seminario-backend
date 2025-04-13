import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI
import uvicorn
from datetime import datetime
from typing import List, Optional, Any, Dict, Union
import bcrypt
from bcrypt import checkpw, gensalt, hashpw
import logging

# Importar los tipos definidos
from types_graphql import (
    User, Course, CourseSection, Category, Module, CourseModule,
    Role, UserRole, Assignment, Section, Submission, Forum,
    ForumDiscussion, ForumPost, GradeItem, Grade, Enrollment,
    CourseCompletion, ErrorResponse, UserResponse, RoleInput,
    UserInput, CourseInput, AssignmentInput, EnrollmentInput,
    SectionInput
)

# Importar la conexión a la base de datos
from db import Database, row_to_dict, rows_to_list

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# Query Type
@strawberry.type
class Query:
    # User Queries
    @strawberry.field
    def users(self) -> List[User]:
        try:
            rows = Database.execute_proc("get_all_users")
            return [User(**row_to_dict(row)) for row in rows]
        except Exception as e:
            logger.error(f"Error al obtener usuarios: {str(e)}")
            raise Exception("Error al obtener usuarios")

    @strawberry.field
    def user(self, user_id: int) -> User:
        try:
            rows = Database.execute_proc("get_user_by_id", user_id)
            if not rows:
                logger.error(f"Usuario no encontrado: {user_id}")
                raise Exception("Usuario no encontrado")
            
            # Convertir los datos y manejar el caso del password
            user_data = row_to_dict(rows[0])
            
            # Si existe la contraseña en los datos pero no queremos exponerla
            # (la clase User debe estar preparada para recibir password en su constructor)
            if 'password' in user_data:
                # Pasamos todos los datos incluyendo password al constructor
                # La clase User sabe que no debe exponer este campo
                return User(**user_data)
            else:
                # Si no hay password, simplemente pasamos los datos tal cual
                return User(**user_data)
        except Exception as e:
            logger.error(f"Error al obtener usuario {user_id}: {str(e)}")
            raise

    # Course Queries
    @strawberry.field
    def courses(self) -> List[Course]:
        try:
            rows = Database.execute_proc("get_all_courses")
            return [Course(**row_to_dict(row)) for row in rows]
        except Exception as e:
            logger.error(f"Error al obtener cursos: {str(e)}")
            raise Exception("Error al obtener cursos")

    @strawberry.field
    def course(self, course_id: int) -> Course:
        try:
            rows = Database.execute_proc("get_course_by_id", course_id)
            if not rows:
                logger.error(f"Curso no encontrado: {course_id}")
                raise Exception("Curso no encontrado")
            return Course(**row_to_dict(rows[0]))
        except Exception as e:
            logger.error(f"Error al obtener curso {course_id}: {str(e)}")
            raise

    @strawberry.field
    def course_sections(self, course_id: int) -> List[CourseSection]:
        try:
            rows = Database.execute_proc("get_course_sections", course_id)
            return [CourseSection(**row_to_dict(row)) for row in rows]
        except Exception as e:
            logger.error(f"Error al obtener secciones del curso {course_id}: {str(e)}")
            raise Exception(f"Error al obtener secciones del curso")

    # Category Queries
    @strawberry.field
    def categories(self) -> List[Category]:
        try:
            rows = Database.execute_proc("get_all_categories")
            return [Category(**row_to_dict(row)) for row in rows]
        except Exception as e:
            logger.error(f"Error al obtener categorías: {str(e)}")
            raise Exception("Error al obtener categorías")

    @strawberry.field
    def category(self, category_id: int) -> Category:
        try:
            rows = Database.execute_proc("get_category_by_id", category_id)
            if not rows:
                logger.error(f"Categoría no encontrada: {category_id}")
                raise Exception("Categoría no encontrada")
            return Category(**row_to_dict(rows[0]))
        except Exception as e:
            logger.error(f"Error al obtener categoría {category_id}: {str(e)}")
            raise

    # Role Queries
    @strawberry.field
    def roles(self) -> List[Role]:
        try:
            rows = Database.execute_proc("get_all_roles")
            return [Role(**row_to_dict(row)) for row in rows]
        except Exception as e:
            logger.error(f"Error al obtener roles: {str(e)}")
            raise Exception("Error al obtener roles")

    @strawberry.field
    def role(self, role_id: int) -> Role:
        try:
            rows = Database.execute_proc("get_role_by_id", role_id)
            if not rows:
                logger.error(f"Rol no encontrado: {role_id}")
                raise Exception("Rol no encontrado")
            return Role(**row_to_dict(rows[0]))
        except Exception as e:
            logger.error(f"Error al obtener rol {role_id}: {str(e)}")
            raise

    # Assignment Queries
    @strawberry.field
    def assignments(self, course_id: Optional[int] = None, section_id: Optional[int] = None) -> List[Assignment]:
        try:
            rows = Database.execute_proc("get_assignments_by_course_section", course_id, section_id)
            return [Assignment(**row_to_dict(row)) for row in rows]
        except Exception as e:
            logger.error(f"Error al obtener asignaciones: {str(e)}")
            raise Exception("Error al obtener asignaciones")
    
    # Todas las asignaciones
    @strawberry.field
    def AllAssigments(self) -> List[Assignment]:
        try:
            rows = Database.execute_proc("get_all_assignments")
            return [Assignment(**row_to_dict(row)) for row in rows]
        except Exception as e:
            logger.error(f"Error al obtener todas las asignaciones: {str(e)}")
            raise Exception("Error al obtener todas las asignaciones")
    
    @strawberry.field
    def AllAssigmentsProx(self) -> List[Assignment]:
        try:
            rows = Database.execute_proc("get_upcoming_assignments")
            return [Assignment(**row_to_dict(row)) for row in rows]
        except Exception as e:
            logger.error(f"Error al obtener asignaciones próximas: {str(e)}")
            raise Exception("Error al obtener asignaciones próximas")
    
    # Asignaciones del curso
    @strawberry.field
    def CourseAssignmentsProx(self, course_id: Optional[int] = None) -> List[Assignment]:
        try:
            rows = Database.execute_proc("get_upcoming_assignments_by_course", course_id)
            return [Assignment(**row_to_dict(row)) for row in rows]
        except Exception as e:
            logger.error(f"Error al obtener asignaciones próximas del curso: {str(e)}")
            raise Exception("Error al obtener asignaciones próximas del curso")

    @strawberry.field
    def assignment(self, assignment_id: int) -> Assignment:
        try:
            rows = Database.execute_proc("get_assignment_by_id", assignment_id)
            if not rows:
                logger.error(f"Asignación no encontrada: {assignment_id}")
                raise Exception("Asignación no encontrada")
            return Assignment(**row_to_dict(rows[0]))
        except Exception as e:
            logger.error(f"Error al obtener asignación {assignment_id}: {str(e)}")
            raise

    # Submission Queries
    @strawberry.field
    def submissions(self, assignment_id: int) -> List[Submission]:
        try:
            rows = Database.execute_proc("get_submissions_by_assignment", assignment_id)
            return [Submission(**row_to_dict(row)) for row in rows]
        except Exception as e:
            logger.error(f"Error al obtener envíos de la asignación {assignment_id}: {str(e)}")
            raise Exception("Error al obtener envíos")

    @strawberry.field
    def user_submissions(self, user_id: int) -> List[Submission]:
        try:
            rows = Database.execute_proc("get_submissions_by_user", user_id)
            return [Submission(**row_to_dict(row)) for row in rows]
        except Exception as e:
            logger.error(f"Error al obtener envíos del usuario {user_id}: {str(e)}")
            raise Exception("Error al obtener envíos del usuario")

    # Forum Queries
    @strawberry.field
    def forums(self, course_id: Optional[int] = None) -> List[Forum]:
        try:
            rows = Database.execute_proc("get_forums", course_id)
            return [Forum(**row_to_dict(row)) for row in rows]
        except Exception as e:
            logger.error(f"Error al obtener foros: {str(e)}")
            raise Exception("Error al obtener foros")

    @strawberry.field
    def forum_discussions(self, forum_id: int) -> List[ForumDiscussion]:
        try:
            rows = Database.execute_proc("get_forum_discussions", forum_id)
            return [ForumDiscussion(**row_to_dict(row)) for row in rows]
        except Exception as e:
            logger.error(f"Error al obtener discusiones del foro {forum_id}: {str(e)}")
            raise Exception("Error al obtener discusiones del foro")

    @strawberry.field
    def forum_posts(self, discussion_id: int) -> List[ForumPost]:
        try:
            rows = Database.execute_proc("get_forum_posts", discussion_id)
            return [ForumPost(**row_to_dict(row)) for row in rows]
        except Exception as e:
            logger.error(f"Error al obtener posts de la discusión {discussion_id}: {str(e)}")
            raise Exception("Error al obtener posts de la discusión")

    # Grade Queries
    @strawberry.field
    def course_grades(self, course_id: int) -> List[GradeItem]:
        try:
            rows = Database.execute_proc("get_grade_items_by_course", course_id)
            return [GradeItem(**row_to_dict(row)) for row in rows]
        except Exception as e:
            logger.error(f"Error al obtener calificaciones del curso {course_id}: {str(e)}")
            raise Exception("Error al obtener calificaciones del curso")

    @strawberry.field
    def user_grades(self, user_id: int) -> List[Grade]:
        try:
            rows = Database.execute_proc("get_grades_by_user", user_id)
            return [Grade(**row_to_dict(row)) for row in rows]
        except Exception as e:
            logger.error(f"Error al obtener calificaciones del usuario {user_id}: {str(e)}")
            raise Exception("Error al obtener calificaciones del usuario")

    # Enrollment Queries
    @strawberry.field
    def course_enrollments(self, course_id: int) -> List[Enrollment]:
        try:
            rows = Database.execute_proc("get_enrollments_by_course", course_id)
            return [Enrollment(**row_to_dict(row)) for row in rows]
        except Exception as e:
            logger.error(f"Error al obtener inscripciones del curso {course_id}: {str(e)}")
            raise Exception("Error al obtener inscripciones del curso")

    @strawberry.field
    def user_enrollments(self, user_id: int) -> List[Enrollment]:
        try:
            rows = Database.execute_proc("get_enrollments_by_user", user_id)
            
            # Los resultados contienen campos del curso y de la inscripción juntos
            enrollments = []
            
            for row in rows:
                row_dict = row_to_dict(row)
                
                # Separar los campos del curso
                course_data = {
                    "id": row_dict["course_id"],
                    "category": row_dict["category"],
                    "sortorder": row_dict["sortorder"],
                    "fullname": row_dict["fullname"],
                    "shortname": row_dict["shortname"],
                    "idnumber": row_dict["idnumber"],
                    "summary": row_dict["summary"],
                    "format": row_dict["format"],
                    "startdate": row_dict["startdate"],
                    "enddate": row_dict["enddate"],
                    "visible": row_dict["visible"],
                    "timecreated": row_dict["course_timecreated"],
                    "timemodified": row_dict["course_timemodified"]
                }
                
                # Crear el objeto Enrollment con el curso incluido
                enrollment_data = {
                    "id": row_dict["id"],
                    "enrolid": row_dict["enrolid"],
                    "userid": row_dict["userid"],
                    "courseid": row_dict["courseid"],
                    "course": Course(**course_data),
                    "status": row_dict["status"],
                    "timestart": row_dict["timestart"],
                    "timeend": row_dict["timeend"],
                    "timecreated": row_dict["timecreated"],
                    "timemodified": row_dict["timemodified"]
                }
                
                enrollments.append(Enrollment(**enrollment_data))
                
            return enrollments
        except Exception as e:
            logger.error(f"Error al obtener inscripciones del usuario {user_id}: {str(e)}")
            raise Exception("Error al obtener inscripciones del usuario")

    @strawberry.field
    def course_completions(self, course_id: int) -> List[CourseCompletion]:
        try:
            rows = Database.execute_proc("get_completions_by_course", course_id)
            return [CourseCompletion(**row_to_dict(row)) for row in rows]
        except Exception as e:
            logger.error(f"Error al obtener completados del curso {course_id}: {str(e)}")
            raise Exception("Error al obtener completados del curso")

    @strawberry.field
    def user_completions(self, user_id: int) -> List[CourseCompletion]:
        try:
            rows = Database.execute_proc("get_completions_by_user", user_id)
            return [CourseCompletion(**row_to_dict(row)) for row in rows]
        except Exception as e:
            logger.error(f"Error al obtener completados del usuario {user_id}: {str(e)}")
            raise Exception("Error al obtener completados del usuario")
    
    @strawberry.field
    def sections(self, course_id: int) -> List[Section]:
        try:
            rows = Database.execute_proc("get_course_sections", course_id)
            return [Section(**row_to_dict(row)) for row in rows]
        except Exception as e:
            logger.error(f"Error al obtener secciones del curso {course_id}: {str(e)}")
            raise Exception("Error al obtener secciones del curso")

# Mutation Type
@strawberry.type
class Mutation:
    # Role Mutations
    @strawberry.mutation
    def create_role(self, input: RoleInput) -> Role:
        try:
            # Usar execute_proc_transaction para asegurar que se ejecuta en una transacción
            rows = Database.execute_proc_transaction(
                "create_role",
                input.name,
                input.shortname,
                input.description,
                input.sortorder,
                input.archetype
            )
            
            if not rows:
                logger.error("Error al crear el rol: no se devolvieron resultados")
                raise Exception("Error al crear el rol")
                
            return Role(**row_to_dict(rows[0]))
        except Exception as e:
            logger.error(f"Error al crear el rol: {str(e)}")
            raise

    @strawberry.mutation
    def update_role(
        self,
        role_id: int,
        input: RoleInput
    ) -> Role:
        try:
            rows = Database.execute_proc_transaction(
                "update_role",
                role_id,
                input.name,
                input.shortname,
                input.description,
                input.sortorder,
                input.archetype
            )
            
            if not rows:
                logger.error(f"Rol no encontrado: {role_id}")
                raise Exception("Rol no encontrado")
                
            return Role(**row_to_dict(rows[0]))
        except Exception as e:
            logger.error(f"Error al actualizar el rol {role_id}: {str(e)}")
            raise

    @strawberry.mutation
    def delete_role(self, role_id: int) -> Role:
        try:
            rows = Database.execute_proc_transaction("delete_role", role_id)
            
            if not rows:
                logger.error(f"Rol no encontrado: {role_id}")
                raise Exception("Rol no encontrado")
                
            return Role(**row_to_dict(rows[0]))
        except Exception as e:
            logger.error(f"Error al eliminar el rol {role_id}: {str(e)}")
            raise

    # User Mutations
    @strawberry.mutation
    def create_user(self, input: UserInput) -> User:
        try:
            # Hash de la contraseña con bcrypt
            hashed_password = bcrypt.hashpw(input.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            
            rows = Database.execute_proc_transaction(
                "create_user",
                input.username,
                hashed_password,
                input.firstname,
                input.lastname,
                input.email,
                input.institution,
                input.department
            )
            
            if not rows:
                logger.error("Error al crear el usuario: no se devolvieron resultados")
                raise Exception("Error al crear el usuario")
                
            return User(**row_to_dict(rows[0]))
        except Exception as e:
            logger.error(f"Error al crear el usuario: {str(e)}")
            raise

    @strawberry.mutation
    def update_user(
        self,
        user_id: int,
        input: UserInput
    ) -> User:
        try:
            # Hash de la contraseña con bcrypt
            hashed_password = bcrypt.hashpw(input.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            
            rows = Database.execute_proc_transaction(
                "update_user",
                user_id,
                input.username,
                hashed_password,
                input.firstname,
                input.lastname,
                input.email,
                input.institution,
                input.department
            )
            
            if not rows:
                logger.error(f"Usuario no encontrado: {user_id}")
                raise Exception("Usuario no encontrado")
                
            return User(**row_to_dict(rows[0]))
        except Exception as e:
            logger.error(f"Error al actualizar el usuario {user_id}: {str(e)}")
            raise

    # Course Mutations
    @strawberry.mutation
    def create_course(self, input: CourseInput) -> Course:
        try:
            rows = Database.execute_proc_transaction(
                "create_course",
                input.category,
                input.sortorder,
                input.fullname,
                input.shortname,
                input.idnumber,
                input.summary,
                input.format,
                input.startdate,
                input.enddate,
                input.visible
            )
            
            if not rows:
                logger.error("Error al crear el curso: no se devolvieron resultados")
                raise Exception("Error al crear el curso")
                
            return Course(**row_to_dict(rows[0]))
        except Exception as e:
            logger.error(f"Error al crear el curso: {str(e)}")
            raise

    @strawberry.mutation
    def update_course(
        self,
        course_id: int,
        input: CourseInput
    ) -> Course:
        try:
            rows = Database.execute_proc_transaction(
                "update_course",
                course_id,
                input.category,
                input.sortorder,
                input.fullname,
                input.shortname,
                input.idnumber,
                input.summary,
                input.format,
                input.startdate,
                input.enddate,
                input.visible
            )
            
            if not rows:
                logger.error(f"Curso no encontrado: {course_id}")
                raise Exception("Curso no encontrado")
                
            return Course(**row_to_dict(rows[0]))
        except Exception as e:
            logger.error(f"Error al actualizar el curso {course_id}: {str(e)}")
            raise

    # Assignment Mutations
    @strawberry.mutation
    def create_assignment(self, input: AssignmentInput) -> Assignment:
        try:
            rows = Database.execute_proc_transaction(
                "create_assignment",
                input.course,
                input.name,
                input.intro,
                input.section,
                input.duedate,
                input.allowsubmissionsfromdate,
                input.grade
            )
            
            if not rows:
                logger.error("Error al crear la asignación: no se devolvieron resultados")
                raise Exception("Error al crear la asignación")
                
            return Assignment(**row_to_dict(rows[0]))
        except Exception as e:
            logger.error(f"Error al crear la asignación: {str(e)}")
            raise

    @strawberry.mutation
    def update_assignment(
        self,
        assignment_id: int,
        input: AssignmentInput
    ) -> Assignment:
        try:
            rows = Database.execute_proc_transaction(
                "update_assignment",
                assignment_id,
                input.name,
                input.intro,
                input.section,
                input.duedate,
                input.allowsubmissionsfromdate,
                input.grade
            )
            
            if not rows:
                logger.error(f"Asignación no encontrada: {assignment_id}")
                raise Exception("Asignación no encontrada")
                
            return Assignment(**row_to_dict(rows[0]))
        except Exception as e:
            logger.error(f"Error al actualizar la asignación {assignment_id}: {str(e)}")
            raise

    # Enrollment Mutations
    @strawberry.mutation
    def create_enrollment(self, input: EnrollmentInput) -> Enrollment:
        try:
            rows = Database.execute_proc_transaction(
                "create_enrollment",
                input.enrolid,
                input.userid,
                input.courseid,
                input.status,
                input.timestart,
                input.timeend
            )
            
            if not rows:
                logger.error("Error al crear la inscripción: no se devolvieron resultados")
                raise Exception("Error al crear la inscripción")
                
            return Enrollment(**row_to_dict(rows[0]))
        except Exception as e:
            logger.error(f"Error al crear la inscripción: {str(e)}")
            raise

    @strawberry.mutation
    def update_enrollment(
        self,
        enrollment_id: int,
        input: EnrollmentInput
    ) -> Enrollment:
        try:
            rows = Database.execute_proc_transaction(
                "update_enrollment",
                enrollment_id,
                input.enrolid,
                input.status,
                input.timestart,
                input.timeend
            )
            
            if not rows:
                logger.error(f"Inscripción no encontrada: {enrollment_id}")
                raise Exception("Inscripción no encontrada")
                
            return Enrollment(**row_to_dict(rows[0]))
        except Exception as e:
            logger.error(f"Error al actualizar la inscripción {enrollment_id}: {str(e)}")
            raise

    @strawberry.mutation
    def delete_enrollment(self, enrollment_id: int) -> Enrollment:
        try:
            rows = Database.execute_proc_transaction("delete_enrollment", enrollment_id)
            
            if not rows:
                logger.error(f"Inscripción no encontrada: {enrollment_id}")
                raise Exception("Inscripción no encontrada")
                
            return Enrollment(**row_to_dict(rows[0]))
        except Exception as e:
            logger.error(f"Error al eliminar la inscripción {enrollment_id}: {str(e)}")
            raise
    
    # Login mutation con manejo de errores usando tipos de respuesta personalizados
    @strawberry.mutation
    def login(self, email: str, password: str) -> UserResponse:
        try:
        # Determinar si el input es un email o un username
            is_email = '@' in email
        
        # Usar el procedimiento almacenado adecuado (login_email o user_login)
            if is_email:
            # Si parece un email, usamos login_email
                rows = Database.execute_proc("login_email", email, password)
            else:
            # Si no parece un email, asumimos que es un username
                rows = Database.execute_proc("user_login", email, password)
        
            if not rows or not rows[0]['is_valid']:
                logger.error(f"Login fallido: Usuario no encontrado o credenciales incorrectas - {email}")
                return UserResponse(
                    error=ErrorResponse(
                        message="Credenciales incorrectas",
                        code=401
                    )
                )

        # Extraer los datos del usuario de la respuesta
            user_data = row_to_dict(rows[0])
        
        # Login exitoso - registrar
            logger.info(f"Login exitoso: {email}")
        
        # Registrar el intento de login exitoso en la tabla de auditoría
            Database.execute_proc(
                "audit_login_attempt",
                user_data['username'],
                "localhost",  # IP placeholder
                "API Client",  # User-Agent placeholder
                True          # Login exitoso
            )
        
        # Retornar los datos del usuario exitosamente
            return UserResponse(
                user=User(
                    id=user_data['user_id'],
                    username=user_data['username'],
                    email=user_data['email'],
                    firstname=user_data['firstname'],
                    lastname=user_data['lastname'],
                    confirmed=True,  # Valor por defecto para usuarios que pueden hacer login
                    deleted=False,   # Un usuario no borrado
                    suspended=False, # Un usuario no suspendido
                    institution=None,
                    department=None,
                    timecreated=datetime.now(),  # Placeholder
                    timemodified=datetime.now()  # Placeholder
                )
            )
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return UserResponse(
                error=ErrorResponse(
                    message=f"Error interno: {str(e)}",
                    code=500
                )
            )
        
    # Mutación para cambiar la contraseña con manejo de errores
    @strawberry.mutation
    def change_password(self, email: str, new_password: str) -> UserResponse:
        try:
            # Hash de la nueva contraseña
            hashed_new_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            
            # Usar el procedimiento almacenado para actualizar la contraseña
            rows = Database.execute_proc_transaction("update_user_password", email, hashed_new_password)
            
            if not rows or not rows[0]['success']:
                logger.error(f"Cambio de contraseña fallido: Usuario no encontrado - {email}")
                return UserResponse(
                    error=ErrorResponse(
                        message="Usuario no encontrado",
                        code=404
                    )
                )
            
            logger.info(f"Contraseña cambiada exitosamente para usuario: {email}")
            
            # Obtener datos del usuario para devolver
            user_rows = Database.execute("SELECT * FROM mdl_user WHERE email = %s AND deleted = FALSE", email, fetch=True)
            
            if not user_rows:
                return UserResponse(
                    error=ErrorResponse(
                        message="Usuario no encontrado después de cambiar contraseña",
                        code=404
                    )
                )
                
            user_data = row_to_dict(user_rows[0])
            
            return UserResponse(
                user=User(**user_data)
            )
        except Exception as e:
            logger.error(f"Error al cambiar contraseña: {str(e)}")
            return UserResponse(
                error=ErrorResponse(
                    message=f"Error interno: {str(e)}",
                    code=500
                )
            )
     
    # Section Mutations
    @strawberry.mutation
    def create_section(self, input: SectionInput) -> Section:
        try:
            rows = Database.execute_proc_transaction(
                "create_section",
                input.course,
                input.name,
                input.summary,
                input.sequence,
                input.visible
            )
            
            if not rows:
                logger.error("Error al crear la sección: no se devolvieron resultados")
                raise Exception("Error al crear la sección")
                
            return Section(**row_to_dict(rows[0]))
        except Exception as e:
            logger.error(f"Error al crear la sección: {str(e)}")
            raise

    @strawberry.mutation
    def update_section(self, section_id: int, input: SectionInput) -> Section:
        try:
            rows = Database.execute_proc_transaction(
                "update_section",
                section_id,
                input.name,
                input.summary,
                input.sequence,
                input.visible
            )
            
            if not rows:
                logger.error(f"Sección no encontrada: {section_id}")
                raise Exception("Sección no encontrada")
                
            return Section(**row_to_dict(rows[0]))
        except Exception as e:
            logger.error(f"Error al actualizar la sección {section_id}: {str(e)}")
            raise

    @strawberry.mutation
    def delete_section(self, section_id: int) -> Section:
        try:
            rows = Database.execute_proc_transaction("delete_section", section_id)
            
            if not rows:
                logger.error(f"Sección no encontrada: {section_id}")
                raise Exception("Sección no encontrada")
                
            return Section(**row_to_dict(rows[0]))
        except Exception as e:
            logger.error(f"Error al eliminar la sección {section_id}: {str(e)}")
            raise


# Create schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Crear un router GraphQL para FastAPI
graphql_app = GraphQLRouter(schema)

# Crear la aplicación FastAPI
app = FastAPI()

# Agregar el router GraphQL
app.include_router(graphql_app, prefix="/graphql")

# Punto de entrada para ejecución directa
if __name__ == "__main__":
    uvicorn.run("schema:app", host="0.0.0.0", port=8000, reload=True)
