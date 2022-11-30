import threading
import os
import time
from PIL import Image
from PIL import ImageEnhance

shared_image_buffer = []

def enhanceBrightness(bF):
    global shared_image_buffer
    imagesDone = 0 # Number of images it has processed
    currImage = 0 # Index of image about to be processed

    while(imagesDone != len(shared_image_buffer)):
        if shared_image_buffer[currImage][1].locked():
            currImage += 1
            currImage %= len(shared_image_buffer)
        else:
            shared_image_buffer[currImage][1].acquire()
            image = shared_image_buffer[currImage][0]
            finalImage = ImageEnhance.Brightness(image).enhance(bF)
            shared_image_buffer[currImage][0] = finalImage
            imagesDone += 1
            shared_image_buffer[currImage][1].release()

def enhanceSharpness(sF):
    global shared_image_buffer
    imagesDone = 0 # Number of images it has processed
    currImage = 0 # Index of image about to be processed

    while(imagesDone != len(shared_image_buffer)):
        if shared_image_buffer[currImage][1].locked():
            currImage += 1
            currImage %= len(shared_image_buffer)
        else:
            shared_image_buffer[currImage][1].acquire()
            image = shared_image_buffer[currImage][0]
            finalImage = ImageEnhance.Sharpness(image).enhance(sF)
            shared_image_buffer[currImage][0] = finalImage
            imagesDone += 1
            shared_image_buffer[currImage][1].release()

def enhanceContrast(sF):
    global shared_image_buffer
    imagesDone = 0 # Number of images it has processed
    currImage = 0 # Index of image about to be processed

    while(imagesDone != len(shared_image_buffer)):
        if shared_image_buffer[currImage][1].locked():
            currImage += 1
            currImage %= len(shared_image_buffer)
        else:
            shared_image_buffer[currImage][1].acquire()
            image = shared_image_buffer[currImage][0]
            finalImage = ImageEnhance.Contrast(image).enhance(cF)
            shared_image_buffer[currImage][0] = finalImage
            imagesDone += 1
            shared_image_buffer[currImage][1].release()

if __name__ == "__main__":

    # Load images onto array with semaphore and enhancement indicator
    path = 'many-images'
    endPath = 'enhanced/'

    path = input('Folder location of images: ')
    endPath = input('Folder location of enhanced images: ')
    files = os.listdir(path)

    for image in files:
        img = Image.open(path + '/' + image)
        shared_image_buffer.append([img, threading.Lock()])

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

