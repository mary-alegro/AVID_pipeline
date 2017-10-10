package edu.ucsf.slidescanner.calibration;

import java.io.Serializable;

import edu.ucsf.slidescanner.plugin.CameraController;

public class SensorConfig implements Serializable{
	
	private int[] sensorSize; //sensor size in pixels
	private int[] sensorOrigin; //sensor origin	
	
	public SensorConfig(int[] ss, int[] or) {
		this(ss[0],ss[1],or[0],or[1]);
	}	
	
	public SensorConfig(int w, int h, int ox, int oy) {
		this.sensorSize = new int[] {w,h};
		this.sensorOrigin = new int[] {ox,oy};
	}
	
	public static SensorConfig getStandardSensor() {
		SensorConfig sc = new SensorConfig(CameraController.STD_SENSOR_SIZE, CameraController.STD_SENSOR_ORIG);		
		return sc;
	}

	public int[] getSensorSize() {
		return sensorSize;
	}

	public void setSensorSize(int[] sensorSize) {
		this.sensorSize = sensorSize;
	}

	public int[] getSensorOrigin() {
		return sensorOrigin;
	}

	public void setSensorOrigin(int[] sensorOrigin) {
		this.sensorOrigin = sensorOrigin;
	}	

	public int W() {
		return this.sensorSize[0]; //X=cols=width
	}
	
	public int H() {
		return this.sensorSize[1]; //Y=rows=height
	}
	
	public int oX() {
		return this.sensorOrigin[0];		
	}
	
	public int oY() {
		return this.sensorOrigin[1];
	}
	
	public boolean equals(Object o) {
		if(o instanceof SensorConfig) {
			SensorConfig cfg = (SensorConfig)o;
			if(this.sensorSize[0] == cfg.W() && this.sensorSize[1] == cfg.H() &&
			   this.sensorOrigin[0] == cfg.oX() && this.sensorOrigin[1] == cfg.oY()) {
				return true;
			}
		}
		return false;
	}
}
