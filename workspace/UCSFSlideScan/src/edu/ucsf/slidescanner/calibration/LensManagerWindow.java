package edu.ucsf.slidescanner.calibration;

import java.awt.EventQueue;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;
import java.util.List;

import javax.swing.AbstractListModel;
import javax.swing.DefaultListModel;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JOptionPane;
import javax.swing.JScrollPane;
import javax.swing.JTextField;

public class LensManagerWindow {

	private JFrame frame;
	private JTextField textBrand;
	private JTextField textModel;
	private JTextField textFOV_X;
	private JTextField textFOV_Y;
	private JTextField textWorkDist;
	private JList listLenses;
	private DefaultListModel listModel;
	
	private LensConfig newLens;
	private String lensFile = LensConfig.lensFile;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					LensManagerWindow window = new LensManagerWindow();
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
	public LensManagerWindow() {
		initialize();
		listModel = new DefaultListModel();
		try {
			List<LensConfig> listLens = LensConfig.loadItems(listModel,lensFile);				
			if(listLens != null) {
				for(LensConfig lens : listLens) {
					listModel.addElement(lens);
				}
			}
		}catch(Exception e) {
			e.printStackTrace();			
		}
		getListLenses().setModel(listModel);
	}
	
	public LensManagerWindow getSelf() {
		return this;
	}
	
	public JFrame getFrame() {
		return frame;
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {
		frame = new JFrame();
		frame.setBounds(100, 100, 450, 482);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.getContentPane().setLayout(null);
		
		JScrollPane scrollPane = new JScrollPane();
		scrollPane.setBounds(10, 11, 414, 170);
		frame.getContentPane().add(scrollPane);
		
		listLenses = new JList();
		listLenses.setModel(new AbstractListModel() {
			String[] values = new String[] {};
			public int getSize() {
				return values.length;
			}
			public Object getElementAt(int index) {
				return values[index];
			}
		});
		scrollPane.setViewportView(listLenses);
		
		JButton btnEdit = new JButton("Edit");
		btnEdit.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				newLens = (LensConfig)listLenses.getSelectedValue();
				if(newLens == null) {
					return;
				}
				textBrand.setEnabled(true);
				textBrand.setText(newLens.getMake());				
				textModel.setEnabled(true);
				textModel.setText(newLens.getModel());
				textWorkDist.setEnabled(true);
				textWorkDist.setText(newLens.getWorkDist()+"");
				textFOV_X.setEnabled(true);
				textFOV_X.setText(newLens.getFOV()[0]+"");
				textFOV_Y.setEnabled(true);
				textFOV_Y.setText(newLens.getFOV()[1]+"");				
			}
		});
		btnEdit.setBounds(122, 192, 82, 23);
		frame.getContentPane().add(btnEdit);
		
		JLabel lblLenseModel = new JLabel("Brand:");
		lblLenseModel.setBounds(10, 251, 98, 14);
		frame.getContentPane().add(lblLenseModel);
		
		textBrand = new JTextField();
		textBrand.setEnabled(false);
		textBrand.setBounds(50, 248, 374, 20);
		frame.getContentPane().add(textBrand);
		textBrand.setColumns(10);
		
		JLabel lblModel = new JLabel("Model:");
		lblModel.setBounds(10, 287, 46, 14);
		frame.getContentPane().add(lblModel);
		
		textModel = new JTextField();
		textModel.setEnabled(false);
		textModel.setColumns(10);
		textModel.setBounds(50, 284, 374, 20);
		frame.getContentPane().add(textModel);
		
		JLabel lblFov = new JLabel("FOV");
		lblFov.setBounds(10, 333, 46, 14);
		frame.getContentPane().add(lblFov);
		
		JLabel lblX = new JLabel("Width:");
		lblX.setBounds(46, 333, 46, 14);
		frame.getContentPane().add(lblX);
		
		textFOV_X = new JTextField();
		textFOV_X.setEnabled(false);
		textFOV_X.setBounds(95, 330, 86, 20);
		frame.getContentPane().add(textFOV_X);
		textFOV_X.setColumns(10);
		
		JLabel lblHeight = new JLabel("Height:");
		lblHeight.setBounds(200, 333, 46, 14);
		frame.getContentPane().add(lblHeight);
		
		textFOV_Y = new JTextField();
		textFOV_Y.setEnabled(false);
		textFOV_Y.setColumns(10);
		textFOV_Y.setBounds(249, 330, 86, 20);
		frame.getContentPane().add(textFOV_Y);
		
		JLabel lblWorkDistance = new JLabel("Work Distance:");
		lblWorkDistance.setBounds(10, 368, 82, 14);
		frame.getContentPane().add(lblWorkDistance);
		
		textWorkDist = new JTextField();
		textWorkDist.setEnabled(false);
		textWorkDist.setColumns(10);
		textWorkDist.setBounds(95, 365, 86, 20);
		frame.getContentPane().add(textWorkDist);
		
		JButton btnAdd = new JButton("+");
		btnAdd.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				newLens = new LensConfig();
				textBrand.setEnabled(true);
				textModel.setEnabled(true);
				textFOV_X.setEnabled(true);
				textFOV_Y.setEnabled(true);
				textWorkDist.setEnabled(true);
				listModel.addElement(newLens);
			}
		});
		btnAdd.setBounds(10, 192, 46, 23);
		frame.getContentPane().add(btnAdd);
		
		JButton btnClear = new JButton("Cancel");
		btnClear.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				textBrand.setText("");
				textModel.setText("");
				textFOV_X.setText("");
				textFOV_Y.setText("");
				textWorkDist.setText("");
				
				if(newLens != null) {
					listModel.removeElement(newLens);
					listLenses.updateUI();
					newLens = null;
				}
			}
		});
		btnClear.setBounds(109, 409, 89, 23);
		frame.getContentPane().add(btnClear);
		
		JButton btnRemove = new JButton("-");
		btnRemove.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				LensConfig select = (LensConfig)listLenses.getSelectedValue();
				if(select == null) {
					return;
				}
				listModel.removeElement(select);
				listLenses.updateUI();
				int response = JOptionPane.showConfirmDialog(getFrame(), "Are you sure you want to delete this lens?");
			    if (response == JOptionPane.YES_OPTION) {
			    	try {
			    		LensConfig.saveItems(listModel,lensFile);	
			    	}catch(Exception ex) {
			    		ex.printStackTrace();
			    	}
			    } 
				
			}
		});
		btnRemove.setBounds(66, 192, 46, 23);
		frame.getContentPane().add(btnRemove);
		
		JButton btnSave = new JButton("Save");
		btnSave.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				if(newLens != null) {
					newLens.setModel(textModel.getText());
					newLens.setMake(textBrand.getText());
					double w = Double.parseDouble(textFOV_X.getText());
					double h = Double.parseDouble(textFOV_X.getText());
					newLens.setFOV(new double[]{w,h});
					double wd = Double.parseDouble(textWorkDist.getText());
					newLens.setWorkDist(wd);
					//getListLenses().setModel(listModel);
					listLenses.updateUI();
					
					try {
						LensConfig.saveItems(listModel,lensFile);						
						JOptionPane.showMessageDialog(getFrame(),"New lens was added with success");
						newLens = null;
					}catch(Exception ex) {
						ex.printStackTrace();
					}
					
				}
			}
		});
		btnSave.setBounds(10, 409, 89, 23);
		frame.getContentPane().add(btnSave);
	}
	protected JList getListLenses() {
		return listLenses;
	}
	

}
