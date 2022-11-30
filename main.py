import os
import threading
import time

# Program requires Pillow, run `pip install Pillow` before running program
from PIL import Image
from PIL import ImageEnhance

sharedImages = []
sharedResourceBuffer = []
semaphoreBuffer = threading.Semaphore(0)

def enhanceImage(image, eBrightness, eSharpness, eContrast):    
    # Enhance brightness
    currBrightness      = ImageEnhance.Brightness(image)
    imageBrightness     = currBrightness.enhance(eBrightness)

    # Enhance sharpness
    currSharpness       = ImageEnhance.Sharpness(imageBrightness)
    imageSharpness      = currSharpness.enhance(eSharpness)

    # Enhance contrast
    currContrast        = ImageEnhance.Contrast(imageSharpness)
    finalImage          = currContrast.enhance(eContrast)

    # finalImage.show()
    finalImage.save('enhanced/gfg-enhanced.png')

class producer (threading.Thread):
    def __init__(self, images):
        threading.Thread.__init__(self)
        self.images = images

    def run(self):
        global sharedResourceBuffer
        global semaphoreBuffer
        print('Producer is initializing.\n')
        time.sleep(2)
        for img in self.images:
            sharedResourceBuffer.append(img)
            semaphoreBuffer.release()
            print('Producer appended an image.\n')
            time.sleep(2)

class consumer (threading.Thread):
    def __init__(self, images, threadId):
        threading.Thread.__init__(self)
        self.counter = len(images)
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
                self.item = sharedResourceBuffer.pop()

                print('Apply brightness')
                print('Apply contrast')
                print('Apply sharpness')

                self.list.append(self.item)
                print("Consumer %i popped an item \n"%(self.id)) 

            time.sleep(2)
        print('The values acquired by consumer ' + str(self.id) + ' are ' + str(self.list) + '\r\n')

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
        img = Image.open(image)
        sharedImages.append(img)

    # Create threads
    producerThread = producer(sharedImages)
    consumerThread = consumer(sharedImages, 1)

    # When finished running all processes
    print('Done!')