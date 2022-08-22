import pytest

from services.ingredient import (
    create_new_ingredient, get_most_used_ingredients
)


@pytest.mark.parametrize(
    'test_input,expected', [
        (
            (
                {
                    'name': 'ingredient_1'
                }
            ),
            (
                {
                    'name': 'ingredient_1',
                }
            )
        )
    ]
)
def test_create_ingredient(db, test_input, expected, init_recipe):
    recipe_1, _ = init_recipe
    ingredient_data = test_input
    new_ingredient = create_new_ingredient(
        ingredient_name=ingredient_data['name'], db=db
    )
    assert new_ingredient.name == expected['name']


@pytest.mark.parametrize(
    'expected', [
        (
            ['ing_2', 'ing_3', 'ing_4', 'ing_5', 'ing_6']
        )
    ]
)
def test_get_most_used_ingredients(db, expected, init_most_used):
    most_used_ings = get_most_used_ingredients(db)
    assert set([ing.name for ing in most_used_ings]) == set(expected)


def test_get_most_used_ingredients_no_result(db):
    most_used_ings = get_most_used_ingredients(db)
    assert len(most_used_ings) == 0
