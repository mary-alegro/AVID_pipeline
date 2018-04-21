import os
import sys
import skimage.io as io
import tifffile
import glob
import gdal
import numpy as np


class TiffTileLoader(object):

    def __init__(self, p1MM, p5MM):
        self.ds = None
        gdal.UseExceptions()
        #default values
        # self.PIX_1MM = 819  # 1mm= 819 pixels
        # self.PIX_5MM = 4095  # 5mm = 4095 pixels
        self.PIX_1MM = p1MM
        self.PIX_5MM = p5MM
        self.coords = []


    def open_file(self,file_name):
        self.ds = gdal.Open(file_name)


    def get_file_dim(self):
        x = self.ds.RasterXSize
        y = self.ds.RasterYSize
        z = self.ds.RasterCount

        return [x,y,z]


    def get_tile(self, x, y, xsize, ysize):
        rCh = self.ds.GetRasterBand(1)
        gCh = self.ds.GetRasterBand(2)
        bCh = self.ds.GetRasterBand(3)

        R = rCh.ReadAsArray(x, y, xsize,ysize)
        G = gCh.ReadAsArray(x, y, xsize, ysize)
        B = bCh.ReadAsArray(x, y, xsize, ysize)

        s = R.shape
        img = np.concatenate((R.reshape(s[0],s[1],1),G.reshape(s[0],s[1],1),B.reshape(s[0],s[1],1)),axis=2)

        return img


    def compute_tile_coords(self,grid_rows,grid_cols):

        grid_rows = float(grid_rows)
        grid_cols = float(grid_cols)

        size = self.get_file_dim()

        #compute row coords
        tile_coords = np.zeros([int(grid_rows*grid_cols),4]) #[row_upper_left, col_upper_left, row_lower_right, col_lower_right]

        row_off = np.floor(size[0]/grid_rows) #initial block size
        row_off = int(row_off)
        row_rem = size[0] % grid_rows
        row_add = np.zeros([int(grid_rows),1]) #correction factor
        if row_rem > 0: # we have to compensate for uneven block sizes (reminder > 0). Make the last block in the row bigger since it's more likely to be background.
            row_add[-1] = row_rem

        col_off = np.floor(size[1]/grid_cols) #initial block size
        col_off = int(col_off)
        col_rem = size[1] % grid_cols
        col_add = np.zeros([int(grid_cols),1]) #correction factor
        if col_rem > 0:
            col_add[-1] = col_rem

        tile_ind = 0
        up_row = 0
        up_col = 0
        for row_count in range(int(grid_rows)):
            for col_count in range(int(grid_cols)):
                #left upper corner
                tile_coords[tile_ind,0] = up_row
                tile_coords[tile_ind,1] = up_col

                low_row = up_row + row_off + row_add[row_count]
                low_col = up_col + col_off + col_add[col_count]
                tile_coords[tile_ind,2] = low_row
                tile_coords[tile_ind,3] = low_col

                up_col = ((col_count+1) * col_off) + np.sum(col_add[0:col_count + 1])
                tile_ind += 1

            up_row = ((row_count+1) * row_off) + np.sum(row_add[0:row_count + 1])

        self.coords = tile_coords
        #return tile_coords


    def get_tile_iterator(self):
        iterator = TileIterator(self.ds,self.coords)
        return iterator


class TileIterator(object):

    def __init__(self,ds,tile_coords):
        self.ds = ds
        self.tile_coords = tile_coords
        self.nTiles = tile_coords.shape[0]
        self.curr = 0

        self.rCh = self.ds.GetRasterBand(1)
        self.gCh = self.ds.GetRasterBand(2)
        self.bCh = self.ds.GetRasterBand(3)

    def __iter__(self):
        return self

    def next(self):
        if self.curr >= self.nTiles:
            raise StopIteration
        else:
            r1,c1,r2,c2 = self.tile_coords[self.curr]
            ysize = r2-r1
            xsize = c2-c1
            tile = self.get_tile(c1,r1,xsize,ysize)
            self.curr += 1
            return tile


    def get_tile(self, x, y, xsize, ysize):

        x = int(x)
        y = int(y)
        xsize = int(xsize)
        ysize = int(ysize)

        R = self.rCh.ReadAsArray(x, y, xsize,ysize)
        G = self.gCh.ReadAsArray(x, y, xsize, ysize)
        B = self.bCh.ReadAsArray(x, y, xsize, ysize)

        s = R.shape
        img = np.concatenate((R.reshape(s[0],s[1],1),G.reshape(s[0],s[1],1),B.reshape(s[0],s[1],1)),axis=2)

        return img











