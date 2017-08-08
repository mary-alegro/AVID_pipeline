package PLI;

import java.awt.EventQueue;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.File;
import java.text.NumberFormat;
import java.util.Formatter;

import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFormattedTextField;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JSeparator;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.text.NumberFormatter;

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
	private JFormattedTextField textAngleCount;

	
	//Plugin attributes
	private Studio gui_;
	private CMMCore core_;
	private PLIControl controler;
	

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
		this.controler = ctr;
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
		textAngleCount.setText(s);
	}
	
	public int getSlice() {
		String str = textSlice.getText();
		int num = Integer.parseInt(str);
		return num;
	}
	
	public int getAngle() {
		String str = textAngleCount.getText();
		int num = Integer.parseInt(str);
		return num;
	}
	
	public String getPrefix() {
		return textFilePrefix.getText();
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {
		frmPliControlV = new JFrame();
		frmPliControlV.setTitle("PLI Control v0.1");
		frmPliControlV.setBounds(100, 100, 439, 583);
		frmPliControlV.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frmPliControlV.getContentPane().setLayout(null);
		
		JLabel lblDestinationFolder = new JLabel("Destination folder:");
		lblDestinationFolder.setBounds(10, 11, 141, 14);
		frmPliControlV.getContentPane().add(lblDestinationFolder);
		
		textDestFolder = new JTextField();
		textDestFolder.setBounds(10, 36, 306, 20);
		frmPliControlV.getContentPane().add(textDestFolder);
		textDestFolder.setColumns(10);
		
		textSlice = new JFormattedTextField();
		textSlice.setBounds(61, 161, 110, 20);
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
		btnChooseDest.setBounds(326, 35, 87, 23);
		frmPliControlV.getContentPane().add(btnChooseDest);
		
		JLabel lblFilePrefix = new JLabel("File prefix:");
		lblFilePrefix.setBounds(10, 67, 99, 14);
		frmPliControlV.getContentPane().add(lblFilePrefix);
		
		textFilePrefix = new JTextField();
		textFilePrefix.setBounds(10, 92, 403, 20);
		frmPliControlV.getContentPane().add(textFilePrefix);
		textFilePrefix.setColumns(10);
		
		JLabel lblSliceNum = new JLabel("Slice #:");
		lblSliceNum.setBounds(10, 164, 46, 14);
		frmPliControlV.getContentPane().add(lblSliceNum);
		
		JLabel lblNewLabel = new JLabel("Angle count:");
		lblNewLabel.setBounds(235, 164, 66, 14);
		frmPliControlV.getContentPane().add(lblNewLabel);
		
		final JTextArea textOutput = new JTextArea();
		textOutput.setBounds(10, 211, 403, 257);
		frmPliControlV.getContentPane().add(textOutput);
		
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
				String curText = textOutput.getText();
				textOutput.setText(curText + "Acquire image!" + System.getProperty("line.separator"));
				controler.acquireImages(18);
			}
		});
		btnRun.setBounds(10, 496, 89, 37);
		frmPliControlV.getContentPane().add(btnRun);
		
		JButton btnHome = new JButton("Home");
		btnHome.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent e) {
				textOutput.setText("");
			}
		});
		btnHome.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
			}
		});
		btnHome.setBounds(109, 496, 89, 37);
		frmPliControlV.getContentPane().add(btnHome);
		
		JSeparator separator = new JSeparator();
		separator.setBounds(10, 198, 403, 2);
		frmPliControlV.getContentPane().add(separator);
		
		JSeparator separator_1 = new JSeparator();
		separator_1.setBounds(10, 479, 403, 2);
		frmPliControlV.getContentPane().add(separator_1);

		textAngleCount = new JFormattedTextField();
		textAngleCount.setBounds(314, 161, 99, 20);
		frmPliControlV.getContentPane().add(textAngleCount);
		
		JButton btnTestShot = new JButton("Test Shot");
		btnTestShot.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent e) {
				controler.doTestShot();
			}
		});
		btnTestShot.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
			}
		});
		btnTestShot.setBounds(324, 496, 89, 37);
		frmPliControlV.getContentPane().add(btnTestShot);

	}
}
