import os
import threading
import time

# Program requires Pillow, run `pip install Pillow` before running program
from PIL import Image
from PIL import ImageEnhance

sharedImages = []
sharedResourceBuffer = []
semaphoreBuffer = threading.Semaphore(0)

class producer (threading.Thread):
    def __init__(self, images):
        threading.Thread.__init__(self)
        self.images = images

    def run(self):
        global sharedResourceBuffer
        global semaphoreBuffer
        print('\nProducer is initializing.')
        for img in self.images:
            sharedResourceBuffer.append(img)
            semaphoreBuffer.release()
            print('Producer appended an image.')

class consumer (threading.Thread):
    def __init__(self, images, brightness, contrast, sharpness, threadId):
        threading.Thread.__init__(self)
            
        self.brightness = brightness
        self.contrast = contrast
        self.sharpness = sharpness
        self.id = threadId

        self.counter = int(len(images)/2)
        if len(images) % 2 == 1 and threadId == 0:
            self.counter = int(len(images)/2 + 1)

    def run(self):
        global sharedResourceBuffer
        global semaphoreBuffer
        print("Consumer %i is waiting \n"%(self.id))
        for i in range(self.counter):
            semaphoreBuffer.acquire() 
            if sharedResourceBuffer:
                origImg = sharedResourceBuffer.pop()
                finalImage = self.applyEffects(origImg[0])
                finalImage.save('enhanced/' + origImg[1])

    def applyEffects(self, image):    
        currBrightness = ImageEnhance.Brightness(image)
        currImage = currBrightness.enhance(self.brightness)
        currContrast = ImageEnhance.Contrast(currImage)
        currImage = currContrast.enhance(self.contrast)
        currSharpness = ImageEnhance.Sharpness(currImage)
        finalImage = currSharpness.enhance(self.sharpness)
        return finalImage

if __name__ == "__main__":
    # Start program
    print('Running Image Enhancer!')
    
    # Take inputs
    # folderImages    = input('Folder name of input images: ')
    # folderEnhanced  = input('Folder name of output images: ')

    bF = float(input('Brightness Factor: '))
    sF = float(input('Sharpess Factor: '))
    cF = float(input('Contrast Factor: '))

    # Load images
    path = './images'
    files = os.listdir(path)

    for imageName in files:
        img = Image.open(path + '/' + imageName)
        sharedImages.append([img, imageName])

    # Create threads
    producerThread = producer(sharedImages)
    consumerThread = consumer(sharedImages, bF, cF, sF, 1)
    consumerThread2 = consumer(sharedImages, bF, cF, sF, 2)

    startTime = time.time()

    producerThread.start()
    consumerThread.start()
    consumerThread2.start()

    producerThread.join()
    consumerThread.join()
    consumerThread2.join()

    # When finished running all processes
    print("--- %s seconds ---" % (time.time() - startTime))