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
import javax.swing.ListModel;

public class WBSettings implements Serializable{
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private String label;
	private double R;
	private double G;
	private double B;
	
	public WBSettings(String s, double r, double g, double b) {
		this.label = s;
		this.R = r;
		this.G = g;
		this.B = b;
	}

	public String getLabel() {
		return label;
	}

	public void setLabel(String label) {
		this.label = label;
	}

	public double getR() {
		return R;
	}

	public void setR(double r) {
		R = r;
	}

	public double getG() {
		return G;
	}

	public void setG(double g) {
		G = g;
	}

	public double getB() {
		return B;
	}

	public void setB(double b) {
		B = b;
	}
	
	public String toString() {
		return label+" ("+R+","+G+","+B+")";
	}
	
	public void setAll(WBSettings w) {
		this.label = w.getLabel();
		this.R = w.getR();
		this.G = w.getG();
		this.B = w.getB();
	}
	
	public boolean equals(Object o) {
		if(o instanceof WBSettings) {
			WBSettings w = (WBSettings)o;
			if(this.R == w.getR() && this.G == w.getG() && this.B == w.getB()) {
				return true;
			}
		}
		return false;
	}
	

	
}
