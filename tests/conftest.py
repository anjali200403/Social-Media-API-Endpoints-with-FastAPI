import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import Base, get_db
from app.oauth import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "user1@gmail.com",
                 "password": "pass123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "user123@gmail.com","password": "pass123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture(scope="function")
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture(scope="function")
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture(scope="function")
def test_posts(test_user,test_user2, session):
    posts_data = [
        {"title": "First Title", "content": "First Content","user_id":test_user['id'],"id":1},
        {"title": "Second Title", "content": "Second Content","user_id":test_user['id'],"id":2},
        {"title": "Third Title", "content": "Third Content","user_id":test_user['id'],"id":3},
        {"title": "Fourth Title", "content": "Fourth Content","user_id":test_user2['id'],"id":4}
    ]

    def create_post_model(post):
        return models.Post(**post)

    posts = [create_post_model(post) for post in posts_data]
    session.add_all(posts)
    session.commit()

    return posts
