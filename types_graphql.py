import strawberry
from datetime import datetime
from typing import List, Optional, Any, Dict, Union

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
    course: Optional[Course] = None
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
    section: int
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
