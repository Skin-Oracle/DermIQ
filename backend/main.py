from fastapi import FastAPI, File, UploadFile, HTTPException
import os

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

    #todo pass the location of the file to image processing pipeline and get valid prediction

    return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'", "prediction": -1}