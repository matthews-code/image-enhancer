import threading
import os
from PIL import Image
from PIL import ImageEnhance

import time

shared_image_buffer = []

# Load images onto array with semaphore and enhancement indicator
path = './images'
files = os.listdir(path)

for image in files:
    img = Image.open(path + '/' + image)
    shared_image_buffer.append([img, threading.Lock(), 0, 0, 0])

def enhanceBrightness(bF):
    global shared_image_buffer

    for i in range(len(shared_image_buffer)):
        shared_image_buffer[i][1].acquire()

        image = shared_image_buffer[i][0]

        finalImage = ImageEnhance.Brightness(image).enhance(bF)
        shared_image_buffer[i][0] = finalImage

        shared_image_buffer[i][1].release()

def enhanceSharpness(sF):
    global shared_image_buffer

    for i in range(len(shared_image_buffer)):
        shared_image_buffer[i][1].acquire()

        image = shared_image_buffer[i][0]

        finalImage = ImageEnhance.Sharpness(image).enhance(sF)
        shared_image_buffer[i][0] = finalImage

        shared_image_buffer[i][1].release()

def enhanceContrast(sF):
    global shared_image_buffer

    for i in range(len(shared_image_buffer)):
        shared_image_buffer[i][1].acquire()

        image = shared_image_buffer[i][0]

        finalImage = ImageEnhance.Contrast(image).enhance(sF)
        shared_image_buffer[i][0] = finalImage

        finalImage.save('enhanced/' + str(i) + '.png')
        shared_image_buffer[i][1].release()

if __name__ == "__main__":
    bF = float(input('Brightness Factor: '))
    sF = float(input('Sharpess Factor: '))
    cF = float(input('Contrast Factor: '))

    bT = threading.Thread(target=enhanceBrightness, args=(bF,))
    sT = threading.Thread(target=enhanceSharpness, args=(sF,))
    cT = threading.Thread(target=enhanceContrast, args=(cF,))
    
    startTime = time.time()

    bT.start()
    sT.start()
    cT.start()

    bT.join()
    sT.join()
    cT.join()

    print("--- %s seconds ---" % (time.time() - startTime))