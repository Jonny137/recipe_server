import logging
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.ingredient import Ingredient
from core.exceptions import RecipeServerException
from schemas.ingredient import Ingredient as IngredientSchema


logger = logging.getLogger(__name__)


def create_new_ingredient(
        ingredient_name: str, db: Session
) -> IngredientSchema:
    """
    Create new ingredient.

    :param ingredient_name: Ingredient name
    :param db: Database session
    :return: Newly create Ingredient
    """
    try:
        new_ingredient = Ingredient(name=ingredient_name)

        db.add(new_ingredient)
        db.commit()

        logger.info(
            f'Successfully added new ingredient with name: {ingredient_name}'
        )
        return new_ingredient
    except IntegrityError:
        logger.error(f'Error ingredient creation with name: {ingredient_name}')
        db.rollback()
        raise RecipeServerException(
            status_code=400, message='Duplicated entry.'
        )


def get_most_used_ingredients(db: Session) -> Optional[IngredientSchema]:
    """
    Returns top five most used ingredients in recipes.

    :param db: Database session
    :return: List of ingredients (up to five)
    """
    return (
        db.query(Ingredient)
        .join(Ingredient.recipes)
        .group_by(Ingredient.id)
        .order_by(func.count().desc()).limit(5).all()
    )
