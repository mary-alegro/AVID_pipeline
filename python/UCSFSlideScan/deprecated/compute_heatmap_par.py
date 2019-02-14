import fnmatch
import os
from skimage import io
import numpy as np
import sys
import glob
import matplotlib.pyplot as plt
from lxml import etree as ET
import multiprocessing as mp
import tifffile


NPIX_MM = 819 #num. pixels in 1mm
NBLOCK_TILE = 5 #tiles are 5x5 grid with 1mm^2 each
MAX_VALUE = 65535 #16bits
N_WORKERS = 4

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


def heatmap_worker(tiles_dir,seg_dir, hm_dir, nblocks_tile, pix_mm, file_bundle, min_max):

    proc = mp.current_process()
    pid = proc.pid
    #pid= 0

    NPIX_BLOCK = int(round(pix_mm*0.1))
    min_val_tissue = 0
    max_val_tissue = 0

    for img_name in file_bundle:
        if img_name.find('_mask.tif') == -1: #not a mask, it's a background tile. so, save empty file.
            tile_name = img_name[0:-4]+'.tif'
            tile_path = os.path.join(tiles_dir,tile_name)
            img = io.imread(tile_path)
            histo_per_tissue = np.zeros(img.shape[0:2])
            hm2_name = os.path.join(hm_dir, img_name[0:-4] + '_hm_pertissue.npy')
            np.save(hm2_name, histo_per_tissue)
            print('{}: File {} saved.'.format(pid, hm2_name))
            continue

        #load tile (I need the original tile to count the number of tissue pixels)
        tile_name = img_name[0:-9]+'.tif'
        tile_path = os.path.join(tiles_dir,tile_name)
        img = io.imread(tile_path)
        #load segmentation
        mask_path = os.path.join(seg_dir, img_name)
        mask = io.imread(mask_path)

        histo_per_tissue = np.zeros(img.shape[0:2])

        n_total_pix_tissue_tile = float(get_num_pix_tissue(img))
        n_total_pix_tile = img.shape[0]*img.shape[1]
        percent_tissue = n_total_pix_tissue_tile/n_total_pix_tile
        print('Percent tissue pixels: {}'.format(percent_tissue))
        if percent_tissue < 0.05:
            print('{} is empty'.format(img_name))
        else:
            print('Processing {}'.format(img_name))
            if os.path.isfile(mask_path): #run image processing routine if mask exists
                #mask = io.imread(mask_path)
                rows = img.shape[0]
                cols = img.shape[1]
                bg_row = 0
                bg_col = 0
                for r in range(nblocks_tile): #process blocks
                    end_row = NPIX_BLOCK * (r + 1)

                    for c in range(nblocks_tile):
                        end_col = NPIX_BLOCK*(c + 1)

                        # last block can be problematic, we have to check if the indices are inside the right range
                        if c == (nblocks_tile-1):
                            if end_col != cols:
                                end_col = cols

                        if r == (nblocks_tile - 1):
                            if end_row != rows:
                                end_row = rows

                        block_mask = mask[bg_row:end_row,bg_col:end_col]
                        block_img = img[bg_row:end_row,bg_col:end_col,:]

                        nonzero_pix_mask = get_num_white(block_mask) #get number of non-zero pixels in mask
                        #total_pix_block = rows*cols #total number of pixel in image block
                        npix_tissue_block = get_num_pix_tissue(block_img)

                        #percent_total = float(nonzero_pix_mask)/float(total_pix_block)
                        percent_tissue = 0.0 if npix_tissue_block == 0 else (float(nonzero_pix_mask)/float(npix_tissue_block))
                        percent_tissue_100 = percent_tissue*100
                        if percent_tissue_100 > 100.00:
                            percent_tissue_100 = 100.0 # this can happen in some situations where the mask is bigger than the tissue are. this usually happens when segmenting background (like sharpie marks)

                        #histo_per_tile[bg_row:end_row,bg_col:end_col] = percent_total*100
                        histo_per_tissue[bg_row:end_row,bg_col:end_col] = percent_tissue_100

                        # histo_per_tile_16[bg_row:end_row,bg_col:end_col] = percent_total*100
                        # histo_per_tissue_16[bg_row:end_row,bg_col:end_col] = percent_tissue*100

                        bg_col = end_col

                    bg_row = end_row
                    bg_col = 0

        #get min and max values for the entire slice, per amount of tissue
        histo_per_tissue_min = histo_per_tissue.min()
        histo_per_tissue_max = histo_per_tissue.max()

        if histo_per_tissue_min < min_val_tissue:
            min_val_tissue = histo_per_tissue_min
        if histo_per_tissue_max > max_val_tissue:
            max_val_tissue = histo_per_tissue_max

        hm2_name = os.path.join(hm_dir,img_name[0:-9]+'_hm_pertissue.npy')
        np.save(hm2_name,histo_per_tissue)
        print('{}: File {} saved. Min: {} Max:{}'.format(pid,hm2_name,histo_per_tissue_min,histo_per_tissue_max))

    min_max[pid] = (min_val_tissue, max_val_tissue)


def compute_heatmap(tiles_dir,seg_dir, hm_dir, tiles_dic, nblocks_tile, pix_mm):

    all_files = tiles_dic.keys()
    #min_max = {}

    nFiles = len(all_files)
    nf_block = int(np.ceil(float(nFiles)/N_WORKERS))

    start_idx = 0
    workers = []
    min_max = mp.Manager().dict()
    for i in xrange(N_WORKERS):
        end_idx = start_idx+nf_block
        if (end_idx > nFiles) or (i == (N_WORKERS + 1) and end_idx < nFiles):
            end_idx = nFiles

        file_bundle = all_files[start_idx:end_idx]
        start_idx = end_idx
        p = mp.Process(target=heatmap_worker, args=(tiles_dir,seg_dir, hm_dir, nblocks_tile, pix_mm,file_bundle, min_max))
        workers.append(p)
        p.start()

    for worker in workers:
        worker.join()

    #heatmap_worker(tiles_dir,seg_dir, hm_dir, nblocks_tile, pix_mm, all_files, min_max)

    #get minimum and maximum percentage values
    min_val_tissue = 0
    max_val_tissue = 0
    for p in min_max.keys():
        vals = min_max[p]
        if vals[0] < min_val_tissue:
            min_val_tissue = vals[0]
        if vals[1] > max_val_tissue:
            max_val_tissue = vals[1]

    #save min and max as numpy file
    min_max_file = os.path.join(hm_dir,'min_max.npy')
    min_max_arr = np.array([min_val_tissue,max_val_tissue])
    np.save(min_max_file,min_max_arr)

    return min_val_tissue,max_val_tissue

    #print('Min: {} Max: {}'.format(min_val_tissue,max_val_tissue))

    # for img_name in tiles_dic.keys():
    #     img_path = os.path.join(root_dir,img_name)
    #     img = io.imread(img_path)
    #
    #     mask_name = img_name[0:-4]+'_mask.tif'
    #     mask_path = os.path.join(root_dir,'masks',mask_name)
    #
    #     histo_per_tile = np.zeros(img.shape[0:2])
    #     histo_per_tissue = np.zeros(img.shape[0:2])
    #
    #     # histo_per_tile_16 = np.zeros(img.shape[0:2])
    #     # histo_per_tissue_16 = np.zeros(img.shape[0:2])
    #
    #     if os.path.isfile(mask_path): #run image processing routine if mask exists
    #         mask = io.imread(mask_path)
    #         rows = img.shape[0]
    #         cols = img.shape[1]
    #         bg_row = 0
    #         bg_col = 0
    #         for r in range(nblocks_tile): #process blocks
    #             end_row = NPIX_BLOCK * (r + 1)
    #
    #             for c in range(nblocks_tile):
    #                 end_col = NPIX_BLOCK*(c + 1)
    #
    #                 # last block can be problematic, we have to check if the indices are inside the right range
    #                 if c == (nblocks_tile-1):
    #                     if end_col != cols:
    #                         end_col = cols
    #
    #                 if r == (nblocks_tile - 1):
    #                     if end_row != rows:
    #                         end_row = rows
    #
    #                 block_mask = mask[bg_row:end_row,bg_col:end_col]
    #                 block_img = img[bg_row:end_row,bg_col:end_col,:]
    #
    #                 nonzero_pix_mask = get_num_white(block_mask) #get number of non-zero pixels in mask
    #                 total_pix_block = rows*cols #total number of pixel in image block
    #                 npix_tissue_block = get_num_pix_tissue(block_img)
    #
    #                 percent_total = float(nonzero_pix_mask)/float(total_pix_block)
    #                 percent_tissue = 0.0 if npix_tissue_block == 0 else (float(nonzero_pix_mask)/float(npix_tissue_block))
    #
    #                 histo_per_tile[bg_row:end_row,bg_col:end_col] = percent_total*100
    #                 histo_per_tissue[bg_row:end_row,bg_col:end_col] = percent_tissue*100
    #
    #                 # histo_per_tile_16[bg_row:end_row,bg_col:end_col] = percent_total*100
    #                 # histo_per_tissue_16[bg_row:end_row,bg_col:end_col] = percent_tissue*100
    #
    #
    #
    #                 bg_col = end_col
    #
    #             bg_row = end_row
    #             bg_col = 0
    #
    #     #get min and max values for the entire slice, per amount of tissue
    #     if histo_per_tissue.min() < min_val_tissue:
    #         min_val_tissue = histo_per_tissue.min()
    #     if histo_per_tissue.max() > max_val_tissue:
    #         max_val_tissue = histo_per_tissue.max()
    #
    #     #get min and max values for the entire slice, per image block
    #     # if histo_per_tile.min() < min_val_block:
    #     #     min_val_block = histo_per_tile.min()
    #     # if histo_per_tile.max() > max_val_block:
    #     #     max_val_block = histo_per_tile.max()
    #
    #
    #     # hm1_name = os.path.join(hm_dir,img_name[0:-4]+'_hm_pertile.tif')
    #     # io.imsave(hm1_name,histo_per_tile_16.astype('float16'))
    #     # hm2_name = os.path.join(hm_dir,img_name[0:-4]+'_hm_pertissue.tif')
    #     # io.imsave(hm2_name,histo_per_tissue_16.astype('float16'))
    #
    #     # hm1_name = os.path.join(hm_dir,img_name[0:-4]+'_hm_pertile.npy')
    #     # np.save(hm1_name,histo_per_tile)
    #     hm2_name = os.path.join(hm_dir,img_name[0:-4]+'_hm_pertissue.npy')
    #     np.save(hm2_name,histo_per_tissue)
    #     print('File {} saved.'.format(hm2_name))
    #
    #
    # return min_val_tissue,max_val_tissue,min_val_block,max_val_block

def create_adj_dic(xml_tree):
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


def exec_compute_heatmap(case_dir,xml_file):

    #output folder
    hm_dir = os.path.join(case_dir, 'heat_map/hm_tiles_0.1')
    if not os.path.exists(hm_dir):
        os.mkdir(hm_dir)

    #tiles folder
    tiles_dir = os.path.join(case_dir,'heat_map/seg_tiles')
    seg_dir = os.path.join(case_dir,'heat_map/TAU_seg_tiles')

    xml_tree = ET.parse(xml_file)
    tiles_node = xml_tree.xpath('//Tiles')[0]
    pix_mm = int(tiles_node.attrib['pix_mm'])
    nblocks = int(tiles_node.attrib['nblocks_tile'])
    nblocks /= 0.1 #0.1mm blocks
    nblocks = int(nblocks)

    tiles_dic = create_adj_dic(xml_tree)

    min_val_t,max_val_t = compute_heatmap(tiles_dir,seg_dir, hm_dir, tiles_dic, nblocks, pix_mm)
    print('Min value per tissue {}/Max value per tissue {}.'.format(str(min_val_t),str(max_val_t)))


def main():
    if len(sys.argv) != 3:
        print('Usage: compute_heatmap_0.1 <root_dir> <xml_metadata_file>')
        exit()

    root_dir = str(sys.argv[1])
    xml_file = str(sys.argv[2])

    #xml_file = '/Volumes/SUSHI_HD/SUSHI/Posdoc/AVID/AV13/AT100#440/TAU_seg_tiles/tiles_metadata.xml'
    #hm_dir = '/Volumes/SUSHI_HD/SUSHI/Posdoc/AVID/AV13/AT100#440/hm_tiles'
    #xml_file = '/home/maryana/storage/Posdoc/AVID/AV13/AT100440/TAU_seg_tiles/tiles_metadata.xml'
    #hm_dir = '/home/maryana/storage/Posdoc/AVID/AV13/AT100440/hm_tiles_0.1'

    exec_compute_heatmap(root_dir,xml_file)


if __name__ == '__main__':
    main()
