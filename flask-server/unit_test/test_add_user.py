import json
import pytest
import logging as log
from db import user

user_collection = user

def add(client, cred_json):
    return client.post('/addstaff', json=cred_json, follow_redirects=False)

def successful_add_staff(client, email, password):
    cred_obj = {"email": email, "password": password}
    cred_json = cred_obj
    response = add(client, cred_json)
    data = json.loads(response.data)
    assert data["status_code"] == 200
    assert 'Staff member added successfully' in data.values()
    user_collection.delete_one({"username":email})

def already_exist(client, email, password):
    cred_obj = {"email": email, "password": password}
    cred_json = cred_obj
    response = add(client, cred_json)
    data = json.loads(response.data)
    assert data["status_code"] == 401
    assert 'User already exists...' in data.values()

def add_incomplete(client, email):
    cred_obj = {"email": email, "password": None}
    cred_json = cred_obj
    response = add(client, cred_json)
    data = json.loads(response.data)
    assert data["status_code"] == 400
    assert 'All fields are required for Adding a User' in data.values()

@pytest.mark.usefixtures("client")
def test_add_staff(client):
    successful_add_staff(client,'staff14@gmail.com','staff14')
    successful_add_staff(client,'staff15@gmail.com','staff15')
    successful_add_staff(client,'staff16@gmail.com','staff16')
    
@pytest.mark.usefixtures("client")
def test_incomplete_add_staff(client):
    add_incomplete(client,'staff17@gmail.com')
    add_incomplete(client,'staff18@gmail.com')
    add_incomplete(client,'staff19@gmail.com')

@pytest.mark.usefixtures("client")
def test_user_exist(client):
    already_exist(client,'admin@gmail.com','admin')
    already_exist(client,'staff@gmail.com','staff')
    already_exist(client,'staff5@gmail.com','staff5')