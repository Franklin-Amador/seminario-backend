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
    
    # No exponemos password en el API pero permitimos inicializarlo
    def __init__(
        self, 
        id: int, 
        username: str, 
        firstname: str, 
        lastname: str, 
        email: str, 
        confirmed: bool, 
        deleted: bool, 
        suspended: bool, 
        institution: Optional[str], 
        department: Optional[str], 
        timecreated: datetime, 
        timemodified: datetime, 
        password: Optional[str] = None, 
        **kwargs
    ):
        self.id = id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.confirmed = confirmed
        self.deleted = deleted
        self.suspended = suspended
        self.institution = institution
        self.department = department
        self.timecreated = timecreated
        self.timemodified = timemodified
        # No guardamos la contraseña como atributo público
        # pero permitimos recibirla en el constructor

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
    showgrades: bool
    newsitems: int
    startdate: datetime
    enddate: Optional[datetime]
    visible: bool
    groupmode: int
    timecreated: datetime
    timemodified: datetime
@strawberry.type
class CourseEnrollment:
    id: int  # Este id corresponde a c.id en la base de datos
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
    timecreated: datetime # Corregido para coincidir con la base de datos
    timemodified: datetime # Corregido para coincidir con la base de datos

@strawberry.type
class CourseSection:
    id: int
    course: int
    section: int
    name: Optional[str]
    summary: Optional[str]
    sequence: Optional[str]
    visible: bool
    availability: Optional[str]
    timemodified: datetime

@strawberry.type
class Category:
    id: int
    name: str
    idnumber: Optional[str]
    description: Optional[str]
    parent: int
    sortorder: int
    coursecount: int
    visible: bool
    visibleold: bool
    timemodified: datetime
    depth: int
    path: str
    theme: Optional[str]

# Module Types
@strawberry.type
class Module:
    id: int
    name: str
    cron: int
    lastcron: Optional[datetime]
    search: Optional[str]
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
    score: int
    indent: int
    visible: bool
    visibleoncoursepage: bool
    visibleold: bool
    groupmode: int
    groupingid: int
    completion: int
    completiongradeitemnumber: Optional[int]
    completionview: bool
    completionexpected: Optional[datetime]
    availability: Optional[str]
    showdescription: bool

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
    userid: int
    roleid: int
    timemodified: datetime

# Assignment Types
@strawberry.type
class Assignment:
    id: int
    course: int
    name: str
    intro: str
    introformat: int
    section: int
    alwaysshowdescription: bool
    nosubmissions: bool
    submissiondrafts: bool
    sendnotifications: bool
    sendlatenotifications: bool
    duedate: Optional[datetime]
    allowsubmissionsfromdate: Optional[datetime]
    grade: Optional[int]
    timemodified: datetime
    requiresubmissionstatement: bool
    completionsubmit: bool
    cutoffdate: Optional[datetime]
    gradingduedate: Optional[datetime]
    teamsubmission: bool
    requireallteammemberssubmit: bool
    teamsubmissiongroupingid: int
    blindmarking: bool
    revealidentities: bool
    attemptreopenmethod: str
    maxattempts: int
    markingworkflow: bool
    markingallocation: bool
@strawberry.type
class Section:
    id: int
    course: int
    section: int
    name: Optional[str]
    summary: Optional[str]
    sequence: Optional[str]
    visible: bool
    availability: Optional[str]
    timemodified: datetime

@strawberry.type
class Submission:
    id: int
    assignment: int
    userid: int
    timecreated: datetime
    timemodified: datetime
    status: str
    groupid: int
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
    introformat: int
    assessed: int
    assesstimestart: Optional[datetime]
    assesstimefinish: Optional[datetime]
    scale: int
    maxbytes: int
    maxattachments: int
    forcesubscribe: int
    trackingtype: int
    rsstype: int
    rssarticles: int
    timemodified: datetime
    warnafter: int
    blockafter: int
    blockperiod: int
    completiondiscussions: int
    completionreplies: int
    completionposts: int
    displaywordcount: bool

@strawberry.type
class ForumDiscussion:
    id: int
    course: int
    forum: int
    name: str
    firstpost: int
    userid: int
    groupid: int
    assessed: bool
    timemodified: datetime
    usermodified: int
    timestart: Optional[datetime]
    timeend: Optional[datetime]
    pinned: bool

@strawberry.type
class ForumPost:
    id: int
    discussion: int
    parent: int
    userid: int
    created: datetime
    modified: datetime
    mailed: int
    subject: str
    message: str
    messageformat: int
    messagetrust: int
    attachment: Optional[str]
    totalscore: int
    mailnow: int

# Grade Types
@strawberry.type
class GradeItem:
    id: int
    courseid: int
    categoryid: Optional[int]
    itemname: Optional[str]
    itemtype: str
    itemmodule: Optional[str]
    iteminstance: Optional[int]
    itemnumber: Optional[int]
    iteminfo: Optional[str]
    idnumber: Optional[str]
    calculation: Optional[str]
    gradetype: int
    grademax: float
    grademin: float
    scaleid: Optional[int]
    outcomeid: Optional[int]
    gradepass: float
    multfactor: float
    plusfactor: float
    aggregationcoef: float
    aggregationcoef2: float
    sortorder: int
    display: int
    decimals: Optional[int]
    hidden: int
    locked: int
    locktime: Optional[datetime]
    needsupdate: int
    weightoverride: int
    timecreated: datetime
    timemodified: datetime

@strawberry.type
class Grade:
    id: int
    itemid: int
    userid: int
    rawgrade: Optional[int]
    rawgrademax: int
    rawgrademin: int
    finalgrade: Optional[int]
    hidden: int
    locked: int
    locktime: Optional[datetime]
    exported: int
    overridden: int
    excluded: int
    feedback: Optional[str]
    feedbackformat: int
    information: Optional[str]
    informationformat: int
    timecreated: datetime
    timemodified: datetime

# Enrollment Types
@strawberry.type
class Enrollment:
    id: int
    enrolid: int
    userid: int
    courseid: int
    course: Optional["CourseEnrollment"] = None  # Relación opcional a Course
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
    reaggregate: Optional[datetime]

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