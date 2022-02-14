from typing import Optional
from fastapi import FastAPI
from IPython.display import Image
from IPython.display import display
from fastapi.responses import FileResponse

import unsplashapi
import requests
import urllib.request
import numpy as np

import clip
import torch
import pandas as pd
from pathlib import Path
from IPython.display import Image
from IPython.display import display
from IPython.core.display import HTML

app = FastAPI()

@app.get("/")
def read_root():

    photo_image_url_1 = "https://unsplash.com/photos/"
    photo_image_url_2 = "/download?ixid=MnwxMjA3fDB8MXxhbGx8fHx8fHx8fHwxNjQ0ODE4NTk4&force=true"

    search_query = "what camera should i buy for youtube"
    text_features = unsplashapi.encode_search_query(search_query)

    photo_features = unsplashapi.load_photo_features("unsplash-dataset/features.npy")

    photo_ids = unsplashapi.load_photo_ids("unsplash-dataset/photo_ids.csv")

    best_photo_ids = unsplashapi.find_best_matches(text_features, photo_features,
                                       photo_ids, 3)

    for photo_id in best_photo_ids:
        r = requests.get(photo_image_url_1 + photo_id + photo_image_url_2, allow_redirects=True)
        open(photo_id+".jpeg", 'wb').write(r.content)

    return FileResponse(photo_id+".jpeg")

