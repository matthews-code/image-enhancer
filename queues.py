import os, queue, threading, time

# Program requires Pillow, run `pip install Pillow` before running program
from PIL import Image
from PIL import ImageEnhance

queue = queue.Queue()
sharedImages = []

producerThreadCount = 2
consumerThreadCount = 2

class producer (threading.Thread):
    def __init__(self, images, threadId):
        threading.Thread.__init__(self)
        self.id = threadId
        self.images = images
        self.counter = int(len(images)/producerThreadCount)

    def run(self):
        global queue
        print('Producer %i  is initializing.'%(self.id))
        i = self.id * self.counter
        for i in range(self.id * self.counter, (self.id * self.counter) + self.counter):
            queue.put(sharedImages[i])
            print('Producer %i appended an image %i.'%(self.id, i))

class consumer (threading.Thread):
    def __init__(self, images, bF, cF, sF, threadId):
        threading.Thread.__init__(self)
        self.counter = int(len(images)/consumerThreadCount)
        self.id = threadId

        self.brightness = bF
        self.contrast = cF
        self.sharpness = sF

    def run(self):
        global queue
        for i in range(self.counter):
            image = queue.get()
            finalImage = self.applyEffects(image)
            finalImage.save('enhanced/' + str(i + (self.id * 10)) + '.png')

            print("Consumer %i got an image %i"%(self.id, i))

        # print('The values acquired by consumer ' + str(self.id) + ' are ' + str(self.list) + '\r\n')

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

    for image in sharedImages:
        print(image.filename)

    # Create threads
    producerThread = producer(sharedImages, 0)
    producerThread2 = producer(sharedImages, 1)
    consumerThread = consumer(sharedImages, bF, cF, sF, 0)
    consumerThread2 = consumer(sharedImages, bF, cF, sF, 1)

    startTime = time.time()

    producerThread.start()
    consumerThread.start()
    producerThread2.start()
    consumerThread2.start()

    producerThread.join()
    consumerThread.join()
    producerThread2.join()
    consumerThread2.join()

    # When finished running all processes
    print("--- %s seconds ---" % (time.time() - startTime))