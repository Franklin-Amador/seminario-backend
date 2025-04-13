from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Añadir clases que faltan para login_controller
class BulkPasswordUpdateRequest(BaseModel):
    admin_key: str
    new_password: str = "1234"

class BulkPasswordUpdateResponse(BaseModel):
    success: bool
    count: Optional[int] = None
    message: Optional[str] = None

# Modelos base (para entrada de datos)
class UserBase(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str
    email: str
    institution: Optional[str] = None
    department: Optional[str] = None

class CourseBase(BaseModel):
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

class CategoryBase(BaseModel):
    name: str
    idnumber: Optional[str] = None
    description: Optional[str] = None
    parent: int = 0
    sortorder: int
    visible: bool = True
    depth: int
    path: str
    theme: Optional[str] = None

class AssignmentBase(BaseModel):
    course: int
    name: str
    intro: str
    introformat: int = 0
    section: int
    duedate: Optional[datetime] = None
    allowsubmissionsfromdate: Optional[datetime] = None
    grade: Optional[int] = None

class SubmissionBase(BaseModel):
    assignment: int
    userid: int
    status: str
    groupid: int = 0
    attemptnumber: int = 0

class ForumBase(BaseModel):
    course: int
    type: str = "general"
    name: str
    intro: str
    introformat: int = 0

class ForumDiscussionBase(BaseModel):
    forum: int
    name: str
    userid: int

class ForumPostBase(BaseModel):
    discussion: int
    parent: int = 0
    userid: int
    subject: str
    message: str
    messageformat: int = 0

class EnrollmentBase(BaseModel):
    enrolid: int
    userid: int
    courseid: int
    status: int = 0
    timestart: Optional[datetime] = None
    timeend: Optional[datetime] = None

class GradeItemBase(BaseModel):
    courseid: int
    itemname: Optional[str] = None
    itemtype: str
    itemmodule: Optional[str] = None
    iteminstance: Optional[int] = None
    grademax: float = 100.0
    grademin: float = 0.0

class GradeBase(BaseModel):
    itemid: int
    userid: int
    rawgrade: Optional[int] = None
    finalgrade: Optional[int] = None
    feedback: Optional[str] = None

class CourseCompletionBase(BaseModel):
    userid: int
    course: int
    timeenrolled: datetime
    timestarted: datetime
    timecompleted: Optional[datetime] = None

class ResourceBase(BaseModel):
    course: int
    name: str
    intro: Optional[str] = None
    introformat: int = 0

class RoleBase(BaseModel):
    name: str
    shortname: str
    description: Optional[str] = None
    sortorder: int
    archetype: Optional[str] = None

class SectionBase(BaseModel):
    course: int
    name: Optional[str] = None
    summary: Optional[str] = None
    visible: bool = True

# Modelos para respuestas (con campos adicionales como id)
class UserResponse(UserBase):
    id: int
    auth: str = "manual"
    confirmed: bool = False
    lang: str = "es"
    timezone: str = "99"
    firstaccess: Optional[datetime] = None
    lastaccess: Optional[datetime] = None
    lastlogin: Optional[datetime] = None
    currentlogin: Optional[datetime] = None
    deleted: bool = False
    suspended: bool = False
    mnethostid: int = 1
    timecreated: datetime
    timemodified: datetime

    class Config:
        from_attributes = True

class CourseResponse(CourseBase):
    id: int
    showgrades: bool = True
    newsitems: int = 5
    groupmode: int = 0
    timecreated: datetime
    timemodified: datetime

    class Config:
        from_attributes = True

class CategoryResponse(CategoryBase):
    id: int
    coursecount: int = 0
    visibleold: bool = True
    timemodified: datetime

    class Config:
        from_attributes = True

class AssignmentResponse(AssignmentBase):
    id: int
    alwaysshowdescription: bool = True
    nosubmissions: bool = False
    submissiondrafts: bool = False
    sendnotifications: bool = False
    sendlatenotifications: bool = False
    requiresubmissionstatement: bool = False
    completionsubmit: bool = False
    teamsubmission: bool = False
    requireallteammemberssubmit: bool = False
    teamsubmissiongroupingid: int = 0
    blindmarking: bool = False
    revealidentities: bool = False
    attemptreopenmethod: str = "none"
    maxattempts: int = -1
    markingworkflow: bool = False
    markingallocation: bool = False
    timemodified: datetime

    class Config:
        from_attributes = True

class SubmissionResponse(SubmissionBase):
    id: int
    timecreated: datetime
    timemodified: datetime
    latest: bool = False

    class Config:
        from_attributes = True

class ForumResponse(ForumBase):
    id: int
    assessed: int = 0
    scale: int = 0
    maxbytes: int = 0
    maxattachments: int = 1
    forcesubscribe: int = 0
    trackingtype: int = 1
    rsstype: int = 0
    rssarticles: int = 0
    timemodified: datetime
    warnafter: int = 0
    blockafter: int = 0
    blockperiod: int = 0
    completiondiscussions: int = 0
    completionreplies: int = 0
    completionposts: int = 0
    displaywordcount: bool = False

    class Config:
        from_attributes = True

class ForumDiscussionResponse(ForumDiscussionBase):
    id: int
    course: int
    firstpost: int
    groupid: int = -1
    assessed: bool = True
    timemodified: datetime
    usermodified: int = 0
    timestart: Optional[datetime] = None
    timeend: Optional[datetime] = None
    pinned: bool = False

    class Config:
        from_attributes = True

class ForumPostResponse(ForumPostBase):
    id: int
    created: datetime
    modified: datetime
    mailed: int = 0
    messagetrust: int = 0
    attachment: Optional[str] = None
    totalscore: int = 0
    mailnow: int = 0

    class Config:
        from_attributes = True

class EnrollmentResponse(EnrollmentBase):
    id: int
    timecreated: datetime
    timemodified: datetime

    class Config:
        from_attributes = True

class GradeItemResponse(GradeItemBase):
    id: int
    categoryid: Optional[int] = None
    itemnumber: Optional[int] = None
    iteminfo: Optional[str] = None
    idnumber: Optional[str] = None
    calculation: Optional[str] = None
    gradetype: int = 1
    scaleid: Optional[int] = None
    outcomeid: Optional[int] = None
    gradepass: float = 0.0
    multfactor: float = 1.0
    plusfactor: float = 0.0
    aggregationcoef: float = 0.0
    aggregationcoef2: float = 0.0
    sortorder: int = 0
    display: int = 0
    decimals: Optional[int] = None
    hidden: int = 0
    locked: int = 0
    locktime: Optional[datetime] = None
    needsupdate: int = 0
    weightoverride: int = 0
    timecreated: datetime
    timemodified: datetime

    class Config:
        from_attributes = True

class GradeResponse(GradeBase):
    id: int
    rawgrademax: int = 100
    rawgrademin: int = 0
    hidden: int = 0
    locked: int = 0
    locktime: Optional[datetime] = None
    exported: int = 0
    overridden: int = 0
    excluded: int = 0
    feedbackformat: int = 0
    information: Optional[str] = None
    informationformat: int = 0
    timecreated: datetime
    timemodified: datetime

    class Config:
        from_attributes = True

class CourseCompletionResponse(CourseCompletionBase):
    id: int
    reaggregate: Optional[datetime] = None

    class Config:
        from_attributes = True

class ResourceResponse(ResourceBase):
    id: int
    tobemigrated: int = 0
    legacyfiles: int = 0
    legacyfileslast: Optional[int] = None
    display: int = 0
    displayoptions: Optional[str] = None
    filterfiles: int = 0
    revision: int = 0
    timemodified: datetime

    class Config:
        from_attributes = True

class RoleResponse(RoleBase):
    id: int

    class Config:
        from_attributes = True

class SectionResponse(SectionBase):
    id: int
    section: int
    sequence: Optional[str] = None
    availability: Optional[str] = None
    timemodified: datetime

    class Config:
        from_attributes = True

# Modelos específicos para autenticación
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    user_id: Optional[int] = None
    username: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    roles: Optional[List[dict]] = None
    message: Optional[str] = None

class UserAuth(BaseModel):
    username: str
    email: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None

class TokenData(BaseModel):
    username: Optional[str] = None