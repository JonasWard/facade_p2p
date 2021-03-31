# Importing the pillow library's 
# desired modules
from PIL import Image, ImageDraw
   
# Opening the image (R prefixed to
# string in order to deal with '\'
# in paths)
img = Image.open("/Users/jonas/Desktop/Screenshot 2021-03-26 at 10.04.57.png")
# img = Image.open(R"sample.png")
  
# Converting the image to RGB mode
img1 = img.convert("RGB") 
  
# Coordinates of the pixel whose value
# would be used as seed
seed = (0, 0)
   
# Pixel Value which would be used for
# replacement 
rep_value = (255, 255, 0)
   
# Calling the floodfill() function and 
# passing it image, seed, value and 
# thresh as arguments
ImageDraw.floodfill(img1, seed, rep_value, thresh=250)
   
# Displaying the image
img1.show()