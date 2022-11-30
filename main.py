import os
import threading
import time

# Program requires Pillow, run `pip install Pillow` before running program
from PIL import Image
from PIL import ImageEnhance

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

        self.counter = int(len(images)/numConsumerThreads)
        if len(images) % 2 == 1 and threadId == 0:
            self.counter = int(len(images)/numConsumerThreads + 1)

    def run(self):
        global sharedResourceBuffer
        global semaphoreBuffer
        print("Consumer %i is waiting \n"%(self.id))
        for i in range(self.counter):
            semaphoreBuffer.acquire() 
            if sharedResourceBuffer:
                origImg = sharedResourceBuffer.pop()
                finalImage = self.applyEffects(origImg[0])
                finalImage.save(destinationPath + origImg[1])

    def applyEffects(self, image):    
        currBrightness = ImageEnhance.Brightness(image)
        currImage = currBrightness.enhance(self.brightness)
        currContrast = ImageEnhance.Contrast(currImage)
        currImage = currContrast.enhance(self.contrast)
        currSharpness = ImageEnhance.Sharpness(currImage)
        finalImage = currSharpness.enhance(self.sharpness)
        return finalImage

sharedImages = []
sharedResourceBuffer = []
semaphoreBuffer = threading.Semaphore(0)
consumerThreadList = []

numConsumerThreads = 2

sourcePath = './images'
destinationPath = './enhanced/'

if __name__ == "__main__":
    # Start program
    print('Running Image Enhancer!')
    
    # Take inputs
    sourcePath    = input('Folder name of input images (Leave blank for `images`): ')
    destinationPath  = input('Folder name of output images (Leave blank for `enhanced`): ')

    # Load images
    files = os.listdir(sourcePath)

    for imageName in files:
        img = Image.open(sourcePath + '/' + imageName)
        sharedImages.append([img, imageName])

    bF = float(input('Brightness Factor: '))
    sF = float(input('Sharpess Factor: '))
    cF = float(input('Contrast Factor: '))

    # Create and run threads
    startTime = time.time()

    producerThread = producer(sharedImages)
    producerThread.start()

    for i in range(numConsumerThreads):
        consumerThread = consumer(sharedImages, bF, cF, sF, i)
        consumerThreadList.append(consumerThread)
        consumerThread.start()

    producerThread.join()

    for consThread in consumerThreadList:
        consThread.join()

    # When finished running all processes
    print("--- %s seconds ---" % (time.time() - startTime))