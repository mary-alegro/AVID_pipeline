package PLI;

import org.micromanager.Studio;

import mmcorej.CMMCore;
import mmcorej.CharVector;

public class PolarimeterController {
	
	private CMMCore core;
	private Studio gui;
	private PLIControl plugin;
	
    private final String ACK_INIT = "001";
    private final String ACK_ROT = "002";
    private final String ACK_HOME = "003";
    private final String ACK_MAX = "004";
    private final String ACK_RESET = "005";
    private final String ACK_LEFT = "006";
    private final String ACK_RIGHT = "007";
    private final String ACK_STATUS = "**";

    private final String CMD_ROT = "0";
    private final String CMD_HOME = "2";
    private final String CMD_RESET = "6";
    private final String CMD_LEFT = "3";
    private final String CMD_RIGHT = "4";	
    
    
    private String port = "COM3";
    final long TIMEOUT = (long)3e10; //30secs in nanosecs
    
	public PolarimeterController(Studio gui_, PLIControl pl) {
		gui = gui_;
		core = gui_.getCMMCore();
		plugin = pl;
	}
	
	public void doRotation() {
		CharVector cmd = str2Charvec(CMD_ROT);
		try {
			//write command to microcontroler
			core.writeToSerialPort(port, cmd);
			
			//read microcontroler msgs
			String ans = "";			
			long startTime = System.nanoTime();				
			do {
				ans = getBoardMsg();	
				long estTime = System.nanoTime() - startTime;
				if(estTime >= TIMEOUT ){
					System.out.println("ERROR: Stage timed out while running rotate routine.");
					break;
				}					
				if(ans.startsWith(ACK_STATUS)) {
					
					String log = ans.replace(ACK_STATUS, "");
					plugin.addTextOutput(log);
				}else if(ans == ACK_ROT) {
					plugin.addTextOutput("Rotation executed");
					System.out.println("Rotation executed");
				}else if(ans == ACK_MAX) {
					plugin.addTextOutput("Maximum reached");
					System.out.println("Maximum reached");
				}
			}while(!ans.equals(ACK_ROT) && !ans.equals(ACK_MAX));			
	
		}catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	public void goHome() {
		CharVector cmd = str2Charvec(CMD_HOME);
		try {
			//write command to microcontroler
			core.writeToSerialPort(port, cmd);
			
			//read microcontroler msgs
			String ans = "";			
			long startTime = System.nanoTime();				
			do {
				ans = getBoardMsg();	
				long estTime = System.nanoTime() - startTime;
				if(estTime >= TIMEOUT ){
					System.out.println("ERROR: Stage timed out while running go home routine.");
					break;
				}					
				if(ans.startsWith(ACK_STATUS)) {
					String log = ans.replace(ACK_STATUS, "");
					plugin.addTextOutput(log);
				}else if(ans == ACK_HOME) {
					plugin.addTextOutput("Filter position reset");
					System.out.println("Filter position reset");
				}
			}while(!ans.equals(ACK_HOME));			
	
		}catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	public String getBoardMsg() throws Exception {
		CharVector ans = core.readFromSerialPort(port);
		String str = charVec2Str(ans);
		return str;
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
}



