
#Importing Required Packages

from PIL import Image
import pytesseract
import configuration
import sqlite3
# In[49]:


#This function will handle the OCR processing of images

def ocr_processing(filename):
    
    text = pytesseract.image_to_string (Image.open(filename),config='--psm 12 --oem 3')  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
           
    return text


# In[50]:


def file_processing(filename): 
    
    try:      
        

        #Python-tesseract is a wrapper for Google’s Tesseract-OCR Engine. Here we connect with tesseract, which installed on system

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        #Passing image to ocr_processing function

        data = ocr_processing(filename)

        #Converting string to list by using split function, where \n is used as split parameter

        data_extracted_from_image = data.split('\n')

        #Creating new list list_without_null_values, where all null values are removed

        list_without_null_values = [i for i in data_extracted_from_image if i]

        #Data in list along with index

        #for index, value in enumerate(list_without_null_values): 
        #    print(index, value)

        #Check if the repory belongs to approved lab and test

        if (list_without_null_values[0] in configuration.approved_labs) and (list_without_null_values[20].replace("Test Name : ","") in configuration.approved_tests):

            #Creating dict with report details

            default_dict = {
            'Lab_Name':list_without_null_values[0],
            'Patient_Name':list_without_null_values[4],
            'Test_Name':list_without_null_values[20],
            'Hemoglobin':list_without_null_values[27],
            'PCV':list_without_null_values[31],
            'RBC':list_without_null_values[35],
            'MCV':list_without_null_values[39],
            'MCH':list_without_null_values[43],
            'MCHC':list_without_null_values[47],
            'RDW':list_without_null_values[51],
            'TLC':list_without_null_values[55],
            'Platelet_Count':list_without_null_values[101],
            'username':list_without_null_values[107]
            }

            insert_into_db(default_dict)
           
            text = "Submitted Reports of Patient Name :- " + default_dict['Patient_Name']
            
            return text
        
        else:

            text = "Invalid File Report"
            
            return text        
        
    except:
        
        text = "Error occurred during file processing!!"
        
        return text        


# In[51]:


#This function will insert data into database

def insert_into_db(patient_data_dict):
           
    con = sqlite3.connect('C:/xampp/htdocs/Lab-master/Lab_Reports.db', timeout=10)
    if con:
        print("OK")
    else:
        print("NOT OK")
    
    cur = con.cursor()
    h=patient_data_dict['Hemoglobin']
    pcv=patient_data_dict['PCV']
    rbc=patient_data_dict['RBC']
    mcv=patient_data_dict['MCV']
    mch=patient_data_dict['MCH'] 
    mchc=patient_data_dict['MCHC']
    rdw=patient_data_dict['RDW']
    tlc=patient_data_dict['TLC']
    pc=patient_data_dict['Platelet_Count']
    if ((float(h)>=14 and float(h)<=18) and (float(pcv)>=35 and float(pcv)<=90) and (float(rbc)>=4.5 and float(rbc)<=6)and (float(mcv) >=82 and float(mcv)<=98) and (float(mch) >=27 and float(mch)<31) and (float(mchc) >=32 and float(mchc)<=36) and (float(rdw) >=11 and float(rdw)<=16) and (float(tlc) >=4.5 and float(tlc)<=11) and (float(pc) >=150 and float(pc)<=450)):
        sql_query = "INSERT INTO CITY_PATHOLOGY_LAB_FEVER_PANEL (Patient_Name,Hemoglobin,PCV,RBC,MCV,MCH,MCHC,RDW,TLC,Platelet_Count,status,username,dates) VALUES (?,?,?,?,?,?,?,?,?,?,'rejected',?,DateTime('now'))"
        cur.execute(sql_query,(patient_data_dict['Patient_Name'],patient_data_dict['Hemoglobin'],patient_data_dict['PCV'],  
        patient_data_dict['RBC'],patient_data_dict['MCV'],patient_data_dict['MCH'], 
        patient_data_dict['MCHC'],patient_data_dict['RDW'],patient_data_dict['TLC'], 
        patient_data_dict['Platelet_Count'], patient_data_dict['username']))

    elif((float(h)<14 or float(h)>18) or (float(pcv)<35 or float(pcv)>90) or (float(rbc)<4.5 or float(rbc)>6)or (float(mcv) <82 or float(mcv)>98) or (float(mch) <27 or float(mch)>31) or (float(mchc) <32 or float(mchc)>36) or (float(rdw) <11 or float(rdw)>16) or (float(tlc) <4.5 or float(tlc)>11) or (float(pc) <150 or float(pc)>450)):
        sql_query = "INSERT INTO CITY_PATHOLOGY_LAB_FEVER_PANEL (Patient_Name,Hemoglobin,PCV,RBC,MCV,MCH,MCHC,RDW,TLC,Platelet_Count,status,username,dates) VALUES (?,?,?,?,?,?,?,?,?,?,'accepted',?,DateTime('now'))"
        cur.execute(sql_query,(patient_data_dict['Patient_Name'],patient_data_dict['Hemoglobin'],patient_data_dict['PCV'],  
        patient_data_dict['RBC'],patient_data_dict['MCV'],patient_data_dict['MCH'], 
        patient_data_dict['MCHC'],patient_data_dict['RDW'],patient_data_dict['TLC'], 
        patient_data_dict['Platelet_Count'],patient_data_dict['username']))

    


    con.commit()
    con.close()  


# In[54]:


#text = file_processing('report3.jpg')

