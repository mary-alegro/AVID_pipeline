package calibration;

import java.io.Serializable;

public class LensInfo implements Serializable{
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private String model;
	private String make;
	private double workDist;
	private double[] FOV = new double[2];
	
	public LensInfo(String m, String mk, double wd, double w, double h) {
		this.model = m;
		this.make = mk;
		this.workDist = w;
		this.FOV[0] = w;
		this.FOV[1] = h;
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
	
}
