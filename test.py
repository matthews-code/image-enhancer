import threading
import os
from PIL import Image
from PIL import ImageEnhance

shared_image_buffer = []

# Load images onto array with semaphore and enhancement indicator

path = './images'
files = os.listdir(path)

for image in files:
    img = Image.open(path + '/' + image)
    shared_image_buffer.append([img, threading.Lock(), 0, 0, 0])
        
def enhanceBrightness(bF):
    global shared_image_buffer

    for i in range (len(shared_image_buffer)):
        shared_image_buffer[i][1].acquire()

        if shared_image_buffer[i][2] == 0:
            image                       = shared_image_buffer[i][0]
            
            finalImage                  = ImageEnhance.Brightness(image).enhance(bF)
            shared_image_buffer[i][0]   = finalImage

            finalImage.show()
            shared_image_buffer[i][2]   = 1
            shared_image_buffer[i][1].release()

        else:
            shared_image_buffer[i][1].release()

# def enhanceSharpness(sF):
#     global shared_image_buffer

#     for i in range (len(shared_image_buffer)):
#         shared_image_buffer[i][1].acquire()

#         if shared_image_buffer[i][3] == 0:
#             image                       = shared_image_buffer[i][0]
            
#             finalImage                  = ImageEnhance.Sharpness(image).enhance(sF)
#             shared_image_buffer[i][0]   = finalImage

#             finalImage.show()
#             shared_image_buffer[i][3]   = 1
#             shared_image_buffer[i][1].release()

#         else:
#             shared_image_buffer[i][1].release()

if __name__ == "__main__":
    bT = threading.Thread(target=enhanceBrightness, args=(1.2,))
    # sT = threading.Thread(target=enhanceSharpness, args=(2.4,))
    
    bT.start()
    # sT.start()

    bT.join()
    # sT.join()