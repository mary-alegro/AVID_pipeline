import sys
import tifffile
import glob
import os
import re



def sort_nicely(l):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    l.sort( key=alphanum_key )

def join_tiles(tiles_dir,out_name):
    files = glob.glob(os.path.join(tiles_dir,'*.tif'))
    nFiles = len(files)
    sort_nicely(files)
    tiffs = []
    nRows = 0
    nCols = 0
    nChan = 0
    for f in range(nFiles):
        name = files[f]
        tiff = tifffile.TiffFile(name)
        size = tiff.series[0].shape

        nRows += size[0]

        if nCols == 0:
            nCols = size[1]
        elif nCols > 0 and size[1] != nCols:
            print('Warning: tiles have different widths (current {}/found {})'.format(nCols,size[1]))

        if nChan == 0:
            nChan = size[2]
        elif nChan > 0 and size[2] != nChan:
            print('Warning: tiles have different num. channels (current {}/found {})'.format(nChan,size[1]))

        tiffs.append(tiff)

    new_img = tifffile.memmap(out_name, shape=(nRows, nCols, nChan), dtype=tiffs[0].series[0].dtype)
    index = 0
    for f in range(nFiles):
        print('Loading tile {} of {}'.format(f,nFiles))
        img = tiffs[f].series[0].asarray()
        new_img[index:index+tiffs[f].series[0].shape[0]] = img
        index += tiffs[f].series[0].shape[0]



def main():
    if len(sys.argv) != 3:
        print('Usage: join_tif_tiles <tiles_dir> <output_name>')
        exit()

    tiles_dir = str(sys.argv[1])
    output_name = str(sys.argv[2])

    join_tiles(tiles_dir,output_name)


if __name__ == '__main__':
    main()