package PLI;

import java.util.logging.Level;
import java.util.logging.Logger;

import org.micromanager.MenuPlugin;
import org.micromanager.Studio;
import org.micromanager.data.Coords;
import org.micromanager.data.Datastore;
import org.micromanager.data.Image;
import org.scijava.plugin.Plugin;

import ij.IJ;
import ij.ImagePlus;
import ij.process.ImageProcessor;
import ij.process.ShortProcessor;

/**
 *
 * @author Maryana
 */
@Plugin(type = MenuPlugin.class)
public class PLIControl implements MenuPlugin {

    public static String menuName = "PLI Control";
    public static String tooltipDescription = "Controls the PLI apparatus";
    Studio studio_;
    private PLIControlUI mWindow_;
    private ImageHelper cameraHelper;

    @Override
    public void setContext(Studio app) {
        studio_ = app;
    }

    @Override
    public String getSubMenu() {
        return "Device Control";
    }

    @Override
    public void onPluginSelected() {
        try {
        	cameraHelper = new ImageHelper(studio_);
            mWindow_ = new PLIControlUI(studio_);
            studio_.events().registerForEvents(mWindow_);
            mWindow_.setControler(this);
            mWindow_.setAngle("0");
            mWindow_.setSlice("0");
            
            
        } catch (Exception e) {
            Logger.getLogger(PLIControlUI.class.getName()).log(Level.SEVERE, null, e);
            studio_.logs().showError(e);
        }
        //wbForm_.setVisible(true);
        mWindow_.getFrame().setVisible(true);
    }

    public void acquireImages(int nAngles)  {
    	try {
	    	Datastore ds = studio_.data().createRAMDatastore();
	    	studio_.displays().createDisplay(ds);
	    	
	    	//Acquire images.
	    	for(int ang=0; ang<nAngles; ang++) {
	    		mWindow_.setAngle(ang+"");
	    		mWindow_.getFrame().repaint();
	    		Image img = cameraHelper.snapImage();
	    		img = img.copyAtCoords(img.getCoords().copy().channel(ang).build());
	    		ds.putImage(img);
	    	}
	    	
	    	//Save images. Here I use IJ save methods so I can change the file names.
	    	saveImages(ds);
	    	
    	}catch(Exception e) {
    		e.printStackTrace();
    	}
    }
    
    public void doTestShot() {
    	try {
	    	Image img = cameraHelper.snapImage();
	    	studio_.displays().show(img);
    	}catch(Exception e) {
    		e.printStackTrace();
    	}	
    }
    
    public void saveImages(Datastore ds) {
    	//Save images. Here I use IJ save methods so I can change the file names.
    	Coords.CoordsBuilder coordBuilder = studio_.data().getCoordsBuilder();
    	int nImgs = ds.getNumImages();
    	for(int i=0; i<nImgs; i++) {
    	
    		int sliceNum = mWindow_.getSlice();
    		String folder = mWindow_.getDestFolder();
    		String filePrefix = mWindow_.getPrefix();

    		String fileName = new StringBuilder().append(folder).append("\\")
    				.append(filePrefix).append(sliceNum)
    				.append("_").append(i)
    				.append(".tif").toString();
	    	coordBuilder.channel(i);
	    	coordBuilder.stagePosition(0);
	    	coordBuilder.time(0);
	    	coordBuilder.z(0);
	    	Coords coord = coordBuilder.build();
    		Image toSave = ds.getImage(coord);
    		ShortProcessor spToSave = new ShortProcessor(toSave.getWidth(),toSave.getHeight(),(short[]) toSave.getRawPixelsCopy(),null);
    	    IJ.save(new ImagePlus("",(ImageProcessor)spToSave).duplicate(),fileName);
    	}
    	
    }
    
    @Override
    public String getName() {
        return menuName;
    }

    @Override
    public String getHelpText() {
        return "Controls the PLI Apparatus";
    }

    @Override
    public String getVersion() {
        return "1.0";
    }

    @Override
    public String getCopyright() {
        return "(C) 2017 UCSF Grinberg Lab";
    }

}
