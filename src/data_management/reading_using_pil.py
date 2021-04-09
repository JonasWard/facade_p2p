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
    # 0:["window"],
    0:["window", "door"]
}

IMAGE_RESOLUTION=256

def dict_mapping():

    # global LABEL_DICT, LABEL_GROUPS
    
    # label_remaper={len(LABEL_GROUPS):[]}
    # for k, v in LABEL_DICT.items():
    #     k_added = False
    #     for k_l, vs in LABEL_GROUPS.items():
    #         if v in vs:
    #             try:
    #                 label_remaper[k_l].append(k)
    #             except:
    #                 label_remaper[k_l]=[k]
    #             k_added=True
    #             break

    #     if not(k_added):
    #         label_remaper[len(LABEL_GROUPS)].append(k)

    # remap_dict = {}
    # for k, vs in label_remaper.items():
    #     for v in vs:
    #         remap_dict[v]=k
    #         print("key: {}, value: {}".format(k,v))
    
    # return remap_dict
    
    a_dict = {}

    for i in range(255):
        a_dict[255-i]=1

    a_dict[1]=3
    a_dict[2]=2
    # a_dict[3]=1

    return a_dict
    # return {
    #     0:2,
    #     1:1,
    #     2:1,
    #     3:0,
    #     4:0,
    #     5:0,
    #     6:0,
    #     7:0,
    #     8:0,
    #     9:0,
    #     10:0,
    #     11:0,
    # }

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

def read_and_save_merged_images_from_list(f_path, f_list):
    directory = os.fsencode(f_path)

    file_dict = {}

    remap_dict = dict_mapping()
    
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".png"):
            pure_file_name = filename.replace(".png",'')

            if pure_file_name in f_list:
                img = Image.open(os.path.join(f_path, filename))

                print(img.histogram())
                n_img = pillow_remap(img, remap_dict)
                # print(img.palette.tostring())
                n_img.putpalette(img.palette)
                # print(.__name__)

                n_img = crop_image(n_img)
                n_img = n_img.convert('RGB')

                try:
                    file_dict[pure_file_name]["input"]=n_img
                except:
                    file_dict[pure_file_name]={"input":n_img}

        elif filename.endswith(".jpg"):

            img = Image.open(os.path.join(f_path, filename))
            img = crop_image(img)

            pure_file_name = filename.replace(".jpg",'')

            if pure_file_name in f_list:
                try:
                    file_dict[pure_file_name]["output"]=img
                except:
                    file_dict[pure_file_name]={"output":img}

        else:
            print("{} is not a png".format(filename))

    for name, img_dict in file_dict.items():
        if len(img_dict) == 2:
            image1, image2 = img_dict["input"], img_dict["output"]

            image1_size = image1.size
            image2_size = image2.size

            new_image = Image.new('RGB',(2*image1_size[0], image1_size[1]), (250,250,250))
            new_image.paste(image1,(0,0))
            new_image.paste(image2,(image1_size[0],0))

            new_image.save(os.path.join(f_path, "output", name + ".png"), "PNG")
        else:
            print("don't have all necessary data for {}".format(name))

def read_and_save_merged_images(f_path):
    directory = os.fsencode(f_path)

    file_dict = {}

    remap_dict = dict_mapping()
    
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".png"):
            pure_file_name = filename.replace(".png",'')

            img = Image.open(os.path.join(f_path, filename))

            # print(img.histogram())
            # n_img = pillow_remap(img, remap_dict)
            # # print(img.palette.tostring())
            # n_img.putpalette(img.palette)
            # print(.__name__)

            n_img = crop_image(img)
            n_img = n_img.convert('RGB')

            try:
                file_dict[pure_file_name]["input"]=n_img
            except:
                file_dict[pure_file_name]={"input":n_img}

        elif filename.endswith(".jpg"):

            img = Image.open(os.path.join(f_path, filename))
            img = crop_image(img)

            pure_file_name = filename.replace(".jpg",'')

            try:
                file_dict[pure_file_name]["output"]=img
            except:
                file_dict[pure_file_name]={"output":img}

        else:
            print("{} is not a png".format(filename))

    for name, img_dict in file_dict.items():
        if len(img_dict) == 2:
            image1, image2 = img_dict["input"], img_dict["output"]

            image1_size = image1.size
            image2_size = image2.size

            new_image = Image.new('RGB',(2*image1_size[0], image1_size[1]), (250,250,250))
            new_image.paste(image1,(0,0))
            new_image.paste(image2,(image1_size[0],0))

            new_image.save(os.path.join(f_path, "output", name + ".png"), "PNG")
        else:
            print("don't have all necessary data for {}".format(name))

def read_and_save_merged_images_butchering(f_path):
    directory = os.fsencode(f_path)

    file_dict = {}

    remap_dict = dict_mapping()
    
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".png"):
            pure_file_name = filename.replace(".png",'')

            img = Image.open(os.path.join(f_path, filename))

            # print(img.histogram())
            # n_img = pillow_remap(img, remap_dict)
            # # print(img.palette.tostring())
            # n_img.putpalette(img.palette)
            # print(.__name__)

            n_img = crop_image(img)
            n_img = n_img.convert('RGB')

            try:
                file_dict[pure_file_name]["output"]=n_img
            except:
                file_dict[pure_file_name]={"output":n_img}

        elif filename.endswith(".jpeg"):
            pass

            img = Image.open(os.path.join(f_path, filename))
            img = crop_image(img)

            pure_file_name = filename.replace(".jpeg",'')

            try:
                file_dict[pure_file_name]["output"]=img
            except:
                file_dict[pure_file_name]={"output":img}

        else:
            print("{} is not a png".format(filename))

    for name, img_dict in file_dict.items():
        if len(img_dict) == 1:
            # image1, image2 = img_dict["input"], img_dict["output"]

            # image1_size = image1.size
            # image2_size = image2.size

            # new_image = Image.new('RGB',(2*image1_size[0], image1_size[1]), (250,250,250))
            # new_image.paste(image1,(0,0))
            # new_image.paste(image2,(image1_size[0],0))

            # image1, image2 = img_dict["input"], img_dict["output"]
            image2 = img_dict["output"]

            image1_size = image2.size
            image2_size = image2.size

            new_image = Image.new('RGB',(2*image1_size[0], image1_size[1]), (250,250,250))
            new_image.paste(image2,(0,0))
            # new_image.paste(image2,(image1_size[0],0))

            new_image.save(os.path.join(f_path, "output", name + ".png"), "PNG")
        else:
            print("don't have all necessary data for {}".format(name))

if __name__ == "__main__":
    # map_dict=dict_mapping(b_channel_dict, LABEL_DICT, LABEL_GROUPS)

    # print(map_dict)
    # read_and_save_merged_images("/Users/jonas/Downloads/fooling_around")
    # file_list=['cmp_b0358', 'cmp_b0371', 'cmp_b0359', 'cmp_b0367', 'cmp_b0372', 'cmp_b0366', 'cmp_b0362', 'cmp_b0375', 'cmp_b0349', 'cmp_b0374', 'cmp_b0329', 'cmp_b0332', 'cmp_b0331', 'cmp_b0378', 'cmp_b0346', 'cmp_b0352', 'cmp_b0347', 'cmp_b0368', 'cmp_b0369', 'cmp_b0355', 'cmp_b0204', 'cmp_b0211', 'cmp_b0011', 'cmp_b0164', 'cmp_b0206', 'cmp_b0161', 'cmp_b0001', 'cmp_b0215', 'cmp_b0003', 'cmp_b0188', 'cmp_b0189', 'cmp_b0267', 'cmp_b0298', 'cmp_b0065', 'cmp_b0064', 'cmp_b0258', 'cmp_b0270', 'cmp_b0072', 'cmp_b0098', 'cmp_b0103', 'cmp_b0248', 'cmp_b0128', 'cmp_b0075', 'cmp_b0044', 'cmp_b0050', 'cmp_b0092', 'cmp_b0051', 'cmp_b0045', 'cmp_b0253', 'cmp_b0286', 'cmp_b0047', 'cmp_b0084', 'cmp_b0127', 'cmp_b0244', 'cmp_b0240', 'cmp_b0080', 'cmp_b0280', 'cmp_b0069', 'cmp_b0323', 'cmp_b0153', 'cmp_b0032', 'cmp_b0024', 'cmp_b0031', 'cmp_b0237', 'cmp_b0035', 'cmp_b0236']
    # read_and_save_merged_images_from_list("/Users/jonas/Downloads/CMP_facade_DB_base/base",file_list)
    # read_and_save_merged_images("/Users/jonas/Downloads/CMP_facade_DB_base/base")

    read_and_save_merged_images_butchering("/Users/jonas/Documents/reps/facade_p2p/data/own/crop_tri")
