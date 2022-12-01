import os
import multiprocessing
import time

# Program requires Pillow, run `pip install Pillow` before running program
from PIL import Image
from PIL import ImageEnhance

class producer (multiprocessing.Process):
    def __init__(self, images, procId, queue):
        multiprocessing.Process.__init__(self)
        self.images = images
        self.id = procId
        self.queue = queue

        self.counter = int(len(images)/numProducerProcs)
        if len(images) % 2 == 1 and procId == 0 and not numProducerProcs == 1:
            self.counter = int(len(images)/numProducerProcs + 1)

        print('Producer init')

    def run(self):
        # print("\nProducer %i has %i counts."%(self.id, self.counter))

        print('Producer run')
        
        i = self.id * self.counter
        for i in range(self.id * self.counter, (self.id * self.counter) + self.counter):
            self.queue.put(self.images[i])

class consumer (multiprocessing.Process):
    def __init__(self, images, brightness, contrast, sharpness, procId, queue):
        multiprocessing.Process.__init__(self)
        self.brightness = brightness
        self.contrast = contrast
        self.sharpness = sharpness
        self.id = procId
        self.queue = queue

        self.counter = int(len(images)/numConsumerProcs)
        if procId < len(images) % numConsumerProcs:
            self.counter += 1

        print('Consumer init')

    def run(self):
        # print("Consumer %i has %i counts."%(self.id, self.counter))
        print('Consumer run')
        for i in range(self.counter):
            origImg = self.queue.get()
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

# ------- Global variables -------

sharedImages = []
sharedResourceBuffer = []

producerProcList = []
consumerProcList = []

numProducerProcs = 1
numConsumerProcs = 0

destinationPath = ''

enhanceTime = 0

if __name__ == "__main__":
    queue = multiprocessing.Queue()

    # ------- Start program -------
    print('Running Image Enhancer!')
    
    # ------- Take path inputs -------
    sourcePath    = input('Folder name of input images [Leave blank for `images`]: ')
    destinationPath  = input('Folder name of output images [Leave blank for `enhanced`]: ')

    if (sourcePath == ''): sourcePath = './images'
    else: sourcePath = './' + sourcePath

    if (destinationPath == ''): destinationPath = 'enhanced'
    else: os.mkdir(destinationPath) 
        
    destinationPath = './' + destinationPath + '/'

    # ------- Take enhancing time input -------
    enhanceTime = input('Enhance time in minutes [Leave blank for 0.1 minute]: ')

    if enhanceTime: enhanceTime = float(enhanceTime) * 60
    else: enhanceTime = 0.1 * 60
    print('Enhance time in seconds: %f'%(enhanceTime))

    # ------- Take factor inputs -------
    bF = input('Brightness Factor [Leave blank for a factor of 1]: ')
    cF = input('Contrast Factor [Leave blank for a factor of 1]: ')
    sF = input('Sharpess Factor [Leave blank for a factor of 1]: ')

    if bF: bF = float(bF)
    else: bF = 1

    if cF: cF = float(cF)
    else: cF = 1

    if sF: sF = float(sF)
    else: sF = 1

    # ------- Take number of Proc input -------
    numConsumerProcs = input('Number of consumer Procs [Leave blank for 1 consumer]: ')

    if numConsumerProcs: numConsumerProcs = int(numConsumerProcs)
    else: numConsumerProcs = 1

    # ------- Load Images -------
    files = os.listdir(sourcePath)

    for imageName in files:
        img = Image.open(sourcePath + '/' + imageName)
        sharedImages.append([img, imageName])

    # ------- Create and run Procs -------
    startTime = time.time()

    for i in range(numProducerProcs):
        producerProc = producer(sharedImages, i, queue)
        producerProcList.append(producerProc)
        producerProc.start()

    for i in range(numConsumerProcs):
        consumerProc = consumer(sharedImages, bF, cF, sF, i, queue)
        consumerProcList.append(consumerProc)
        consumerProc.start()

    # time.sleep(enhanceTime)

    for prodProc in producerProcList:
        prodProc.terminate()

    for consProc in consumerProcList:
        consProc.terminate()

    # When finished running all processes
    print("\n--- %s seconds with %i producer/s and %i consumer/s ---" % (time.time() - startTime, numProducerProcs, numConsumerProcs))