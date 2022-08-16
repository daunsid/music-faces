from logging import exception
from fastapi import FastAPI, UploadFile, File
from .get_songs import get_song
#import trainer.detect as detect




app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(files: UploadFile = File(...)):
    file_location = f"datasets/test/{files.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(files.file.read())
    return {"info": f"file '{files.filename}' saved at '{file_location}'"}

#results = detect.detect()
#print(results)

results = get_song()

@app.get('/')
async def get_results():
    return {'results':results}
