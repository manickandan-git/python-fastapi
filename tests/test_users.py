
import pytest
from jose import jwt
from app import schemas

from app.config import settings

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}    

def test_create_user(client):
    response = client.post(
        "/users/",
        json={"email": "test7@example.com", "password": "testpassword", "phone_number": "1234567890"}
    )
    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "test7@example.com"
    assert new_user.phone_number == "1234567890"
    assert response.status_code == 201

def test_login_user(test_user, client):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('test@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('test3@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password, "phone_number": "1234567890"})

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'
        