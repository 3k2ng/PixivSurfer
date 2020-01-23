from tkinter import *
from pixivpy3 import *
import json
from PIL import Image, ImageTk
import requests
from io import BytesIO

import illust_panel
from ps_utils import *

aapi = AppPixivAPI()
papi = PixivAPI()
pixiv_login(aapi)
pixiv_login(papi)

class PixivUser:
    def __init__(self, id):
        self.id = id
        self.user_json = aapi.user_detail(id).user
        self.name = self.user_json.name
        self.profile_img = url_to_image(self.user_json.profile_image_urls.medium)
        self.following = self.user_json.is_followed
    
    def get_illust(self, page):
        return [illust_panel.PixivIllust(illust.id) for illust in papi.users_works(self.id, page, 3).response]
    
    def thumbnail_update(self):
        self.thumbnail_render = []
        for i in range(3):
            self.thumbnail_render.append(ImageTk.PhotoImage(fit_in_square(self.get_illust(self.current_page)[i].get_thumbnail(), 128)))
            self.thumbnails[i].configure(image = self.thumbnail_render[i])
    
    def access_illust(self, order):
        return lambda : self.get_illust(self.current_page)[order].get_panel().mainloop()
    
    def change_ac(self, inc):
        def change():
            if inc:
                self.current_page += 1
            else:
                if self.current_page > 1:
                    self.current_page -= 1
            self.thumbnail_update()
        return change

    def get_panel(self):
        self.root = Toplevel()
        self.current_page = 1
        self.root.title("User_" + str(self.id) + " named " + self.name)
        self.pf_render = ImageTk.PhotoImage(fit_in_square(self.profile_img, 128))

        self.thumbnails = []
        for i in range(3):
            self.thumbnails.append(Button(self.root, width = 128, height = 128, command = self.access_illust(i)))
        self.thumbnail_update()
        Label(self.root, text = self.name).pack(side = TOP)

        pfi = Label(self.root, image = self.pf_render)
        pfi.pack(side = LEFT)
        Button(self.root, text = "<", command = self.change_ac(False)).pack(side = LEFT)
        for i in range(3):
            self.thumbnails[i].pack(side = LEFT)
        Button(self.root, text = ">", command = self.change_ac(True)).pack(side = LEFT)
        return self.root