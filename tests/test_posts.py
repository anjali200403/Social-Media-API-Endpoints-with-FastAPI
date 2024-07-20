import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts")  

    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)


def test_unauthorized_user_get_all_posts(client):
    res = client.get("/posts")  

    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")  

    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/88888") 

    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")  

    assert res.status_code == 200
    post = schemas.PostOut(**res.json())
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize("title, content, published", [
    ("Awesome New Title", "Awesome New Content", True),
    ("Favorite Pizza", "I Love Pepperoni", False),
    ("Tallest Skyscrapers", "Wahoo", True),
])
def test_create_post(authorized_client, test_user, title, content, published):
    data = {
        "title": title,
        "content": content,
        "published": published
    }
    res = authorized_client.post("/posts", json=data)  

    assert res.status_code == 201


def test_create_post_default_published_true(authorized_client, test_user):
    data = {
        "title": "Arbitrary Title",
        "content": "Arbitrary Content"
    }
    res = authorized_client.post("/posts", json=data) 

    assert res.status_code == 201


def test_unauthorized_user_create_post(client):
    data = {
        "title": "Unauthorized Title",
        "content": "Unauthorized Content",
        "published": True
    }
    res = client.post("/posts", json=data) 

    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts{test_posts[0].id}")  

    assert res.status_code == 404


def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")  

    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client):
    res = authorized_client.delete("/posts/8000000") 

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")  

    assert res.status_code == 403


def test_update_post(authorized_client, test_posts):
    data = {
        "title": "Updated Title",
        "content": "Updated Content"
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)  

    assert res.status_code == 202
    updated_post = schemas.Post(**res.json())
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_user2, test_posts):
    data = {
        "title": "Updated Title",
        "content": "Updated Content"
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)  

    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_posts):
    res = client.put(f"/posts{test_posts[0].id}")  

    assert res.status_code == 404


def test_update_post_non_exist(authorized_client):
    data = {
        "title": "Updated Title",
        "content": "Updated Content"
    }
    res = authorized_client.put(f"/posts/8000000", json=data)  # Updated endpoint path

    assert res.status_code == 404
