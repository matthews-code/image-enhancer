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
    def __init__(self, images, bF, cF, sF, threadId):
        threading.Thread.__init__(self)
        self.counter = len(images)
        self.brightness = bF
        self.contrast = cF
        self.sharpness = sF
        self.id = threadId
        self.list = []
        self.item = 0

    def run(self):
        global sharedResourceBuffer
        global semaphoreBuffer
        print("Consumer %i is waiting \n"%(self.id))
        for i in range(self.counter):
            semaphoreBuffer.acquire() 
            if sharedResourceBuffer:
                origImg = sharedResourceBuffer.pop()
                self.item = self.applyEffects(origImg)

                self.item.save('enhanced/' + str(i) + '.png')

                self.list.append(self.item)
                print("Consumer %i popped an image"%(self.id))

        print('The values acquired by consumer ' + str(self.id) + ' are ' + str(self.list) + '\r\n')

    def applyEffects(self, image):    
        currBrightness      = ImageEnhance.Brightness(image)
        currImage     = currBrightness.enhance(self.brightness)

        currContrast        = ImageEnhance.Contrast(currImage)
        currImage          = currContrast.enhance(self.contrast)
        
        currSharpness       = ImageEnhance.Sharpness(currImage)
        finalImage      = currSharpness.enhance(self.sharpness)

        return finalImage

if __name__ == "__main__":
    # Start program
    print('Running Image Enhancer!')
    
    # Take inputs
    folderImages    = input('Folder name of input images: ')
    folderEnhanced  = input('Folder name of output images: ')

    # Example inputs: 2.5, 8.3, 0.3
    bF = float(input('Brightness Factor: '))
    sF = float(input('Sharpess Factor: '))
    cF = float(input('Contrast Factor: '))

    # Load images
    path = './images'
    files = os.listdir(path)

    for image in files:
        img = Image.open(path + '/' + image)
        sharedImages.append(img)

    # Create threads
    producerThread = producer(sharedImages)
    consumerThread = consumer(sharedImages, bF, cF, sF, 1)

    startTime = time.time()

    producerThread.start()
    consumerThread.start()

    producerThread.join()
    consumerThread.join()

    # When finished running all processes
    print("--- %s seconds ---" % (time.time() - startTime))