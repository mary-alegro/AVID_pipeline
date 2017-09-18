package edu.ucsf.slidescanner.calibration;

import java.awt.EventQueue;

import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTextField;

import edu.ucsf.slidescanner.plugin.SlideScan;

import javax.swing.JButton;
import javax.swing.JFileChooser;

import java.awt.event.ActionListener;
import java.io.File;
import java.awt.event.ActionEvent;

public class DarkFrameWindow {

	private JFrame frame;
	
	private SlideScan scanCtr;
	private JTextField textDarkDir;
	private JTextField textNumFrames;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					DarkFrameWindow window = new DarkFrameWindow();
					window.frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the application.
	 */
	
	public DarkFrameWindow(SlideScan sc) {
		this();
		this.scanCtr = sc;
		frame.setVisible(true);
	}
	
	public DarkFrameWindow() {
		initialize();
		//frame.setVisible(true);
	}
	
	public JFrame getFrame() {
		return frame;
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {
		frame = new JFrame();
		frame.setBounds(100, 100, 451, 220);
		frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
		frame.getContentPane().setLayout(null);
		
		JLabel lblNewLabel = new JLabel("Dark frames:");
		lblNewLabel.setBounds(10, 35, 72, 14);
		frame.getContentPane().add(lblNewLabel);
		
		textDarkDir = new JTextField();
		textDarkDir.setBounds(79, 32, 254, 20);
		frame.getContentPane().add(textDarkDir);
		textDarkDir.setColumns(10);
		
		JButton btnOpenDarkDir = new JButton("Open...");
		btnOpenDarkDir.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				JFileChooser chooser = new JFileChooser();
				chooser.setDialogTitle("Choose destination directory.");
				chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
				if(chooser.showOpenDialog(getFrame()) == JFileChooser.APPROVE_OPTION) {
					File folder = chooser.getSelectedFile();
					textDarkDir.setText(folder.getPath());
				}
			}
		});
		btnOpenDarkDir.setBounds(352, 31, 72, 23);
		frame.getContentPane().add(btnOpenDarkDir);
		
		JLabel lblNumFrames = new JLabel("Num. frames:");
		lblNumFrames.setBounds(10, 78, 72, 14);
		frame.getContentPane().add(lblNumFrames);
		
		textNumFrames = new JTextField();
		textNumFrames.setBounds(79, 75, 86, 20);
		frame.getContentPane().add(textNumFrames);
		textNumFrames.setColumns(10);
		
		JButton btnRunDark = new JButton("Run Acquisition");
		btnRunDark.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int numFrames = Integer.parseInt(textNumFrames.getText());
				String dir = textDarkDir.getText();
				scanCtr.acquireDarkFrames(numFrames, dir);
			}
		});
		btnRunDark.setBounds(10, 125, 117, 42);
		frame.getContentPane().add(btnRunDark);
		
		JButton btnCreateMaster = new JButton("Create master");
		btnCreateMaster.setBounds(148, 125, 117, 42);
		frame.getContentPane().add(btnCreateMaster);
	}

}
