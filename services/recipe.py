from typing import List, Optional
from sqlalchemy.orm import Session

from models.recipe import Recipe
from schemas.recipe import RecipeCreate
from models.ingredient import Ingredient
from schemas.recipe import Recipe as RecipeSchema
from services.ingredient import create_new_ingredient


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

    return new_recipe


def get_all_recipes(db: Session) -> List[RecipeSchema]:
    return db.query(Recipe).all()


def get_recipe_by_name(name: str, db: Session) -> Optional[RecipeSchema]:
    return db.query(Recipe).filter(Recipe.name == name).first()
