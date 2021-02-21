import cv2 as cv
import os
import csv

f_path="/Users/jonas/Downloads/labelmefacade-master/labels"

paths=os.listdir(f_path)
print(type(paths[0]))
print(paths[0])

sizes=dict()
path_size_list=[]

for p in paths:
    try:
        loc_path=os.path.join(f_path, p)
        img=cv.imread(loc_path)

        # print(img.shape)

        x, y=img.shape[0], img.shape[1]
        try:
            sizes[(x,y)]+=1
        except:
            sizes[(x,y)]=1

        if (x,y)==(512, 683):
            path_size_list.append(p)
    except:
        print(p)

print(sizes)
print(path_size_list)

f_write=open("/Users/jonas/Downloads/labelmefacade-master/512_683.csv", "w")
f_write.write('\n'.join(path_size_list))
f_write.close()

# cv.imshow('image',img)
# cv.waitKey(0)
# cv.destroyAllWindows()