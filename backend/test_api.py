from fastapi.testclient import File, TestClient
import os

working_dir = os.getcwd()

from .main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

def test_valid_image():
    response = client.post("/prediction")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

def test_invalid_image():
    file_location = f"{working_dir}/test_images/ucsb_test.heic"
    with open(file_location, "rb") as file:
        response = client.post("/uploadfile/", file={"file": (file_location, file, "text/plain")})
    assert response.status_code == 200
    assert response.json() == {"filename": "testfile.txt"}