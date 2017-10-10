package edu.ucsf.slidescanner.plugin;

import java.util.ArrayList;
import java.util.List;

import javax.swing.JOptionPane;

import org.micromanager.Studio;

import mmcorej.CMMCore;
import mmcorej.CharVector;

public class StageController {
	
	//Stage constants
	final long TIMEOUT = (long)3e10; //30secs in nanosecs
	public static final int CTSPERMM = 8000; // 1mm = 8000counts
	final float ACQSPEED = 15; // 10mm/s
	final long[] DEFAULTMAX_X = new long[] {-607200,607200}; //left to right
	final long[] DEFAULTMAX_Y = new long[] {607200,-607200}; //to to bottom
	final int DELAY_CONST = 400; //in ms
	long[] LIMIT_X = new long[2];
	long[] LIMIT_Y = new long[2];
	private int[] tileGrid = new int[2];
	private List<List> tileCoords;
	
	private CMMCore core;
	private Studio gui;
	private SlideScan plugin;
	//private Studio studio;
	//private List<String> ports = new ArrayList<String>();
	private String port = "COM3";
	private String cmdTerminator="\r";
		
	//Stage codes
	private String STG_ERROR = "?";
	private String STG_OK = ":";
	private String STG_HOME_OK = "H";
	private String STG_PREPMO_OK = "P";
	private String STG_MOVE_OK = "M";
	
	public StageController(Studio gui_, SlideScan sc) {
		gui = gui_;
		core = gui_.getCMMCore();
		//ports.add("COM1");
		//ports.add("COM3");
		plugin = sc;
	}
	
//	public List<String> getPorts() {	
//		return ports;
//	}
		
	public void findHome() {
		
		//find home routine
		String strCmd = "XQ#HOMEALL,7" + cmdTerminator;
		CharVector cmd = str2Charvec(strCmd);
		try {	
			//stop joystick routine
			stopJoystick();
			//run find home
			core.writeToSerialPort(port, cmd);
			String ret = getStageMsg();
			System.out.println(ret);
			if(ret.equals(STG_ERROR)) {
				System.out.println("ERROR: There was an error running find home routine.");
				return;
			}
			String ans = "";
			long startTime = System.nanoTime();
			while(!ans.equals(STG_HOME_OK)) {
				ans = getStageMsg();
				System.out.println(ans);
				long estTime = System.nanoTime() - startTime;
				if(estTime >= TIMEOUT ){
					System.out.println("ERROR: Stage timed out while running find home routine.");
					break;
				}
			}	
		}catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	public String getStageMsg() throws Exception {
		Thread.sleep(300);
		CharVector ans = core.readFromSerialPort(port);		
		String str = charVec2Str(ans);
		return str;
	}
	
	public String getStageError() throws Exception{
		String strCmd = "TC1" + cmdTerminator;
		CharVector cmd = str2Charvec(strCmd);
		core.writeToSerialPort(port, cmd);
		String ans = getStageMsg();
		if(ans.equals(STG_ERROR)) {
			System.out.println("ERROR: There was and error reding stage ERROR MSG");
			return "";
		}
		return ans;
	}
	
	public int[] getStagePos() throws Exception {

		String strCmd = "TP" + cmdTerminator;
		CharVector cmd = str2Charvec(strCmd);
		core.writeToSerialPort(port, cmd);
		
		Thread.sleep(200);
		
		String str = "";
		CharVector ans = core.readFromSerialPort(port);
		str = charVec2Str(ans);
		System.out.println(str);
		if(str.equals(STG_ERROR)) {
			System.out.println("ERROR: There was an error in the stage controler side.");
			throw new Exception("ERROR: There was an error in the stage controler side.");
		}
		long startTime = System.nanoTime();
		while(!str.contains(":" )) {
			str = getStageMsg();
			System.out.println(ans);
			long estTime = System.nanoTime() - startTime;
			if(estTime >= TIMEOUT ){
				System.out.println("ERROR: Stage timed out while getting current position.");
				throw new Exception("ERROR: Stage timed out while getting current position.");
			}
		}
		
		//get values out of string returned by stage controller 
		str = str.replaceAll(":","");
		str = str.replaceAll("\\s","");
		int idx = str.indexOf(",");
		String strX = str.substring(0, idx);
		String strY = str.substring(idx+1, str.length());
		
		int X = Integer.parseInt(strX);
		int Y = Integer.parseInt(strY);
		
		return (new int[]{X,Y});

	}
	
	public void stopJoystick() throws Exception {
		String strCmd = "ST" + cmdTerminator;
		CharVector cmd = str2Charvec(strCmd);
		core.writeToSerialPort(port, cmd);
		String ans = getStageMsg();
		if(ans.equals(STG_ERROR)) {
			System.out.println("ERROR: There was and error stoping the joystick routine");
			throw new Exception("ERROR: There was and error stoping the joystick routine");
		}
	}
	
	public void restartJoystick() throws Exception{
		String strCmd = "XQ#RUNJOY,4" + cmdTerminator;
		CharVector cmd = str2Charvec(strCmd);
		core.writeToSerialPort(port, cmd);
		String ans = getStageMsg();
		System.out.println(ans);
		if(ans.equals(STG_ERROR)) {
			System.out.println("ERROR: There was and error restarting the joystick routine");
			throw new Exception("ERROR: There was and error restarting the joystick routine");
		}
	}
	
	public void resetStage() throws Exception{
		String strCmd = "XQ#AUTO" + cmdTerminator;
		CharVector cmd = str2Charvec(strCmd);
		core.writeToSerialPort(port, cmd);
		String ans = getStageMsg();
		if(ans.equals(STG_ERROR)) {
			System.out.println("ERROR: There was and error resting the stage");
			throw new Exception("ERROR: There was and error resting the stage");
		}
	}
	
	public void prepForMotion() throws Exception{
		String strCmd = "XQ#STOPALL" + cmdTerminator;
		CharVector cmd = str2Charvec(strCmd);
		core.writeToSerialPort(port, cmd);
		String ans = getStageMsg();
		System.out.println(ans);
		if(ans.equals(STG_ERROR)) {
			System.out.println("ERROR: There was and error preparing stage for motion");
			throw new Exception("ERROR: There was and error preparing stage for motion");
		}
		
		Thread.sleep(200);
		
		strCmd = "XQ#PREPMO,6" + cmdTerminator;
		cmd = str2Charvec(strCmd);
		core.writeToSerialPort(port, cmd);
		ans = getStageMsg();
		System.out.println(ans);
		if(ans.equals(STG_ERROR)) {
			System.out.println("ERROR: There was and error preparing stage for motion");
			throw new Exception("ERROR: There was and error preparing stage for motion");
		}
		long startTime = System.nanoTime();
		while(!ans.contains(STG_PREPMO_OK)) {
			ans = getStageMsg();
			System.out.println(ans);
			long estTime = System.nanoTime() - startTime;
			if(estTime >= TIMEOUT ){
				System.out.println("ERROR: Stage timed out while running prepare motion routine.");
				throw new Exception("ERROR: Stage timed out while running prepare motion routine.");
			}
		}
		
	}
	
	public void moveToAbsPos(int x, int y) throws Exception{
		int[] pos = {x,y};
		moveToAbsPos(pos);
	}
	
//	public void moveToAbsPos(int[] pos) throws Exception {
//		String strCmd = "PA " + pos[0] + "," + pos[1] + cmdTerminator;
//		CharVector cmd = str2Charvec(strCmd);
//		core.writeToSerialPort(port, cmd);
//		String ans = getStageMsg();
//		System.out.println(ans);
//		if(ans.contains(STG_ERROR)) {
//			String error = getStageError();
//			System.out.println("ERROR: There was and error moving the stage: set XY");
//			System.out.println(error);
//			throw new Exception("ERROR: There was and error moving the stage: set XY");
//		}else {
//			strCmd = "BG"  + cmdTerminator;
//			cmd = str2Charvec(strCmd);
//			core.writeToSerialPort(port, cmd);
//			ans = getStageMsg();
//			System.out.println(ans);
//			if(ans.contains(STG_ERROR)) {
//				String error = getStageError();
//				System.out.println("ERROR: There was and error moving the stage: moving");
//				System.out.println(error);
//				throw new Exception("ERROR: There was and error moving the stage: moving");
//			}
//		}
//	}
	
	public void moveToAbsPos(int[] pos) throws Exception {
		
		//set pos_x in stage
		String strCmd = "pos_x=" + pos[0] + cmdTerminator;
		CharVector cmd = str2Charvec(strCmd);
		core.writeToSerialPort(port, cmd);
		String ans = getStageMsg();
		System.out.println(ans);		
		if(ans.contains(STG_OK)) { //set 1st variable OK
			
			//set pos_y in stage
			strCmd = "pos_y=" + pos[1] + cmdTerminator;
			cmd = str2Charvec(strCmd);
			core.writeToSerialPort(port, cmd);
			ans = getStageMsg();
			System.out.println(ans);
			if(ans.contains(STG_OK)) { //set 2nd variable OK
				
				//send move command
				strCmd = "XQ#MOV2POS" + cmdTerminator;
				cmd = str2Charvec(strCmd);
				core.writeToSerialPort(port, cmd);
				ans = getStageMsg();
				System.out.println(ans);
				long startTime = System.nanoTime();				
				while(!ans.contains(STG_MOVE_OK)) { //busy wait to make sure program doesn't run while stage is moving
					ans = getStageMsg();
					System.out.println(ans);
					long estTime = System.nanoTime() - startTime;
					if(estTime >= TIMEOUT ){
						System.out.println("ERROR: Stage timed out while running move2pos routine.");
						throw new Exception("ERROR: Stage timed out while running move2pos motion routine.");
					}
				}
			}else {
				throw new Exception("ERROR: There was and error setting Y position");
			}
		}else {
			throw new Exception("ERROR: There was and error setting X position");
		}		
	}
	
	public CharVector str2Charvec(String str) {
		char [] array = str.toCharArray();
		CharVector cArray = new CharVector();
		int nChars = array.length;
		for(int i=0; i<nChars; i++) {
			char c = array[i];
			cArray.add(c);
		}		
		return cArray;
	}
	
	public String charVec2Str(CharVector ans) {
		String str = "";
		if (ans.capacity() > 0) {
		   for(int i=0; i<ans.capacity(); i++){
			   char c = (char)ans.get(i);
			   c = (char)(c & 0x7f); //cleans most significant bit, which carries parity
			   if(c=='\n' || c=='\r') { //ignore line feeds and carriage returns
				   continue;
			   }
		       str = str + c;
		   }
		}
		return str;		
	}
	
	public int[] getTileGrid() {
		return tileGrid;
	}
	
	public List<String> getTileCoords(){
		List<String> xyCoords = new ArrayList<String>();
		if(this.tileCoords != null) {
			List<Integer> coordsX = (List<Integer>)this.tileCoords.get(0);
			List<Integer> coordsY = (List<Integer>)this.tileCoords.get(1);	
			List<Boolean> isTile = (List<Boolean>)this.tileCoords.get(2);	
			
			int nTiles = coordsX.size();
			for(int i = 0; i<nTiles; i++) {
				if(isTile.get(i)) { //if it's an actual tile, not one of the "return positions"
					int x = coordsX.get(i);
					int y = coordsY.get(i);
					xyCoords.add(" ("+x+", "+y+") ");
				}
			}
		}
		
		return xyCoords;
	}
	
	public List<List> computeTileCoords(double[]FOV,int[]A,int[]B,int olap) {
		
		List<List> coords = new ArrayList<List>();
		List<Integer> coordsX = new ArrayList<Integer>();
		List<Integer> coordsY = new ArrayList<Integer>();
		List<Boolean> isTile = new ArrayList<Boolean>();
		
		//set stage X limits
		LIMIT_X[0] = A[0]<DEFAULTMAX_X[0] ? A[0] : DEFAULTMAX_X[0];
		LIMIT_X[1] = B[0]>DEFAULTMAX_X[1] ? B[0] : DEFAULTMAX_X[1];
		//set stage Y limits
		LIMIT_Y[0] = A[1]>DEFAULTMAX_Y[0] ? A[1] : DEFAULTMAX_Y[0];
		LIMIT_Y[1] = B[1]<DEFAULTMAX_Y[1] ? B[1] : DEFAULTMAX_Y[1];
		
		int[] ROI = new int[2];
		ROI[0] = Math.abs(A[0]-B[0]);
		ROI[1] = Math.abs(A[1]-B[1]);
		
		double w = FOV[0]; //sensor size (in mm)
		double h = FOV[1];
		w*=CTSPERMM; //convert sensor size to counts
		h*=CTSPERMM;
		float W = (float)Math.round(w);
		float H = (float)Math.round(h);
		
		float X = ROI[0]; //size of region to be imaged (in counts)
		float Y = ROI[1];
		float overlap = (float)olap/100;
		
		//compute num of tiles along X
		float tW = W - (2*overlap*W); //tile width without removing overlap area: tile_width = sensor_width - 2*overlap_percent*sensor_width (in counts)
		float regX = X - tW/2;
		int numTilesW = (int)Math.ceil(regX/tW); //num. tiles along the width (X)
		
		//compute num necessary rows
		float tH = H - (2*overlap*H); //tile width without removing overlap area: tile_width = sensor_width - 2*overlap_percent*sensor_width (in counts)
		float regY = Y - tH/2;
		int numTilesH = (int)Math.ceil(regY/tH); //num. tiles along the height (Y)
				
		for(int r = 0; r < (numTilesH+1); r++) { //iterates over rows
			int y = A[1]-((int)tH)*r;
			if(y < LIMIT_Y[1]) { //y if out of the lower (negative) limit
				y = B[1];
			}
			
			//adds one entire row of tiles
			int x1_row = 0;
			for(int c = 0; c < (numTilesW+1); c++) { 
				int x = A[0]+((int)tW)*c;
				if(x > LIMIT_X[1]) {
					x = B[0];
				}
				//add points to list
				coordsX.add(x);
				coordsY.add(y);		
				isTile.add(true);
				if(c == 0) {
					x1_row = x;
				}
			}
			//adds coord of the first tile in row to the array. 
			//this will make the stage rewind before moving to next row.
			coordsX.add(x1_row);
			coordsY.add(y);		
			isTile.add(false);
		}
		
		//add grid size information
		List<Integer> gridSize = new ArrayList<Integer>();
		gridSize.add((numTilesW+1));
		gridSize.add((numTilesH+1));
		
		coords.add(coordsX);
		coords.add(coordsY);
		coords.add(isTile);		
		coords.add(gridSize);
		
		//show grid in GUI
		plugin.setNumTiles("X: " + (numTilesW+1) + " Y: " + (numTilesH+1)); 
		
		//compute estimated time and show in GUI
		String estTime = computeEstimatedTime(coordsX, coordsY);
		plugin.setAcqTime(estTime);
		
		//for metadata
		this.tileGrid[0] = numTilesW+1; //X
		this.tileGrid[1] = numTilesH+1;	//Y			
		this.tileCoords = coords;
		
		return coords;
	}
	
	public void runAcquisition(double[]FOV,int[]A,int[]B,int overlap, CameraController camCtr, String destFolder,
			boolean saveRaw, boolean saveAuto) {
		List<List> coords = computeTileCoords(FOV, A, B, overlap);
		
		//save metadata
		plugin.saveMetadata();
		
		List<Integer> coordsX = (List<Integer>)coords.get(0);
		List<Integer> coordsY = (List<Integer>)coords.get(1);	
		List<Boolean> isTile = (List<Boolean>)coords.get(2);	
		List<Integer> sGrid = (List<Integer>)coords.get(3);
		
		int nTiles = coordsX.size();			
		int posCount = 0;
		int initPos = 0;
		int nImgs = sGrid.get(0)*sGrid.get(1);
		int imgNum = 1;
		try {
			//camCtr.createDataStore(destFolder);
			camCtr.createDataStore();
			prepForMotion();
			
			int[] curPos;	
			for(int i=0; i<nTiles; i++) {
				int x = coordsX.get(i); //coord in counts
				int y = coordsY.get(i); //coord in counts
				
				//compute time necessary for moving stage to new pos
				float xMM = (float)x/(float)CTSPERMM; //convert to mm
				float yMM = (float)y/(float)CTSPERMM;
				curPos = getStagePos(); //current position in counts
				float cxMM = (float)curPos[0]/(float)CTSPERMM; //convert to mm
				float cyMM = (float)curPos[1]/(float)CTSPERMM;
				double d = Math.sqrt(Math.pow(xMM-cxMM,2) + Math.pow(yMM-cyMM,2)); //compute distance in mm
				double t = (d/ACQSPEED); //compute delay
				t*=1000; //convert to millis
				
				//move stage
				//prepForMotion();
				Thread.sleep(DELAY_CONST/2);
				moveToAbsPos(x,y);				
				//Thread.sleep((long)(t*1.05) + DELAY_CONST);
				Thread.sleep(DELAY_CONST/2); 
				//snap edu.ucsf.slidescanner.image here	
				if(isTile.get(i)) {
					camCtr.acquireImage(posCount);
					
					System.out.println("Image (" + (imgNum++) + "/" + nImgs + ")" );					
					
					//camCtr.acquireImage(0);
					
					//System.out.println(camCtr.getNumImgs());
					
					//if(posCount > 0 && ((posCount % CameraController.MAX_NUMIMG_MEM) == 0 || i == (nTiles-1))) {
					if(posCount >= CameraController.MAX_NUMIMG_MEM || i == (nTiles-2)) {
						//save images every MAX_NUMIMG_MEM counts to save memory
						//camCtr.freezeDataStore();
						if(plugin.isColorModeOn()) {
							camCtr.saveImagesRGB(destFolder, initPos, nImgs, saveRaw, saveAuto);
						}else {
							camCtr.saveImages(destFolder, initPos);
						}
						//if(i != (nTiles-1)) { //not the last batch
							//camCtr.createDataStore(); //dispose old DS and create an empty one
						//}	
						initPos = initPos+posCount+1;
						posCount = 0;
					}else {
						posCount++;
					}					
				}
			}			
			
//			//camCtr.freezeDataStore();
//			if(plugin.isColorModeOn()) {
//				camCtr.saveImagesRGB(destFolder, initPos, saveRaw, saveAuto);
//				//camCtr.saveTIFFDataStore();
//			}else {
//				camCtr.saveImages(destFolder, initPos);
//			}			
			
		}catch(Exception e) {
			System.out.println("ERROR: Problem moving stage.");
			e.printStackTrace();
		}
		
		//restart joystick routine after imaging	
		try {
			restartJoystick();
		}catch(Exception e) {
			System.out.println("ERROR: Couldn't restart stage after crash.");
			e.printStackTrace();
		}
		
		plugin.showEndMsg();
		
	}
	
	private String computeEstimatedTime(List<Integer> coordsX, List<Integer> coordsY) {
		int nTiles = coordsX.size();
		int x = coordsX.get(0);
		int y = coordsY.get(0);
		float cxMM = (float)x/(float)CTSPERMM; //convert to mm
		float cyMM = (float)y/(float)CTSPERMM;		
		double time = 0;
		
		for(int i=1; i<nTiles; i++) {
			//compute time necessary for moving stage to new pos
			float xMM = (float)coordsX.get(i)/(float)CTSPERMM; //convert to mm
			float yMM = (float)coordsY.get(i)/(float)CTSPERMM;
			double d = Math.sqrt(Math.pow(xMM-cxMM,2) + Math.pow(yMM-cyMM,2)); //compute distance in mm
			double t = (d/ACQSPEED); //compute delay	
			t*=1000; //convert to millis
			time += (t*1.05) + DELAY_CONST;
			cxMM = xMM;
			cyMM = yMM;			
		}
		
		time *= 2;
		
		long second = ((long)time / 1000) % 60;
		long minute = ((long)time / (1000 * 60)) % 60;
		long hour = ((long)time / (1000 * 60 * 60)) % 24;

		String strTime = String.format("%02d:%02d:%02d", hour, minute, second);
		return strTime;
	}
	
}
