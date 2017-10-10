package edu.ucsf.slidescanner.plugin;

import java.awt.EventQueue;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.File;

import javax.swing.DefaultComboBoxModel;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTabbedPane;
import javax.swing.JTextField;
import javax.swing.JTextPane;

import org.micromanager.Studio;

import edu.ucsf.slidescanner.calibration.DarkFrameWindow;
import edu.ucsf.slidescanner.calibration.LensConfig;
import edu.ucsf.slidescanner.calibration.SensorConfig;
import edu.ucsf.slidescanner.calibration.WBSettings;
import edu.ucsf.slidescanner.persistacq.AcqPersist;
import edu.ucsf.slidescanner.persistacq.PersistParam;
import mmcorej.CMMCore;

public class SlideScanUI {

	private JFrame frmUcsfSlideScan;
	
	//Plugin attributes
	private Studio gui_;
	private CMMCore core_;
	private SlideScan plugin_;
	
	@PersistParam(id="colorMode")
	private boolean isColorOn;
	
	
//    private double[] FOV = new double[2];
//    private int[] A = new int[2];
//    private int[] B  = new int[2];
//    private int overlap = 15;
    private Thread scanWorker; 
    
    @PersistParam(id="lensConfig")
    protected LensConfig lensConfig;
    @PersistParam(id="WBInfo")
    protected WBSettings WBInfo;
    
    
    private JTextField textFOV_W;
    private JTextField textFOV_H;
    @PersistParam(id="overlap")
    private JTextField textOverlap;
    @PersistParam(id="imgFolder")
    private JTextField textImgFolder;
    @PersistParam(id="red")
    private JTextField textRed;
    @PersistParam(id="green")
    private JTextField textGreen;
    @PersistParam(id="blue")
    private JTextField textBlue;
    private JLabel lblNumTiles;
    private JLabel lblAcqTime;
    private JComboBox comboColorMode;
    private JComboBox comboWBPreset;
    private JComboBox comboLens;
    @PersistParam(id="saveRaw")
    private JCheckBox chkSaveRaw;
    @PersistParam(id="saveAuto")
    private JCheckBox chkSaveAutostretch;
    @PersistParam(id="AX")
    private JTextField textXA;
    @PersistParam(id="AY")
    private JTextField textYA;
    @PersistParam(id="BX")
    private JTextField textXB;
    @PersistParam(id="BY")
    private JTextField textYB;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					SlideScanUI window = new SlideScanUI();
					window.frmUcsfSlideScan.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
	
	public SlideScanUI(Studio gui, SlideScan sScan) throws Exception{
		gui_ = gui;
		plugin_= sScan;
        try {
            core_ = gui_.getCMMCore();
        } catch (Exception ex) {
            throw new Exception("SlideScan plugin could not get MMCore");
        }
        //Init GUI
		initialize();
        initCombos();
        setColorModeOn(true);
        getComboWBPreset().setSelectedIndex(0);
        getComboLens().setSelectedIndex(0);
        
	}

	/**
	 * Create the application.
	 */
	public SlideScanUI() {
		initialize();
	}
	
	public JFrame getFrame() {
		return this.frmUcsfSlideScan;
	}
	
	public void setControler(SlideScan ctr) {
		plugin_ = ctr;
	}
	
	private SlideScanUI getSelf() {
		return this;
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {
		frmUcsfSlideScan = new JFrame();
		frmUcsfSlideScan.setTitle("UCSF Slide Scan v0.01");
		frmUcsfSlideScan.setBounds(100, 100, 508, 517);
		frmUcsfSlideScan.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frmUcsfSlideScan.getContentPane().setLayout(null);
		
		JTabbedPane tabbedPane = new JTabbedPane(JTabbedPane.TOP);
		tabbedPane.setBounds(0, 36, 490, 434);
		frmUcsfSlideScan.getContentPane().add(tabbedPane);
		
		JPanel panelCamLens = new JPanel();
		tabbedPane.addTab("Camera/Lens", null, panelCamLens, null);
		panelCamLens.setLayout(null);
		
		JLabel lblLensFovmm = new JLabel("Lens FOV (mm):");
		lblLensFovmm.setBounds(68, 104, 105, 14);
		panelCamLens.add(lblLensFovmm);
		
		JLabel label_1 = new JLabel("W:");
		label_1.setBounds(183, 104, 25, 14);
		panelCamLens.add(label_1);
		
		textFOV_W = new JTextField();
		textFOV_W.setEditable(false);
		textFOV_W.setColumns(10);
		textFOV_W.setBounds(207, 101, 67, 20);
		panelCamLens.add(textFOV_W);
		
		JLabel label_2 = new JLabel("H:");
		label_2.setBounds(319, 104, 25, 14);
		panelCamLens.add(label_2);
		
		textFOV_H = new JTextField();
		textFOV_H.setEditable(false);
		textFOV_H.setColumns(10);
		textFOV_H.setBounds(344, 104, 67, 20);
		panelCamLens.add(textFOV_H);
		
		JLabel lblColorMode = new JLabel("Color mode:");
		lblColorMode.setBounds(68, 231, 58, 14);
		panelCamLens.add(lblColorMode);
		
		JLabel lblRed = new JLabel("Red:");
		lblRed.setBounds(24, 317, 46, 14);
		panelCamLens.add(lblRed);
		
		JLabel lblGree = new JLabel("Green:");
		lblGree.setBounds(162, 317, 46, 14);
		panelCamLens.add(lblGree);
		
		textRed = new JTextField();
		textRed.setEnabled(false);
		textRed.setBounds(68, 314, 67, 20);
		panelCamLens.add(textRed);
		textRed.setColumns(10);
		
		textGreen = new JTextField();
		textGreen.setEnabled(false);
		textGreen.setBounds(207, 314, 67, 20);
		panelCamLens.add(textGreen);
		textGreen.setColumns(10);
		
		JLabel lblBlue = new JLabel("Blue:");
		lblBlue.setBounds(303, 317, 46, 14);
		panelCamLens.add(lblBlue);
		
		textBlue = new JTextField();
		textBlue.setEnabled(false);
		textBlue.setBounds(340, 314, 67, 20);
		panelCamLens.add(textBlue);
		textBlue.setColumns(10);
		
		comboColorMode = new JComboBox();
		comboColorMode.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int select = comboColorMode.getSelectedIndex();
				if(select == 0) { //GRY
					isColorOn = false;
					textRed.setEnabled(false);
					textGreen.setEnabled(false);
					textBlue.setEnabled(false);
					comboWBPreset.setEnabled(false);
					if(plugin_ != null) {
						plugin_.setColorOFF();
					}
				}else if(select == 1) { //RGB
					isColorOn = true;
					textRed.setEnabled(true);
					textGreen.setEnabled(true);
					textBlue.setEnabled(true);
					comboWBPreset.setEnabled(true);	
					if(plugin_ != null) {
						plugin_.setColorON(WBInfo.getR(), WBInfo.getG(), WBInfo.getB());
					}
				}
			}
		});
		comboColorMode.setModel(new DefaultComboBoxModel(new String[] {"GRY", "RGB"}));
		comboColorMode.setBounds(207, 228, 67, 20);
		panelCamLens.add(comboColorMode);
		
		comboLens = new JComboBox();
		comboLens.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				LensConfig lens = (LensConfig)comboLens.getSelectedItem();
				textFOV_W.setText(lens.getFOV()[0]+"");
				textFOV_H.setText(lens.getFOV()[1]+"");
				lensConfig = lens;				
				plugin_.setCurrLensCfg(lensConfig);
				
			}
				
		});
		comboLens.setBounds(80, 53, 327, 20);
		panelCamLens.add(comboLens);
		
		JLabel lblLens = new JLabel("Lens:");
		lblLens.setBounds(24, 56, 46, 14);
		panelCamLens.add(lblLens);
		
		JLabel lblPresets = new JLabel("Presets:");
		lblPresets.setBounds(24, 277, 67, 14);
		panelCamLens.add(lblPresets);
		
		comboWBPreset = new JComboBox();
		comboWBPreset.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				WBSettings wb = (WBSettings)comboWBPreset.getSelectedItem();
				textRed.setText(wb.getR()+"");
				textGreen.setText(wb.getG()+"");
				textBlue.setText(wb.getB()+"");
				WBInfo = wb;
				
				double r = 1.0;
				double g = 1.0;
				double b = 1.0;
				if(wb != null) {
					r = wb.getR();
					g = wb.getG();
					b = wb.getB();
				}
				if(plugin_ != null) {
					plugin_.setColorON(r,g,b);
				}
			}
		});
		comboWBPreset.setBounds(80, 274, 327, 20);
		panelCamLens.add(comboWBPreset);
		
		JPanel panelAcquisition = new JPanel();
		tabbedPane.addTab("Acquisition", null, panelAcquisition, null);
		panelAcquisition.setLayout(null);
		
		JLabel label_3 = new JLabel("Overlap (%):");
		label_3.setBounds(29, 80, 111, 22);
		panelAcquisition.add(label_3);
		
		textOverlap = new JTextField();
		textOverlap.setColumns(10);
		textOverlap.setBounds(175, 81, 54, 20);
		panelAcquisition.add(textOverlap);
		
		JButton btnSetA = new JButton("Set A");
		btnSetA.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent e) {
				try {
					//int A[] = plugin_.setCoordsA();
					int A[] = plugin_.getStagePosition();
					textXA.setText(A[0]+"");
					textYA.setText(A[1]+"");
				}catch(Exception ex) {
					ex.printStackTrace();
				}
			}
		});
		btnSetA.setBounds(29, 113, 89, 23);
		panelAcquisition.add(btnSetA);
		
		JButton btnSetB = new JButton("Set B");
		btnSetB.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent e) {
				try {
					//int B[] = plugin_.setCoordsB();
					int B[] = plugin_.getStagePosition();
					textXB.setText(B[0]+"");
					textYB.setText(B[1]+"");
				}catch(Exception ex) {
					ex.printStackTrace();
				}
			}
		});
		btnSetB.setBounds(140, 113, 89, 23);
		panelAcquisition.add(btnSetB);
		
		JLabel label_4 = new JLabel("Upper left corner (A):");
		label_4.setBounds(7, 166, 111, 14);
		panelAcquisition.add(label_4);
		
		JLabel label_6 = new JLabel("Lower right corner (B):");
		label_6.setBounds(7, 194, 111, 14);
		panelAcquisition.add(label_6);		

		JLabel label_8 = new JLabel("Estimated num. tiles:");
		label_8.setBounds(7, 248, 122, 14);
		panelAcquisition.add(label_8);
		
		lblNumTiles = new JLabel("...");
		lblNumTiles.setBounds(131, 248, 251, 14);
		panelAcquisition.add(lblNumTiles);
		
		JButton btnFindHome = new JButton("Find Home");
		btnFindHome.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent e) {
				plugin_.getStageController().findHome();
			}
		});
		btnFindHome.setBounds(227, 345, 89, 46);
		panelAcquisition.add(btnFindHome);
		
		JButton btnScan = new JButton("Scan");
		btnScan.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent e) {
				double FOV[] = new double[2];
				//FOV[0] = Double.parseDouble(textFOV_W.getText());
				//FOV[1] = Double.parseDouble(textFOV_H.getText());
				FOV[0] = lensConfig.getFOV()[0];
				FOV[1] = lensConfig.getFOV()[1];
				String folder = textImgFolder.getText();
				int over = Integer.parseInt(textOverlap.getText());
				int Ax = Integer.parseInt(textXA.getText());
				int Ay = Integer.parseInt(textYA.getText());
				int Bx = Integer.parseInt(textXB.getText());
				int By = Integer.parseInt(textYB.getText());
				plugin_.setCoordsA(new int[]{Ax,Ay});
				plugin_.setCoordsB(new int[]{Bx,By});
				plugin_.setShouldSaveRaw(chkSaveRaw.isSelected());
				plugin_.setShouldSaveAuto(chkSaveAutostretch.isSelected());
				
//		    	double[] FOV = {18.78,15.37};
//		    	int[] A = {-370340,486093};
//		    	int[] B = {-271876,481792};
//		    	int over = 15;
//		    	plugin_.setA(A[0],A[1]);
//		    	plugin_.setB(B[0],B[1]);
//				String folder = "C:\\Users\\Maryana\\Desktop\\test_stitch\\tif2";
		    	
				plugin_.acquireImages(FOV, over, folder);
			}
		});
		btnScan.setBounds(7, 345, 89, 46);
		panelAcquisition.add(btnScan);
		
		JButton btnCancel = new JButton("Cancel");
		btnCancel.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				if(scanWorker != null) {
					scanWorker.interrupt();
					plugin_.restartJoystick();
				}
			}
		});
		btnCancel.setBounds(326, 345, 89, 46);
		panelAcquisition.add(btnCancel);
		
		JLabel lblImageFolder = new JLabel("Image folder:");
		lblImageFolder.setBounds(10, 26, 67, 14);
		panelAcquisition.add(lblImageFolder);
		
		textImgFolder = new JTextField();
		textImgFolder.setBounds(87, 23, 254, 20);
		panelAcquisition.add(textImgFolder);
		textImgFolder.setColumns(10);
		
		JButton btnOpenImgDir = new JButton("Open...");
		btnOpenImgDir.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
			}
		});
		btnOpenImgDir.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent e) {
				JFileChooser chooser = new JFileChooser();
				chooser.setDialogTitle("Choose destination directory.");
				chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
				if(chooser.showOpenDialog(getFrame()) == JFileChooser.APPROVE_OPTION) {
					File folder = chooser.getSelectedFile();
					textImgFolder.setText(folder.getPath());
				}
			}
		});
		btnOpenImgDir.setBounds(351, 22, 67, 23);
		panelAcquisition.add(btnOpenImgDir);
		
		chkSaveRaw = new JCheckBox("Save as raw");
		chkSaveRaw.setSelected(true);
		chkSaveRaw.setBounds(282, 80, 97, 23);
		panelAcquisition.add(chkSaveRaw);
		
		chkSaveAutostretch = new JCheckBox("Save autostretch");
		chkSaveAutostretch.setBounds(282, 113, 136, 23);
		panelAcquisition.add(chkSaveAutostretch);
		
		JLabel lblX = new JLabel("X:");
		lblX.setBounds(140, 166, 28, 14);
		panelAcquisition.add(lblX);
		
		textXA = new JTextField();
		
		textXA.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int xa = 0;
				int ya = 0;
				if(!textXA.getText().isEmpty()) {
					xa = Integer.parseInt(textXA.getText());
				}
				if(!textYA.getText().isEmpty()) {
					ya = Integer.parseInt(textYA.getText());
				}
				plugin_.setCoordsA(new int[] {xa,ya});
			}
			
		});
		textXA.setBounds(157, 163, 118, 20);
		panelAcquisition.add(textXA);
		textXA.setColumns(10);
		
		JLabel lblY = new JLabel("Y:");
		lblY.setBounds(285, 166, 46, 14);
		panelAcquisition.add(lblY);
		
		textYA = new JTextField();
		textYA.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int xa = 0;
				int ya = 0;
				if(!textXA.getText().isEmpty()) {
					xa = Integer.parseInt(textXA.getText());
				}
				if(!textYA.getText().isEmpty()) {
					ya = Integer.parseInt(textYA.getText());
				}
				plugin_.setCoordsA(new int[] {xa,ya});
			}
		});
		textYA.setColumns(10);
		textYA.setBounds(299, 163, 118, 20);
		panelAcquisition.add(textYA);
		
		JLabel label = new JLabel("X:");
		label.setBounds(140, 194, 28, 14);
		panelAcquisition.add(label);
		
		textXB = new JTextField();
		textXB.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int xb = 0;
				int yb = 0;
				if(!textXB.getText().isEmpty()) {
					xb = Integer.parseInt(textXB.getText());
				}
				if(!textYB.getText().isEmpty()) {
					yb = Integer.parseInt(textYB.getText());
				}
				plugin_.setCoordsB(new int[] {xb,yb});
			}
		});
		textXB.setColumns(10);
		textXB.setBounds(157, 191, 118, 20);
		panelAcquisition.add(textXB);
		
		JLabel label_5 = new JLabel("Y:");
		label_5.setBounds(285, 194, 46, 14);
		panelAcquisition.add(label_5);
		
		textYB = new JTextField();
		textYB.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int xb = 0;
				int yb = 0;
				if(!textXB.getText().isEmpty()) {
					xb = Integer.parseInt(textXB.getText());
				}
				if(!textYB.getText().isEmpty()) {
					yb = Integer.parseInt(textYB.getText());
				}
				plugin_.setCoordsB(new int[] {xb,yb});
			}
		});
		textYB.setColumns(10);
		textYB.setBounds(299, 191, 118, 20);
		panelAcquisition.add(textYB);
		
		JLabel lblEstimatedAcqTime = new JLabel("Estimated acq. time:");
		lblEstimatedAcqTime.setBounds(7, 282, 122, 14);
		panelAcquisition.add(lblEstimatedAcqTime);
		
		lblAcqTime = new JLabel("...");
		lblAcqTime.setBounds(131, 281, 251, 14);
		panelAcquisition.add(lblAcqTime);
		
		JMenuBar menuBar = new JMenuBar();
		menuBar.setBounds(0, 0, 433, 21);
		frmUcsfSlideScan.getContentPane().add(menuBar);
		
		JMenu mnNewMenu = new JMenu("File");
		menuBar.add(mnNewMenu);
		
		JMenuItem menuOpenAcq = new JMenuItem("Open...");
		menuOpenAcq.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				JFileChooser chooser = new JFileChooser();
				chooser.setDialogTitle("Choose destination file.");
				chooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
				if(chooser.showOpenDialog(getFrame()) == JFileChooser.APPROVE_OPTION) {
					File fName = chooser.getSelectedFile();
					try {
						(new AcqPersist()).loadParams(fName.getPath(), (new Object[] {getSelf()}));
						getSelf().refreshCombos();
					}catch(Exception ex) {
						ex.printStackTrace();
					}
					
				}
			}
		});
		mnNewMenu.add(menuOpenAcq);
		
		JMenuItem menuSaveAcq = new JMenuItem("Save...");
		menuSaveAcq.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				JFileChooser chooser = new JFileChooser();
				chooser.setDialogTitle("Choose destination file.");
				chooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
				if(chooser.showOpenDialog(getFrame()) == JFileChooser.APPROVE_OPTION) {
					File fName = chooser.getSelectedFile();
					if (fName.exists()) {
					    int response = JOptionPane.showConfirmDialog(null, //
					            "Do you want to replace the existing file?", //
					            "Confirm", JOptionPane.YES_NO_OPTION, //
					            JOptionPane.QUESTION_MESSAGE);
					    if (response != JOptionPane.YES_OPTION) {
					        return;
					    } 
					}
					try {
						(new AcqPersist()).saveParams(fName.getPath(), (new Object[] {getSelf()}));
					}catch(Exception ex) {
						ex.printStackTrace();
					}
					JOptionPane.showMessageDialog(getFrame(), "Acquisition parameters saved with success.");
				}
			}
		});
		mnNewMenu.add(menuSaveAcq);
		
		JMenu mnTools = new JMenu("Tools");
		menuBar.add(mnTools);
		
		JMenuItem mntmCreateDarkFrames = new JMenuItem("Create dark frames");
		mntmCreateDarkFrames.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				DarkFrameWindow dFrame = new DarkFrameWindow(plugin_);	
			}
		});
		mnTools.add(mntmCreateDarkFrames);
		
		JMenuItem mntmLenses = new JMenuItem("Lenses");
		mntmLenses.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
			}
		});
		mnTools.add(mntmLenses);
		
		JMenuItem mntmWhiteBalance = new JMenuItem("White Balance");
		mntmWhiteBalance.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
			}
		});
		mnTools.add(mntmWhiteBalance);
	}
	
	public void setNumTiles(String str) {
		lblNumTiles.setText(str);
	}
	
	public void setAcqTime(String str) {
		lblAcqTime.setText(str);
	}
	
	public String getDestFolder() {
		return textImgFolder.getText();
	}
	
	public boolean isColorModeOn() {
		return isColorOn;
	}
	
	public void setColorModeOn(boolean mode) {
		if(mode) {
			getComboColorMode().setSelectedIndex(1);
			isColorOn = true;
		}else {
			getComboColorMode().setSelectedIndex(0);
			isColorOn = false;
		}
	}
	
	public void setWorker(Thread t) {
		scanWorker = t;
	}
	
	private JComboBox getComboColorMode() {
		return comboColorMode;
	}
	
	private void initCombos() {
		
		WBSettings blankCanon = new WBSettings("Blank slide - Canon", 2.69, 1.00, 1.54);
		WBSettings blank = new WBSettings("Blank slide", 2.77, 1.00, 1.49);
		WBSettings gallo2 = new WBSettings("Gallo 2", 2.35, 0.90, 1.25);
		WBSettings gallo1 = new WBSettings("Gallo 1", 2.71, 1.00, 1.36);
		WBSettings tau = new WBSettings("TAU 1", 2.50, 1.00, 1.66);
		WBSettings chart = new WBSettings("Test Chart", 1.08, 1.00, 2.95);
		getComboWBPreset().addItem(blankCanon);
		getComboWBPreset().addItem(blank);
		getComboWBPreset().addItem(gallo1);
		getComboWBPreset().addItem(gallo2);
		getComboWBPreset().addItem(tau);
		getComboWBPreset().addItem(chart);
		
		//LensConfig lensCanon = new LensConfig("3X Macro", "Canon", 49, 3.709, 3.035846);
//		LensConfig lensCanon1 = new LensConfig("1X Macro", "Canon", 98.5, 12.0469, 9.8598);
//		LensConfig lensCanon3 = new LensConfig("3X Macro", "Canon", 41, 4.21599, 3.45059);
//		LensConfig lensLighbox = new LensConfig("50mm Lighbox", "Rodenstock", 88, 17.39, 15.37);	
//		LensConfig lensNavitar3x = new LensConfig("Navitar 3x", "Navitar", 11.2, 7.772, 6.3617);
//		LensConfig lensNavitar4_5x = new LensConfig("Navitar 4.5x", "Navitar", 9.6, 5.1039, 4.1773);
		LensConfig lensNavitar4_5x1_5x = new LensConfig("Navitar 4.5x 1.5X insert", "Navitar", 5.2, 1.22121);
		LensConfig lensNavitar4_5x1_5x_ROI = new LensConfig("Navitar 4.5/1.5 2/3in", "Navitar", 5.2, 1.22121);
		SensorConfig sc = new SensorConfig(1920, 1460, 383, 369); // 2/3" sensor dims 
		lensNavitar4_5x1_5x_ROI.setSensorCfg(sc);
		
//		
		getComboLens().addItem(lensNavitar4_5x1_5x);
		getComboLens().addItem(lensNavitar4_5x1_5x_ROI);
//		getComboLens().addItem(lensNavitar4_5x);
//		getComboLens().addItem(lensNavitar3x);
//		getComboLens().addItem(lensCanon1);
//		getComboLens().addItem(lensCanon3);
//		getComboLens().addItem(lensLighbox);
		
	}
	
	private void refreshCombos() {
		if(WBInfo != null) {
			getComboWBPreset().setSelectedItem(this.WBInfo);			
		}
		if(lensConfig != null) {
			getComboLens().setSelectedItem(this.lensConfig);
		}
		if(isColorOn) {
			getComboColorMode().setSelectedIndex(1);
		}else {
			getComboColorMode().setSelectedIndex(0);
		}
	}
	
	public JComboBox getComboWBPreset() {
		return comboWBPreset;
	}
	public JComboBox getComboLens() {
		return comboLens;
	}
	public JCheckBox getChkSaveRaw() {
		return chkSaveRaw;
	}
	public JCheckBox getChkSaveAutostrech() {
		return chkSaveAutostretch;
	}
	public boolean shouldSaveRaw() {
		return getChkSaveRaw().isSelected();
	}
	public boolean shouldSaveAuto() {
		return getChkSaveAutostrech().isSelected();
	}
	public String getOverlap() {
		return textOverlap.getText();
	}
	public LensConfig getLensInfo() {
		return this.lensConfig;
	}	
	public WBSettings getWBInfo(){
		return this.WBInfo;
	}
}
