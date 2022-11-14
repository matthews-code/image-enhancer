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

    finalImage.show()

if __name__ == "__main__":
    print('Running Image Enhancer!')

    # Load/Open image file
    image = Image.open('images\gfg.png')

    enhanceImage(image, 2.5, 8.3, 0.3)