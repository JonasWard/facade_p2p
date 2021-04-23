from PIL import Image
import numpy as np

dict_rectangles = {
    "bathroom" : [
        (48, 813),
        (129, 676)
    ],
    "window_1_left" : [
        (298, 423),
        (555, 113)
    ],
    "window_1_right" : [
        (785, 423),
        (1039, 111)
    ],
    "window_0_right" : [
        (780, 943),
        (1039, 628)
    ],
    "door" : [
        (290, 1092),
        (539, 602)
    ]
}

def img_to_obj(img, rec = None, file_name = None):
    img = Image.open(img)
    x, y, _ = np.array(img).shape

    print(x,y)

    print(rec)

    if rec is None:
        rec = [(0., 0.), (x, y)]
    rec = [tuple([float(v) for v in vals]) for vals in rec]
    
    print(rec)

    rec_b = [(rec[0][0], rec[1][1]), (rec[1][0], rec[0][1])]
    
    rec_t_s = [(i/x, 1.-j/y) for i,j in rec]
    rec_t_bs = [(i/x, 1.-j/y) for i,j in rec_b]

    obj_str_list = [
        "# JonasWard\n",
        "mtllib vp.mtl",
        "usemtl anImage",
        # "g tetrahedron",
        "v {} {} 0.0".format(*rec[0]),
        "v {} {} 0.0".format(*rec_b[1]),
        "v {} {} 0.0".format(*rec[1]),
        "v {} {} 0.0".format(*rec_b[0]),
        # "vt {} {}".format(*rec[0]),
        # "vt {} {}".format(*rec_b[1]),
        # "vt {} {}".format(*rec[1]),
        # "vt {} {}".format(*rec_b[0]),
        "vt {} {}".format(*rec_t_s[0]),
        "vt {} {}".format(*rec_t_bs[1]),
        "vt {} {}".format(*rec_t_s[1]),
        "vt {} {}".format(*rec_t_bs[0]),
        # "vt {} {}".format(*rec_t_bs[0]),
        # "vt {} {}".format(*rec_t_s[1]),
        # "vt {} {}".format(*rec_t_bs[1]),
        # "vt {} {}".format(*rec_t_s[0]),
        # "vt {} {}".format(*rec_t_s[1]),
        # "vt {} {}".format(*rec_t_bs[0]),
        # "vt {} {}".format(*rec_t_s[0]),
        # "vt {} {}".format(*rec_t_bs[1]),
        "vn 0. 0. 1.",
        "vn 0. 0. 1.",
        "vn 0. 0. 1.",
        "vn 0. 0. 1.",
        # "f 1 2 3 4",
        # "f 0 1 2",
        # "f 0 2 3",
        # "f 1/1 2/2 3/3 4/4",
        "f 1/1/1 2/2/2 3/3/3 4/4/4",
        # "f 0//0 2//2 3//3",
    ]

    if file_name is None:
        f = open("default.obj", 'w')
    else:
        f = open("{}.obj".format(file_name), 'w')

    f.write('\n'.join(obj_str_list))
    
    f.close()

    print('\n'.join(obj_str_list))

if __name__ == "__main__":
    import os

    # wondelgem = "/Users/jonas/Desktop/Wondelgem.png"
    # allwirlen = "/Users/jonas/Desktop/Allwirlen.png"

    # img_to_obj(wondelgem, file_name="wondelgem")
    # img_to_obj(allwirlen, file_name="allwirlen")

    oberhausen = "/Users/jonas/Desktop/oberhausen.png"
    img_to_obj(oberhausen, "oberhausen")

    # img_to_obj("/Users/jonas/Documents/reps/facade_p2p/img_to_facade/image.png")

    # for name, rec in dict_rectangles.items():
    #     img_to_obj("/Users/jonas/Documents/reps/facade_p2p/img_to_facade/image.png", rec, name)