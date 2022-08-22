INGREDIENT_ENDPOINT = '/api/ingredients'


def test_get_most_used_ingredients(client, init_most_used):
    expected_list = ['ing_2', 'ing_3', 'ing_4', 'ing_5', 'ing_6']
    response = client.get(f'{INGREDIENT_ENDPOINT}/most_used')

    assert response.status_code == 200
    assert set([ing['name'] for ing in response.json()]) == set(expected_list)
