# Program requires Pillow, run `pip install Pillow` before running program
from PIL import Image
from PIL import ImageEnhance

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

    # Load/Save image file
    image = Image.open('images/gfg.png')
    enhanceImage(image, bF, sF, cF)

    # When finished running all processes
    print('Done!')