package edu.ucsf.slidescanner.calibration;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import javax.swing.DefaultListModel;

import edu.ucsf.slidescanner.plugin.CameraController;
import edu.ucsf.slidescanner.plugin.StageController;

public class LensConfig implements Serializable{
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private String model;
	private String make;
	private double workDist; //in mm
	private double[] FOV = new double[2]; //in mm
	private double pixSize; //pixel size in um
	private double pixSizeCts; //pixel size in scanner counts
	private SensorConfig sensorCfg;
	
	public static String lensFile = "lenses.ser";
	
	public LensConfig(String m, String mk, double wd, double ps) {
		this.model = m;
		this.make = mk;
		this.workDist = wd;
		//this.FOV[0] = w;
		//this.FOV[1] = h;
		this.pixSize = ps;	//in um
		this.pixSizeCts = um2mm(pixSize) * StageController.CTSPERMM;
		this.sensorCfg = SensorConfig.getStandardSensor();
		
		//set FOV based on standard sensor dimensions
		this.FOV[0] = sensorCfg.W()*um2mm(pixSize); 
		this.FOV[1] = sensorCfg.H()*um2mm(pixSize); 		
	}
	
	public LensConfig() {
		this.model = "";
		this.make = "";
		this.workDist = 0;
		this.FOV[0] = 0;
		this.FOV[1] = 0;
		this.pixSize = 1;	
		this.pixSizeCts = um2mm(pixSize) * StageController.CTSPERMM;
		this.sensorCfg = SensorConfig.getStandardSensor();
	}	
	
	public void setSensorCfg(SensorConfig s) {
		this.sensorCfg = s;
		
		this.FOV[0] = this.sensorCfg.W()*um2mm(pixSize); 
		this.FOV[1] = this.sensorCfg.H()*um2mm(pixSize);
	}

	public SensorConfig getSensorCfg() {
		return this.sensorCfg;
	}
	
	public void setPixSize(double s) {
		this.pixSize = s;		
		//update FOV and pixSizeCnt
		this.pixSizeCts = um2mm(pixSize) * StageController.CTSPERMM;
		this.FOV[0] = sensorCfg.W()*um2mm(pixSize); 
		this.FOV[1] = sensorCfg.H()*um2mm(pixSize);  	
	}
	
	public double getPixSize() {
		return this.pixSize;
	}
	
	public void setPixSizeCts(double c) {
		this.pixSizeCts = c;
	}
	
	public double getPixSizeCts() {
		return this.pixSizeCts;
	}
	
	public String getModel() {
		return model;
	}

	public void setModel(String model) {
		this.model = model;
	}

	public String getMake() {
		return make;
	}

	public void setMake(String make) {
		this.make = make;
	}

	public double getWorkDist() {
		return workDist;
	}

	public void setWorkDist(double workDist) {
		this.workDist = workDist;
	}

	public double[] getFOV() {
		return FOV;
	}

	public void setFOV(double[] fOV) {
		FOV = fOV;
	}
	
	public void setAll(LensConfig l) {
		this.model = l.getModel();
		this.make = l.getMake();
		this.workDist = l.getWorkDist();
		this.FOV[0] = l.getFOV()[0];
		this.FOV[1] = l.getFOV()[1];
		this.pixSize = l.getPixSize();		
		this.sensorCfg = l.getSensorCfg();
		this.pixSizeCts = l.getPixSizeCts();
	}
	
	private double um2mm(double n) {
		if(n == 0) {
			return n;
		}
		return (n/1000);
	}
	
	private double mm2um(double n) {
		return n*1000;
	}
	
	public String toString() {
		return (make+" "+model+" @ "+ FOV[0]+"x"+FOV[1]);
	}
	
	public boolean equals(Object o) {
		if(o instanceof LensConfig) {
			LensConfig l = (LensConfig)o;
			if(this.workDist == l.getWorkDist() && this.FOV[0] == l.getFOV()[0] && this.FOV[1] == l.getFOV()[1]) {
				return true;
			}
		}
		return false;
	}
	
	public static void saveItems(DefaultListModel listModel, String lensFile) throws Exception {
		List<LensConfig> lenses = new ArrayList<LensConfig>();
		int nItems = listModel.getSize();
		for(int i=0; i<nItems; i++) {
			LensConfig l = (LensConfig)listModel.get(i);
			lenses.add(l);
		}
		
		//persist hashtable
		FileOutputStream fileOut = new FileOutputStream(lensFile);
		ObjectOutputStream out = new ObjectOutputStream(fileOut);
		out.writeObject(lenses);
		out.close();
		fileOut.close();		
	}
	
	public static List<LensConfig> loadItems(DefaultListModel listModel, String lensFile) throws Exception{
		//read hashtable
		List<LensConfig> list = null;
		if((new File(lensFile)).exists()){	
	        FileInputStream fileIn = new FileInputStream(lensFile);
	        ObjectInputStream in = new ObjectInputStream(fileIn);
	        list = (List<LensConfig>) in.readObject();
	        in.close();
	        fileIn.close();         
		}        
        return list;
	}
	
}
