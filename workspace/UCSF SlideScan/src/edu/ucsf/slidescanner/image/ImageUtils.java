package edu.ucsf.slidescanner.image;

import java.io.File;
import java.io.FilenameFilter;

import ij.process.ShortProcessor;

public class ImageUtils {
	
	
    public static final ShortProcessor rgb2gry(ShortProcessor r, ShortProcessor g, ShortProcessor b) {
        int height = (int)r.getHeight();
        int width = (int)r.getWidth();
        ShortProcessor img = new ShortProcessor(width,height);
        
        for(int y=0; y<height; y++) {
        	for(int x=0; x<width; x++) {
        		double rpix = (double)r.getPixel(x, y);
        		double gpix = (double)g.getPixel(x, y);
        		double bpix = (double)b.getPixel(x, y);
        		int grypix = (int)Math.round(0.2989*rpix + 0.5870*gpix + 0.1140*bpix);
        		img.putPixel(x, y, grypix);
        	}
        }
        
    	return img;
    }
	

    public static final int[] calculateLinearLUT(int min, int max) {
        int[] result = new int[256];
        for (int i = 0; i < result.length; ++i) {
           result[i] = (int) Math.max(0, Math.min(255,
                    256.0 * (i - min) / (max - min)));
        }
        return result;
     }
    
    public static final void createMasterDarkFrame(String dir) {
    	
    	File directory = new File(dir);
    	File [] files = directory.listFiles(new FilenameFilter() {
    	    public boolean accept(File dir, String name) {
    	        return name.endsWith(".tif");
    	    }
    	});

    	int nFiles = files.length;
    	int f = 0;
    	do {
    		
    	}while(f<nFiles);
    	
    }
}
