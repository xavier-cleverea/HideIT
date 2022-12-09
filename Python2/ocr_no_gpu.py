from imutils.object_detection import non_max_suppression
from google.colab.patches import cv2_imshow
import numpy as np
import argparse
import time
import cv2
import PIL.Image

path_rec = "./Resources/Test-Image.png"
path_out = "./out/test_output2.png"

def ocr(path_rec, path_out):

    image = cv2.imread(path_rec)

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

    cv2_imshow(image)
        
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H), (123.68, 116.78, 103.94), swapRB=True, crop=False)
        

    outputLayers = []
    outputLayers.append("feature_fusion/Conv_7/Sigmoid")
    outputLayers.append("feature_fusion/concat_3")

    for i in range(0,10):
        start = time.time()
        net.setInput(blob)
        output = net.forward(outputLayers)
        end = time.time()
        print("time:" + str(end-start))

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
            if scoresData[x] < 0.5:
                continue

            (offsetX, offsetY) = (x * 4.0, y * 4.0)


            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)


            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]


            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)


            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])


    boxes = non_max_suppression(np.array(rects), probs=confidences)

    for (startX, startY, endX, endY) in boxes:
        
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)

        cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

    cv2.imwrite(path_out,orig)
