from genericpath import isfile
import io, os, base64
from PIL import Image
from typing import List
from .get_songs import get_song


from fastapi import FastAPI, UploadFile, File, Response, HTTPException, status
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
async def make_recommedation(files: UploadFile= File(...)):
    
    
    if files.content_type != 'image/jpeg':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No image uploaded please upload a jpg image")

    file_path = f"datasets/test/{files.filename}"
    outcome = {"results":None}
    
    with open(file_path, 'wb+') as imfile:
        imfile.write(files.file.read())
        imfile.close()

    try:
        outcome = get_song()       
        if os.path.isfile(outcome['image']):
            Image.open(outcome['image']).show('detected image')
        outcome["image"] = "image displayed"
        
    except Exception as error:
        print(error.args)

    finally:
        if os.path.isfile(f"datasets/test/{files.filename}"):
            os.remove(f"datasets/test/{files.filename}")
        if os.path.isfile(f"trainer/outcome/test/{files.filename.replace('.jpg', '.png')}"):
            os.remove(f"trainer/outcome/test/{files.filename.replace('.jpg', '.png')}")
    return outcome