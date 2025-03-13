from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime
import bcrypt
from db import prisma_client as prisma

from models.base import (
    UserBase, UserResponse,
    CourseBase, CourseResponse,
    CategoryBase, CategoryResponse,
    AssignmentBase, AssignmentResponse,
    SubmissionBase, SubmissionResponse,
    ForumBase, ForumResponse,
    ForumDiscussionBase, ForumDiscussionResponse,
    ForumPostBase, ForumPostResponse,
    EnrollmentBase, EnrollmentResponse,
    GradeItemBase, GradeItemResponse,
    GradeBase, GradeResponse,
    CourseCompletionBase, CourseCompletionResponse,
    ResourceBase, ResourceResponse,
    RoleBase, RoleResponse, SectionBase, SectionResponse
)

# Router para REST API básica
router = APIRouter(
    prefix="/api",
    tags=["rest_api"],
    responses={404: {"description": "Not found"}}
)

# ----- OPERACIONES CRUD PARA ROLES ----- #

@router.post("/roles", response_model=RoleResponse)
async def create_role(role: RoleBase):
    try:
        new_role = await prisma.role.create(
            data={
                "name": role.name,
                "shortname": role.shortname,
                "description": role.description,
                "sortorder": role.sortorder,
                "archetype": role.archetype
            }
        )
        return new_role
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating role: {str(e)}"
        )

@router.get("/roles", response_model=List[RoleResponse])
async def get_roles():
    roles = await prisma.role.find_many()
    return roles

@router.get("/roles/{role_id}", response_model=RoleResponse)
async def get_role(role_id: int):
    role = await prisma.role.find_unique(where={"id": role_id})
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    return role

@router.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role(role_id: int, role: RoleBase):
    try:
        updated_role = await prisma.role.update(
            where={"id": role_id},
            data={
                "name": role.name,
                "shortname": role.shortname,
                "description": role.description,
                "sortorder": role.sortorder,
                "archetype": role.archetype
            }
        )
        return updated_role
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating role: {str(e)}"
        )

@router.delete("/roles/{role_id}", response_model=RoleResponse)
async def delete_role(role_id: int):
    try:
        deleted_role = await prisma.role.delete(where={"id": role_id})
        return deleted_role
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting role: {str(e)}"
        )

# ----- OPERACIONES CRUD PARA USUARIOS ----- #

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserBase):
    try:
        # Verificar si el nombre de usuario o email ya existen
        existing_user = await prisma.user.find_first(
            where={
                "OR": [
                    {"username": user.username},
                    {"email": user.email}
                ]
            }
        )
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists"
            )
        
         # Encriptar la contraseña
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        # Crear el nuevo usuario
        now = datetime.utcnow()
        new_user = await prisma.user.create(
            data={
                "username": user.username,
                "password": hashed_password,  # En producción, esto debería estar hasheado
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "institution": user.institution,
                "department": user.department,
                "auth": "manual",
                "confirmed": False,
                "lang": "es",
                "timezone": "99",
                "deleted": False,
                "suspended": False,
                "mnethostid": 1,
                "timecreated": now,
                "timemodified": now
            }
        )
        
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user: {str(e)}"
        )

@router.get("/users", response_model=List[UserResponse])
async def get_users(search: Optional[str] = None):
    # Buscar usuarios
    if search:
        users = await prisma.user.find_many(
            where={
                "OR": [
                    {"username": {"contains": search}},
                    {"firstname": {"contains": search}},
                    {"lastname": {"contains": search}},
                    {"email": {"contains": search}}
                ]
            }
        )
    else:
        users = await prisma.user.find_many()
    
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = await prisma.user.find_unique(where={"id": user_id})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserBase):
    try:
        # Verificar si el usuario existe
        existing_user = await prisma.user.find_unique(where={"id": user_id})
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Actualizar usuario
        updated_user = await prisma.user.update(
            where={"id": user_id},
            data={
                "username": user.username,
                "password": user.password,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "institution": user.institution,
                "department": user.department,
                "timemodified": datetime.utcnow()
            }
        )
        
        return updated_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating user: {str(e)}"
        )

@router.delete("/users/{user_id}", response_model=UserResponse)
async def delete_user(user_id: int):
    try:
        # En lugar de eliminar físicamente, marcamos como eliminado
        deleted_user = await prisma.user.update(
            where={"id": user_id},
            data={
                "deleted": True,
                "timemodified": datetime.utcnow()
            }
        )
        
        return deleted_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting user: {str(e)}"
        )

# ----- OPERACIONES CRUD PARA CURSOS ----- #

@router.post("/courses", response_model=CourseResponse)
async def create_course(course: CourseBase):
    try:
        # Verificar si la categoría existe
        category = await prisma.category.find_unique(where={"id": course.category})
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category does not exist"
            )
        
        # Crear el curso
        now = datetime.utcnow()
        new_course = await prisma.course.create(
            data={
                "category": course.category,
                "sortorder": course.sortorder,
                "fullname": course.fullname,
                "shortname": course.shortname,
                "idnumber": course.idnumber,
                "summary": course.summary,
                "format": course.format,
                "showgrades": True,
                "newsitems": 5,
                "startdate": course.startdate,
                "enddate": course.enddate,
                "visible": course.visible,
                "groupmode": 0,
                "timecreated": now,
                "timemodified": now
            }
        )
        
        # Crear la relación con la categoría
        await prisma.categorycourse.create(
            data={
                "categoryId": course.category,
                "courseId": new_course.id
            }
        )
        
        # Crear sección inicial del curso
        await prisma.coursesection.create(
            data={
                "course": new_course.id,
                "section": 0,
                "name": "General",
                "summary": "Sección general",
                "visible": True,
                "timemodified": now
            }
        )
        
        return new_course
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating course: {str(e)}"
        )

@router.get("/courses", response_model=List[CourseResponse])
async def get_courses(
    category: Optional[int] = None,
    visible_only: bool = True
):
    # Construir condiciones de búsqueda
    where_conditions = {}
    if category:
        where_conditions["category"] = category
    if visible_only:
        where_conditions["visible"] = True
    
    courses = await prisma.course.find_many(where=where_conditions)
    
    return courses

@router.get("/courses/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int):
    course = await prisma.course.find_unique(where={"id": course_id})
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    return course

@router.put("/courses/{course_id}", response_model=CourseResponse)
async def update_course(course_id: int, course: CourseBase):
    try:
        # Verificar si el curso existe
        existing_course = await prisma.course.find_unique(where={"id": course_id})
        if not existing_course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Actualizar curso
        updated_course = await prisma.course.update(
            where={"id": course_id},
            data={
                "category": course.category,
                "sortorder": course.sortorder,
                "fullname": course.fullname,
                "shortname": course.shortname,
                "idnumber": course.idnumber,
                "summary": course.summary,
                "format": course.format,
                "startdate": course.startdate,
                "enddate": course.enddate,
                "visible": course.visible,
                "timemodified": datetime.utcnow()
            }
        )
        
        return updated_course
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating course: {str(e)}"
        )

@router.delete("/courses/{course_id}", response_model=CourseResponse)
async def delete_course(course_id: int):
    try:
        # En lugar de eliminar, hacer que el curso no sea visible
        deleted_course = await prisma.course.update(
            where={"id": course_id},
            data={
                "visible": False,
                "timemodified": datetime.utcnow()
            }
        )
        
        return deleted_course
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting course: {str(e)}"
        )

# ----- OPERACIONES CRUD PARA CATEGORÍAS ----- #

@router.post("/categories", response_model=CategoryResponse)
async def create_category(category: CategoryBase):
    try:
        now = datetime.utcnow()
        new_category = await prisma.category.create(
            data={
                "name": category.name,
                "idnumber": category.idnumber,
                "description": category.description,
                "parent": category.parent,
                "sortorder": category.sortorder,
                "coursecount": 0,
                "visible": category.visible,
                "visibleold": category.visible,
                "timemodified": now,
                "depth": category.depth,
                "path": category.path
            }
        )
        
        return new_category
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating category: {str(e)}"
        )

@router.get("/categories", response_model=List[CategoryResponse])
async def get_categories(parent: Optional[int] = None):
    if parent is not None:
        categories = await prisma.category.find_many(where={"parent": parent})
    else:
        categories = await prisma.category.find_many()
    
    return categories

@router.get("/categories/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int):
    category = await prisma.category.find_unique(where={"id": category_id})
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return category

@router.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, category: CategoryBase):
    try:
        updated_category = await prisma.category.update(
            where={"id": category_id},
            data={
                "name": category.name,
                "idnumber": category.idnumber,
                "description": category.description,
                "parent": category.parent,
                "sortorder": category.sortorder,
                "visible": category.visible,
                "visibleold": category.visible,
                "timemodified": datetime.utcnow(),
                "depth": category.depth,
                "path": category.path
            }
        )
        
        return updated_category
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating category: {str(e)}"
        )

@router.delete("/categories/{category_id}", response_model=CategoryResponse)
async def delete_category(category_id: int):
    try:
        # Verificar si hay cursos asociados
        category_courses = await prisma.categorycourse.find_many(
            where={"categoryId": category_id}
        )
        
        if category_courses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete category with associated courses"
            )
        
        deleted_category = await prisma.category.delete(
            where={"id": category_id}
        )
        
        return deleted_category
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting category: {str(e)}"
        )

# ----- OPERACIONES CRUD PARA ASSIGNACIONES ----- #

@router.post("/courses/{course_id}/assignments", response_model=AssignmentResponse)
async def create_assignment(
    course_id: int,
    assignment: AssignmentBase
):
    if assignment.course != course_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course ID in path does not match course ID in assignment data"
        )
    
    try:
        # Verificar si el curso existe
        course = await prisma.course.find_unique(where={"id": course_id})
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Crear la tarea
        now = datetime.utcnow()
        new_assignment = await prisma.assignment.create(
            data={
                "course": course_id,
                "name": assignment.name,
                "intro": assignment.intro,
                "introformat": assignment.introformat,
                "section": assignment.section,
                "duedate": assignment.duedate,
                "allowsubmissionsfromdate": assignment.allowsubmissionsfromdate,
                "grade": assignment.grade,
                "timemodified": now,
                "alwaysshowdescription": True,
                "nosubmissions": False,
                "submissiondrafts": False,
                "sendnotifications": False,
                "sendlatenotifications": False,
                "requiresubmissionstatement": False,
                "completionsubmit": False,
                "teamsubmission": False,
                "requireallteammemberssubmit": False,
                "teamsubmissiongroupingid": 0,
                "blindmarking": False,
                "revealidentities": False,
                "attemptreopenmethod": "none",
                "maxattempts": -1,
                "markingworkflow": False,
                "markingallocation": False
            }
        )
        
        # Crear un ítem de calificación para la tarea
        if assignment.grade:
            await prisma.gradeitem.create(
                data={
                    "courseid": course_id,
                    "itemname": assignment.name,
                    "itemtype": "mod",
                    "itemmodule": "assign",
                    "iteminstance": new_assignment.id,
                    "grademax": assignment.grade,
                    "grademin": 0,
                    "timecreated": now,
                    "timemodified": now
                }
            )
        
        return new_assignment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating assignment: {str(e)}"
        )

@router.get("/courses/{course_id}/assignments", response_model=List[AssignmentResponse])
async def get_course_assignments(course_id: int):
    # Verificar si el curso existe
    course = await prisma.course.find_unique(where={"id": course_id})
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Obtener las tareas del curso
    assignments = await prisma.assignment.find_many(where={"course": course_id})
    
    return assignments

@router.get("/assignments/{assignment_id}", response_model=AssignmentResponse)
async def get_assignment(assignment_id: int):
    assignment = await prisma.assignment.find_unique(where={"id": assignment_id})
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    return assignment

@router.put("/assignments/{assignment_id}", response_model=AssignmentResponse)
async def update_assignment(assignment_id: int, assignment: AssignmentBase):
    try:
        updated_assignment = await prisma.assignment.update(
            where={"id": assignment_id},
            data={
                "section": assignment.section,
                "name": assignment.name,
                "intro": assignment.intro,
                "introformat": assignment.introformat,
                "duedate": assignment.duedate,
                "allowsubmissionsfromdate": assignment.allowsubmissionsfromdate,
                "grade": assignment.grade,
                "timemodified": datetime.utcnow()
            }
        )
        
        # Actualizar el ítem de calificación si existe
        if assignment.grade:
            grade_item = await prisma.gradeitem.find_first(
                where={
                    "itemmodule": "assign",
                    "iteminstance": assignment_id
                }
            )
            
            if grade_item:
                await prisma.gradeitem.update(
                    where={"id": grade_item.id},
                    data={
                        "itemname": assignment.name,
                        "grademax": assignment.grade,
                        "timemodified": datetime.utcnow()
                    }
                )
        
        return updated_assignment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating assignment: {str(e)}"
        )

@router.delete("/assignments/{assignment_id}", response_model=AssignmentResponse)
async def delete_assignment(assignment_id: int):
    try:
        # Eliminar las entregas asociadas
        await prisma.submission.delete_many(
            where={"assignment": assignment_id}
        )
        
        # Eliminar el ítem de calificación si existe
        grade_item = await prisma.gradeitem.find_first(
            where={
                "itemmodule": "assign",
                "iteminstance": assignment_id
            }
        )
        
        if grade_item:
            await prisma.gradeitem.delete(
                where={"id": grade_item.id}
            )
        
        # Eliminar la tarea
        deleted_assignment = await prisma.assignment.delete(
            where={"id": assignment_id}
        )
        
        return deleted_assignment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting assignment: {str(e)}"
        )

# ----- OPERACIONES CRUD PARA ENTREGAS (SUBMISSIONS) ----- #

@router.post("/assignments/{assignment_id}/submissions", response_model=SubmissionResponse)
async def create_submission(assignment_id: int, submission: SubmissionBase):
    if submission.assignment != assignment_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assignment ID in path does not match assignment ID in submission data"
        )
    
    try:
        # Verificar si la tarea existe
        assignment = await prisma.assignment.find_unique(where={"id": assignment_id})
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        # Verificar si el usuario existe
        user = await prisma.user.find_unique(where={"id": submission.userid})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Marcar la última entrega como no actual
        await prisma.submission.update_many(
            where={
                "assignment": assignment_id,
                "userid": submission.userid
            },
            data={"latest": False}
        )
        
        # Crear la nueva entrega
        now = datetime.utcnow()
        new_submission = await prisma.submission.create(
            data={
                "assignment": assignment_id,
                "userid": submission.userid,
                "status": submission.status,
                "groupid": submission.groupid,
                "attemptnumber": submission.attemptnumber,
                "latest": True,
                "timecreated": now,
                "timemodified": now
            }
        )
        
        return new_submission
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating submission: {str(e)}"
        )

@router.get("/assignments/{assignment_id}/submissions", response_model=List[SubmissionResponse])
async def get_assignment_submissions(assignment_id: int):
    # Verificar si la tarea existe
    assignment = await prisma.assignment.find_unique(where={"id": assignment_id})
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    # Obtener las entregas
    submissions = await prisma.submission.find_many(
        where={"assignment": assignment_id}
    )
    
    return submissions

@router.get("/users/{user_id}/submissions", response_model=List[SubmissionResponse])
async def get_user_submissions(user_id: int):
    # Verificar si el usuario existe
    user = await prisma.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Obtener las entregas
    submissions = await prisma.submission.find_many(
        where={"userid": user_id}
    )
    
    return submissions

@router.put("/submissions/{submission_id}", response_model=SubmissionResponse)
async def update_submission(submission_id: int, submission: SubmissionBase):
    try:
        # Verificar si la entrega existe
        existing_submission = await prisma.submission.find_unique(
            where={"id": submission_id}
        )
        
        if not existing_submission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Submission not found"
            )
        
        # Actualizar la entrega
        updated_submission = await prisma.submission.update(
            where={"id": submission_id},
            data={
                "status": submission.status,
                "timemodified": datetime.utcnow()
            }
        )
        
        return updated_submission
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating submission: {str(e)}"
        )

@router.delete("/submissions/{submission_id}", response_model=SubmissionResponse)
async def delete_submission(submission_id: int):
    try:
        deleted_submission = await prisma.submission.delete(
            where={"id": submission_id}
        )
        
        return deleted_submission
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting submission: {str(e)}"
        )

# ----- OPERACIONES CRUD PARA MATRÍCULAS (ENROLLMENTS) ----- #

@router.post("/enrollments", response_model=EnrollmentResponse)
async def create_enrollment(enrollment: EnrollmentBase):
    try:
        # Verificar si el curso existe
        course = await prisma.course.find_unique(where={"id": enrollment.courseid})
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Verificar si el usuario existe
        user = await prisma.user.find_unique(where={"id": enrollment.userid})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verificar si ya existe una matrícula
        existing_enrollment = await prisma.enrollment.find_first(
            where={
                "userid": enrollment.userid,
                "courseid": enrollment.courseid
            }
        )
        
        if existing_enrollment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already enrolled in this course"
            )
        
        # Crear la matrícula
        now = datetime.utcnow()
        new_enrollment = await prisma.enrollment.create(
            data={
                "enrolid": enrollment.enrolid,
                "userid": enrollment.userid,
                "courseid": enrollment.courseid,
                "status": enrollment.status,
                "timestart": enrollment.timestart,
                "timeend": enrollment.timeend,
                "timecreated": now,
                "timemodified": now
            }
        )
        
        # Crear registro de inicio de compleción del curso
        await prisma.coursecompletion.create(
            data={
                "userid": enrollment.userid,
                "course": enrollment.courseid,
                "timeenrolled": now,
                "timestarted": now
            }
        )
        
        return new_enrollment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating enrollment: {str(e)}"
        )

@router.get("/courses/{course_id}/enrollments", response_model=List[EnrollmentResponse])
async def get_course_enrollments(course_id: int):
    # Verificar si el curso existe
    course = await prisma.course.find_unique(where={"id": course_id})
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Obtener las matrículas del curso
    enrollments = await prisma.enrollment.find_many(where={"courseid": course_id})
    
    return enrollments

@router.get("/users/{user_id}/enrollments", response_model=List[EnrollmentResponse])
async def get_user_enrollments(user_id: int):
    # Verificar si el usuario existe
    user = await prisma.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Obtener las matrículas del usuario
    enrollments = await prisma.enrollment.find_many(where={"userid": user_id})
    
    return enrollments

@router.put("/enrollments/{enrollment_id}", response_model=EnrollmentResponse)
async def update_enrollment(enrollment_id: int, enrollment: EnrollmentBase):
    try:
        # Verificar si la matrícula existe
        existing_enrollment = await prisma.enrollment.find_unique(
            where={"id": enrollment_id}
        )
        
        if not existing_enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found"
            )
        
        # Actualizar la matrícula
        updated_enrollment = await prisma.enrollment.update(
            where={"id": enrollment_id},
            data={
                "status": enrollment.status,
                "timestart": enrollment.timestart,
                "timeend": enrollment.timeend,
                "timemodified": datetime.utcnow()
            }
        )
        
        return updated_enrollment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating enrollment: {str(e)}"
        )

@router.delete("/enrollments/{enrollment_id}", response_model=EnrollmentResponse)
async def delete_enrollment(enrollment_id: int):
    try:
        # Obtener información de la matrícula
        enrollment = await prisma.enrollment.find_unique(
            where={"id": enrollment_id}
        )
        
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found"
            )
        
        # Eliminar registro de compleción del curso
        await prisma.coursecompletion.delete_many(
            where={
                "userid": enrollment.userid,
                "course": enrollment.courseid
            }
        )
        
        # Eliminar la matrícula
        deleted_enrollment = await prisma.enrollment.delete(
            where={"id": enrollment_id}
        )
        
        return deleted_enrollment
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting enrollment: {str(e)}"
        )

# ----- OPERACIONES CRUD PARA FOROS ----- #

@router.post("/courses/{course_id}/forums", response_model=ForumResponse)
async def create_forum(
    course_id: int,
    forum: ForumBase
):
    if forum.course != course_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course ID in path does not match course ID in forum data"
        )
    
    try:
        # Verificar si el curso existe
        course = await prisma.course.find_unique(where={"id": course_id})
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Crear el foro
        now = datetime.utcnow()
        new_forum = await prisma.forum.create(
            data={
                "course": course_id,
                "type": forum.type,
                "name": forum.name,
                "intro": forum.intro,
                "introformat": forum.introformat,
                "timemodified": now,
                "assessed": 0,
                "scale": 0,
                "maxbytes": 0,
                "maxattachments": 1,
                "forcesubscribe": 0,
                "trackingtype": 1,
                "rsstype": 0,
                "rssarticles": 0,
                "warnafter": 0,
                "blockafter": 0,
                "blockperiod": 0,
                "completiondiscussions": 0,
                "completionreplies": 0,
                "completionposts": 0,
                "displaywordcount": False
            }
        )
        
        return new_forum
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating forum: {str(e)}"
        )

@router.get("/courses/{course_id}/forums", response_model=List[ForumResponse])
async def get_course_forums(course_id: int):
    # Verificar si el curso existe
    course = await prisma.course.find_unique(where={"id": course_id})
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Obtener los foros
    forums = await prisma.forum.find_many(where={"course": course_id})
    
    return forums

@router.get("/forums/{forum_id}", response_model=ForumResponse)
async def get_forum(forum_id: int):
    forum = await prisma.forum.find_unique(where={"id": forum_id})
    
    if not forum:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Forum not found"
        )
    
    return forum

@router.put("/forums/{forum_id}", response_model=ForumResponse)
async def update_forum(forum_id: int, forum: ForumBase):
    try:
        updated_forum = await prisma.forum.update(
            where={"id": forum_id},
            data={
                "name": forum.name,
                "type": forum.type,
                "intro": forum.intro,
                "introformat": forum.introformat,
                "timemodified": datetime.utcnow()
            }
        )
        
        return updated_forum
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating forum: {str(e)}"
        )

@router.delete("/forums/{forum_id}", response_model=ForumResponse)
async def delete_forum(forum_id: int):
    try:
        # Eliminar discusiones y mensajes asociados
        discussions = await prisma.forumdiscussion.find_many(
            where={"forum": forum_id}
        )
        
        for discussion in discussions:
            # Eliminar mensajes
            await prisma.forumpost.delete_many(
                where={"discussion": discussion.id}
            )
            
            # Eliminar discusión
            await prisma.forumdiscussion.delete(
                where={"id": discussion.id}
            )
        
        # Eliminar el foro
        deleted_forum = await prisma.forum.delete(
            where={"id": forum_id}
        )
        
        return deleted_forum
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting forum: {str(e)}"
        )

# ----- OPERACIONES CRUD PARA DISCUSIONES DEL FORO ----- #

@router.post("/forums/{forum_id}/discussions", response_model=ForumDiscussionResponse)
async def create_forum_discussion(
    forum_id: int,
    discussion: ForumDiscussionBase
):
    if discussion.forum != forum_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Forum ID in path does not match forum ID in discussion data"
        )
    
    try:
        # Verificar si el foro existe
        forum = await prisma.forum.find_unique(where={"id": forum_id})
        if not forum:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Forum not found"
            )
        
        # Verificar si el usuario existe
        user = await prisma.user.find_unique(where={"id": discussion.userid})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Crear el primer mensaje para la discusión
        now = datetime.utcnow()
        first_post = await prisma.forumpost.create(
            data={
                "discussion": 0,  # Temporal, se actualizará después
                "parent": 0,
                "userid": discussion.userid,
                "created": now,
                "modified": now,
                "subject": discussion.name,
                "message": "Mensaje inicial de la discusión",
                "messageformat": 1,
                "mailed": 0,
                "totalscore": 0,
                "mailnow": 0
            }
        )
        
        # Crear la discusión
        new_discussion = await prisma.forumdiscussion.create(
            data={
                "course": forum.course,
                "forum": forum_id,
                "name": discussion.name,
                "firstpost": first_post.id,
                "userid": discussion.userid,
                "groupid": -1,
                "assessed": True,
                "timemodified": now,
                "usermodified": discussion.userid,
                "pinned": False
            }
        )
        
        # Actualizar el primer mensaje con el ID de la discusión
        await prisma.forumpost.update(
            where={"id": first_post.id},
            data={"discussion": new_discussion.id}
        )
        
        return new_discussion
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating discussion: {str(e)}"
        )

@router.get("/forums/{forum_id}/discussions", response_model=List[ForumDiscussionResponse])
async def get_forum_discussions(forum_id: int):
    # Verificar si el foro existe
    forum = await prisma.forum.find_unique(where={"id": forum_id})
    if not forum:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Forum not found"
        )
    
    # Obtener las discusiones
    discussions = await prisma.forumdiscussion.find_many(
        where={"forum": forum_id}
    )
    
    return discussions

@router.get("/discussions/{discussion_id}", response_model=ForumDiscussionResponse)
async def get_discussion(discussion_id: int):
    discussion = await prisma.forumdiscussion.find_unique(
        where={"id": discussion_id}
    )
    
    if not discussion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discussion not found"
        )
    
    return discussion

@router.put("/discussions/{discussion_id}", response_model=ForumDiscussionResponse)
async def update_discussion(discussion_id: int, discussion: ForumDiscussionBase):
    try:
        updated_discussion = await prisma.forumdiscussion.update(
            where={"id": discussion_id},
            data={
                "name": discussion.name,
                "timemodified": datetime.utcnow(),
                "usermodified": discussion.userid
            }
        )
        
        return updated_discussion
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating discussion: {str(e)}"
        )

@router.delete("/discussions/{discussion_id}", response_model=ForumDiscussionResponse)
async def delete_discussion(discussion_id: int):
    try:
        # Eliminar mensajes asociados
        await prisma.forumpost.delete_many(
            where={"discussion": discussion_id}
        )
        
        # Eliminar la discusión
        deleted_discussion = await prisma.forumdiscussion.delete(
            where={"id": discussion_id}
        )
        
        return deleted_discussion
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting discussion: {str(e)}"
        )

# ----- OPERACIONES CRUD PARA RECURSOS ----- #

@router.post("/courses/{course_id}/resources", response_model=ResourceResponse)
async def create_resource(course_id: int, resource: ResourceBase):
    if resource.course != course_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course ID in path does not match course ID in resource data"
        )
    
    try:
        # Verificar si el curso existe
        course = await prisma.course.find_unique(where={"id": course_id})
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Crear el recurso
        now = datetime.utcnow()
        new_resource = await prisma.resource.create(
            data={
                "course": course_id,
                "name": resource.name,
                "intro": resource.intro,
                "introformat": resource.introformat,
                "tobemigrated": 0,
                "legacyfiles": 0,
                "display": 0,
                "filterfiles": 0,
                "revision": 1,
                "timemodified": now
            }
        )
        
        return new_resource
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating resource: {str(e)}"
        )

@router.get("/courses/{course_id}/resources", response_model=List[ResourceResponse])
async def get_course_resources(course_id: int):
    # Verificar si el curso existe
    course = await prisma.course.find_unique(where={"id": course_id})
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Obtener los recursos
    resources = await prisma.resource.find_many(
        where={"course": course_id}
    )
    
    return resources

@router.get("/resources/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id: int):
    resource = await prisma.resource.find_unique(
        where={"id": resource_id}
    )
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    
    return resource

@router.put("/resources/{resource_id}", response_model=ResourceResponse)
async def update_resource(resource_id: int, resource: ResourceBase):
    try:
        # Incrementar la revisión
        existing_resource = await prisma.resource.find_unique(
            where={"id": resource_id}
        )
        
        if not existing_resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )
        
        # Actualizar el recurso
        updated_resource = await prisma.resource.update(
            where={"id": resource_id},
            data={
                "name": resource.name,
                "intro": resource.intro,
                "introformat": resource.introformat,
                "revision": existing_resource.revision + 1,
                "timemodified": datetime.utcnow()
            }
        )
        
        return updated_resource
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating resource: {str(e)}"
        )

@router.delete("/resources/{resource_id}", response_model=ResourceResponse)
async def delete_resource(resource_id: int):
    try:
        deleted_resource = await prisma.resource.delete(
            where={"id": resource_id}
        )
        
        return deleted_resource
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting resource: {str(e)}"
        )

# ----- OPERACIONES CRUD PARA CALIFICACIONES ----- #

@router.post("/courses/{course_id}/grades", response_model=GradeResponse)
async def create_grade(course_id: int, grade: GradeBase):
    try:
        # Verificar si el ítem de calificación existe y pertenece al curso
        grade_item = await prisma.gradeitem.find_unique(where={"id": grade.itemid})
        if not grade_item or grade_item.courseid != course_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Grade item not found in this course"
            )
        
        # Verificar si el usuario existe
        user = await prisma.user.find_unique(where={"id": grade.userid})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verificar si ya existe una calificación para este usuario y elemento
        existing_grade = await prisma.grade.find_first(
            where={
                "itemid": grade.itemid,
                "userid": grade.userid
            }
        )
        
        now = datetime.utcnow()
        
        if existing_grade:
            # Actualizar la calificación existente
            updated_grade = await prisma.grade.update(
                where={"id": existing_grade.id},
                data={
                    "rawgrade": grade.rawgrade,
                    "finalgrade": grade.finalgrade,
                    "feedback": grade.feedback,
                    "timemodified": now
                }
            )
            return updated_grade
        else:
            # Crear una nueva calificación
            new_grade = await prisma.grade.create(
                data={
                    "itemid": grade.itemid,
                    "userid": grade.userid,
                    "rawgrade": grade.rawgrade,
                    "rawgrademax": grade_item.grademax,
                    "rawgrademin": grade_item.grademin,
                    "finalgrade": grade.finalgrade,
                    "feedback": grade.feedback,
                    "feedbackformat": 0,
                    "timecreated": now,
                    "timemodified": now
                }
            )
            return new_grade
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating grade: {str(e)}"
        )

@router.get("/courses/{course_id}/grades", response_model=List[GradeItemResponse])
async def get_course_grade_items(course_id: int):
    # Verificar si el curso existe
    course = await prisma.course.find_unique(where={"id": course_id})
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Obtener los ítems de calificación del curso
    grade_items = await prisma.gradeitem.find_many(where={"courseid": course_id})
    
    return grade_items

@router.get("/courses/{course_id}/user/{user_id}/grades", response_model=List[GradeResponse])
async def get_user_course_grades(course_id: int, user_id: int):
    # Verificar si el curso existe
    course = await prisma.course.find_unique(where={"id": course_id})
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Verificar si el usuario existe
    user = await prisma.user.find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Obtener los ítems de calificación del curso
    grade_items = await prisma.gradeitem.find_many(where={"courseid": course_id})
    
    if not grade_items:
        return []
    
    # Obtener todas las calificaciones del usuario para los ítems del curso
    item_ids = [item.id for item in grade_items]
    grades = await prisma.grade.find_many(
        where={
            "itemid": {
                "in": item_ids
            },
            "userid": user_id
        }
    )
    
    return grades

@router.put("/grades/{grade_id}", response_model=GradeResponse)
async def update_grade(grade_id: int, grade: GradeBase):
    try:
        # Verificar si la calificación existe
        existing_grade = await prisma.grade.find_unique(
            where={"id": grade_id}
        )
        
        if not existing_grade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Grade not found"
            )
        
        # Actualizar la calificación
        updated_grade = await prisma.grade.update(
            where={"id": grade_id},
            data={
                "rawgrade": grade.rawgrade,
                "finalgrade": grade.finalgrade,
                "feedback": grade.feedback,
                "timemodified": datetime.utcnow()
            }
        )
        
        return updated_grade
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating grade: {str(e)}"
        )

@router.delete("/grades/{grade_id}", response_model=GradeResponse)
async def delete_grade(grade_id: int):
    try:
        deleted_grade = await prisma.grade.delete(
            where={"id": grade_id}
        )
        
        return deleted_grade
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting grade: {str(e)}"
        )
        
        
@router.get("/sections", response_model=List[SectionResponse])
async def get_sections():
    sections = await prisma.coursesection.find_many()
    return sections
        
@router.get("/sections/{course_id}", response_model=SectionResponse)
async def get_section_modules(course_id:int):
    # Verificar si el curso existe
    course = await prisma.course.find_unique(where={"id": course_id})
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Obtener las secciones del curso
    sections = await prisma.coursesection.find_many(where={"course": course_id})
    
    return sections

@router.post("/sections", response_model=SectionResponse)
async def create_section(section: SectionBase):
    try:
        # Contar cuántas secciones tiene el curso
        section_count = await prisma.coursesection.count(where={"course": section.course})
        
        # Asignar el número de sección automáticamente
        new_section_number = section_count + 1
        
        timemodified = datetime.utcnow()
        new_section = await prisma.coursesection.create(
            data={
                "course": section.course,
                "name": section.name,
                "section": new_section_number,
                "summary": section.summary,
                "visible": section.visible,
                "timemodified": timemodified
            }
        )
        return new_section
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating section: {str(e)}"
        )

@router.put("/sections/{section_id}", response_model=SectionResponse)
async def update_section(section_id: int, section: SectionBase):
    try:
        updated_section = await prisma.coursesection.update(
            where={"id": section_id},
            data={
                "name": section.name,
                "summary": section.summary,
                "visible": section.visible,
                "timemodified": datetime.utcnow()
            }
        )
        return updated_section
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating section: {str(e)}"
        )

@router.delete("/sections/{section_id}", response_model=SectionResponse)
async def delete_section(section_id: int):
    try:
        deleted_section = await prisma.coursesection.delete(
            where={"id": section_id}
        )
        return deleted_section
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting section: {str(e)}"
        )
