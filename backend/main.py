from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

import torch
import torchvision
import torchvision.transforms as t
from PIL import Image

import logging
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError

import os, sys

model_path = "best_model.pt"

class Derm_Vision:
    def __init__(self):
        self.model = torch.load(model_path, map_location=torch.device('cpu'))
        self.transform_m = t.Compose([
            t.Resize(384, interpolation=t.InterpolationMode.BILINEAR),
            t.CenterCrop(384),
            t.ToTensor(),
            t.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
         ])


        self.model_class_data = {0: 'akiec',
                            1: 'bcc',
                            2: 'benign',
                            3: 'bkl',
                            4: 'df',
                            5: 'mel',
                            6: 'nv',
                            7: 'other',
                            8: 'vasc',
        }       

    def predict(self, image_path):
        img = Image.open(image_path).convert('RGB')  
        trans_img = self.transform_m (img)
        trans_img = trans_img.unsqueeze(0)
        outputs = self.model(trans_img)
        _, predicted = torch.max(outputs, 1)
        diagnosis = self.model_class_data[predicted.item()]

        probs = torch.nn.functional.softmax(outputs, dim=1).tolist()[0]
        
        Confidence = {"akiec" : probs[0], 
                      "bcc": probs[1], 
                      'benign': probs[2], 
                      'bkl': probs[3], 
                      'df': probs[4], 
                      'mel': probs[5],  
                      'nv': probs[6],  
                      'other': probs[7],  
                      'vasc': probs[8], }

        result = {'Diagnosis': diagnosis, 'Confidence': Confidence}


        return result
    
app = FastAPI()
model = Derm_Vision()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	logging.error(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


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

    prediction = model.predict(file_location)
    response_content = {"Diagnosis" : prediction}
    
    return  JSONResponse(content = response_content)
    #return JSONResponse(content=response_content)




