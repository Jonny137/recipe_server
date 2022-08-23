from typing import Any, List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from dependencies import get_db
from schemas.ingredient import Ingredient
from services.ingredient import get_most_used_ingredients
ingredient_router = APIRouter()


@ingredient_router.get('/most_used', response_model=List[Ingredient])
def most_used_ingredients(db: Session = Depends(get_db)) -> Any:
    """
    Returns top five most used ingredients in recipes.

    :param db: Database session
    :return: List of ingredients (up to five)
    """

    most_used_ings = get_most_used_ingredients(db)

    return most_used_ings
