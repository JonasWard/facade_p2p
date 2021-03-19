from PIL import Image
import numpy as np
import os

LABEL_DICT = {
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

LABEL_GROUPS = {
    0:["background"],
    1:["window", "door"]
}

IMAGE_RESOLUTION=300

def dict_mapping():

    global LABEL_DICT, LABEL_GROUPS
    
    label_remaper={len(LABEL_GROUPS):[]}
    for k, v in LABEL_DICT.items():
        k_added = False
        for k_l, vs in LABEL_GROUPS.items():
            if v in vs:
                try:
                    label_remaper[k_l].append(k)
                except:
                    label_remaper[k_l]=[k]
                k_added=True
                break

        if not(k_added):
            label_remaper[len(LABEL_GROUPS)].append(k)

    remap_dict = {}
    for k, vs in label_remaper.items():
        for v in vs:
            remap_dict[v]=k
    
    return remap_dict

def pillow_remap(img, dict_map):
    np_array=np.array(img)
    np_copy =np_array.copy()

    for k, v in dict_map.items(): np_copy[np_array==k] = v

    return Image.fromarray(np_copy)

def crop_image(img):
    global IMAGE_RESOLUTION
    # getting the w & h of the image
    w, h = img.size

    # setting the scales:
    i = min(IMAGE_RESOLUTION/w, IMAGE_RESOLUTION/h)
    a = max(IMAGE_RESOLUTION/w, IMAGE_RESOLUTION/h)

    # creating thumbnail
    img.thumbnail((IMAGE_RESOLUTION*a/i,IMAGE_RESOLUTION*a/i), Image.ANTIALIAS)
    w, h = img.size

    # cropping
    left = (w - IMAGE_RESOLUTION)/2
    top = (h - IMAGE_RESOLUTION)/2
    right = (w + IMAGE_RESOLUTION)/2
    bottom = (h + IMAGE_RESOLUTION)/2

    return img.crop((left, top, right, bottom))

def read_folder(f_path):
    directory = os.fsencode(f_path)

    remap_dict = dict_mapping()
    
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".png"):
            pure_file_name = filename.replace(".png",'')
            img = Image.open(os.path.join(f_path, filename))
            print(img.histogram())
            print(type(img))
            n_img = pillow_remap(img, remap_dict)
            n_img.putpalette(img.palette)
            print(n_img.histogram())
            # print(.__name__)

            n_img = crop_image(n_img)
            n_img.save(os.path.join(f_path, pure_file_name + "_gt.png"), "PNG")

            # img=read_and_map_image(img, map_dict)
            # pseudocolor_image(img, len(set(map_dict.values())), filename)
        elif filename.endswith(".jpg"):

            img = Image.open(os.path.join(f_path, filename))
            img = crop_image(img)

            pure_file_name = filename.replace(".jpg",'')
            img.save(os.path.join(f_path, pure_file_name + "_in.png"), "PNG")
        else:
            print("{} is not a png".format(filename))

if __name__ == "__main__":
    # map_dict=dict_mapping(b_channel_dict, LABEL_DICT, LABEL_GROUPS)

    # print(map_dict)
    read_folder("/Users/jonas/Downloads/CMP_facade_DB_extended (1)/extended")
