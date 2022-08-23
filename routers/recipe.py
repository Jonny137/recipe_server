from typing import Any, List

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
    """
    Create new recipe.

    :param recipe: Recipe model containing name,
                   preparation and ingredients fields.
    :param db: Database session.
    :return: Newly created recipe
    """
    new_recipe = create_new_recipe(recipe, db)

    return new_recipe


@recipe_router.get('/all', response_model=List[Recipe])
def all_recipes(db: Session = Depends(get_db)) -> Any:
    """
    Get all recipes.

    :param db: Database session.
    :return: List of recipes.
    """
    recipes = get_all_recipes(db)

    return recipes


@recipe_router.get('/', response_model=Recipe)
def recipe_by_name(name: str, db: Session = Depends(get_db)) -> Any:
    """
    Get recipe by it's name.

    :param name: Name of the recipe.
    :param db: Database session.
    :return: Found recipe.
    """
    recipe = get_recipe_by_name(name, db)

    return recipe
