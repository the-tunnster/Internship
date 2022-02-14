from typing import Optional
from fastapi import FastAPI
from IPython.display import Image
from IPython.display import display
from fastapi.responses import FileResponse

import unsplashapi
import requests
import urllib.request
import numpy as np

app = FastAPI()

@app.get("/")
def read_root():

    best_photo_ids = unsplashapi.doStuff()

    photo_image_url_1 = "https://unsplash.com/photos/"
    photo_image_url_2 = "/download?ixid=MnwxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNjQ0ODE4NTk4&force=true"

    for photo_id in best_photo_ids:
        r = requests.get(photo_image_url_1 + photo_id + photo_image_url_2, allow_redirects=True)
        open(photo_id+".jpeg", 'wb').write(r.content)

    return FileResponse(photo_id+".jpeg")

