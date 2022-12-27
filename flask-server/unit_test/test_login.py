import json
import pytest
import logging as log

def login(client, cred_json):
    return client.post('/login', json=cred_json, follow_redirects=False)

def login_success(client,email,password):
    cred_obj = {"email": email, "password": password}
    cred_json = cred_obj
    response = login(client, cred_json)
    data = json.loads(response.data)
    assert data["status_code"] == 200
    assert 'you are Successfully Logged In' in data.values()
    assert 'access_token' in data.keys()

def login_incomplete(client,email):
    cred_obj = {"email": email, "password": None}
    cred_json = cred_obj
    response = login(client, cred_json)
    data = json.loads(response.data)
    assert data["status_code"] == 400
    assert 'All fields are required for logging in' in data.values()
    assert 'access_token' not in data.keys()

# def test_login_incorrect_email(client):
#     cred_obj = {"email": "thu12@gmail.com", "password": "Abcdefgh1234#"}
#     cred_json = json.dumps(cred_obj)
#     response = login(client, cred_json)
#     data=json.loads(response.data)
#     assert response.status_code == 404
#     assert 'Email does not exist...' in data.values()
#     assert 'access_token' not in data.keys()

def login_incorrect_password(client,email,password):
    cred_obj = {"email": email, "password": password}
    cred_json = cred_obj
    response = login(client, cred_json)
    data = json.loads(response.data)
    assert data["status_code"] == 401
    assert 'Password is incorrect...' in data.values()
    assert 'access_token' not in data.keys()

# def login_password_with_no_uppercase_letter(client,email,password):
#     cred_obj = {"email": email, "password": password}
#     cred_json = json.dumps(cred_obj)
#     response = login(client, cred_json)
#     data=json.loads(response.data)
#     print(data)
#     assert response.status_code == 400
#     assert 'Password must contain at least one uppercase letter' in data['error'].values()
#     assert 'access_token' not in data.keys()

# def login_password_with_no_lowercase_letter(client,email,password):
#     cred_obj = {"email": email, "password": password}
#     cred_json = json.dumps(cred_obj)
#     response = login(client, cred_json)
#     data=json.loads(response.data)
#     print(data)
#     assert response.status_code == 400
#     assert 'Password must contain at least one lowercase letter' in data['error'].values()
#     assert 'access_token' not in data.keys()

# def login_password_with_no_number(client,email,password):
#     cred_obj = {"email": email, "password": password}
#     cred_json = json.dumps(cred_obj)
#     response = login(client, cred_json)
#     data=json.loads(response.data)
#     print(data)
#     assert response.status_code == 400
#     assert 'Password must contain at least one number' in data['error'].values()
#     assert 'access_token' not in data.keys()

# def login_password_with_no_character(client,email,password):
#     cred_obj = {"email": email, "password": password}
#     cred_json = json.dumps(cred_obj)
#     response = login(client, cred_json)
#     data=json.loads(response.data)
#     print(data)
#     assert response.status_code == 400
#     assert 'Password must contain at least one special character' in data['error'].values()
#     assert 'access_token' not in data.keys()


@pytest.mark.usefixtures("client")
def test_login_success(client):
    login_success(client,'admin@gmail.com','admin')
    login_success(client,'staff@gmail.com','staff')
    login_success(client,'staff5@gmail.com','staff5')
    login_success(client,'staff7@gmail.com','staff7')

@pytest.mark.usefixtures("client")
def test_login_incomplete(client):
    login_incomplete(client,'admin@gmail.com')
    login_incomplete(client,'staff@gmail.com')
    login_incomplete(client,'staff5@gmail.com')

@pytest.mark.usefixtures("client")
def test_login_incorrect_password(client):
    login_incorrect_password(client,'admin@gmail.com','admi')
    login_incorrect_password(client,'staff@gmail.com','staf')
    login_incorrect_password(client,'staff5@gmail.com','stafff5')
    login_incorrect_password(client,'admin@gmail.com','adminn')
    login_incorrect_password(client,'staff@gmail.com','staffff')
    login_incorrect_password(client,'staff5@gmail.com','staf5')


# @pytest.mark.usefixtures("client")
# def test_login_incorrect_password(client):
#     login_password_with_no_uppercase_letter(client,'thu@gmail.com','ssaf2@')
#     login_password_with_no_uppercase_letter(client,'thur@gmail.com','ssaf2@')

# @pytest.mark.usefixtures("client")
# def test_login_incorrect_password(client):
#     login_password_with_no_lowercase_letter(client,'thu@gmail.com','A2@')
#     login_password_with_no_lowercase_letter(client,'thur@gmail.com','AF2@')

# @pytest.mark.usefixtures("client")
# def test_login_incorrect_password(client):
#     login_password_with_no_number(client,'thu@gmail.com','Adfsdf@')
#     login_password_with_no_number(client,'thur@gmail.com','Afsdaf@')

# @pytest.mark.usefixtures("client")
# def test_login_incorrect_password(client):
#     login_password_with_no_character(client,'thu@gmail.com','Ad3fsdff')
#     login_password_with_no_character(client,'thur@gmail.com','Af3sdaff')





