from driver import *

import re

class ImageProcessor:
    
    def __get_substring_bbox__(self,bbox,l_str,s_str):
        new_bbox = bbox
        start = l_str.find(s_str)
        end = start+len(s_str)
        lenght = len(l_str)
        if end-start != lenght:
            offset = (int)((bbox[1][0]-bbox[0][0])/lenght)
            new_bbox[0][0] = bbox[0][0]+offset*start
            new_bbox[2][0] = new_bbox[0][0]
            new_bbox[1][0] = bbox[1][0]-offset*(lenght-end)
            new_bbox[3][0] = new_bbox[1][0]
        return new_bbox

    def __init__(self, name, path=""):
        self.name = name
        self.img_rgb = load_img_rgb(path+name)
        self.data = load_img_data(self.img_rgb)

    def blur_all_text(self):
        for word in self.data:
            blur_img_bbox(self.img_rgb,word['bbox'])

    def blur_if_regex(self,regex):
        program = re.compile(regex)
        for word in self.data:
            l_text = program.findall(word['text'])
            if len(l_text)>0:
                for text in l_text:
                    bbox = self.__get_substring_bbox__(word['bbox'],word['text'],text)
                    blur_img_bbox(self.img_rgb,bbox)



    def blur_if_contains(self,text):
        for word in self.data:
            if text in word['text']:
                bbox = self.__get_substring_bbox__(word['bbox'],word['text'],text)
                blur_img_bbox(self.img_rgb,bbox)

    def save(self,path):
        save_img_rgb(self.img_rgb, path+self.name)
