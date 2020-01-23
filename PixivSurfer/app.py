from tkinter import *
from pixivpy3 import *
import json
from PIL import Image, ImageTk
import requests
from io import BytesIO

from illust_panel import PixivIllust
from user_panel import PixivUser
from ps_utils import *

aapi = AppPixivAPI()
papi = PixivAPI()
pixiv_login(aapi)
pixiv_login(papi)

with open("listed_user.json", "r") as users_file:
    users = json.load(users_file)
    GUI = Tk()

    GUI.title("Pixiv Surfer")
    def get_user(i):
        return lambda: PixivUser(users[i]["id"]).get_panel().mainloop()
    for i in range(len(users)):
        Button(GUI, text = users[i]["name"], command = get_user(i)).pack()
    GUI.mainloop()

