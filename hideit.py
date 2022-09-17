from driver import *

class ImageProcessor:

    def __init__(self, name, path=""):
        self.name = name
        self.img_rgb = load_img_rgb(path+name)
        self.data = load_img_data(self.img_rgb)

    def blur_all_text(self):
        for word in self.data:
            blur_img_bbox(self.img_rgb,word['bbox'])

    def blur_if_regex(self,regex):
        pass

    def blur_if_contains(self,text):
        for word in self.data:
            if text in word['text']:
                bbox = word['bbox']
                s = word['text'].find(text)
                e = s+len(text)
                l = len(word['text'])
                if e-s != l:
                    print((bbox[0][0]),bbox[3][0])
                    jump = (int)((bbox[1][0]-bbox[0][0])/l)
                    print(jump)
                    bbox[0][0] = bbox[0][0]+jump*s
                    bbox[2][0] = bbox[0][0]
                    bbox[1][0] = bbox[1][0]-jump*(l-e)
                    bbox[3][0] = bbox[1][0]
                    print((bbox[0][0]),bbox[3][0])
                blur_img_bbox(self.img_rgb,bbox)

    def save(self):
        save_img_rgb(self.img_rgb, self.name)
