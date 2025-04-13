from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime

from models.base import CategoryBase, CategoryResponse
from db import fetch_data, fetch_one, execute_query, execute_query_returning_id

router = APIRouter(
    prefix="/api",
    tags=["rest_api"],
    responses={404: {"description": "Not found"}}
)

@router.post("/categories", response_model=CategoryResponse)
async def create_category(category: CategoryBase):
    try:
        now = datetime.utcnow()
        insert_query = """
        INSERT INTO mdl_course_categories (
            name, idnumber, description, parent, sortorder,
            coursecount, visible, visibleold, timemodified,
            depth, path, theme
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
        """
        
        values = (
            category.name,
            category.idnumber,
            category.description,
            category.parent,
            category.sortorder,
            0,  # coursecount
            category.visible,
            category.visible,  # visibleold
            now,
            category.depth,
            category.path,
            category.theme
        )
        
        new_category = fetch_one(insert_query, values)
        
        return new_category
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating category: {str(e)}"
        )

@router.get("/categories", response_model=List[CategoryResponse])
async def get_categories(parent: Optional[int] = None):
    try:
        if parent is not None:
            query = """
            SELECT * FROM mdl_course_categories
            WHERE parent = %s
            ORDER BY sortorder
            """
            categories = fetch_data(query, (parent,))
        else:
            query = """
            SELECT * FROM mdl_course_categories
            ORDER BY sortorder
            """
            categories = fetch_data(query)
        
        return categories
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching categories: {str(e)}"
        )

@router.get("/categories/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int):
    query = """
    SELECT * FROM mdl_course_categories
    WHERE id = %s
    """
    category = fetch_one(query, (category_id,))
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return category

@router.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, category: CategoryBase):
    try:
        # Actualizar categoría
        update_query = """
        UPDATE mdl_course_categories
        SET name = %s,
            idnumber = %s,
            description = %s,
            parent = %s,
            sortorder = %s,
            visible = %s,
            visibleold = %s,
            timemodified = %s,
            depth = %s,
            path = %s,
            theme = %s
        WHERE id = %s
        RETURNING *
        """
        
        values = (
            category.name,
            category.idnumber,
            category.description,
            category.parent,
            category.sortorder,
            category.visible,
            category.visible,  # visibleold
            datetime.utcnow(),
            category.depth,
            category.path,
            category.theme,
            category_id
        )
        
        updated_category = fetch_one(update_query, values)
        
        if not updated_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
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
        check_query = """
        SELECT COUNT(*) as count FROM mdl_course_category_map
        WHERE category = %s
        """
        result = fetch_one(check_query, (category_id,))
        
        if result and result.get('count', 0) > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete category with associated courses"
            )
        
        # Obtener los datos de la categoría antes de eliminarla
        get_query = """
        SELECT * FROM mdl_course_categories
        WHERE id = %s
        """
        category = fetch_one(get_query, (category_id,))
        
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        
        # Eliminar la categoría
        delete_query = """
        DELETE FROM mdl_course_categories
        WHERE id = %s
        """
        execute_query(delete_query, (category_id,))
        
        return category
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting category: {str(e)}"
        )