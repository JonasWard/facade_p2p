from PIL import Image
import numpy as np

img = Image.open("/Users/jonas/Desktop/colors_to_diff.png")
img_nps = np.array(img)

r = img_nps[:,:,:1]
g = img_nps[:,:,1:2]
b = img_nps[:,:,2:3]
alpha = img_nps[:,:,3:]

color_a = (45, 254, 253)
color_b = (4, 20, 166)

d_a = np.sqrt(np.power(r-color_a[0], 2)+np.power(g-color_a[1], 2)+np.power(b-color_a[2], 2))
d_b = np.sqrt(np.power(r-color_b[0], 2)+np.power(g-color_b[1], 2)+np.power(b-color_b[2], 2))

indexes = (d_b > d_a).astype(np.uint8)
print(indexes)
print(indexes.shape)
print(indexes.shape[:2])
remapped = indexes.reshape(indexes.shape[:2])

im = Image.fromarray(remapped, mode="P")
im.putpalette(list(color_a)+list(color_b))
im.show()
color_b_count = np.sum(remapped)
x,y = remapped.shape
px_cnt = x*y
print("total pixels: {}, of which color b: {}, relative: {}".format(px_cnt, color_b_count, color_b_count/px_cnt))

# img.numpy()