package PLI;

import org.micromanager.Studio;
import org.micromanager.data.Coords;
import org.micromanager.data.Datastore;
import org.micromanager.data.Image;
import org.micromanager.display.DisplayWindow;

import ij.IJ;
import ij.ImagePlus;
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
    private final String PROP_SENSOR_CFA = "Color - Sensor CFA";
    private final String PROP_RED_SCALE = "Color - Red scale";
    
    private String cameraLabel;
    private boolean isColorCamera = false;
    private int CFAPattern = -1;
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
	        } else if (cfaPat.contains("BGGR")) {
	            CFAPattern = CFA_BGGR; 
	        } else if (cfaPat.contains("GRBG")) {
	            CFAPattern = CFA_GRBG;
	        } else if (cfaPat.contains("GBRG")) {
	            CFAPattern = CFA_GBRG;
	        } else {
	            CFAPattern = CFA_GRBG; 
	        }
		}	
	}

//    //snap a single image
//    private ShortProcessor snapImage() throws Exception {
//        try {
//            //core_.setExposure(Math.round(exposure));
//            core_.snapImage();
//            Object newImage = core_.getImage();
//            ShortProcessor CapturedImageShort = new ShortProcessor((int) core_.getImageWidth(), (int) core_.getImageHeight(), (short[]) newImage, null);
//            return CapturedImageShort;
//        } catch (Exception ex) {
//        	ex.printStackTrace();
//            throw new Exception("Acquisition failed");
//        }
//    }
    
   
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
    
    public Image snapImage() {
    	Image img = null;
    	try {
	    	//Datastore ds = studio_.data().createRAMDatastore();
	    	//studio_.displays().createDisplay(ds);
	    	//double exp = core_.getExposure();
	    	img = studio_.live().snap(false).get(0);
	    	//ds.putImage(img);
	    	if(isColorCamera) {
	    		ShortProcessor imgOrig = new ShortProcessor(img.getWidth(),img.getHeight(),(short[]) img.getRawPixelsCopy(),null);
	    		//ShortProcessor R = debayerRedChannel(imgOrig);
	    		ShortProcessor G = debayerGreenChannel(imgOrig);
	    		//ShortProcessor B = debayerBlueChannel(imgOrig);
	    		//Image imgR = studio_.data().ij().createImage(R,img.getCoords(),img.getMetadata());
	    		//Image imgG = studio_.data().ij().createImage(G,img.getCoords(),img.getMetadata());
	    		img = studio_.data().ij().createImage(G,img.getCoords(),img.getMetadata());
	    		//Image imgB = studio_.data().ij().createImage(B,img.getCoords(),img.getMetadata());
	    		//studio_.displays().show(imgR);
	    		//studio_.displays().show(imgG);
	    		//studio_.displays().show(imgB);
	    		//IJ.save(new ImagePlus("",(ImageProcessor)R).duplicate(),"C:\\Users\\Maryana\\red.tif");
	    		//IJ.save(new ImagePlus("",(ImageProcessor)G).duplicate(),"C:\\Users\\Maryana\\gree.tif");
	    		//IJ.save(new ImagePlus("",(ImageProcessor)B).duplicate(),"C:\\Users\\Maryana\\blue.tif");
	    	}

    	}catch(Exception e) {
    		e.printStackTrace();
    	}
		return img;   	
    }
    
    public void snapImage(int pos) {	
    	try {
	    	Image img = snapImage();
	    	img = img.copyAtCoords(img.getCoords().copy().channel(pos).build());
			this.ds.putImage(img);
    	}catch(Exception e) {
    		e.printStackTrace();
    	}
    }
    
    public void createDataStore() {
    	if(this.ds == null) { //create new datastore
        	this.ds = studio_.data().createRewritableRAMDatastore();
        	//this.ds = studio_.data().createRewritableRAMDatastore();      		
        	this.dw = studio_.displays().createDisplay(this.ds);              	
    	}
    }
    
    public void doTestShot() {
    	try {
	    	Image img = snapImage();
	    	studio_.displays().show(img);
    	}catch(Exception e) {
    		e.printStackTrace();
    	}	
    }
    
    public void saveImages(int sliceNum, String folder, String filePrefix) {
    	//Save images. Here I use IJ save methods so I can change the file names.
    	Coords.CoordsBuilder coordBuilder = studio_.data().getCoordsBuilder();
    	int nImgs = this.ds.getNumImages();
    	for(int i=0; i<nImgs; i++) {
    		String fileName = new StringBuilder().append(folder).append("\\")
    				.append(filePrefix).append(sliceNum)
    				.append("_").append(i)
    				.append(".tif").toString();
	    	coordBuilder.channel(i);
	    	coordBuilder.stagePosition(0);
	    	coordBuilder.time(0);
	    	coordBuilder.z(0);
	    	Coords coord = coordBuilder.build();
    		Image toSave = this.ds.getImage(coord);
    		ShortProcessor spToSave = new ShortProcessor(toSave.getWidth(),toSave.getHeight(),(short[]) toSave.getRawPixelsCopy(),null);
    	    IJ.save(new ImagePlus("",(ImageProcessor)spToSave).duplicate(),fileName);
    	}
    	
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
