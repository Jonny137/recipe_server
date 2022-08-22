from typing import Any, List, Union

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from dependencies import get_db
from schemas.recipe import Recipe
from schemas.recipe import RecipeCreate
from services.recipe import (
    create_new_recipe, get_all_recipes, get_recipe_by_name
)

recipe_router = APIRouter()


@recipe_router.post('/create', response_model=Recipe)
def create_recipe(
        recipe: RecipeCreate, db: Session = Depends(get_db)
) -> Any:
    new_recipe = create_new_recipe(recipe, db)

    return new_recipe


@recipe_router.get('/all', response_model=List[Recipe])
def all_recipes(db: Session = Depends(get_db)) -> Any:
    recipes = get_all_recipes(db)

    return recipes


@recipe_router.get('/', response_model=Union[Recipe | str])
def recipe_by_name(name: str, db: Session = Depends(get_db)) -> Any:
    recipe = get_recipe_by_name(name, db)

    if not recipe:
        return f'No recipe with name: {name}'
    return recipe
