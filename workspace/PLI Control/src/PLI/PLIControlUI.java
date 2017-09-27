package PLI;

import java.awt.EventQueue;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.File;

import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFormattedTextField;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JScrollPane;
import javax.swing.JSeparator;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.text.DefaultCaret;

import org.micromanager.Studio;

import mmcorej.CMMCore;

/**
*
* @author Maryana
*/

public class PLIControlUI {

	private JFrame frmPliControlV;
	private JTextField textDestFolder;
	private JTextField textFilePrefix;
	private JFormattedTextField textSlice;

	
	//Plugin attributes
	private Studio gui_;
	private CMMCore core_;
	private PLIControl plugin;
	private JTextArea textOutput;
	

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					PLIControlUI window = new PLIControlUI();
					window.frmPliControlV.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the application.
	 */
	public PLIControlUI() {
		initialize();
		setSlice("0");
		setAngle("0");
	}
	
	public PLIControlUI(Studio gui) throws Exception{
		gui_ = gui;
        try {
            core_ = gui_.getCMMCore();
        } catch (Exception ex) {
            throw new Exception("PLI Control plugin could not get MMCore");
        }
        
        //Init GUI
		initialize();
	}
	
	public void setControler(PLIControl ctr) {
		this.plugin = ctr;
	}
	
	public JFrame getFrame() {
		return this.frmPliControlV;
	}
	
	public String getDestFolder() {
		return textDestFolder.getText();
	}
	
	public void setSlice(String s) {
		textSlice.setText(s);
	}
	
	public void setAngle(String s) {
	}
	
	public int getSlice() {
		String str = textSlice.getText();
		int num = Integer.parseInt(str);
		return num;
	}
	
//	public int getAngle() {
//		String str = textAngleCount.getText();
//		int num = Integer.parseInt(str);
//		return num;
//	}
	
	public String getPrefix() {
		return textFilePrefix.getText();
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {
		frmPliControlV = new JFrame();
		frmPliControlV.setTitle("PLI Control v0.1");
		frmPliControlV.setBounds(100, 100, 596, 630);
		frmPliControlV.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frmPliControlV.getContentPane().setLayout(null);
		
		JLabel lblDestinationFolder = new JLabel("Destination folder:");
		lblDestinationFolder.setBounds(10, 11, 196, 14);
		frmPliControlV.getContentPane().add(lblDestinationFolder);
		
		textDestFolder = new JTextField();
		textDestFolder.setBounds(10, 36, 389, 20);
		frmPliControlV.getContentPane().add(textDestFolder);
		textDestFolder.setColumns(10);
		
		textSlice = new JFormattedTextField();
		textSlice.setBounds(148, 161, 110, 20);
		frmPliControlV.getContentPane().add(textSlice);
		
		JButton btnChooseDest = new JButton("Choose...");
		btnChooseDest.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent e) {
				JFileChooser chooser = new JFileChooser();
				chooser.setDialogTitle("Choose destination directory.");
				chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
				if(chooser.showOpenDialog(getFrame()) == JFileChooser.APPROVE_OPTION) {
					File folder = chooser.getSelectedFile();
					textDestFolder.setText(folder.getPath());
				}
			}
		});
		btnChooseDest.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
			}
		});
		btnChooseDest.setBounds(420, 35, 129, 23);
		frmPliControlV.getContentPane().add(btnChooseDest);
		
		JLabel lblFilePrefix = new JLabel("File prefix:");
		lblFilePrefix.setBounds(10, 67, 161, 14);
		frmPliControlV.getContentPane().add(lblFilePrefix);
		
		textFilePrefix = new JTextField();
		textFilePrefix.setBounds(10, 92, 539, 20);
		frmPliControlV.getContentPane().add(textFilePrefix);
		textFilePrefix.setColumns(10);
		
		JLabel lblSliceNum = new JLabel("Slice #:");
		lblSliceNum.setBounds(10, 164, 89, 14);
		frmPliControlV.getContentPane().add(lblSliceNum);
		
		JButton btnRun = new JButton("Run");
		btnRun.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent e) {
				String folder = textDestFolder.getText();
				if(folder.isEmpty()) {
					JOptionPane.showMessageDialog(frmPliControlV, "You must select the destination folder.");
					return;
				}
				String prefix = textFilePrefix.getText();
				if(prefix.isEmpty()) {
					JOptionPane.showMessageDialog(frmPliControlV, "You must type the file prefix.");
					return;
				}
				//String curText = textOutput.getText();
				//textOutput.setText(curText + "Acquire image!" + System.getProperty("line.separator"));
				plugin.runAcquisition(plugin.NUM_ANGLES);				
			}
		});
		btnRun.setBounds(10, 496, 89, 37);
		frmPliControlV.getContentPane().add(btnRun);
		
		JButton btnHome = new JButton("Home");
		btnHome.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent e) {
				plugin.goHome();
			}
		});
		btnHome.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
			}
		});
		btnHome.setBounds(109, 496, 89, 37);
		frmPliControlV.getContentPane().add(btnHome);
		
		JSeparator separator = new JSeparator();
		separator.setBounds(10, 202, 526, -2);
		frmPliControlV.getContentPane().add(separator);
		
		JScrollPane scrollPane = new JScrollPane();
		scrollPane.setBounds(20, 208, 537, 264);
		frmPliControlV.getContentPane().add(scrollPane);
		
		textOutput = new JTextArea();
		DefaultCaret caret = (DefaultCaret)textOutput.getCaret();
		caret.setUpdatePolicy(DefaultCaret.ALWAYS_UPDATE);
		scrollPane.setViewportView(textOutput);

	}
	public JTextArea getTextOutput() {
		return textOutput;
	}
	public JFormattedTextField getTextSlice() {
		return textSlice;
	}
	public JTextField getTextFilePrefix() {
		return textFilePrefix;
	}
	public JTextField getTextDestFolder() {
		return textDestFolder;
	}
}
