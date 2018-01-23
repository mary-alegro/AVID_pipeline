from lxml import etree as ET
import fnmatch
import os
from skimage import io
import numpy as np
import sys
import glob
import matplotlib.pyplot as plt

def sub2ind(size,r,c):
    ind = r*size[1]+c
    return ind

def create_adj_dic(grid_shape):
    rows = grid_shape[0]
    cols = grid_shape[1]

    tiles_dic = {}
    for r in range(rows):
        for c in range(cols):

            N = -1
            S = -1
            E = -1
            W = -1
            curr = sub2ind(grid_shape,r,c)
            #get north
            if r > 0:
                N = sub2ind(grid_shape,r-1,c)
            #get south
            if r < rows:
                S = sub2ind(grid_shape,r+1,c)
            #get west
            if c > 0:
                W = sub2ind(grid_shape,r,c-1)
            #get east
            if c < cols:
                E = sub2ind(grid_shape,r,c+1)

            tiles_dic[curr] = np.array([N,S,E,W])

    return tiles_dic


def create_xml_metadata(tile_dir, rows, cols, nblocks_tile, file_pt = 'tile_{:04d}.tif', pix_mm = 819):
    grid_shape = np.array([rows,cols])
    tiles_dic = create_adj_dic(grid_shape)

    root_xml = ET.Element('Tiles', attrib={'rows': str(rows), 'cols': str(cols), 'pix_mm': str(pix_mm), 'nblocks_tile': str(nblocks_tile), 'root_dir':tile_dir})

    keys = tiles_dic.keys()
    for tile_num in keys:

        #load current image
        img_name = file_pt.format(tile_num)
        img_path = os.path.join(tile_dir,img_name)
        img = io.imread(img_path)

        tile_xml = ET.SubElement(root_xml, 'Tile', attrib={'name':img_name, 'rows':str(img.shape[0]), 'cols':str(img.shape[1])})

        nbors = tiles_dic[tile_num] #Neighbors are always in N,S,E,W order
        #get north:
        if nbors[0] != -1:
            n_name = file_pt.format(nbors[0])
            N_tile_xml = ET.SubElement(tile_xml, 'North', attrib={'name':n_name})

        #get south:
        if nbors[1] != -1:
            s_name = file_pt.format(nbors[1])
            S_tile_xml = ET.SubElement(tile_xml, 'South', attrib={'name':s_name})

        #get east:
        if nbors[2] != -1:
            e_name = file_pt.format(nbors[2])
            E_tile_xml = ET.SubElement(tile_xml, 'East', attrib={'name':e_name})

        #get west:
        if nbors[3] != -1:
            w_name = file_pt.format(nbors[3])
            W_tile_xml = ET.SubElement(tile_xml, 'West', attrib={'name':w_name})



    xml_tree = ET.ElementTree(root_xml)
    return xml_tree


def main():

    print('Exporting tiles metadata...')

    tile_dir = '/home/maryana/storage/Posdoc/AVID/AV13/AT100440/TAU_seg_tiles'
    xml_file = '/home/maryana/storage/Posdoc/AVID/AV13/AT100440/TAU_seg_tiles/tiles_metadata.xml'
    nblocks = 5
    cols = 20
    rows = 9
    xml_tree = create_xml_metadata(tile_dir, rows, cols, nblocks)

    print(ET.tostring(xml_tree, pretty_print=True, xml_declaration=True, encoding='UTF-8'))

    with open(xml_file, 'w+') as out:
        out.write(ET.tostring(xml_tree, pretty_print=True, xml_declaration=True, encoding='UTF-8'))

    print('Metadata saved in {}'.format(xml_file))

if __name__ == '__main__':
    main()