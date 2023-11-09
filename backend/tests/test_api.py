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
    
    image_file = open("tests/test_images/ucsb_test.png", 'rb')

    response = client.post("/predict", files={"uploaded_file": ("ucsb_test.png", image_file, "image/jpeg")})
    print(response.json())
    image_file.close() 

    response_content = {"info": "file 'ucsb_test.png' saved at '/Users/parsahafezi/Workspace/DermaQ/Skin-Oracle/backend/images/ucsb_test.png'", "prediction": -1}
    assert response.status_code == 200
    assert response.json() == response_content





def test_invalid_image():
    image_file = open("tests/test_images/ucsb_test.heic", 'rb')

    response = client.post("/predict", files={"uploaded_file": ("ucsb_test.heic", image_file, "image/jpeg")})
    print(response.json())
    image_file.close() 

    response_content = {"detail": "Invalid photo format"}      
    assert response.json() == response_content
    assert response.status_code == 415