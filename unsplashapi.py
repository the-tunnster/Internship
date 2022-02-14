import clip
import torch
import urllib.request
import requests
import pandas as pd
import numpy as np

from pathlib import Path
from IPython.display import Image
from IPython.display import display
from IPython.core.display import HTML

def encode_search_query(search_query):
    with torch.no_grad():
        # Encode and normalize the search query using CLIP
        text_encoded = model.encode_text(
            clip.tokenize(search_query).to(device))
        text_encoded /= text_encoded.norm(dim=-1, keepdim=True)

    # Retrieve the feature vector
    return text_encoded

def find_best_matches(text_features,
                      photo_features,
                      photo_ids,
                      results_count=3):
    # Compute the similarity between the search query and each photo using the Cosine similarity
    similarities = (photo_features @ text_features.T).squeeze(1)

    # Sort the photos by their similarity score
    best_photo_idx = (-similarities).argsort()

    # Return the photo IDs of the best matches
    return [photo_ids[i] for i in best_photo_idx[:results_count]]

def display_photo(photo_id):
    # Get the URL of the photo resized to have a width of 320px
    photo_image_url = f"https://unsplash.com/photos/{photo_id}/download?w=320"

    # Display the photo
    display(Image(url=photo_image_url))

    # Display the attribution text
    display(HTML(f'Photo on <a target="_blank" href="https://unsplash.com/photos/{photo_id}">Unsplash</a> '))
    print()

def search_unslash(search_query, photo_features, photo_ids, results_count=3):
    
    # Encode the search query
    text_features = encode_search_query(search_query)

    # Find the best matches
    best_photo_ids = find_best_matches(text_features, photo_features,
                                       photo_ids, results_count)

    # Display the best photos
    for photo_id in best_photo_ids:
        display_photo(photo_id)

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def load_photo_ids(fileName):
    photo_ids = pd.read_csv("unsplash-dataset/photo_ids.csv")
    photo_ids = list(photo_ids['photo_id'])
    return(photo_ids)


photo_ids = pd.read_csv("unsplash-dataset/photo_ids.csv")
photo_ids = list(photo_ids['photo_id'])

# Load the features vectors
def load_photo_features(fileName):
    photo_features = np.load("unsplash-dataset/features.npy")
    return(photo_features)

photo_features = np.load("unsplash-dataset/features.npy")

# Convert features to Tensors: Float32 on CPU and Float16 on GPU
if device == "cpu":
    photo_features = torch.from_numpy(photo_features).float().to(device)
else:
    photo_features = torch.from_numpy(photo_features).to(device)

# Print some statistics
print(f"Photos loaded: {len(photo_ids)}")

search_query = "what camera should i buy for youtube"

search_unslash(search_query, photo_features, photo_ids, 3)