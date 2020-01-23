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

root = Tk()

root.title("Pixiv Surfer")

logo = Image.open("pixiv_logo.png")

root.render = ImageTk.PhotoImage(fit_in_square(logo, 640))
pic = Label(root, image = root.render)
status = Label(root, text = "None loaded")
user = Label(root, text = "N/A")
root.can_download = False
root.illust = None


def click():
    try:
        id = int(illust_id.get())
        root.illust = PixivIllust(id)
        illust = root.illust.get_images()[0]
        root.render = ImageTk.PhotoImage(fit_in_square(illust,640))
        pic.configure(image = root.render)
        status.configure(text = "Success")
        root.can_download = True
        user.configure(text = root.illust.user.name)
        download.configure(text = "Download")
    except:
        status.configure(text = "Invalid ID")
        user.configure(text = "N/A")
        download.configure(text = "N/A")
        root.can_download = False

def down():
    if root.can_download:
        try:
            aapi.download(root.illust.url)
            status.configure(text = "Downloaded")
        except:
            root.can_download = False
            download.configure(text = "N/A")
    
download = Button(root, text = "N/A", command = down)
illust_id_label = Label(root, text = "Illust ID")
illust_id = Entry(root)
illust_id_submit = Button(root, text = "Submit ID", command = click)


status.pack(side = BOTTOM)
pic.pack(side = BOTTOM)

download.pack(side = RIGHT)
user.pack(side = RIGHT)

illust_id_label.pack(side = LEFT)
illust_id.pack(side = LEFT)
illust_id_submit.pack(side = LEFT)

root.mainloop()