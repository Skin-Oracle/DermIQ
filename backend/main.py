from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse


import logging
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	logging.error(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

import os, sys

sys.path.append("/Users/parsahafezi/Workspace/DermaQ/Skin-Oracle/backend")
# make a directory to store images
working_dir = os.getcwd()
image_dir = f"{working_dir}/images"
if not os.path.exists(image_dir):
    os.makedirs(image_dir)


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/predict")
async def create_upload_file(uploaded_file: UploadFile = File(...)):
    
    #validates file extension
    if(not uploaded_file.filename.lower().endswith(('.png', '.jpg', '.jpeg'))):
        raise HTTPException(status_code=415, detail="Invalid photo format")
    
    #stores the files in imagedir
    file_location = os.path.join(image_dir, uploaded_file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())

    print(uploaded_file.filename)
    #todo pass the location of the file to image processing pipeline and get valid prediction
    response_content = {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'", "prediction": -1}
    
    return response_content
    #return JSONResponse(content=response_content)