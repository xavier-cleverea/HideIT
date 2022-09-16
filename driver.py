import cv2
import pytesseract

def load_img_rgb(path):
    return cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)

def load_img_data(img_rgb):
    return pytesseract.image_to_data(img_rgb)

def blur_img_bbox(img_rgb, bbox):
    pass

def paint_img_bbox(img_rgb, bbox, color):
    pass

def write_text_on_img(img_rgb, bbox, font, fontsize, color):
    pass

def save_img_rgb(img_rgb, name):
    pass





if __name__ == "__main__":
    img_rgb = 0
    img_data = 0
    while True:
        print(
"""Enter option:
    a <path>\tload an image
    b <text>\tblur text
    e <text>\terase text
    o <old text> <new text>\toverwrite text
    s <name>\tsave the image
    q\tquit""")
        inp = list(input().split())
        if inp[0] == 'a':
            img_rgb = load_img_rgb(inp[1])
            img_data = load_img_data(img_rgb)
            print(img_data)
        if inp[0] == 'q':
            break
            
# By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
# we need to convert from BGR to RGB format/mode:
    
# OR

#img_rgb = Image.frombytes('RGB', img_cv.shape[:2], img_cv, 'raw', 'BGR', 0, 0)
#print(pytesseract.image_to_string(img_rgb))
