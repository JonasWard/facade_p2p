# Importing the pillow library's 
# desired modules
from PIL import Image, ImageDraw
   
# Opening the image (R prefixed to
# string in order to deal with '\'
# in paths)
# img = Image.open("/Users/jonas/Desktop/probe_2.png")
img = Image.open("/Users/jonas/Documents/reps/facade_p2p/data/own/IMG_1607.png")
# img = Image.open(R"sample.png")
  
# Converting the image to RGB mode
img1 = img.convert("RGB") 
  
# Coordinates of the pixel whose value
# would be used as seed
seed = (1740, 500)
   
# Pixel Value which would be used for
# replacement 
rep_value = (255, 255, 0)
   
# Calling the floodfill() function and 
# passing it image, seed, value and 
# thresh as arguments
ImageDraw.floodfill(img1, seed, rep_value, thresh=20)
   
# Displaying the image
img1.show()