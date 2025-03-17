
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime
from db import prisma_client as prisma

from models.base import ForumBase, ForumResponse, ForumDiscussionBase, ForumDiscussionResponse

router = APIRouter(
    prefix="/api",
    tags=["rest_api"],
    responses={404: {"description": "Not found"}}
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