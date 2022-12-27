import sys
import pytest
sys.path.append('./')
import db 

@pytest.fixture  #TESTING INTIALIZER
def client():
    SERVER = db.app
    with SERVER.test_client() as client:
        yield client
