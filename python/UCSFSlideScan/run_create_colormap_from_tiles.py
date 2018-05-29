
import os
import sys
import glob
import create_colormap_from_tiles as ccmap


def get_folder_list(root_dir):
    dir_list = []
    list_dirs = glob.glob(root_dir + '/*/')
    for ldir in list_dirs:
        if os.path.isdir(ldir):
            if ldir.find('magick_tmp') != -1:
                continue
            else:
                dir_list.append(ldir)
    return dir_list


def run_create_colormap_tiles(root_dir):
    dir_list = get_folder_list(root_dir)
    for folder in dir_list:
        ccmap.compose_image(folder)


def main():
    if len(sys.argv) != 2:
        print('Usage: run_create_colormap_from_tiles.py <root_dir> ')
        exit()

    root_dir = str(sys.argv[1])  # abs path to where the images are
    run_create_colormap_tiles(root_dir)

if __name__ == '__main__':
    main()