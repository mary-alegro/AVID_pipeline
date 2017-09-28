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
    private final String ACK_LOG = "**";
    private final String ACK_STATUS = "##";

    private final String CMD_ROT = "0";
    private final String CMD_HOME = "2";
    private final String CMD_RESET = "6";
    private final String CMD_LEFT = "3";
    private final String CMD_RIGHT = "4";	
    
    private boolean max_reached = false;
    
    
    private String port = "COM4";
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
			long estTime = 0;
			boolean doRead = true;
			
			while(estTime < TIMEOUT && doRead) {
				ans = getBoardMsg();	
				System.out.println(ans);
				estTime = System.nanoTime() - startTime;
				
				String tokens[] = ans.split("(\\*\\*)");
				for(String token : tokens) {
					if(token.startsWith(ACK_STATUS)) {
						String status = token.replace(ACK_STATUS, "");
						if(status.equals(ACK_ROT)) { //rotation complete
							System.out.println("Rotation completed");
							doRead = false;
							break;
						}else if(status.equals(ACK_MAX)) {
							System.out.println("Maximum angle reached");
							doRead = false;
							this.max_reached = true;
							break;
						}
					}else {
						plugin.addTextOutput(token);
					}
				}
			}
			if(estTime >= TIMEOUT ){
				System.out.println("ERROR: Stage timed out while running rotate routine.");
			}				
	
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
			long estTime = 0;
			boolean doRead = true;
			
			while(estTime < TIMEOUT && doRead) {
				ans = getBoardMsg();	
				System.out.println(ans);
				estTime = System.nanoTime() - startTime;
				
				String tokens[] = ans.split("(\\*\\*)");
				for(String token : tokens) {
					if(token.startsWith(ACK_STATUS)) {
						String status = token.replace(ACK_STATUS, "");
						if(status.equals(ACK_HOME)) { //rotation complete
							System.out.println("Filters position reset");
							this.max_reached = false;
							doRead = false;
							break;
						}
					}else {
						plugin.addTextOutput(token);
					}
				}
			}
			if(estTime >= TIMEOUT ){
				System.out.println("ERROR: Stage timed out while running rotate routine.");
			}						
	
	
		}catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	public boolean isMaxReached() {
		return this.max_reached;
	}
	
	public String getBoardMsg() throws Exception {
		Thread.sleep(200);
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



