package edu.ucsf.slidescanner.plugin;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

import javax.swing.JOptionPane;

import org.micromanager.MenuPlugin;
import org.micromanager.Studio;
import org.scijava.plugin.Plugin;
import org.scijava.plugin.SciJavaPlugin;

import edu.ucsf.slidescanner.calibration.LensConfig;
import edu.ucsf.slidescanner.calibration.WBSettings;

/**
 *
 * @author Maryana Alegro
 */
@Plugin(type = MenuPlugin.class)
public class SlideScan implements MenuPlugin, SciJavaPlugin {

    public static String menuName = "Large-Slide Scan";
    public static String tooltipDescription = "Controls the Large Slide Scanner";
    Studio studio_;
    private SlideScanUI mWindow_;
    private StageController stageCtr;
    private CameraController camCtr;
    private int A[] = new int[2];
    private int B[] = new int[2];
    //private int[] WB = new int[3]; //white balance point in RGB 
    private boolean shouldSaveRaw = true;
    private boolean shouldSaveAuto = false;
    private LensConfig currLensCfg;
    

    @Override
    public void setContext(Studio app) {
        studio_ = app;
        System.out.println("### Large Slide Scanner Loaded ###");
    }

    @Override
    public String getSubMenu() {
        return "Device Control";
    }

    @Override
    public void onPluginSelected() {
        try {
        	camCtr = new CameraController(studio_);
        	stageCtr = new StageController(studio_,this);        	
            mWindow_ = new SlideScanUI(studio_, this);
            studio_.events().registerForEvents(mWindow_);            
            mWindow_.setControler(this);            
            if(mWindow_.isColorModeOn()) {
            	WBSettings wb = mWindow_.getWBInfo();
            	if(wb != null) {
            		camCtr.initColorMode(wb.getR(), wb.getG(), wb.getB());
            	}else {
            		System.out.println("There was a problem initializing the color mode.");
            	}
            }
            
            //stageHelper.resetStage();
            
        } catch (Exception e) {
            Logger.getLogger(SlideScanUI.class.getName()).log(Level.SEVERE, null, e);
            studio_.logs().showError(e);
        }
        //wbForm_.setVisible(true);
        mWindow_.getFrame().setVisible(true);
    }

    public StageController getStageController() {
    	return stageCtr;
    }    
    
    @Override
    public String getName() {
        return menuName;
    }

    @Override
    public String getHelpText() {
        return "Controls the Large Slide Scanner";
    }

    @Override
    public String getVersion() {
        return "0.01";
    }

    @Override
    public String getCopyright() {
        return "(C) 2017 UCSF Grinberg Lab";
    }
    
    public void acquireImages(double[] FOV, int overlap, String folder)  {
    	//String folder = mWindow_.getDestFolder();
    	//stageHelper.runAcquisition(FOV, A, B, overlap, cameraHelper, folder);
    	Thread worker = new ScanWorker("Scanworker1",  FOV, A, B, overlap, folder, shouldSaveRaw, shouldSaveAuto);
    	mWindow_.setWorker(worker);
    	worker.start();
    }
    
    public void acquireDarkFrames(int nF,String dir) {
    	camCtr.acquireDarkFrames(nF, dir);
    }
    
    public void shotTestImage(String folder) {
    	camCtr.doTestShotRGB(folder);
    }
    
    public void setNumTiles(String str) {
    	mWindow_.setNumTiles(str);
    }
    
    public void setAcqTime(String str) {
    	mWindow_.setAcqTime(str);
    }
       
    public int[] setCoordsA() throws Exception {
    	int[]pos = stageCtr.getStagePos();
    	A[0] = pos[0];
    	A[1] = pos[1];
    	return A;
    }
    
    public int[] setCoordsB() throws Exception {
    	int[]pos = stageCtr.getStagePos();
    	B[0] = pos[0];
    	B[1] = pos[1];
    	return B;
    }
    
    public void setCoordsA(int[] a) {
    	this.A[0] = a[0];
    	this.A[1] = a[1];	
    }
    
    public void setCoordsB(int[] b) {
    	this.B[0] = b[0];
    	this.B[1] = b[1];
    }
    
    public int[] getStagePosition() throws Exception{
    	int[]pos = stageCtr.getStagePos();
    	return pos;
    }
    
    public boolean isColorModeOn() {
    	return mWindow_.isColorModeOn();
    }
    
    public void setColorON(double r, double g, double b) {
    	try {
    		camCtr.initColorMode(r, g, b);
    	}catch(Exception e) {
    		e.printStackTrace();
    	}
    }
    
    public void setColorOFF() {
    	try {
    		camCtr.initBWMode();
    	}catch(Exception e) {
    		e.printStackTrace();
    	}
    }    
    
    public void setShouldSaveRaw(boolean b) {
    	this.shouldSaveRaw = b;
    }
    
    public void setShouldSaveAuto(boolean b) {
    	this.shouldSaveAuto = b;
    }
    
    public void restartJoystick() {
    	try {
    		stageCtr.restartJoystick();
    	}catch(Exception e) {
    		e.printStackTrace();
    	}
    }
    
    public void setCurrLensCfg(LensConfig lens) {
    	this.currLensCfg = lens;    
    	camCtr.setSensorROI(this.currLensCfg);
    }
    
    public LensConfig getCurreLensCfg() {
    	return this.currLensCfg;
    }
    
    public void saveMetadata() {    	
    	String outDir = mWindow_.getDestFolder();
    	String imgDir = "Folder: " + outDir;
    	String sensorSize = "Sensor: (" + this.currLensCfg.getSensorCfg().W() + "," 
    					+ this.currLensCfg.getSensorCfg().H() + ")";
    	String pixSize = "Pixel: " + this.currLensCfg.getPixSize();
    	String pixSizeCts = "Pixel_cts: " + this.currLensCfg.getPixSizeCts();
    	String overlap = "Overlap: " + mWindow_.getOverlap();
    	String A = "A: (" + this.A[0] + ", " + this.A[1] + ")";
    	String B = "B:  (" + this.B[0] + ", " + this.B[1] + ")";
    	String grid = "Grid: (" +  stageCtr.getTileGrid()[0] + ", " + stageCtr.getTileGrid()[1] + ")";
    	List<String> xyCoords = stageCtr.getTileCoords();
    	
    	String coords;
    	StringBuilder builder = new StringBuilder();
    	
    	for(int i = 0; i < xyCoords.size(); i++) {    		
    		String str = xyCoords.get(i);    		
    		builder.append(i+": ")
    		.append(str)
    		.append("\n");
    	}
    	
//    	for(String str: xyCoords) {
//    		builder.append(str).append("\n");
//    	}
    	coords = builder.toString();    	
    	String metaData = new StringBuilder().append(imgDir).append("\n")
    						.append(sensorSize).append("\n")
    						.append(pixSize).append("\n")
    						.append(pixSizeCts).append("\n")
    						.append(overlap).append("\n")
    						.append(A).append("\n")
    						.append(B).append("\n")
    						.append(grid).append("\n")
    						.append(coords).toString();   	    				
    	//save file
    	String outFile = outDir + "\\Metadata.txt";
    	System.out.println(outFile);    	
    	try {
    		
    		File dir = new File(outDir);
    		if(!dir.exists()) {
    			dir.mkdir();
    		}
    		
    	    File file = new File(outFile);
    	    if (! file.exists())
    	        file.createNewFile();

    	    FileWriter fw = new FileWriter(file.getAbsoluteFile());
    	    BufferedWriter bw = new BufferedWriter(fw);
    	    bw.write(metaData);
    	    bw.close();    		
    	}catch(Exception e) {
    		e.printStackTrace();
    	}
    }
    
    public void showEndMsg() {
    	JOptionPane.showMessageDialog(mWindow_.getFrame(),"Acquisition finished.");
    }
    
    //
    //edu.ucsf.slidescanner.image acquisition thread
    //
    private class ScanWorker extends Thread{
        private double[] FOV;
        private int[] A;
        private int[] B;
        private int overlap;    
        private String dest;
        private boolean sRaw;
        private boolean sAuto;
    	ScanWorker(String name,double[]FOV,int[]A,int[]B,int olap,String destFolder, boolean saveRaw, boolean saveAuto){
    		super(name);
    		this.FOV = FOV;
    		this.A = A;
    		this.B = B;
    		this.overlap = olap;
    		this.dest = destFolder; 	
    		this.sRaw = saveRaw;
    		this.sAuto = saveAuto;
    	}
    	public void run() {
    		stageCtr.runAcquisition(FOV, A, B, overlap, camCtr, dest, sRaw, sAuto);
    	}

    }

}
