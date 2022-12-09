from imutils.object_detection import non_max_suppression
from google.colab.patches import cv2_imshow
import numpy as np
import argparse
import time
import cv2
import PIL.Image
from tesserocr import PyTessBaseAPI, image_to_text


#toca tener instalado el tesseract con el modelo de ingles
api = PyTessBaseAPI(lang='eng', path='/usr/share/tesseract-ocr/5/tessdata')

image = cv2.imread("./Test-Image.png")

banned_words = ["hola","test","hound","hare", "lair", "goat" ] #poner todo en minusculas



def contains_substring(s, word):
    #print(s + " " + word)
    if word in s:
        return True
    else:
        return False







# image height and width should be multiple of 32
# toca revisar esto porque ahora mismo lo que hace es aplastar la imagen un poco, por eso los bounding boxes salen mal
imgWidth=1920
imgHeight=1056 #1080

orig = image.copy()
(H, W) = image.shape[:2]
(newW, newH) = (imgWidth, imgHeight)

rW = W / float(newW)
rH = H / float(newH)
image = cv2.resize(image, (newW, newH))

(H, W) = image.shape[:2]

     
net = cv2.dnn.readNet("frozen_east_text_detection.pb")

     
blob = cv2.dnn.blobFromImage(image, 1.0, (W, H), (123.68, 116.78, 103.94), swapRB=True, crop=False)
     

outputLayers = []
outputLayers.append("feature_fusion/Conv_7/Sigmoid")
outputLayers.append("feature_fusion/concat_3")


net.setInput(blob)
output = net.forward(outputLayers)

scores = output[0]
geometry = output[1]

(numRows, numCols) = scores.shape[2:4]
rects = []
confidences = []



for y in range(0, numRows):
    scoresData = scores[0, 0, y]
    xData0 = geometry[0, 0, y]
    xData1 = geometry[0, 1, y]
    xData2 = geometry[0, 2, y]
    xData3 = geometry[0, 3, y]
    anglesData = geometry[0, 4, y]

    for x in range(0, numCols):
        # if our score does not have sufficient probability, ignore it
        if scoresData[x] < 0.5:
            continue

        # compute the offset factor as our resulting feature maps will
        # be 4x smaller than the input image
        (offsetX, offsetY) = (x * 4.0, y * 4.0)

        # extract the rotation angle for the prediction and then
        # compute the sin and cosine
        angle = anglesData[x]
        cos = np.cos(angle)
        sin = np.sin(angle)

        # use the geometry volume to derive the width and height of
        # the bounding box
        h = xData0[x] + xData2[x]
        w = xData1[x] + xData3[x]

        # compute both the starting and ending (x, y)-coordinates for
        # the text prediction bounding box
        endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
        endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
        startX = int(endX - w)
        startY = int(endY - h)

        # add the bounding box coordinates and probability score to
        # our respective lists
        rects.append((startX, startY, endX, endY))
        confidences.append(scoresData[x])

# apply non-maxima suppression to suppress weak, overlapping bounding
boxes = non_max_suppression(np.array(rects), probs=confidences)






banned_boxes = []

# loop de bounding boxes


start = time.time()
for (startX, startY, endX, endY) in boxes:
    #Y = vertical, X = horizontal
    #expando un poco las bounding boxes para que no queden cortas
    
    endY+=10
    if endY > 1080: endY = 1080
    
    startX-=10
    if startX < 0: startX = 0
    
    crop_img = image[startY:(endY), startX:endX]
    
    api.SetImage(PIL.Image.fromarray(crop_img)) #toca cambiar el formato de la imagen
    
    word = api.GetUTF8Text()
    word = word.lower()
    word = word.strip()
    #print(word)
    for banned_word in banned_words:
        if contains_substring(word,banned_word):
            print("banned word : " + banned_word + " found.")
            banned_boxes.append((startX,startY,endX,endY))
            break
        
        
    #cv2.imwrite("tmp/" + word + ".png",crop_img) #para testear que lee las palabras bien
end = time.time()
print(end-start)

print(banned_boxes)


#guarda las imagenes borradas
#for (startX, startY, endX, endY) in banned_boxes:
    #crop_img = image[startY:endY, startX:endX]
    #cv2.imwrite("tmp/" + str(startX) + str(startY) + str(endX) + str(endY) + ".png",crop_img)
     
