from typing import Any
from sqlalchemy.orm import Session
from models.ingredient import Ingredient


def create_new_ingredient(ingredient_name: str, db: Session) -> Any:
    new_ingredient = Ingredient(name=ingredient_name)

    db.add(new_ingredient)
    db.commit()

    return new_ingredient
