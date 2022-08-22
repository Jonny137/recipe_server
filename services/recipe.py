import logging
from typing import List
from sqlalchemy.orm import Session

from models.recipe import Recipe
from schemas.recipe import RecipeCreate
from models.ingredient import Ingredient
from core.exceptions import RecipeServerException
from schemas.recipe import Recipe as RecipeSchema
from services.ingredient import create_new_ingredient


logger = logging.getLogger(__name__)


def create_new_recipe(recipe: RecipeCreate, db: Session) -> RecipeSchema:
    ingredient_list = []

    for ingredient_name in recipe.ingredients:
        ingredient = db.query(Ingredient).filter(
            Ingredient.name == ingredient_name
        ).first()

        if ingredient:
            ingredient_list.append(ingredient)
        else:
            ingredient_list.append(create_new_ingredient(ingredient_name, db))

    new_recipe = Recipe(
        name=recipe.name,
        preparation=recipe.preparation,
        ingredients=ingredient_list
    )

    db.add(new_recipe)
    db.commit()

    logger.info(f'Successfully added new recipe with name: {recipe.name}')
    return new_recipe


def get_all_recipes(db: Session) -> List[RecipeSchema]:
    return db.query(Recipe).all()


def get_recipe_by_name(name: str, db: Session) -> RecipeSchema:
    recipe = db.query(Recipe).filter(Recipe.name == name).first()

    if not recipe:
        logger.error(f'Error during fetching recipe with name: {name}')
        raise RecipeServerException(
            status_code=404,
            message='Recipe with specified name does not exist.'
        )

    return recipe
