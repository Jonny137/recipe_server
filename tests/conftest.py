import pytest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from sqlalchemy_utils import database_exists, create_database

from app import app
from db.base_class import Base
from dependencies import get_db
from core.configuration import settings

from schemas.recipe import RecipeCreate
from services.recipe import create_new_recipe


@pytest.fixture(scope='session', autouse=True)
def db_engine():
    engine = create_engine(settings.TEST_DATABASE_URL)
    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope='function')
def db(db_engine):
    connection = db_engine.connect()

    # begin a non-ORM transaction
    connection.begin()

    # bind an individual Session to the connection
    db = Session(bind=connection)

    yield db

    db.rollback()
    connection.close()


@pytest.fixture(scope='function')
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c


@pytest.fixture
def init_recipe(db):
    recipe_1 = create_new_recipe(
        RecipeCreate(
            name='existing_recipe_1',
            preparation='preparation_1',
            ingredients=['ing_1', 'ing_2']
        ),
        db
    )
    recipe_2 = create_new_recipe(
        RecipeCreate(
            name='existing_recipe_2',
            preparation='preparation_2',
            ingredients=['ing_1', 'ing_2']
        ),
        db
    )

    return recipe_1, recipe_2


@pytest.fixture
def init_most_used(db):
    create_new_recipe(
        RecipeCreate(
            name='recipe_1',
            preparation='preparation',
            ingredients=['ing_1', 'ing_2']
        ),
        db
    )
    create_new_recipe(
        RecipeCreate(
            name='recipe_2',
            preparation='preparation',
            ingredients=['ing_2', 'ing_3']
        ),
        db
    )
    create_new_recipe(
        RecipeCreate(
            name='recipe_3',
            preparation='preparation',
            ingredients=['ing_3', 'ing_4']
        ),
        db
    )
    create_new_recipe(
        RecipeCreate(
            name='recipe_4',
            preparation='preparation',
            ingredients=['ing_4', 'ing_5']
        ),
        db
    )
    create_new_recipe(
        RecipeCreate(
            name='recipe_5',
            preparation='preparation',
            ingredients=['ing_5', 'ing_6']
        ),
        db
    )
    create_new_recipe(
        RecipeCreate(
            name='recipe_6',
            preparation='preparation',
            ingredients=['ing_6']
        ),
        db
    )
