from tkinter import *
from pixivpy3 import *
import json
from PIL import Image, ImageTk
import requests
from io import BytesIO

aapi = AppPixivAPI()
papi = PixivAPI()
with open("user.json", "r") as user_file:
    custom = json.load(user_file)

def pixiv_login(aapi):
    aapi.login(custom["user"], custom["password"])

def fit_in_square(img, size):
    dominent_size_percent = (size/float(max(img.size[0], img.size[1])))
    dominated_size = int((float(min(img.size[0], img.size[1]))*float(dominent_size_percent)))
    if img.size[0] >= img.size[1]:
        return img.resize((size, dominated_size), Image.ANTIALIAS)
    else:
        return img.resize((dominated_size, size), Image.ANTIALIAS)

def expansion(img, size):
    dominent_size_percent = (size/float(min(img.size[0], img.size[1])))
    dominated_size = int((float(max(img.size[0], img.size[1]))*float(dominent_size_percent)))
    if img.size[0] < img.size[1]:
        return img.resize((size, dominated_size), Image.ANTIALIAS)
    else:
        return img.resize((dominated_size, size), Image.ANTIALIAS)

def url_to_image(url):
    referer='https://app-api.pixiv.net/'
    response = aapi.requests_call('GET', url, headers = {'Referer': referer}, stream=True)
    return Image.open(BytesIO(response.content))