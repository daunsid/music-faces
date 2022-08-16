from typing import List
from logging import exception
from .get_songs import get_song
import io
from PIL import Image

from fastapi import FastAPI, UploadFile, File, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse, StreamingResponse
from fastapi.responses import FileResponse



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

@app.post("/recommend", response_class=Response)
async def create_upload_file(files: List[UploadFile] = File(...)):
    file_location = [f"datasets/test/{fn.filename}" for fn in files]
    list(map(lambda x,y: open(x, 'wb+').write(y.file.read()), file_location, files))
    results = get_song()
    results['confidence(%)'] = str(results['confidence(%)'])
    results['music_id'] = str(results['music_id'])

    img = Image.open(results['image'])
    bytes_image = io.BytesIO()
    img.save(bytes_image, format='PNG')

    bytes_image.seek(0)
    return StreamingResponse(bytes_image, headers=results, media_type="image/png")


