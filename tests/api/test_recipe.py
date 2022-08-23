RECIPE_ENDPOINT = '/api/recipes'


def test_create_new_recipe(client):
    req_body = {
        'name': 'recipe_name',
        'preparation': 'Some preparation text.',
        'ingredients': ['ing_1', 'ing_2']
    }
    response = client.post(f'{RECIPE_ENDPOINT}/create', json=req_body)

    assert response.status_code == 200
    assert response.json()['name'] == req_body['name']
    assert response.json()['preparation'] == req_body['preparation']
    assert len(response.json()['ingredients']) == 2


def test_get_all_recipe(client, init_recipe):
    response = client.get(f'{RECIPE_ENDPOINT}/all')

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_all_recipe_no_result(client):
    response = client.get(f'{RECIPE_ENDPOINT}/all')

    assert response.status_code == 200
    assert len(response.json()) == 0


def test_get_recipe_by_name(client, init_recipe):
    recipe_1, _ = init_recipe
    response = client.get(f'{RECIPE_ENDPOINT}/?name=existing_recipe_1')

    assert response.status_code == 200
    assert response.json()['name'] == recipe_1.name
    assert response.json()['preparation'] == recipe_1.preparation
    assert len(response.json()['ingredients']) == len(recipe_1.ingredients)
