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
    private CameraController camCtr;
    private PolarimeterController polCtr;
    public static final int NUM_ANGLES = 18;
    
    private boolean max_reached = false;

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
        	camCtr = new CameraController(studio_);
        	polCtr = new PolarimeterController(studio_, this);
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
    
    public void doTestShot() {
    	
    }
    
    //run PLI acquisition
//    public void runAcquisition(int nAngles)  {
//    	try {	    	
//	    	//camCtr.createDataStore();	    	
//	    	//Acquire images.
//	    	for(int ang=0; ang<nAngles; ang++) {
//	    		//camCtr.snapImage();
//	    		polCtr.doRotation();
//	    	}	    	
//	    	//Save images. Here I use IJ save methods so I can change the file names.
//	    	String folder = mWindow_.getDestFolder();
//	    	int sliceNum = mWindow_.getSlice();
//	    	String prefix = mWindow_.getPrefix();
//	    	//camCtr.saveImages(sliceNum, folder, prefix);
//	    	
//    	}catch(Exception e) {
//    		e.printStackTrace();
//    	}
//    }
    
    public void runAcquisition(int nAngles) {
    	Thread worker = new PolWorker("Polworker1");
    	worker.start();
    }
    
    public void addTextOutput(String txt) {
    	String oldTxt = mWindow_.getTextOutput().getText();
    	String newTxt = oldTxt +"\n"+ txt;
    	mWindow_.getTextOutput().setText(newTxt);    	
    }
    
    //send filters to home position
    public void goHome() {
    	polCtr.goHome();
    	max_reached = false;
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
        return "(C) 2017 Maryana Alegro - UCSF Grinberg Lab";
    }
        
    
    //
    //edu.ucsf.slidescanner.image acquisition thread
    //
    private class PolWorker extends Thread{
    	
    	PolWorker(String name){
    		super(name);
    	}
    	
        //run PLI acquisition
        private void runAcquisition(int nAngles)  {
        	
        	if(max_reached) {
        		addTextOutput("You must reset filter positions.");
        		return;
        	}
        	
        	try {	    	
    	    	camCtr.createDataStore();	    	
    	    	//Acquire images.
    	    	for(int ang=0; ang<nAngles-1; ang++) { 
    	    		Thread.sleep(200);
    	    		camCtr.snapImage(ang);	
    	    		polCtr.doRotation();
    	    	}	    
    	    	
    	    	//Save images. Here I use IJ save methods so I can change the file names.
    	    	if(!max_reached) {
	    	    	String folder = mWindow_.getDestFolder();
	    	    	int sliceNum = mWindow_.getSlice();
	    	    	String prefix = mWindow_.getPrefix();
	    	    	camCtr.saveImages(sliceNum, folder, prefix);
    	    	}
    	    	max_reached = true;
    	    	
        	}catch(Exception e) {
        		e.printStackTrace();
        	}
        }
    	
    	public void run() {
    		runAcquisition(PLIControl.NUM_ANGLES);
    	}

    }

}


