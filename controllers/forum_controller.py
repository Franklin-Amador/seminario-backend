from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime

from models.base import ForumBase, ForumResponse, ForumDiscussionBase, ForumDiscussionResponse, ForumPostBase, ForumPostResponse
from db import fetch_data, fetch_one, execute_query

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
        course_query = """
        SELECT id FROM mdl_course WHERE id = %s
        """
        course = fetch_one(course_query, (course_id,))
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Crear el foro
        now = datetime.utcnow()
        insert_query = """
        INSERT INTO mdl_forum (
            course, type, name, intro, introformat, timemodified,
            assessed, scale, maxbytes, maxattachments, forcesubscribe,
            trackingtype, rsstype, rssarticles, warnafter, blockafter,
            blockperiod, completiondiscussions, completionreplies, completionposts,
            displaywordcount
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
        """
        
        values = (
            course_id,
            forum.type,
            forum.name,
            forum.intro,
            forum.introformat,
            now,  # timemodified
            0,    # assessed
            0,    # scale
            0,    # maxbytes
            1,    # maxattachments
            0,    # forcesubscribe
            1,    # trackingtype
            0,    # rsstype
            0,    # rssarticles
            0,    # warnafter
            0,    # blockafter
            0,    # blockperiod
            0,    # completiondiscussions
            0,    # completionreplies
            0,    # completionposts
            False # displaywordcount
        )
        
        new_forum = fetch_one(insert_query, values)
        
        return new_forum
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating forum: {str(e)}"
        )

@router.get("/courses/{course_id}/forums", response_model=List[ForumResponse])
async def get_course_forums(course_id: int):
    try:
        # Verificar si el curso existe
        course_query = """
        SELECT id FROM mdl_course WHERE id = %s
        """
        course = fetch_one(course_query, (course_id,))
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Obtener los foros
        query = """
        SELECT * FROM mdl_forum
        WHERE course = %s
        ORDER BY id
        """
        forums = fetch_data(query, (course_id,))
        
        return forums
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching forums: {str(e)}"
        )

@router.get("/forums/{forum_id}", response_model=ForumResponse)
async def get_forum(forum_id: int):
    query = """
    SELECT * FROM mdl_forum
    WHERE id = %s
    """
    forum = fetch_one(query, (forum_id,))
    
    if not forum:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Forum not found"
        )
    
    return forum

@router.put("/forums/{forum_id}", response_model=ForumResponse)
async def update_forum(forum_id: int, forum: ForumBase):
    try:
        # Actualizar foro
        update_query = """
        UPDATE mdl_forum
        SET name = %s,
            type = %s,
            intro = %s,
            introformat = %s,
            timemodified = %s
        WHERE id = %s
        RETURNING *
        """
        
        values = (
            forum.name,
            forum.type,
            forum.intro,
            forum.introformat,
            datetime.utcnow(),
            forum_id
        )
        
        updated_forum = fetch_one(update_query, values)
        
        if not updated_forum:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Forum not found"
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
        # Obtener el foro antes de eliminarlo
        get_query = """
        SELECT * FROM mdl_forum
        WHERE id = %s
        """
        forum = fetch_one(get_query, (forum_id,))
        
        if not forum:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Forum not found"
            )
        
        # Obtener discusiones asociadas
        discussions_query = """
        SELECT id FROM mdl_forum_discussions
        WHERE forum = %s
        """
        discussions = fetch_data(discussions_query, (forum_id,))
        
        # Eliminar mensajes y discusiones asociados
        for discussion in discussions:
            # Eliminar mensajes
            delete_posts_query = """
            DELETE FROM mdl_forum_posts
            WHERE discussion = %s
            """
            execute_query(delete_posts_query, (discussion['id'],))
            
            # Eliminar discusión
            delete_discussion_query = """
            DELETE FROM mdl_forum_discussions
            WHERE id = %s
            """
            execute_query(delete_discussion_query, (discussion['id'],))
        
        # Eliminar el foro
        delete_query = """
        DELETE FROM mdl_forum
        WHERE id = %s
        """
        execute_query(delete_query, (forum_id,))
        
        return forum
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
        forum_query = """
        SELECT * FROM mdl_forum
        WHERE id = %s
        """
        forum = fetch_one(forum_query, (forum_id,))
        
        if not forum:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Forum not found"
            )
        
        # Verificar si el usuario existe
        user_query = """
        SELECT id FROM mdl_user
        WHERE id = %s AND deleted = FALSE
        """
        user = fetch_one(user_query, (discussion.userid,))
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Crear el primer mensaje para la discusión (temporal)
        now = datetime.utcnow()
        first_post_query = """
        INSERT INTO mdl_forum_posts (
            discussion, parent, userid, created, modified,
            subject, message, messageformat, mailed, totalscore, mailnow
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
        """
        
        first_post_values = (
            0,  # discussion (temporal, se actualizará después)
            0,  # parent
            discussion.userid,
            now,  # created
            now,  # modified
            discussion.name,  # subject
            "Mensaje inicial de la discusión",  # message
            1,  # messageformat
            0,  # mailed
            0,  # totalscore
            0   # mailnow
        )
        
        first_post = fetch_one(first_post_query, first_post_values)
        
        # Crear la discusión
        discussion_query = """
        INSERT INTO mdl_forum_discussions (
            course, forum, name, firstpost, userid, groupid,
            assessed, timemodified, usermodified, pinned
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
        """
        
        discussion_values = (
            forum['course'],
            forum_id,
            discussion.name,
            first_post['id'],  # firstpost
            discussion.userid,
            -1,  # groupid
            True,  # assessed
            now,  # timemodified
            discussion.userid,  # usermodified
            False  # pinned
        )
        
        new_discussion = fetch_one(discussion_query, discussion_values)
        
        # Actualizar el primer mensaje con el ID de la discusión
        update_post_query = """
        UPDATE mdl_forum_posts
        SET discussion = %s
        WHERE id = %s
        """
        execute_query(update_post_query, (new_discussion['id'], first_post['id']))
        
        return new_discussion
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating discussion: {str(e)}"
        )

@router.get("/forums/{forum_id}/discussions", response_model=List[ForumDiscussionResponse])
async def get_forum_discussions(forum_id: int):
    try:
        # Verificar si el foro existe
        forum_query = """
        SELECT id FROM mdl_forum
        WHERE id = %s
        """
        forum = fetch_one(forum_query, (forum_id,))
        
        if not forum:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Forum not found"
            )
        
        # Obtener las discusiones
        query = """
        SELECT * FROM mdl_forum_discussions
        WHERE forum = %s
        ORDER BY timemodified DESC
        """
        discussions = fetch_data(query, (forum_id,))
        
        return discussions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching discussions: {str(e)}"
        )

@router.get("/discussions/{discussion_id}", response_model=ForumDiscussionResponse)
async def get_discussion(discussion_id: int):
    query = """
    SELECT * FROM mdl_forum_discussions
    WHERE id = %s
    """
    discussion = fetch_one(query, (discussion_id,))
    
    if not discussion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discussion not found"
        )
    
    return discussion

@router.put("/discussions/{discussion_id}", response_model=ForumDiscussionResponse)
async def update_discussion(discussion_id: int, discussion: ForumDiscussionBase):
    try:
        # Actualizar discusión
        update_query = """
        UPDATE mdl_forum_discussions
        SET name = %s,
            timemodified = %s,
            usermodified = %s
        WHERE id = %s
        RETURNING *
        """
        
        values = (
            discussion.name,
            datetime.utcnow(),
            discussion.userid,
            discussion_id
        )
        
        updated_discussion = fetch_one(update_query, values)
        
        if not updated_discussion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Discussion not found"
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
        # Obtener la discusión antes de eliminarla
        get_query = """
        SELECT * FROM mdl_forum_discussions
        WHERE id = %s
        """
        discussion = fetch_one(get_query, (discussion_id,))
        
        if not discussion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Discussion not found"
            )
        
        # Eliminar mensajes asociados
        delete_posts_query = """
        DELETE FROM mdl_forum_posts
        WHERE discussion = %s
        """
        execute_query(delete_posts_query, (discussion_id,))
        
        # Eliminar la discusión
        delete_query = """
        DELETE FROM mdl_forum_discussions
        WHERE id = %s
        """
        execute_query(delete_query, (discussion_id,))
        
        return discussion
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting discussion: {str(e)}"
        )