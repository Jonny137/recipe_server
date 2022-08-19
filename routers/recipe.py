from typing import Any

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Body

from dependencies import get_db
from models.ingredient import Ingredient
from models.recipe import Recipe

from schemas.recipe import Recipe as RecipeSchema
from schemas.recipe import RecipeCreate
from schemas.ingredient import Ingredient as IngredientSchema
from schemas.ingredient import IngredientCreate

recipe_router = APIRouter()


@recipe_router.post('/v1', response_model=RecipeSchema)
def create_new_recipe(
        recipe: RecipeCreate, db: Session = Depends(get_db)
) -> Any:
    ingredient_list = []
    for ingredient_name in recipe.ingredients:
        ingredient = db.query(Ingredient).filter(
            Ingredient.name == ingredient_name
        ).first()

        if ingredient:
            ingredient_list.append(ingredient)

    new_recipe = Recipe(
        name=recipe.name,
        preparation=recipe.preparation,
        ingredients=ingredient_list
    )

    db.add(new_recipe)
    db.commit()

    return new_recipe


@recipe_router.post('/v2', response_model=IngredientSchema)
def create_new_ingredient(
        ingredient: IngredientCreate, db: Session = Depends(get_db)
) -> Any:
    new_ingredient = Ingredient(name=ingredient.name)

    db.add(new_ingredient)
    db.commit()

    return new_ingredient
