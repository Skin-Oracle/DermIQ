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

model_path = "trained_model.pt"


class Derm_Vision:
    def __init__(self):
        self.model = torch.load(model_path, map_location=torch.device('cpu'))
        self.transform_m = t.Compose([
            t.Resize(384, interpolation=t.InterpolationMode.BILINEAR),
            t.CenterCrop(384),
            t.ToTensor(),
            t.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
         ])

        self.model_class_data = {0: 'acanthosis nigricans',
                            1: 'acne',
                            2: 'acne vulgaris',
                            3: 'acquired autoimmune bullous diseaseherpes gestationis',
                            4: 'acrodermatitis enteropathica',
                            5: 'actinic keratosis',
                            6: 'allergic contact dermatitis',
                            7: 'aplasia cutis',
                            8: 'basal cell carcinoma',
                            9: 'basal cell carcinoma morpheiform',
                            10: 'becker nevus',
                            11: 'behcets disease',
                            12: 'calcinosis cutis',
                            13: 'cheilitis',
                            14: 'congenital nevus',
                            15: 'dariers disease',
                            16: 'dermatofibroma',
                            17: 'dermatomyositis',
                            18: 'disseminated actinic porokeratosis',
                            19: 'drug eruption',
                            20: 'drug induced pigmentary changes',
                            21: 'dyshidrotic eczema',
                            22: 'eczema',
                            23: 'ehlers danlos syndrome',
                            24: 'epidermal nevus',
                            25: 'epidermolysis bullosa',
                            26: 'erythema annulare centrifigum',
                            27: 'erythema elevatum diutinum',
                            28: 'erythema multiforme',
                            29: 'erythema nodosum',
                            30: 'factitial dermatitis',
                            31: 'fixed eruptions',
                            32: 'folliculitis',
                            33: 'fordyce spots',
                            34: 'granuloma annulare',
                            35: 'granuloma pyogenic',
                            36: 'hailey hailey disease',
                            37: 'halo nevus',
                            38: 'hidradenitis',
                            39: 'ichthyosis vulgaris',
                            40: 'incontinentia pigmenti',
                            41: 'juvenile xanthogranuloma',
                            42: 'kaposi sarcoma',
                            43: 'keloid',
                            44: 'keratosis pilaris',
                            45: 'langerhans cell histiocytosis',
                            46: 'lentigo maligna',
                            47: 'lichen amyloidosis',
                            48: 'lichen planus',
                            49: 'lichen simplex',
                            50: 'livedo reticularis',
                            51: 'lupus erythematosus',
                            52: 'lupus subacute',
                            53: 'lyme disease',
                            54: 'lymphangioma',
                            55: 'malignant melanoma',
                            56: 'melanoma',
                            57: 'milia',
                            58: 'mucinosis',
                            59: 'mucous cyst',
                            60: 'mycosis fungoides',
                            61: 'myiasis',
                            62: 'naevus comedonicus',
                            63: 'necrobiosis lipoidica',
                            64: 'nematode infection',
                            65: 'neurodermatitis',
                            66: 'neurofibromatosis',
                            67: 'neurotic excoriations',
                            68: 'neutrophilic dermatoses',
                            69: 'nevocytic nevus',
                            70: 'nevus sebaceous of jadassohn',
                            71: 'papilomatosis confluentes and reticulate',
                            72: 'paronychia',
                            73: 'pediculosis lids',
                            74: 'perioral dermatitis',
                            75: 'photodermatoses',
                            76: 'pilar cyst',
                            77: 'pilomatricoma',
                            78: 'pityriasis lichenoides chronica',
                            79: 'pityriasis rosea',
                            80: 'pityriasis rubra pilaris',
                            81: 'porokeratosis actinic',
                            82: 'porokeratosis of mibelli',
                            83: 'porphyria',
                            84: 'port wine stain',
                            85: 'prurigo nodularis',
                            86: 'psoriasis',
                            87: 'pustular psoriasis',
                            88: 'pyogenic granuloma',
                            89: 'rhinophyma',
                            90: 'rosacea',
                            91: 'sarcoidosis',
                            92: 'scabies',
                            93: 'scleroderma',
                            94: 'scleromyxedema',
                            95: 'seborrheic dermatitis',
                            96: 'seborrheic keratosis',
                            97: 'solid cystic basal cell carcinoma',
                            98: 'squamous cell carcinoma',
                            99: 'stasis edema',
                            100: 'stevens johnson syndrome',
                            101: 'striae',
                            102: 'sun damaged skin',
                            103: 'superficial spreading melanoma ssm',
                            104: 'syringoma',
                            105: 'telangiectases',
                            106: 'tick bite',
                            107: 'tuberous sclerosis',
                            108: 'tungiasis',
                            109: 'urticaria',
                            110: 'urticaria pigmentosa',
                            111: 'vitiligo',
                            112: 'xanthomas',
                            113: 'xeroderma pigmentosum'}        

    def predict(self, image_path):
        img = Image.open(image_path).convert('RGB')  
        trans_img = self.transform_m (img)
        trans_img = trans_img.unsqueeze(0)
        outputs = self.model(trans_img)
        _, predicted = torch.max(outputs, 1)
        return self.model_class_data[predicted.item()] 
    
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




