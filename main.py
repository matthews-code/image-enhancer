import os
import threading
import time

# Program requires Pillow, run `pip install Pillow` before running program
from PIL import Image
from PIL import ImageEnhance

class producer (threading.Thread):
    def __init__(self, images, threadId):
        threading.Thread.__init__(self)
        self.images = images
        self.id = threadId

        self.counter = int(len(images)/numProducerThreads)
        if len(images) % 2 == 1 and threadId == 0 and not numProducerThreads == 1:
            self.counter = int(len(images)/numProducerThreads + 1)

    def run(self):
        global sharedResourceBuffer
        global semaphoreBuffer
        print("Producer %i has %i counts."%(self.id, self.counter))
        i = self.id * self.counter

        # 0 and 1
        # range 0, 4 
        # range 3, 6
        for i in range(self.id * self.counter, (self.id * self.counter) + self.counter):
            sharedResourceBuffer.append(self.images[i])
            semaphoreBuffer.release()

class consumer (threading.Thread):
    def __init__(self, images, brightness, contrast, sharpness, threadId):
        threading.Thread.__init__(self)
            
        self.brightness = brightness
        self.contrast = contrast
        self.sharpness = sharpness
        self.id = threadId

        self.counter = int(len(images)/numConsumerThreads)
        if len(images) % 2 == 1 and threadId == 0 and not numConsumerThreads == 1:
            self.counter = int(len(images)/numConsumerThreads + 1)

    def run(self):
        global sharedResourceBuffer
        global semaphoreBuffer
        print("Consumer %i has %i counts."%(self.id, self.counter))
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

producerThreadList = []
consumerThreadList = []

numProducerThreads = 1
numConsumerThreads = 1

destinationPath = ''

if __name__ == "__main__":
    # Start program
    print('Running Image Enhancer!')
    
    # Take inputs
    sourcePath    = input('Folder name of input images [eave blank for `images`]: ')
    destinationPath  = input('Folder name of output images [Leave blank for `enhanced`]: ')

    if (sourcePath == ''):
        sourcePath = './images'
    else:
        sourcePath = './' + sourcePath

    if (destinationPath == ''):
        destinationPath = './enhanced/'
    else:
        destinationPath = './' + destinationPath + '/'

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

    for i in range(numProducerThreads):
        producerThread = producer(sharedImages, i)
        producerThreadList.append(producerThread)
        producerThread.start()

    for i in range(numConsumerThreads):
        consumerThread = consumer(sharedImages, bF, cF, sF, i)
        consumerThreadList.append(consumerThread)
        consumerThread.start()

    for prodThread in producerThreadList:
        prodThread.join()

    for consThread in consumerThreadList:
        consThread.join()

    # When finished running all processes
    print("--- %s seconds with %i producers and %i consumers ---" % (time.time() - startTime, numProducerThreads, numConsumerThreads))