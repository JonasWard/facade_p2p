import numpy as np
import cv2 as cv
import os

b_channel_dict = {
    167:0,
    250:1,
    251:2,
    173:11,
    14:10,
    97:3,
    31:5,
    41:8,
    56:7,
    27:6,
    254:9,
    252:4
}

label_dict = {
    0:"background",
    1:"facade",
    2:"window",
    11:"shop",
    10:"pillar",
    3:"door",
    5:"sill",
    8:"deco",
    7:"blind",
    6:"balcony",
    9:"molding",
    4:"cornice"
}

label_groups = {
    0:["background"],
    1:["window", "door"]
}

def dict_mapping(channel_dict, label_dict, label_groups):
    inverse_channel_dict = {}
    for k, v in channel_dict.items():
        inverse_channel_dict[v]=k
    
    label_remaper={len(label_groups):[]}
    for k, v in label_dict.items():
        k_added = False
        for k_l, vs in label_groups.items():
            if v in vs:
                try:
                    label_remaper[k_l].append(inverse_channel_dict[k])
                except:
                    label_remaper[k_l]=[inverse_channel_dict[k]]
                k_added=True
                break

        if not(k_added):
            label_remaper[len(label_groups)].append(inverse_channel_dict[k])

    remap_dict = {}
    for k, vs in label_remaper.items():
        for v in vs:
            remap_dict[v]=k
    
    return remap_dict

def read_and_map_image(img, map_dict):
    bs=img[:,:,0]
    n_img=np.copy(bs)
    print(np.min(bs), np.max(bs))
    print(map_dict)
    for k, v in map_dict.items(): n_img[bs==k] = v
    
    print(np.min(n_img), np.max(n_img))
    return n_img

def pseudocolor_image(img, c_cnt, dis_name=None):
    img=(img*(255./c_cnt)).astype(np.uint8)
    img=cv.applyColorMap(img, cv.COLORMAP_JET)
    
    dis_name = "color vis" if dis_name is None else dis_name
    cv.imshow(dis_name, img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def read_folder(f_path, map_dict):
    directory = os.fsencode(f_path)
    
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".png"):
            img=cv.imread(os.path.join(f_path, filename))
            img=read_and_map_image(img, map_dict)
            pseudocolor_image(img, len(set(map_dict.values())), filename)
        else:
            print("{} is not a png".format(filename))

if __name__ == "__main__":
    map_dict=dict_mapping(b_channel_dict, label_dict, label_groups)

    print(map_dict)
    read_folder("/Users/jonas/Downloads/CMP_facade_DB_extended (1)/extended", map_dict)