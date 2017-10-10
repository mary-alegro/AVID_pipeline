package edu.ucsf.slidescanner.persistacq;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;

import javax.swing.JCheckBox;
import javax.swing.JTextField;

import edu.ucsf.slidescanner.calibration.LensConfig;
import edu.ucsf.slidescanner.calibration.WBSettings;


public class AcqPersist {
	
	public AcqPersist() {
	}

	public void saveParams(String fileName, Object[] objs) throws Exception {
		
		Hashtable<String,Object> params = new Hashtable<String,Object>();
		
		for(Object o : objs) {
			Field[] fields = o.getClass().getDeclaredFields();
			for(Field f : fields) {
				f.setAccessible(true);
				Class type = f.getType();
				PersistParam param = f.getAnnotation(PersistParam.class);
				if(param != null) {
					String id = param.id();		
					Object data = null;
					// If its a JTextField, just save the String content
					if(type == JTextField.class) {
						data = ((JTextField)f.get(o)).getText();						
					}else if(type == JCheckBox.class) {
						data = (Boolean)((JCheckBox)f.get(o)).isSelected();
					}else {
						data = f.get(o);
					}
					params.put(id, data);
				}		
			}
		}
		
		//persist hashtable
		FileOutputStream fileOut = new FileOutputStream(fileName);
		ObjectOutputStream out = new ObjectOutputStream(fileOut);
		out.writeObject(params);
		out.close();
		fileOut.close();		      
	}
	
	public void loadParams(String fileName, Object[] objs) throws Exception{
		
		//read hashtable
        FileInputStream fileIn = new FileInputStream(fileName);
        ObjectInputStream in = new ObjectInputStream(fileIn);
        Hashtable<String,Object> pList = (Hashtable<String,Object>) in.readObject();
        in.close();
        fileIn.close();       
        
        for(Object obj: objs) {
			Field[] fields = obj.getClass().getDeclaredFields();
			for(Field field : fields) {
				
				boolean isAcessible = field.isAccessible();
				field.setAccessible(true);
				
				Class type = field.getType();
				PersistParam param = field.getAnnotation(PersistParam.class);
				if(param != null) {
					
					String id = param.id();		
					Object data = pList.get(id);
					
					if(data != null) {
						if(type == JTextField.class ) {
							((JTextField)field.get(obj)).setText((String)data);
						}else if(type == JCheckBox.class) {
							((JCheckBox)field.get(obj)).setSelected((Boolean)data);
						}else if(type == LensConfig.class) {
							field.set(obj,data); //obj is the instance whose field i need to change, data is the new value
						}else if(type == WBSettings.class) {
							field.set(obj,data);							
						}
					}
				}	
				
				field.setAccessible(isAcessible);
			}

        }
		
	}
	
}
