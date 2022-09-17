import cv2
import pytesseract
from pytesseract import Output

def load_img_rgb(path):
    return cv2.imread(path)
    return cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)

def load_img_data(img_rgb):
    data = pytesseract.image_to_data(img_rgb,output_type=Output.DICT)
    
    n = len(data['level'])
    l = []
    for i in range(n):
        if data['conf'][i] > 0:
            word = {
                'text': data['text'][i],
                'page': data['page_num'][i],
                'block': data['block_num'][i],
                'par': data['par_num'][i],
                'line': data['line_num'][i],
                'word': data['word_num'][i],
                'bbox': (
                    [data['left'][i],data['top'][i]],
                    [data['left'][i]+data['width'][i],data['top'][i]],
                    [data['left'][i],data['top'][i]+data['height'][i]],
                    [data['left'][i]+data['width'][i],data['top'][i]+data['height'][i]]
                )
            }
            l.append(word)
    return l

def blur_img_bbox(img_rgb, bbox):
    crop = img_rgb[bbox[0][1]:bbox[3][1],bbox[0][0]:bbox[3][0]]
    crop = cv2.blur(crop,(10,10))
    img_rgb[bbox[0][1]:bbox[3][1],bbox[0][0]:bbox[3][0]]=crop
    return img_rgb

# bbox = {tl - tr - bl - br}
def paint_img_bbox(img_rgb, bbox, color):
    return cv2.rectangle(img_rgb,bbox[0],bbox[3],color,1)

def write_text_on_img(img_rgb, bbox, font, fontsize, color):
    pass

def save_img_rgb(img_rgb, name):
    cv2.imwrite(name,img_rgb)


if __name__ == "__main__":
    img_rgb = 0
    img_data = 0
    while True:
        print(
"""Enter option:
    a <path>\tload an image
    b <text>\tblur text
    e <text>\terase text
    m\tmark elements found
    o <old text> <new text>\toverwrite text
    p\tshow image
    s <name>\tsave the image
    q\tquit""")
        inp = list(input().split())
        if inp[0] == 'a':
            img_rgb = load_img_rgb(inp[1])
            img_data = load_img_data(img_rgb)
            print(img_data)
        elif inp[0] == 'b':
            for word in img_data:
                if inp[1] in word['text']:
                    print(word['text'])
                    blur_img_bbox(img_rgb,word['bbox'])
        elif inp[0] == 'm':
            for word in img_data:
                paint_img_bbox(img_rgb,word['bbox'],(0,0,255))
        elif inp[0] == 'p':
            cv2.imshow(r'Image',img_rgb)
            cv2.waitKey(0)
        elif inp[0] == 'q':
            break
        elif inp[0] == 's':
            save_img_rgb(img_rgb,inp[1])
# By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
# we need to convert from BGR to RGB format/mode:
    
# OR

#img_rgb = Image.frombytes('RGB', img_cv.shape[:2], img_cv, 'raw', 'BGR', 0, 0)
#print(pytesseract.image_to_string(img_rgb))
