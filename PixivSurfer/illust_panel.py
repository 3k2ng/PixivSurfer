from tkinter import *
from pixivpy3 import *
import json
from PIL import Image, ImageTk
import requests
from io import BytesIO

import user_panel
from ps_utils import *

with open("user.json", "r") as user_file:
    custom = json.load(user_file)

aapi = AppPixivAPI()
papi = PixivAPI()
pixiv_login(aapi)
pixiv_login(papi)

class PixivIllust:
    def __init__(self, id):
        self.id = id
        self.illust_json = aapi.illust_detail(id).illust
        self.user = user_panel.PixivUser(self.illust_json.user.id)
        self.length = self.illust_json.page_count
        if self.length == 1:
            self.urls = [self.illust_json.meta_single_page.original_image_url]
        else:
            meta = self.illust_json.meta_pages
            self.urls = [meta[i].image_urls.original for i in range(self.length)]
        
        self.size = (self.illust_json.width, self.illust_json.height)

        self.thumbnail_url = self.illust_json.image_urls.medium
        self.pic_size = 512

    def get_images(self):
        return [url_to_image(url) for url in self.urls]

    def get_image(self, page):
        return url_to_image(self.urls[page])
    
    def get_thumbnail(self):
        return url_to_image(self.thumbnail_url)

    def download_illust(self):
        for url in self.urls:
            aapi.download(url, path = custom["path"])
    
    def reload_pic(self):
        img = self.get_image(self.current_page)
        self.render = ImageTk.PhotoImage(expansion(img, self.pic_size))
        self.pic.configure(image = self.render)
        self.page.configure(text =  "Current page: " + str(self.current_page))

    def change_page(self):
        if self.length > 1:
            if self.current_page + 1 < self.length:
                self.current_page += 1
            else:
                self.current_page = 0
            self.reload_pic()
    
    def load_user(self):
        root = self.user.get_panel()
        root.mainloop()
    
    def get_panel(self):
        self.root = Toplevel()
        self.root.title("ID_" + str(self.id) + " by " + self.user.name)
        self.current_page = 0
        self.ava_render = ImageTk.PhotoImage(fit_in_square(self.user.profile_img, 32))
        user_ava = Button(self.root, image = self.ava_render, command = self.load_user)
        user = Label(self.root, text = self.user.name)
        download = Button(self.root, text = "Download", command = self.download_illust)

        self.page = Button(self.root, command = self.change_page)

        self.pic = Label(self.root)

        self.reload_pic()

        self.pic.pack(side = BOTTOM)
        user_ava.pack(side = LEFT)
        user.pack(side = LEFT)
        download.pack(side = RIGHT)
        self.page.pack(side = RIGHT)

        return self.root
