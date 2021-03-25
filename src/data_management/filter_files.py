import os

# copy file

def return_file_name_list(f_path):
    directory = os.fsencode(f_path)

    # file_dict = {}

    # remap_dict = dict_mapping()
    file_list = []

    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        if filename.endswith(".png"):
            pure_file_name = filename.replace(".png",'')
            file_list.append(pure_file_name)

    return file_list

if __name__ == "__main__":
    f_str_list=return_file_name_list("/Users/jonas/Desktop/stoHomeFiltered/test")
    f_str_list.extend(return_file_name_list("/Users/jonas/Desktop/stoHomeFiltered/train"))

    print(f_str_list)


