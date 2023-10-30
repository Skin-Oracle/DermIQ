from fastapi.testclient import TestClient
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

import os
import sys

working_dir = os.getcwd()

sys.path.append("/Users/parsahafezi/Workspace/DermaQ/Skin-Oracle/backend")

from  main import app


client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_valid_image():
    file_location = f"{working_dir}/test_images/ucsb_test.png"
    print(file_location)
    with open(file_location, "rb") as image_file:
        response = client.post("/predict", files={'file': image_file})

    # assert response.status_code == 200
    response_content = {"info": f"file 'ucsb_test.png' saved at '{file_location}'", "prediction": -1}
    assert response.json() == JSONResponse(content=response_content)

def test_invalid_image():
    file_location = f"{working_dir}/test_images/ucsb_test.heic"
    with open(file_location, "rb") as image_file:
        response = client.post("/predict", files={'file': ('ucsb_test.heic', image_file)})

    response_content = {"Invalid photo format"}    
    assert response.json() == JSONResponse(content=response_content)
    assert response.status_code == 415