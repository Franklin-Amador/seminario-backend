import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI
import uvicorn
from datetime import datetime
from typing import List, Optional, Any, Dict, Union
import bcrypt
from bcrypt import checkpw, gensalt, hashpw
from db import prisma_client
from exceptions import NotFoundError, UnauthorizedError
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# User Types
@strawberry.type
class User:
    id: int
    username: str
    firstname: str
    lastname: str
    email: str
    confirmed: bool
    deleted: bool
    suspended: bool
    institution: Optional[str]
    department: Optional[str]
    timecreated: datetime
    timemodified: datetime

# Course Types
@strawberry.type
class Course:
    id: int
    category: int
    sortorder: int
    fullname: str
    shortname: str
    idnumber: Optional[str]
    summary: Optional[str]
    format: str
    startdate: datetime
    enddate: Optional[datetime]
    visible: bool
    timecreated: datetime
    timemodified: datetime

@strawberry.type
class CourseSection:
    id: int
    course: int
    section: int
    name: Optional[str]
    summary: Optional[str]
    sequence: Optional[str]
    visible: bool
    timemodified: datetime

@strawberry.type
class Category:
    id: int
    name: str
    idnumber: Optional[str]
    description: Optional[str]
    parent: int
    sortorder: int
    visible: bool
    depth: int
    path: str

# Module Types
@strawberry.type
class Module:
    id: int
    name: str
    visible: bool

@strawberry.type
class CourseModule:
    id: int
    course: int
    module: int
    instance: int
    section: int
    idnumber: Optional[str]
    added: datetime
    visible: bool

# Role Types
@strawberry.type
class Role:
    id: int
    name: str
    shortname: str
    description: Optional[str]
    sortorder: int
    archetype: Optional[str]

@strawberry.type
class UserRole:
    id: int
    roleid: int
    contextid: int
    userid: int
    timemodified: datetime

# Assignment Types
@strawberry.type
class Assignment:
    id: int
    course: int
    name: str
    intro: str
    section: int
    duedate: Optional[datetime]
    allowsubmissionsfromdate: Optional[datetime]
    grade: Optional[int]
    timemodified: datetime
    
@strawberry.type
class Section:
    id: int
    course: int
    section: int
    name: str
    summary: Optional[str]
    sequence: Optional[str]
    visible: bool
    timemodified: datetime

@strawberry.type
class Submission:
    id: int
    assignment: int
    userid: int
    timecreated: datetime
    timemodified: datetime
    status: str
    attemptnumber: int
    latest: bool

# Forum Types
@strawberry.type
class Forum:
    id: int
    course: int
    type: str
    name: str
    intro: str
    timemodified: datetime

@strawberry.type
class ForumDiscussion:
    id: int
    course: int
    forum: int
    name: str
    userid: int
    timemodified: datetime

@strawberry.type
class ForumPost:
    id: int
    discussion: int
    parent: int
    userid: int
    created: datetime
    modified: datetime
    subject: str
    message: str

# Grade Types
@strawberry.type
class GradeItem:
    id: int
    courseid: int
    itemname: Optional[str]
    itemtype: str
    itemmodule: Optional[str]
    grademax: int
    grademin: int
    timecreated: datetime
    timemodified: datetime

@strawberry.type
class Grade:
    id: int
    itemid: int
    userid: int
    rawgrade: Optional[int]
    finalgrade: Optional[int]
    timecreated: datetime
    timemodified: datetime

# Enrollment Types
@strawberry.type
class Enrollment:
    id: int
    enrolid: int
    userid: int
    courseid: int
    course: Course
    status: int
    timestart: Optional[datetime]
    timeend: Optional[datetime]
    timecreated: datetime
    timemodified: datetime

@strawberry.type
class CourseCompletion:
    id: int
    userid: int
    course: int
    timeenrolled: datetime
    timestarted: datetime
    timecompleted: Optional[datetime]

# Error types para manejo de errores
@strawberry.type
class ErrorResponse:
    message: str
    code: int

@strawberry.type
class UserResponse:
    user: Optional[User] = None
    error: Optional[ErrorResponse] = None

# Input Types for Mutations
@strawberry.input
class RoleInput:
    name: str
    shortname: str
    description: Optional[str] = None
    sortorder: int
    archetype: Optional[str] = None

@strawberry.input
class UserInput:
    username: str
    password: str
    firstname: str
    lastname: str
    email: str
    institution: Optional[str] = None
    department: Optional[str] = None

@strawberry.input
class CourseInput:
    category: int
    sortorder: int
    fullname: str
    shortname: str
    idnumber: Optional[str] = None
    summary: Optional[str] = None
    format: str = "topics"
    startdate: datetime
    enddate: Optional[datetime] = None
    visible: bool = True

@strawberry.input
class AssignmentInput:
    course: int
    section:int
    name: str
    intro: str
    duedate: Optional[datetime] = None
    allowsubmissionsfromdate: Optional[datetime] = None
    grade: Optional[int] = None

@strawberry.input
class EnrollmentInput:
    enrolid: int
    userid: int
    courseid: int
    status: int = 0
    timestart: Optional[datetime] = None
    timeend: Optional[datetime] = None
    
@strawberry.input
class SectionInput:
    course: int
    name: Optional[str]
    summary: Optional[str] = None
    sequence: Optional[str] = None
    visible: bool = True

# Query Type
@strawberry.type
class Query:
    # User Queries
    @strawberry.field
    async def users(self) -> List[User]:       
        users = await prisma_client.user.find_many()       
        return users

    @strawberry.field
    async def user(self, user_id: int) -> User:      
        user = await prisma_client.user.find_unique(where={"id": user_id})       
        if not user:
            logger.error(f"User not found: {user_id}")
            raise Exception("User not found")
        return user

    # Course Queries
    @strawberry.field
    async def courses(self) -> List[Course]:        
        courses = await prisma_client.course.find_many()       
        return courses

    @strawberry.field
    async def course(self, course_id: int) -> Course:        
        course = await prisma_client.course.find_unique(where={"id": course_id})
        
        if not course:
            logger.error(f"Course not found: {course_id}")
            raise Exception("Course not found")
        return course

    @strawberry.field
    async def course_sections(self, course_id: int) -> List[CourseSection]:        
        sections = await prisma_client.coursesection.find_many(where={"course": course_id})        
        return sections

    # Category Queries
    @strawberry.field
    async def categories(self) -> List[Category]:        
        categories = await prisma_client.category.find_many()       
        return categories

    @strawberry.field
    async def category(self, category_id: int) -> Category:       
        category = await prisma_client.category.find_unique(where={"id": category_id})
        
        if not category:
            logger.error(f"Category not found: {category_id}")
            raise Exception("Category not found")
        return category

    # Role Queries
    @strawberry.field
    async def roles(self) -> List[Role]:        
        roles = await prisma_client.role.find_many()
        
        if not roles:
            logger.error("Roles not found")
            raise Exception("Roles not found")
        return roles

    @strawberry.field
    async def role(self, role_id: int) -> Role:       
        role = await prisma_client.role.find_unique(where={"id": role_id})        
        if not role:
            logger.error(f"Role not found: {role_id}")
            raise Exception("Role not found")
        return role

    # Assignment Queries
    @strawberry.field
    async def assignments(self, course_id: Optional[int] = None, section_id: Optional[int] = None) -> List[Assignment]:       
        if course_id and section_id:
            assignments = await prisma_client.assignment.find_many(where={"course": course_id, "section": section_id})
        else:
            assignments = await prisma_client.assignment.find_many()      
        return assignments
    
    # Todas las asignaciones
    @strawberry.field
    async def AllAssigments(self) -> List[Assignment]:        
        assignments = await prisma_client.assignment.find_many()       
        return assignments
    
    # Asignaciones del curso
    @strawberry.field
    async def CourseAssignments(self, course_id: Optional[int] = None) -> List[Assignment]:       
        if course_id:
            assignments = await prisma_client.assignment.find_many(where={"course": course_id})
        else:
            assignments = await prisma_client.assignment.find_many()      
        return assignments

    @strawberry.field
    async def assignment(self, assignment_id: int) -> Assignment:       
        assignment = await prisma_client.assignment.find_unique(where={"id": assignment_id})      
        if not assignment:
            logger.error(f"Assignment not found: {assignment_id}")
            raise Exception("Assignment not found")
        return assignment

    # Submission Queries
    @strawberry.field
    async def submissions(self, assignment_id: int) -> List[Submission]:      
        submissions = await prisma_client.submission.find_many(where={"assignment": assignment_id})      
        return submissions

    @strawberry.field
    async def user_submissions(self, user_id: int) -> List[Submission]:      
        submissions = await prisma_client.submission.find_many(where={"userid": user_id})      
        return submissions

    # Forum Queries
    @strawberry.field
    async def forums(self, course_id: Optional[int] = None) -> List[Forum]:       
        if course_id:
            forums = await prisma_client.forum.find_many(where={"course": course_id})
        else:
            forums = await prisma_client.forum.find_many()       
        return forums

    @strawberry.field
    async def forum_discussions(self, forum_id: int) -> List[ForumDiscussion]:      
        discussions = await prisma_client.forumdiscussion.find_many(where={"forum": forum_id})       
        return discussions

    @strawberry.field
    async def forum_posts(self, discussion_id: int) -> List[ForumPost]:       
        posts = await prisma_client.forumpost.find_many(where={"discussion": discussion_id})       
        return posts

    # Grade Queries
    @strawberry.field
    async def course_grades(self, course_id: int) -> List[GradeItem]:      
        grade_items = await prisma_client.gradeitem.find_many(where={"courseid": course_id})       
        return grade_items

    @strawberry.field
    async def user_grades(self, user_id: int) -> List[Grade]:      
        grades = await prisma_client.grade.find_many(where={"userid": user_id})  
        return grades

    # Enrollment Queries
    @strawberry.field
    async def course_enrollments(self, course_id: int) -> List[Enrollment]:
        enrollments = await prisma_client.enrollment.find_many(where={"courseid": course_id})
        return enrollments

    @strawberry.field
    async def user_enrollments(self, user_id: int) -> List[Enrollment]:
        enrollments = await prisma_client.enrollment.find_many(where={"userid": user_id}, include={"course": True})   
        return enrollments

    @strawberry.field
    async def course_completions(self, course_id: int) -> List[CourseCompletion]:
        completions = await prisma_client.coursecompletion.find_many(where={"course": course_id})
        return completions

    @strawberry.field
    async def user_completions(self, user_id: int) -> List[CourseCompletion]:
        completions = await prisma_client.coursecompletion.find_many(where={"userid": user_id})
        return completions
    
    @strawberry.field
    async def sections(self, course_id: int) -> List[Section]:
        sections = await prisma_client.coursesection.find_many(where={"course": course_id})
        return sections

# Mutation Type
@strawberry.type
class Mutation:
    # Role Mutations
    @strawberry.mutation
    async def create_role(self, input: RoleInput) -> Role:
        
        new_role = await prisma_client.role.create(
            data={
                "name": input.name,
                "shortname": input.shortname,
                "description": input.description,
                "sortorder": input.sortorder,
                "archetype": input.archetype
            }
        )
        
        return new_role

    @strawberry.mutation
    async def update_role(
        self,
        role_id: int,
        input: RoleInput
    ) -> Role:
        
        updated_role = await prisma_client.role.update(
            where={"id": role_id},
            data={
                "name": input.name,
                "shortname": input.shortname,
                "description": input.description,
                "sortorder": input.sortorder,
                "archetype": input.archetype
            }
        )
        
        if not updated_role:
            logger.error(f"Role not found: {role_id}")
            raise Exception("Role not found")
        return updated_role

    @strawberry.mutation
    async def delete_role(self, role_id: int) -> Role:
        
        deleted_role = await prisma_client.role.delete(where={"id": role_id})
        
        if not deleted_role:
            logger.error(f"Role not found: {role_id}")
            raise Exception("Role not found")
        return deleted_role

    # User Mutations
    @strawberry.mutation
    async def create_user(self, input: UserInput) -> User:
        
        now = datetime.utcnow()
        # Ensure password is hashed before storing
        hashed_password = bcrypt.hashpw(input.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        
        new_user = await prisma_client.user.create(
            data={
                "username": input.username,
                "password": hashed_password,
                "firstname": input.firstname,
                "lastname": input.lastname,
                "email": input.email,
                "institution": input.institution,
                "department": input.department,
                "timecreated": now,
                "timemodified": now,
                "confirmed": True,
                "deleted": False,
                "suspended": False
            }
        )
        
        return new_user

    @strawberry.mutation
    async def update_user(
        self,
        user_id: int,
        input: UserInput
    ) -> User:
        # Ensure password is hashed before storing
        hashed_password = bcrypt.hashpw(input.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        
        updated_user = await prisma_client.user.update(
            where={"id": user_id},
            data={
                "username": input.username,
                "password": hashed_password,
                "firstname": input.firstname,
                "lastname": input.lastname,
                "email": input.email,
                "institution": input.institution,
                "department": input.department,
                "timemodified": datetime.utcnow(),
            }
        )
        
        if not updated_user:
            logger.error(f"User not found: {user_id}")
            raise Exception("User not found")
        return updated_user

    # Course Mutations
    @strawberry.mutation
    async def create_course(self, input: CourseInput) -> Course:
        
        now = datetime.utcnow()
        new_course = await prisma_client.course.create(
            data={
                "category": input.category,
                "sortorder": input.sortorder,
                "fullname": input.fullname,
                "shortname": input.shortname,
                "idnumber": input.idnumber,
                "summary": input.summary,
                "format": input.format,
                "startdate": input.startdate,
                "enddate": input.enddate,
                "visible": input.visible,
                "timecreated": now,
                "timemodified": now,
            }
        )
        
        return new_course

    @strawberry.mutation
    async def update_course(
        self,
        course_id: int,
        input: CourseInput
    ) -> Course:
        
        updated_course = await prisma_client.course.update(
            where={"id": course_id},
            data={
                "category": input.category,
                "sortorder": input.sortorder,
                "fullname": input.fullname,
                "shortname": input.shortname,
                "idnumber": input.idnumber,
                "summary": input.summary,
                "format": input.format,
                "startdate": input.startdate,
                "enddate": input.enddate,
                "visible": input.visible,
                "timemodified": datetime.utcnow(),
            }
        )
        
        if not updated_course:
            logger.error(f"Course not found: {course_id}")
            raise Exception("Course not found")
        return updated_course

    # Assignment Mutations
    @strawberry.mutation
    async def create_assignment(self, input: AssignmentInput) -> Assignment:
        
        now = datetime.utcnow()
        new_assignment = await prisma_client.assignment.create(
            data={
                "course": input.course,
                "name": input.name,
                "intro": input.intro,
                "section": input.section,
                "duedate": input.duedate,
                "allowsubmissionsfromdate": input.allowsubmissionsfromdate,
                "grade": input.grade,
                "timemodified": now,
                "introformat": 1,  # Default format
            }
        )
        
        return new_assignment

    @strawberry.mutation
    async def update_assignment(
        self,
        assignment_id: int,
        input: AssignmentInput
    ) -> Assignment:
        
        updated_assignment = await prisma_client.assignment.update(
            where={"id": assignment_id},
            data={
                "section": input.section,
                "name": input.name,
                "intro": input.intro,
                "duedate": input.duedate,
                "allowsubmissionsfromdate": input.allowsubmissionsfromdate,
                "grade": input.grade,
                "timemodified": datetime.utcnow(),
            }
        )
        
        if not updated_assignment:
            logger.error(f"Assignment not found: {assignment_id}")
            raise Exception("Assignment not found")
        return updated_assignment

    # Enrollment Mutations
    @strawberry.mutation
    async def create_enrollment(self, input: EnrollmentInput) -> Enrollment:
        
        now = datetime.utcnow()
        new_enrollment = await prisma_client.enrollment.create(
            data={
                "enrolid": input.enrolid,
                "userid": input.userid,
                "courseid": input.courseid,
                "status": input.status,
                "timestart": input.timestart,
                "timeend": input.timeend,
                "timecreated": now,
                "timemodified": now,
            }
        )
        
        return new_enrollment

    @strawberry.mutation
    async def update_enrollment(
        self,
        enrollment_id: int,
        input: EnrollmentInput
    ) -> Enrollment:
        
        updated_enrollment = await prisma_client.enrollment.update(
            where={"id": enrollment_id},
            data={
                "enrolid": input.enrolid,
                "status": input.status,
                "timestart": input.timestart,
                "timeend": input.timeend,
                "timemodified": datetime.utcnow(),
            }
        )
        
        if not updated_enrollment:
            logger.error(f"Enrollment not found: {enrollment_id}")
            raise Exception("Enrollment not found")
        return updated_enrollment

    @strawberry.mutation
    async def delete_enrollment(self, enrollment_id: int) -> Enrollment:
        
        deleted_enrollment = await prisma_client.enrollment.delete(where={"id": enrollment_id})
        
        if not deleted_enrollment:
            logger.error(f"Enrollment not found: {enrollment_id}")
            raise Exception("Enrollment not found")
        return deleted_enrollment
    
    # Login mutation con manejo de errores usando tipos de respuesta personalizados
    @strawberry.mutation
    async def login(self, email: str, password: str) -> UserResponse:
        try:
            user = await prisma_client.user.find_unique(where={"email": email})
            
            # Verificar si el usuario existe
            if not user:
                logger.error(f"Login failed: Usuario no encontrado - {email}")
                return UserResponse(
                    error=ErrorResponse(
                        message="Usuario no encontrado",
                        code=404
                    )
                )

            # Verificar la contraseña utilizando bcrypt
            if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                logger.error(f"Login failed: Credenciales incorrectas - {email}")
                return UserResponse(
                    error=ErrorResponse(
                        message="Credenciales incorrectas",
                        code=401
                    )
                )

            # Login exitoso - registrar
            logger.info(f"Login successful: {email}")
            
            # Retornar los datos del usuario exitosamente
            return UserResponse(
                user=User(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    firstname=user.firstname,
                    lastname=user.lastname,
                    confirmed=user.confirmed,
                    deleted=user.deleted,
                    suspended=user.suspended,
                    institution=user.institution,
                    department=user.department,
                    timecreated=user.timecreated,
                    timemodified=user.timemodified
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
    async def change_password(self, email: str, new_password: str) -> UserResponse:
        try:
            user = await prisma_client.user.find_unique(where={"email": email})

            if not user:
                logger.error(f"Change password failed: Usuario no encontrado - {email}")
                return UserResponse(
                    error=ErrorResponse(
                        message="Usuario no encontrado",
                        code=404
                    )
                )

            hashed_new_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            updated_user = await prisma_client.user.update(
                where={"email": email},
                data={"password": hashed_new_password, "timemodified": datetime.utcnow()}
            )
            
            logger.info(f"Password changed successfully for user: {email}")
            return UserResponse(user=updated_user)
        except Exception as e:
            logger.error(f"Change password error: {str(e)}")
            return UserResponse(
                error=ErrorResponse(
                    message=f"Error interno: {str(e)}",
                    code=500
                )
            )
     
    # Section Mutations
    @strawberry.mutation
    async def create_section(self, input: SectionInput) -> Section:
        now = datetime.utcnow()
        
        # Obtener el número de secciones actuales del curso
        section_count = await prisma_client.coursesection.count(where={"course": input.course})
        
        # Asignar el número de sección automáticamente
        new_section_number = section_count + 1
        
        new_section = await prisma_client.coursesection.create(
            data={
                "course": input.course,
                "section": new_section_number,
                "name": input.name,
                "summary": input.summary,
                "sequence": input.sequence,
                "visible": input.visible,
                "timemodified": now,
            }
        )
        return new_section

    @strawberry.mutation
    async def update_section(self, section_id: int, input: SectionInput) -> Section:
        updated_section = await prisma_client.coursesection.update(
            where={"id": section_id},
            data={
                "name": input.name,
                "summary": input.summary,
                "sequence": input.sequence,
                "visible": input.visible,
                "timemodified": datetime.utcnow(),
            }
        )
        if not updated_section:
            logger.error(f"Section not found: {section_id}")
            raise Exception("Section not found")
        return updated_section

    @strawberry.mutation
    async def delete_section(self, section_id: int) -> Section:
        deleted_section = await prisma_client.coursesection.delete(where={"id": section_id})
        if not deleted_section:
            logger.error(f"Section not found: {section_id}")
            raise Exception("Section not found")
        return deleted_section


# Create schema without extensions (usando un enfoque más sencillo)
schema = strawberry.Schema(query=Query, mutation=Mutation)
