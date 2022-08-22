from typing import Any

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from dependencies import get_db
from schemas.recipe import Recipe
from schemas.recipe import RecipeCreate
from services.recipe import create_new_recipe

recipe_router = APIRouter()


@recipe_router.post('/create', response_model=Recipe)
def create_recipe(
        recipe: RecipeCreate, db: Session = Depends(get_db)
) -> Any:
    new_recipe = create_new_recipe(recipe, db)

    return new_recipe
