package persistacq;

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

import calibration.LensInfo;
import calibration.WBSettings;


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
				PersistAcq param = f.getAnnotation(PersistAcq.class);
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
		
		//persist list
		FileOutputStream fileOut = new FileOutputStream(fileName);
		ObjectOutputStream out = new ObjectOutputStream(fileOut);
		out.writeObject(params);
		out.close();
		fileOut.close();		      
	}
	
	public void loadParams(String fileName, Object[] objs) throws Exception{
		
		//read list
        FileInputStream fileIn = new FileInputStream(fileName);
        ObjectInputStream in = new ObjectInputStream(fileIn);
        Hashtable<String,Object> pList = (Hashtable<String,Object>) in.readObject();
        in.close();
        fileIn.close();       
        
        for(Object o: objs) {
			Field[] fields = o.getClass().getDeclaredFields();
			for(Field f : fields) {
				f.setAccessible(true);
				Class type = f.getType();
				PersistAcq param = f.getAnnotation(PersistAcq.class);
				if(param != null) {
					String id = param.id();		
					Object data = pList.get(id);
					if(data != null) {
						if(type == JTextField.class ) {
							((JTextField)f.get(o)).setText((String)data);
						}else if(type == JCheckBox.class) {
							((JCheckBox)f.get(o)).setSelected((Boolean)data);
						}else if(type == LensInfo.class) {
							LensInfo d = (LensInfo)data;
							LensInfo orig = (LensInfo)f.get(o);
							orig.setAll(d);
						}else if(type == WBSettings.class) {
							WBSettings d = (WBSettings)data;
							WBSettings orig = (WBSettings)f.get(o);
							orig.setAll(d);
						}
					}
				}		
			}

        }
		
	}
	
}
