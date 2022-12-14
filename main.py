import os, shutil
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
        self.counter = int(len(images))

    def run(self):
        #print("\nProducer %i has %i counts."%(self.id, self.counter))
        global sharedResourceBuffer
        global semaphoreBuffer

        for i in range(self.counter):

            if endEvent.is_set():
                break

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

        # print("Consumer %i has %i counts."%(self.id, self.counter))

        for i in range(self.counter):
            semaphoreBuffer.acquire()

            # print(semaphoreBuffer._value) # Current value of semaphore

            if endEvent.is_set():
                break

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

def ending():  

    for prodThread in producerThreadList:
        prodThread.join()

    for consThread in consumerThreadList:
        consThread.join()

    # When finished running all processes
    seconds = (time.time() - startTime)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    files = os.listdir(destinationPath)

    lines = [
        'Program Stats',
        '| ==================================== |',
        "Successfully Enhanced [%d / %d] images with %d consumer/s." % (len(files), len(sharedImages), numConsumerThreads),
        "Compile Time: %d Minutes & %f Seconds" % (minutes, seconds),
        "Output Folder: %s" % destinationPath
    ]

    with open('stats.txt', 'w') as f:
        f.write('\n'.join(lines))

    print("\nCompile Time: %d Minutes & %f Seconds" % (minutes, seconds))
    print('\033[92m' + "Success! See details in stats.txt.\n" '\033[0m')

def endKaagad():
    endEvent.set()
    ending()
    quit()

def asciiIntro():
    print('\033[92m' + '    ______  ______   ____________                    ')
    print('   /  _/  |/  /   | / ____/ ____/                    ')
    print('   / // /|_/ / /| |/ / __/ __/                       ')
    print(' _/ // /  / / ___ / /_/ / /___                       ')
    print('/___/_/__/_/_/__|_\____/_____/   __________________  ')
    print('   / ____/ | / / / / /   |  / | / / ____/ ____/ __ \ ')
    print('  / __/ /  |/ / /_/ / /| | /  |/ / /   / __/ / /_/ / ')
    print(' / /___/ /|  / __  / ___ |/ /|  / /___/ /___/ _, _/  ')
    print('/_____/_/ |_/_/ /_/_/  |_/_/ |_/\____/_____/_/ |_|   ' + '\033[0m')
                                                    

# ------- Global variables -------

endEvent = threading.Event()

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
    asciiIntro()
    print('\nRunning Image Enhancer!\n')
    print('||===========================||\n')
    
    # ------- Take path inputs -------

    sourcePath = input(
        'Folder name of input images    [Leave blank for `images`]: ')

    print('\033[91m' + '\n!!! WARNING WILL DELETE/CLEAR CONTENTS OF OUTPUT FOLDER !!!' + '\033[0m')
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

    # ------- Delete enhanced folder -------
    for f in os.listdir(destinationPath):
        os.remove(os.path.join(destinationPath, f))

    # ------- Take enhancing time input -------
    enhanceTime = input(
        '\nEnhance time in minutes        [Leave blank for 1 second]: ')

    if enhanceTime:
        enhanceTime = float(enhanceTime) * 60
    else:
        enhanceTime = 0.01666667 * 60

    # ------- Take factor inputs -------
    bF = input('Brightness Factor              [Leave blank for a factor of 1]: ')
    cF = input('Contrast Factor                [Leave blank for a factor of 1]: ')
    sF = input('Sharpess Factor                [Leave blank for a factor of 1]: ')

    if bF: bF = float(bF)
    else: bF = 1

    if cF: cF = float(cF)
    else: cF = 1

    if sF: sF = float(sF)
    else: sF = 1

    # ------- Take number of thread input -------

    numConsumerThreads = input(
        'Number of consumer threads     [Leave blank for 1 consumer]: ')

    print('\n||===========================||')

    if numConsumerThreads:
        numConsumerThreads = int(numConsumerThreads)
    else:
        numConsumerThreads = 1

    # ------- Load Images -------
    files = os.listdir(sourcePath)

    for imageName in files:
        img = Image.open(sourcePath + '/' + imageName)
        if(img.format == 'GIF'):
            for i in range(img.n_frames):
                img.seek(i)
                # img.save(sourcePath + '/' + str(i) + imageName)
        sharedImages.append([img, imageName])

    # ------- Create and run threads -------
    startTime = time.time()

    for i in range(numConsumerThreads):
        consumerThread = consumer(sharedImages, bF, cF, sF, i)
        consumerThreadList.append(consumerThread)
        consumerThread.start()

    for i in range(numProducerThreads):
        producerThread = producer(sharedImages, i)
        producerThreadList.append(producerThread)
        producerThread.start()
    
    # Kill thread here
    timer = threading.Timer(enhanceTime, endKaagad)
    timer.start()