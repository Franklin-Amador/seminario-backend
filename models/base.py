from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Base models
class RoleBase(BaseModel):
    name: str
    shortname: str
    description: Optional[str] = None
    sortorder: int
    archetype: Optional[str] = None

class RoleResponse(RoleBase):
    id: int
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str
    email: str
    institution: Optional[str] = None
    department: Optional[str] = None

class UserResponse(UserBase):
    id: int
    confirmed: bool
    deleted: bool
    suspended: bool
    timecreated: datetime
    timemodified: datetime
    
    class Config:
        from_attributes = True
        
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

class CourseResponse(CourseBase):
    id: int
    timecreated: datetime
    timemodified: datetime
    
    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    idnumber: Optional[str] = None
    description: Optional[str] = None
    parent: int = 0
    sortorder: int
    visible: bool = True
    depth: int
    path: str
    
class CategoryResponse(CategoryBase):
    id: int
    timemodified: datetime
    
    class Config:
        from_attributes = True
        
class CourseSectionBase(BaseModel):
    course: int
    section: int
    name: Optional[str] = None
    summary: Optional[str] = None
    sequence: Optional[str] = None
    visible: bool = True
    
class CourseSectionResponse(CourseSectionBase):
    id: int
    timemodified: datetime
    
    class Config:
        from_attributes = True
        
class AssignmentBase(BaseModel):
    course: int
    name: str
    intro: str
    introformat: int = 1
    section:int
    duedate: Optional[datetime] = None
    allowsubmissionsfromdate: Optional[datetime] = None
    grade: Optional[int] = None
    
class AssignmentResponse(AssignmentBase):
    id: int
    timemodified: datetime
    
    class Config:
        from_attributes = True
        
class SubmissionBase(BaseModel):
    assignment: int
    userid: int
    status: str
    groupid: int = 0
    attemptnumber: int = 0
    
class SubmissionResponse(SubmissionBase):
    id: int
    timecreated: datetime
    timemodified: datetime
    latest: bool
    
    class Config:
        from_attributes = True
        
class ForumBase(BaseModel):
    course: int
    type: str = "general"
    name: str
    intro: str
    introformat: int = 0
    
class ForumResponse(ForumBase):
    id: int
    timemodified: datetime
    
    class Config:
        from_attributes = True
        
class ForumDiscussionBase(BaseModel):
    course: int
    forum: int
    name: str
    firstpost: int
    userid: int
    
class ForumDiscussionResponse(ForumDiscussionBase):
    id: int
    timemodified: datetime
    
    class Config:
        from_attributes = True
        
class ForumPostBase(BaseModel):
    discussion: int
    parent: int = 0
    userid: int
    subject: str
    message: str
    messageformat: int = 0
    
class ForumPostResponse(ForumPostBase):
    id: int
    created: datetime
    modified: datetime
    
    class Config:
        from_attributes = True
        
class EnrollmentBase(BaseModel):
    enrolid: int
    userid: int
    courseid: int
    status: int = 0
    timestart: Optional[datetime] = None
    timeend: Optional[datetime] = None
    
class EnrollmentResponse(EnrollmentBase):
    id: int
    timecreated: datetime
    timemodified: datetime
    
    class Config:
        from_attributes = True
        
class GradeItemBase(BaseModel):
    courseid: int
    itemname: Optional[str] = None
    itemtype: str
    itemmodule: Optional[str] = None
    iteminstance: Optional[int] = None
    grademax: int = 100
    grademin: int = 0
    
class GradeItemResponse(GradeItemBase):
    id: int
    timecreated: datetime
    timemodified: datetime
    
    class Config:
        from_attributes = True
        
class GradeBase(BaseModel):
    itemid: int
    userid: int
    rawgrade: Optional[int] = None
    finalgrade: Optional[int] = None
    feedback: Optional[str] = None
    
class GradeResponse(GradeBase):
    id: int
    timecreated: datetime
    timemodified: datetime
    
    class Config:
        from_attributes = True
        
class CourseCompletionBase(BaseModel):
    userid: int
    course: int
    timeenrolled: datetime
    timestarted: datetime
    timecompleted: Optional[datetime] = None
    
class CourseCompletionResponse(CourseCompletionBase):
    id: int
    
    class Config:
        from_attributes = True
        
class ResourceBase(BaseModel):
    course: int
    name: str
    intro: Optional[str] = None
    introformat: int = 0
    
class ResourceResponse(ResourceBase):
    id: int
    timemodified: datetime
    
    class Config:
        from_attributes = True
        
class SectionBase(BaseModel):
    course: int
    # section:int
    name: str
    summary: Optional[str] = None
    sequence: Optional[str] = None
    visible: bool = True
    # timemodied: Optional[datetime] = None
    
class SectionResponse(SectionBase):
    id: int
    timemodified: datetime
    
    class Config:
        from_attributes = True