package calibration;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import javax.swing.DefaultListModel;

public class LensInfo implements Serializable{
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private String model;
	private String make;
	private double workDist;
	private double[] FOV = new double[2];
	
	public static String lensFile = "lenses.ser";
	
	public LensInfo(String m, String mk, double wd, double w, double h) {
		this.model = m;
		this.make = mk;
		this.workDist = w;
		this.FOV[0] = w;
		this.FOV[1] = h;
	}
	
	public LensInfo() {
		this.model = "";
		this.make = "";
		this.workDist = 0;
		this.FOV[0] = 0;
		this.FOV[1] = 0;
	}
	
	public double getPixSize(double fovw, double sw) {
		return (fovw/sw);
	}
	
	public double[] getFOV(double pix, double sw, double sh) {
		double w = sw*pix;
		double h = sh*pix;	
		return (new double[] {w,h});	
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
	
	public void setAll(LensInfo l) {
		this.model = l.getModel();
		this.make = l.getMake();
		this.workDist = l.getWorkDist();
		this.FOV[0] = l.getFOV()[0];
		this.FOV[1] = l.getFOV()[1];
	}
	
	public String toString() {
		return (make+" "+model+" @ "+ FOV[0]+"x"+FOV[1]);
	}
	
	public boolean equals(Object o) {
		if(o instanceof LensInfo) {
			LensInfo l = (LensInfo)o;
			if(this.workDist == l.getWorkDist() && this.FOV[0] == l.getFOV()[0] && this.FOV[1] == l.getFOV()[1]) {
				return true;
			}
		}
		return false;
	}
	
	public static void saveItems(DefaultListModel listModel, String lensFile) throws Exception {
		List<LensInfo> lenses = new ArrayList<LensInfo>();
		int nItems = listModel.getSize();
		for(int i=0; i<nItems; i++) {
			LensInfo l = (LensInfo)listModel.get(i);
			lenses.add(l);
		}
		
		//persist hashtable
		FileOutputStream fileOut = new FileOutputStream(lensFile);
		ObjectOutputStream out = new ObjectOutputStream(fileOut);
		out.writeObject(lenses);
		out.close();
		fileOut.close();		
	}
	
	public static List<LensInfo> loadItems(DefaultListModel listModel, String lensFile) throws Exception{
		//read hashtable
		List<LensInfo> list = null;
		if((new File(lensFile)).exists()){	
	        FileInputStream fileIn = new FileInputStream(lensFile);
	        ObjectInputStream in = new ObjectInputStream(fileIn);
	        list = (List<LensInfo>) in.readObject();
	        in.close();
	        fileIn.close();         
		}        
        return list;
	}
	
}
