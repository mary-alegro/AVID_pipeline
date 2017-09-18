package edu.ucsf.slidescanner.calibration;

import java.awt.EventQueue;

import javax.swing.JFrame;
import javax.swing.JList;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JTextField;

public class WBPresetsManagerWindow {

	private JFrame frame;
	private JTextField textField;
	private JTextField textField_1;
	private JTextField textField_2;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					WBPresetsManagerWindow window = new WBPresetsManagerWindow();
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
	public WBPresetsManagerWindow() {
		initialize();
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {
		frame = new JFrame();
		frame.setBounds(100, 100, 450, 323);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.getContentPane().setLayout(null);
		
		JList list = new JList();
		list.setBounds(11, 11, 412, 111);
		frame.getContentPane().add(list);
		
		JButton button = new JButton("+");
		button.setBounds(11, 133, 46, 23);
		frame.getContentPane().add(button);
		
		JButton button_1 = new JButton("-");
		button_1.setBounds(67, 133, 46, 23);
		frame.getContentPane().add(button_1);
		
		JButton button_2 = new JButton("Edit");
		button_2.setBounds(123, 133, 82, 23);
		frame.getContentPane().add(button_2);
		
		JLabel lblRed = new JLabel("Red:");
		lblRed.setBounds(11, 184, 46, 14);
		frame.getContentPane().add(lblRed);
		
		textField = new JTextField();
		textField.setEnabled(false);
		textField.setColumns(10);
		textField.setBounds(48, 181, 86, 20);
		frame.getContentPane().add(textField);
		
		JLabel lblGreen = new JLabel("Green:");
		lblGreen.setBounds(150, 184, 46, 14);
		frame.getContentPane().add(lblGreen);
		
		textField_1 = new JTextField();
		textField_1.setEnabled(false);
		textField_1.setColumns(10);
		textField_1.setBounds(192, 181, 86, 20);
		frame.getContentPane().add(textField_1);
		
		JButton button_3 = new JButton("Save");
		button_3.setBounds(17, 250, 89, 23);
		frame.getContentPane().add(button_3);
		
		JButton button_4 = new JButton("Cancel");
		button_4.setBounds(116, 250, 89, 23);
		frame.getContentPane().add(button_4);
		
		JLabel lblBlue = new JLabel("Blue:");
		lblBlue.setBounds(288, 184, 46, 14);
		frame.getContentPane().add(lblBlue);
		
		textField_2 = new JTextField();
		textField_2.setEnabled(false);
		textField_2.setColumns(10);
		textField_2.setBounds(330, 181, 86, 20);
		frame.getContentPane().add(textField_2);
	}

}
