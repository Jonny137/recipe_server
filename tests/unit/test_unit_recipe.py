import pytest


from schemas.recipe import RecipeCreate
from core.exceptions import RecipeServerException
from services.recipe import (
    create_new_recipe, get_all_recipes, get_recipe_by_name
)


@pytest.mark.parametrize(
    'test_input,expected', [
        (
            (
                {
                    'name': 'recipe_1',
                    'preparation': 'prep',
                    'ingredients': ['ing1', 'ing2']
                }
            ),
            (
                {
                    'name': 'recipe_1',
                    'preparation': 'prep',
                    'ingredients': ['ing1', 'ing2']
                }
            )
        )
    ]
)
def test_create_recipe(db, test_input, expected):
    new_recipe = create_new_recipe(RecipeCreate(**test_input), db)

    assert new_recipe.name == expected['name']
    assert new_recipe.preparation == expected['preparation']
    assert (
        set(
            [ing.name for ing in new_recipe.ingredients]
        ) == set(expected['ingredients'])
    )


@pytest.mark.parametrize(
    'test_input', [
        (
            {
                'name': 'existing_recipe_1',
                'preparation': 'prep',
                'ingredients': ['ing1', 'ing2']
            }
        )
    ]
)
def test_create_recipe_existing(db, test_input, init_recipe):
    with pytest.raises(RecipeServerException):
        create_new_recipe(RecipeCreate(**test_input), db)


def test_get_all_recipes(db, init_recipe):
    recipes = get_all_recipes(db)

    assert len(recipes) == 2


@pytest.mark.parametrize(
    'test_input,expected', [
        (
                (
                        {
                            'name': 'existing_recipe_1',
                        }
                ),
                (
                        {
                            'name': 'existing_recipe_1',
                            'preparation': 'preparation_1',
                            'ingredients': ['ing_1', 'ing_2']
                        }
                )
        )
    ]
)
def test_get_recipe_by_name(db, test_input, expected, init_recipe):
    recipe = get_recipe_by_name(name=test_input['name'], db=db)

    assert recipe.name == expected['name']
    assert recipe.preparation == expected['preparation']
    assert (
        set(
            [ing.name for ing in recipe.ingredients]
        ) == set(expected['ingredients'])
    )


@pytest.mark.parametrize(
    'test_input', [
        (
            {
                'name': 'recipe_1',
            }
        )
    ]
)
def test_get_recipe_by_name_non_existent(db, test_input, init_recipe):
    with pytest.raises(RecipeServerException):
        get_recipe_by_name(name=test_input['name'], db=db)
