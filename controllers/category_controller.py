
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime
import bcrypt
from db import prisma_client as prisma

from models.base import CategoryBase, CategoryResponse

router = APIRouter(
    prefix="/api",
    tags=["rest_api"],
    responses={404: {"description": "Not found"}}
)

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