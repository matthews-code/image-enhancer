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

        i = self.id * self.counter
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
        if threadId < len(images) % numConsumerThreads:
            self.counter += 1

    def run(self):
        global sharedResourceBuffer
        global semaphoreBuffer

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

# ------- Global variables -------


sharedImages = []
sharedResourceBuffer = []
semaphoreBuffer = threading.Semaphore(0)

producerThreadList = []
consumerThreadList = []

numProducerThreads = 1
numConsumerThreads = 0

destinationPath = ''

enhanceTime = 0

if __name__ == "__main__":
    # ------- Start program -------
    print('\nRunning Image Enhancer!\n')
    print('||===========================||\n')
    # ------- Take path inputs -------
    sourcePath = input(
        'Folder name of input images    [Leave blank for `images`]: ')
    destinationPath = input(
        'Folder name of output images   [Leave blank for `enhanced`]: ')

    if (sourcePath == ''):
        sourcePath = './images'
    else:
        sourcePath = './' + sourcePath

    if (destinationPath == ''):
        destinationPath = 'enhanced'
    else:
        os.mkdir(destinationPath)

    destinationPath = './' + destinationPath + '/'

    # ------- Take enhancing time input -------
    enhanceTime = input(
        'Enhance time in minutes        [Leave blank for 0.1 minute]: ')

    if enhanceTime:
        enhanceTime = float(enhanceTime) * 60
    else:
        enhanceTime = 0.1 * 60

    # ------- Take factor inputs -------
    bF = input('Brightness Factor              [Leave blank for a factor of 1]: ')
    cF = input('Contrast Factor                [Leave blank for a factor of 1]: ')
    sF = input('Sharpess Factor                [Leave blank for a factor of 1]: ')

    if bF:
        bF = float(bF)
    else:
        bF = 1

    if cF:
        cF = float(cF)
    else:
        cF = 1

    if sF:
        sF = float(sF)
    else:
        sF = 1

    # ------- Take number of thread input -------
    numConsumerThreads = input(
        'Number of consumer threads     [Leave blank for 1 consumer]: ')

    print('\n||===========================||')

    if numConsumerThreads:
        numConsumerThreads = int(numConsumerThreads)
    else:
        numConsumerThreads = 1

    # # ------- Load Images -------
    files = os.listdir(sourcePath)

    for imageName in files:
        img = Image.open(sourcePath + '/' + imageName)
        sharedImages.append([img, imageName])

    # # ------- Create and run threads -------
    startTime = time.time()

    for i in range(numProducerThreads):
        producerThread = producer(sharedImages, i)
        producerThreadList.append(producerThread)
        producerThread.start()

    for i in range(numConsumerThreads):
        consumerThread = consumer(sharedImages, bF, cF, sF, i)
        consumerThreadList.append(consumerThread)
        consumerThread.start()

    time.sleep(1.5)
    # Kill thread here

    for consThread in consumerThreadList:
        consThread.join()    

    for prodThread in producerThreadList:
        prodThread.join()

    for consThread in consumerThreadList:
        consThread.join()

    # When finished running all processes
    seconds = (time.time() - startTime)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    lines = [
        'Program Stats',
        '| ==================================== |',
        "Compile Time: %d Minutes & %f Seconds" % (minutes, seconds),
        "Number of Images: %d" % len(sharedImages),
        "Output Folder: %s" % destinationPath
    ]

    with open('stats.txt', 'w') as f:
        f.write('\n'.join(lines))

    print("\nCompile Time: %d Minutes & %f Seconds" % (minutes, seconds))
    print("Success! See details in stats.txt.\n")
