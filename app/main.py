from genericpath import isfile
import io, os, base64
from PIL import Image
from typing import List
from .get_songs import get_song


from fastapi import FastAPI, UploadFile, File, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def welcome():

    content="""</br><b>Let's recommend some songs to you but first of all let decide what your mood is</b>"""
    return {'response':'Hi! Welcome to my API'+content}

@app.post("/recommend", response_class=ORJSONResponse)
async def create_upload_file(files: UploadFile= File(...)):

    file_path = f"datasets/test/{files.filename}"
    outcome = {"results":None}
    
    with open(file_path, 'wb+') as imfile:
        imfile.write(files.file.read())
        imfile.close()
    try:
        outcome = get_song()       
        if os.path.isfile(outcome['image']):
            print(Image.open(outcome['image']))
        outcome["image"] = "image displayed"
        
    except Exception as e:
        error = e.args
        print(error)
    
    finally:
        if os.path.isfile(f"datasets/test/{files.filename}") or os.path.isfile(f"outcome/test/{files.filename}"):
            os.remove(f"datasets/test/{files.filename}")
            os.remove(f"trainer/outcome/test/{files.filename.replace('.jpg', '.png')}")
    return outcome


