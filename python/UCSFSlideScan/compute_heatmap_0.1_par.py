import fnmatch
import os
from skimage import io
import numpy as np
import sys
import glob
import matplotlib.pyplot as plt
from lxml import etree as ET


NPIX_MM = 819 #num. pixels in 1mm
NBLOCK_TILE = 5 #tiles are 5x5 grid with 1mm^2 each
MAX_VALUE = 65535 #16bits

def sub2ind(array_shape, rows, cols):
    ind = rows*array_shape[1] + cols
    ind[ind < 0] = -1
    ind[ind >= array_shape[0]*array_shape[1]] = -1
    return ind

def ind2sub(array_shape, ind):
    ind[ind < 0] = -1
    ind[ind >= array_shape[0]*array_shape[1]] = -1
    rows = (ind.astype('int') / array_shape[1])
    cols = ind % array_shape[1]
    return (rows, cols)

def get_num_white(block):
    # num. non zeros in the blue channel
    tmp_nnz_b = block.flatten().nonzero()
    nnz_b = float(len(tmp_nnz_b[0])) #number of non-zero pixel in BLOCK matrix
    return nnz_b

def get_num_pix_tissue(img): #assumes RGB image
    tmp_img = img[:,:,0]+img[:,:,1]+img[:,:,2]
    tmp_nnz_b = tmp_img.flatten().nonzero()
    nnz_b = float(len(tmp_nnz_b[0]))  # number of non-zero pixel in img
    return nnz_b

def create_adj_dic(xml_meta_file):
    xml_tree = ET.parse(xml_meta_file)
    tiles_list = xml_tree.xpath('//Tiles/Tile')

    tiles_dic = {}
    for T in tiles_list:
        T_att = T.attrib

        att = {}
        att['rows'] = T_att['rows']
        att['cols'] = T_att['cols']

        N = T.xpath('North')
        S = T.xpath('South')
        E = T.xpath('East')
        W = T.xpath('West')
        if N:
            att['North'] = N[0].attrib['name']
        if S:
            att['South'] = S[0].attrib['name']
        if E:
            att['East'] = E[0].attrib['name']
        if W:
            att['West'] = W[0].attrib['name']

        tiles_dic[T_att['name']] = att

    return tiles_dic


def load_metadata(xml_meta_file):
    xml_tree = ET.parse(xml_meta_file)
    tiles_node = xml_tree.xpath('//Tiles')[0]
    orig_rows = int(tiles_node.attrib['img_rows'])
    orig_cols = int(tiles_node.attrib['img_cols'])
    root_dir = tiles_node.attrib['root_dir']
    pix_mm = int(tiles_node.attrib['pix_mm'])
    nblocks = int(tiles_node.attrib['nblocks_tile'])

    return orig_rows, orig_cols, root_dir, pix_mm, nblocks


def compute_heatmap(hm_out_dir,xml_meta_file):
    orig_rows, orig_cols, root_dir, pix_mm, nblocks = load_metadata(xml_meta_file)
    tiles_dic = create_adj_dic(xml_meta_file)

    # Note: nblock = num. of 5mm^2 block inside each tile
    nblocks /= 0.1 #0.1mm blocks
    # Note: nim. of 0.1mm^2 blocks inside each tile
    nblocks = int(nblocks)

    hm_file = os.path.join(hm_out_dir,'heat_map_full.npy')






def main():
    if len(sys.argv) != 3:
        print('Usage: compute_heatmap_0.1_par.py <hmap_out_dir> <metadata_xml_file>')
        exit()

    hm_out_dir = str(sys.argv[1])
    xml_meta_file = str(sys.argv[2])
    compute_heatmap(hm_out_dir,xml_meta_file)


if __name__ == '__main__':
    main()