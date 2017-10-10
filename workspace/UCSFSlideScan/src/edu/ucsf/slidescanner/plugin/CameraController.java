package edu.ucsf.slidescanner.plugin;

import java.io.File;
import java.util.List;

import org.micromanager.Studio;
import org.micromanager.data.Coords;
import org.micromanager.data.Datastore;
import org.micromanager.data.Image;
import org.micromanager.data.Metadata;
import org.micromanager.data.Metadata.MetadataBuilder;
import org.micromanager.display.DisplaySettings;
import org.micromanager.display.DisplaySettings.ContrastSettings;

import edu.ucsf.slidescanner.calibration.LensConfig;
import edu.ucsf.slidescanner.image.ImageUtils;

import org.micromanager.display.DisplayWindow;

import ij.IJ;
import ij.ImagePlus;
import ij.process.ByteProcessor;
import ij.process.ColorProcessor;
import ij.process.ImageProcessor;
import ij.process.ShortProcessor;
import mmcorej.CMMCore;

/**
*
* @author Maryana
*/

public class CameraController {
	
    private static final int CFA_RGGB = 0;
    private static final int CFA_BGGR = 1;
    private static final int CFA_GRBG = 2;
    private static final int CFA_GBRG = 3;
    
    private static final String STR_RGGB = "R-G-G-B";
    private static final String STR_BGGR = "B-G-G-R";
    private static final String STR_GRBG = "G-R-B-G";
    private static final String STR_GBRG = "G-B-R-G";
    
    private static final String PROP_SENSOR_CFA = "Color - Sensor CFA";
    private static final String PROP_ALG_CFA_AUTO = "Color - Algorithm CFA Auto";
    private static final String PROP_ALG_CFA = "Color - Algorithm CFA";
    private static final String PROP_RED_SCALE = "Color - Red scale";
    private static final String PROP_GREEN_SCALE = "Color - Green scale";
    private static final String PROP_BLUE_SCALE = "Color - Blue scale"; 
    private static final String PROP_PIXELTYPE = "PixelType";
    private static final String PROP_COLOR = "Color";
    private static final String PROP_XDIM = "X-dimension";
    private static final String PROP_YDIM = "Y-dimension";
    
    private static final String RAW_DIR = "raw";
    private static final String AUTO_DIR = "auto";
    private static final String CORRECTED_DIR = "corrected";
    
    public static final int MAX_NUMIMG_MEM = 10;
    
    public static final int[] STD_SENSOR_SIZE = {2688,2200};
    public static final int[] STD_SENSOR_ORIG = {0,0};
    
    private String cameraLabel;
    private boolean isColorCamera = false;
    private int CFAPattern = -1;
    private String CFAMask = STR_GBRG;
	private CMMCore core_;
	private Studio studio_;
	private Datastore ds = null;
	private DisplayWindow dw = null;
	
	public CameraController(Studio gui) {
		studio_ = gui;
		core_ = studio_.core();
		initCameraSettings();		
	}
	
	public void initCameraSettings() {
		cameraLabel = core_.getCameraDevice();
		isColorCamera = this.isColor();
		if(isColorCamera) {
			String cfaPat = this.getCFAPattern();
	        if (cfaPat.contains("RGGB")) {
	            CFAPattern = CFA_RGGB;
	            CFAMask = STR_RGGB;
	        } else if (cfaPat.contains("BGGR")) {
	            CFAPattern = CFA_BGGR; 
	            CFAMask = STR_BGGR; 
	        } else if (cfaPat.contains("GRBG")) {
	            CFAPattern = CFA_GRBG;
	            CFAMask = STR_GRBG;
	        } else if (cfaPat.contains("GBRG")) {
	            CFAPattern = CFA_GBRG;
	            CFAMask = STR_GBRG;
	        } else {
	            CFAPattern = CFA_GRBG; 
	            CFAMask = STR_GRBG;
	        }
		}	
	}
	
	public void setSensorROI(LensConfig lens) {		
		try {
			int[] currSize = new int[2];
			currSize[0] = (int)Math.round(core_.getROI().getWidth());	
			currSize[1] = (int)Math.round(core_.getROI().getHeight());
			if(lens.getSensorCfg().W() != currSize[0] || lens.getSensorCfg().H() != currSize[1]) {			
				int x = lens.getSensorCfg().oX();
				int y = lens.getSensorCfg().oY();
				int xSize = lens.getSensorCfg().W();
				int ySize = lens.getSensorCfg().H();
			    studio_.live().setSuspended(true);
				core_.setROI(x, y, xSize, ySize);
			    studio_.app().refreshGUI();
			    studio_.live().setSuspended(false);
			}
		}catch(Exception e) {
			e.printStackTrace();
		}
	}    
   
    private String getCFAPattern() {
        String cfaPattern;
        try {
            cfaPattern = core_.getProperty(cameraLabel, PROP_SENSOR_CFA);            
        } catch (Exception ex) {
            cfaPattern = "GRBG";
        }
        
        return cfaPattern;
    }
    
    private boolean isColor() {
        boolean isColor = true;
        try {
            if (!core_.hasProperty(cameraLabel, PROP_RED_SCALE)) {
                isColor = false;
            }
        } catch (Exception ex) {
            isColor = false;
        }

        return isColor;
    }
    
    public int[] getSensorSize() {
    	int[] dims = null; //X=cols,Y=rows
        try {
            String x = core_.getProperty(cameraLabel, PROP_XDIM);     
            String y = core_.getProperty(cameraLabel, PROP_YDIM); 
            
            dims = new int[2];
            dims[0] = Integer.parseInt(x); //cols
            dims[1] = Integer.parseInt(y); //rows
        } catch (Exception ex) {
        	ex.printStackTrace();
        }
        
        return dims;
    }
    
    public void initColorMode(double rs, double gs, double bs) throws Exception{
    	//core_.setProperty(cameraLabel, PROP_ALG_CFA, "OFF");
    	studio_.live().setSuspended(true);
        core_.setProperty(cameraLabel, PROP_RED_SCALE, rs);
        core_.setProperty(cameraLabel, PROP_GREEN_SCALE, gs);
        core_.setProperty(cameraLabel, PROP_BLUE_SCALE, bs);
        core_.setProperty(cameraLabel, PROP_COLOR, "ON");
        core_.setProperty(cameraLabel, PROP_ALG_CFA, CFAMask);
        studio_.app().refreshGUI();
        studio_.live().setSuspended(false);
    }
    
    public void initBWMode() throws Exception{
    	studio_.live().setSuspended(true);
        core_.setProperty(cameraLabel, PROP_COLOR, "OFF");
        studio_.app().refreshGUI();
        studio_.live().setSuspended(false);
    }
    
    public Image snapImage() {
    	Image img = null;
    	try {
	    	img = studio_.live().snap(false).get(0);
	    	if(isColorCamera) {	
	    		int nChannels = img.getNumComponents();
	    		if(nChannels == 1) {
	    			ShortProcessor imgOrig = new ShortProcessor(img.getWidth(),img.getHeight(),(short[]) img.getRawPixelsCopy(),null);
		    		ShortProcessor R = debayerRedChannel(imgOrig);
		    		ShortProcessor G = debayerGreenChannel(imgOrig);
		    		ShortProcessor B = debayerBlueChannel(imgOrig);
		    		ShortProcessor gry = ImageUtils.rgb2gry(R, G, B);
		    		img = studio_.data().ij().createImage(gry,img.getCoords(),img.getMetadata());
	    		}	    		
	    	}
    	}catch(Exception e) {
    		e.printStackTrace();
    	}
		return img;   	
    }
    
    public void doTestShot(String dir) {
    	try {
	    	createDataStore();
	    	acquireImage(0);
	    	saveImages(dir,0);
    	}catch(Exception e) {
    		e.printStackTrace();
    	}
    }
    
    public void doTestShotRGB(String dir) {
    	try {		   		
    		  		
    		String dir2 = "C:\\Users\\Maryana\\Desktop\\test_stitch\\test2";
    		initColorMode(2.35, 1.00, 1.36);
    		core_.setExposure(90);
    		createDataStore();
    		acquireImage(0);
    		saveImagesRGB(dir2, 0, 1,true, false);
    		
//        	Coords.CoordsBuilder coordBuilder = studio_.data().getCoordsBuilder();
//    	    coordBuilder.channel(0);
//    	    coordBuilder.stagePosition(0);
//    	    coordBuilder.time(0);
//    	    coordBuilder.z(0);
//    	    Coords coord = coordBuilder.build();
//        	Image img = ds.getImage(coord);
//
//        	ImageProcessor ip = studio_.data().ij().createProcessor(img);
//        	if(ip.getNChannels() > 1) {
//        		ColorProcessor cip = ip.convertToColorProcessor();
//        		DisplaySettings dset = studio_.displays().getCurrentWindow().getDisplaySettings();
//        		ContrastSettings[] csets = dset.getChannelContrastSettings();
//        		ContrastSettings cset = csets[0];
//        		
//        		Double[] gammas = cset.getContrastGammas();
//        		Integer[] maxes = cset.getContrastMaxes();
//        		Integer[] mins = cset.getContrastMins();
//        		for(int c=0; c<cip.getNChannels(); c++) {
//        			Double gamma = cset.getSafeContrastGamma(c, 1.0);
//        			Integer max = cset.getSafeContrastMax(c, maxes[c]);
//        			Integer min = cset.getSafeContrastMin(c, mins[c]);	
//        			
//        			int[] lut = ImageUtils.calculateLinearLUT(min, max);
//        			int idx = 1 << (2 - c);
//        			cip.applyTable(lut, idx);
//        		}
//    			String fileName = dir2+"\\test_RGB.tif";
//    			IJ.save(new ImagePlus("",cip).duplicate(),fileName);
//        	}

    	}catch(Exception e) {
    		e.printStackTrace();
    	}
    }
    
    public int getNumImgs() {
    	if(this.ds != null) {
    		return this.ds.getNumImages();
    	}
    	return -1;
    }
    
    public void createDataStore(String dir) throws Exception{
    	if(this.ds == null) { //create new datastore
        	this.ds = studio_.data().createSinglePlaneTIFFSeriesDatastore(dir);
        	this.dw = studio_.displays().createDisplay(this.ds);        	
    	}else { //clean old DS, create a new one - I made this to save memory
    		this.dw.requestToClose();
    		studio_.displays().closeDisplaysFor(this.ds);
    		this.ds = studio_.data().createSinglePlaneTIFFSeriesDatastore(dir);
        	this.dw = studio_.displays().createDisplay(this.ds);
    	}
    }
    
    
    public void createDataStore() {
    	if(this.ds == null) { //create new datastore
        	this.ds = studio_.data().createRewritableRAMDatastore();
        	//this.ds = studio_.data().createRewritableRAMDatastore();      		
        	this.dw = studio_.displays().createDisplay(this.ds);      
        	
    	}else { //clean old DS, create a new one - I made this to save memory
    		//studio_.displays().closeDisplaysFor(this.ds);
    		this.dw.requestToClose();
    		this.dw.forceClosed();
        	this.ds = studio_.data().createRewritableRAMDatastore();
        	this.dw = studio_.displays().createDisplay(this.ds);
    	}
    }
    
    public void freezeDataStore() {
    	if(this.ds != null) {
    		this.ds.freeze();
    	}
    }
    
    public void acquireImage(int pos)  {
    	try {
	    	Image img = snapImage();	    
	    	img = img.copyAtCoords(img.getCoords().copy().stagePosition(pos).build());	  
	    	//img = img.copyWithMetadata(img.getMetadata().copy().positionName("position").build());
	    	//Metadata.MetadataBuilder mBuilder = studio_.data().getMetadataBuilder();	  
	    	//img.copyWith(img.getCoords().copy().stagePosition(pos).build(),img.getMetadata().copy().positionName("").build());
	    	this.ds.putImage(img);	    	
	    	System.gc();
    	}catch(Exception e) {
    		e.printStackTrace();
    	}
    }
     
    public void saveImages(String folder, int initPos) {    	
    	//Save images. Here I use IJ save methods so I can change the file names.
    	Coords.CoordsBuilder coordBuilder = studio_.data().getCoordsBuilder();
    	int nImgs = ds.getNumImages();
    	for(int i=0; i<nImgs; i++) {
    		String fileName = new StringBuilder().append(folder).append("\\")
    				.append("tile_").append((initPos+i))
    				.append(".tif").toString();
	    	coordBuilder.channel(0);
	    	coordBuilder.stagePosition((initPos+i));
	    	coordBuilder.time(0);
	    	coordBuilder.z(0);
	    	Coords coord = coordBuilder.build();
    		Image toSave = ds.getImage(coord);
	    	ImageProcessor spToSave = new ShortProcessor(toSave.getWidth(),toSave.getHeight(),(short[]) toSave.getRawPixelsCopy(),null);
	    	ByteProcessor byteImage = spToSave.convertToByteProcessor(); //convert channel to 8bits
	    	IJ.save(new ImagePlus("",(ImageProcessor)byteImage).duplicate(),fileName);
    	}	
    }
    
    public void saveImagesRGB(String folder, int initPos, int totalImg, boolean saveRaw, boolean saveAuto) {    	
    	//create folders
    	String rawImgDir = "";
    	String autoImgDir = "";
    	if(saveRaw) {
    		rawImgDir = new StringBuilder().append(folder).append("\\").append(RAW_DIR).toString();
    		(new File(rawImgDir)).mkdirs();
    	}
    	if(saveAuto) {
    		autoImgDir = new StringBuilder().append(folder).append("\\").append(AUTO_DIR).toString();
    		(new File(autoImgDir)).mkdirs();
    	}

    	Coords.CoordsBuilder coordBuilder = studio_.data().getCoordsBuilder();
    	int nImgs = ds.getNumImages();
    	for(int i=0; i<nImgs; i++) {
    		
    		if(initPos+i >= totalImg) { //check if we are not saving duplicated images
    			break;
    		}

	    	coordBuilder.channel(0);
	    	coordBuilder.stagePosition(i);
	    	coordBuilder.time(0);
	    	coordBuilder.z(0);
	    	Coords coord = coordBuilder.build();
    		Image img = ds.getImage(coord);
    		
    		//save raw edu.ucsf.slidescanner.image version 
	    	if(saveRaw) {	
	    		ImageProcessor ip = studio_.data().ij().createProcessor(img);
	    		ImageProcessor ip2 = (new ImagePlus("",ip)).duplicate().getProcessor();
	    		
	    		String fileName = new StringBuilder().append(rawImgDir).append("\\")
	    				.append("tile_").append((initPos+i))
	    				.append(".tif").toString();    		 
	        	IJ.save(new ImagePlus("",ip2).duplicate(),fileName);
	    	}
    		
    		//save histogram autostrech version 
	    	if(saveAuto) {	
	    		ImageProcessor ip = studio_.data().ij().createProcessor(img);
	    		ImageProcessor ip2 = (new ImagePlus("",ip)).duplicate().getProcessor();
	    		
	    		String fileName = new StringBuilder().append(autoImgDir).append("\\")
	    				.append("tile_").append((initPos+i))
	    				.append(".tif").toString();    		
	        	ColorProcessor cip = ip2.convertToColorProcessor();
	        	List<DisplayWindow> dwins = studio_.displays().getAllImageWindows();
	        	DisplayWindow currwin = dwins.get(0);
	        	DisplaySettings dsets = currwin.getDisplaySettings();
	        	ContrastSettings[] csets = dsets.getChannelContrastSettings();
	        	ContrastSettings cset = csets[0];
        		
	        	Double[] gammas = cset.getContrastGammas();
	        	Integer[] maxes = cset.getContrastMaxes();
	        	Integer[] mins = cset.getContrastMins();
	        	for(int c=0; c<cip.getNChannels(); c++) {
        		Double gamma = cset.getSafeContrastGamma(c, 1.0);
	        		Integer max = cset.getSafeContrastMax(c, maxes[c]);
	        		Integer min = cset.getSafeContrastMin(c, mins[c]);	

	        		int[] lut = ImageUtils.calculateLinearLUT(min, max);
	        		int idx = 1 << (2 - c);
	        		cip.applyTable(lut, idx);
	        	}	 
	        	IJ.save(new ImagePlus("",cip).duplicate(),fileName);
	    	}    		
    	}	
    }
    
    public void acquireDarkFrames(int numFrames, String dir) {
    	createDataStore();
    	for(int f=0; f<numFrames; f++) {
    		acquireImage(f);
    	}
    	saveImagesRGB(dir, 0, 1,true, false);	
    }

    private ShortProcessor debayerGreenChannel(ShortProcessor imgOrig) {
    	
        int height = (int)imgOrig.getHeight();
        int width = (int)imgOrig.getWidth();

        ShortProcessor g = new ShortProcessor(width,height);
        ShortProcessor ip = imgOrig;
        int one;

        if (CFAPattern == CFA_GRBG || CFAPattern == CFA_GBRG) {

            for (int y = 0; y < height; y += 2) {
                for (int x = 0; x < width; x += 2) {
                    one = ip.getPixel(x, y);
                    g.putPixel(x, y, one);
                    g.putPixel(x + 1, y, one);
                }
            }
            for (int y = 1; y < height; y += 2) {
                for (int x = 1; x < width; x += 2) {
                    one = ip.getPixel(x, y);
                    g.putPixel(x, y, one);
                    g.putPixel(x + 1, y, one);
                }
            }


        } else if (CFAPattern == CFA_RGGB || CFAPattern == CFA_BGGR) {

            for (int y = 0; y < height; y += 2) {
                for (int x = 1; x < width; x += 2) {
                    one = ip.getPixel(x, y);
                    g.putPixel(x, y, one);
                    g.putPixel(x + 1, y, one);
                }
            }
            for (int y = 1; y < height; y += 2) {
                for (int x = 0; x < width; x += 2) {
                    one = ip.getPixel(x, y);
                    g.putPixel(x, y, one);
                    g.putPixel(x + 1, y, one);
                }
            }

        }
        
        return g;
    }
    
    private ShortProcessor debayerRedChannel(ShortProcessor imgOrig) {
    	
        int height = (int)imgOrig.getHeight();
        int width = (int)imgOrig.getWidth();
        ShortProcessor r = new ShortProcessor(width,height);
        ShortProcessor ip = imgOrig;
        int one;

        if (CFAPattern == CFA_GRBG || CFAPattern == CFA_GBRG) {

            for (int y = 0; y < height; y += 2) {
                for (int x = 1; x < width; x += 2) {
                    one = ip.getPixel(x, y);
                    r.putPixel(x, y, one);
                    r.putPixel(x + 1, y, one);
                    r.putPixel(x, y + 1, one);
                    r.putPixel(x + 1, y + 1, one);
                }
            }

        } else if (CFAPattern == CFA_RGGB || CFAPattern == CFA_BGGR) {

            for (int y = 1; y < height; y += 2) {
                for (int x = 1; x < width; x += 2) {
                    one = ip.getPixel(x, y);
                    r.putPixel(x, y, one);
                    r.putPixel(x + 1, y, one);
                    r.putPixel(x, y + 1, one);
                    r.putPixel(x + 1, y + 1, one);
                }
            }
        }
        
        return r;
    }
    
private ShortProcessor debayerBlueChannel(ShortProcessor imgOrig) {
    	
        int height = (int)imgOrig.getHeight();
        int width = (int)imgOrig.getWidth();
        ShortProcessor b = new ShortProcessor(width,height);
        ShortProcessor ip = imgOrig;
        int one;

        if (CFAPattern == CFA_GRBG || CFAPattern == CFA_GBRG) {
            for (int y = 1; y < height; y += 2) {
                for (int x = 0; x < width; x += 2) {
                    one = ip.getPixel(x, y);
                    b.putPixel(x, y, one);
                    b.putPixel(x + 1, y, one);
                    b.putPixel(x, y + 1, one);
                    b.putPixel(x + 1, y + 1, one);
                }
            }

        } else if (CFAPattern == CFA_RGGB || CFAPattern == CFA_BGGR) {
            for (int y = 0; y < height; y += 2) {
                for (int x = 0; x < width; x += 2) {
                    one = ip.getPixel(x, y);
                    b.putPixel(x, y, one);
                    b.putPixel(x + 1, y, one);
                    b.putPixel(x, y + 1, one);
                    b.putPixel(x + 1, y + 1, one);
                }
            }
        }
        
        return b;
    }
    

}
