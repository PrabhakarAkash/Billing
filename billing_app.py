import streamlit as st
import pandas as pandas
import numpy as np
from pathlib import Path
import os
import math
import datetime
from PIL import Image
import time
import math
import base64
timestr = time.strftime("%Y%m%d-%H%M%S")	
#import docx2txt
#import pdfplumber
import pandas as pd 
from billing_app_2 import *

def csv_downloader(data):
	csvfile = data.to_csv()
	b64 = base64.b64encode(csvfile.encode()).decode()
	new_filename = "Monthly_Bill_{}_.csv".format(timestr)
	st.markdown("#### Download file ###")
	href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!!</a>'
	st.markdown(href,unsafe_allow_html=True)

img = Image.open("GMR.jpg")
col7, col8, col9, cola, colb = st.beta_columns(5)
with col9:
	st.image(img,width = 120,use_column_width=True)


# def save_uploaded_file(uploadedfile):
# 	with open(os.path.join("tempDir",uploadedfile.name),"wb") as f:
# 		f.write(uploadedfile.getbuffer())
# 	return st.success("Saved file :{} in tempDir".format(uploadedfile.name))

@st.cache(allow_output_mutation=True)
def load_data():
	df3 = pd.read_csv('final_end2.csv',index_col=0)
	return df3

def change_date_format(month,year):
	if month<10:
		new = str(year)+'-0'+str(month)+'-01'
	else:
		new = str(year)+'-'+str(month)+'-01'	
	return str(new)



def main():
	menu = ['Monthly Bill','Data Updation','Load Data','PPA Synopsis']
	choice = st.sidebar.selectbox('Menu',menu)

	if choice == 'Monthly Bill':
		col20, col21, col22 = st.beta_columns([1.5,3,1])
		with col21:
			st.header('Monthly Bill Calculation')
		df3 = pd.read_csv('final_end2.csv',index_col=0)
		entry = st.date_input('Select Month')

		#st.write(entry)
		#st.write(type(entry))
		entry = change_date_format(entry.month,entry.year)
		#st.write(entry)
		#st.dataframe(df3)
		location = df3[df3['Period']==entry].index[0]
		#st.write(location)
		
		# entry = datetime.datetime.strptime
		#st.write(change_date_format(entry.month,entry.year))
		
		
		col3, col4 = st.beta_columns(2)
		with col3:
			DE = st.number_input('Enter Declared Energy (kWh)')
		with col4:
			SE = st.number_input('Enter Scheduled Energy (kWh)')
		st.write('')

		if st.button('Submit',key='new2'):
			with st.spinner('Calculating the Bill...'):
				time.sleep(0.8)
				st.success('Done!') 
			calculated_bill = bill(DE,SE,location,df3)
			csv_downloader(calculated_bill)
		
		


	elif choice == 'Data Updation':	
		col23, col24, col25 = st.beta_columns([2.2,3,1])
		with col24:
			st.header('Data Updation')
			st.write('')
			st.write('')
		df3 = pd.read_csv('final_end2.csv',index_col=0)
		df3['Period'] = df3['Period'].astype(str)
		
		######################################################## 1. To enter Escalation Rates   ###################################################
		st.subheader('Update CERC Escalation Rates')
		st.write('')
		col1, col2 = st.beta_columns(2)
		with col1:
		    fr = st.date_input('Select Start month')
		    fr = change_date_format(fr.month,fr.year)	
		    #st.write(fr)
		    per1 = df3[df3['Period']==fr].index[0]
		    #st.write(per1)
		with col2:
			to = st.date_input('Select End month')	
			to = change_date_format(to.month,to.year)
			per2 = df3[df3['Period']==to].index[0]
			#st.write(per2)
		

		colp, colq, colr = st.beta_columns(3)
		with colp:
			CERC_energy = st.number_input("Esc. Rate for Energy Charge(%)",0.0000,10.0000)
		with colq:
			CERC_capacity = st.number_input("Esc. Rate for Capacity Charge(%)",0.0000,10.0000)
		with colr:
			CERC_inland = st.number_input("Esc. Rate for transportation Charge(%)",0.0000,10.0000)
		
		#st.write(CERC_energy,CERC_capacity,CERC_inland)
		
		if st.button('Submit',key='new03'):
			if per2-per1  != 6:
				st.error('Please select 6 month period')
			else:
				df3.iloc[per1:per2+1,1] = CERC_energy/100
				df3.iloc[per1:per2+1,2] = CERC_inland/100
				df3.iloc[per1:per2+1,3] = CERC_capacity/100
				with st.spinner('Updating data...'):
					time.sleep(0.8)
					st.success('Done!')   


		##################################################### 2. To enter DE and SE  ##############################################################
		st.write('')
		st.write('')
		st.subheader('Update Energy Parameters')
		st.write('')
		entry2 = st.date_input('Select Month')
		entry2 = change_date_format(entry2.month,entry2.year)
		location2 = df3[df3['Period']==entry2].index[0]
		#st.write(location2)
		colx, coly= st.beta_columns(2)
		with colx:
			DE2 = st.number_input('Enter Declared Energy')
		with coly:
			SE2 = st.number_input('Enter Scheduled Energy')
		
		if st.button('Submit',key='new04'):
			df3.loc[location2,'Declared_energy'] = DE2	
			df3.loc[location2,'Scheduled_energy'] = SE2
			with st.spinner('Updating data...'):
				time.sleep(0.8)
				st.success('Done!')  

		df3.to_csv('final_end2.csv')	
		
	# elif choice == 'Billing Process':
		
	# 	df3 = pd.read_csv('final_end2.csv',index_col=0)
	# 	colj, colk = st.beta_columns(2)
	# 	with colj:
	# 		entry4 = st.date_input('Bill Presented On')
	# 	with colk:
	# 		entry5 = st.date_input('Payment done on')
	# 	st.write(str(entry4)[-2:])

	# 	if st.button('Submit',key='new06'):
	# 		if entry5-entry4:
	# 			pass

	# 	#entry4 = change_date_format(entry3.month,entry3.year)
	# 	location4 = df3[df3['Period']==entry4].index[0]


	   

	elif choice == 'Load Data':

		col30, col31, col32 = st.beta_columns([2.7,3,1])
		with col31:
			st.header('Load Data')
		df3 = pd.read_csv('final_end2.csv',index_col=0)
		entry3 = st.date_input('Select Month')
		entry3 = change_date_format(entry3.month,entry3.year)
		location3 = df3[df3['Period']==entry3].index[0]
		df_copy = df3.copy()
		df_copy.columns = ['Period','Escalated Energy', 'Escalated Inland Transportation',
       'Escalated Capacity Charge', 'Month_code', 'Base_inland', 'MS_inland',
       'ME_inland', 'EI_inland', 'MEITPn', 'MS_energy', 'ME_energy',
       'EI_energy', 'MEEPn', 'Base_energy', 'MS_capacity', 'ME_capacity',
       'EI_capacity', 'MECPn', 'Base_capacity', 'Non esc. Capacity charge',
       'Non esc. Energy charge', 'Non esc. Inland Tr. charge', 'Total Capacity charge',
       'Total Energy charge', 'Total Inland Tr. charge', 'Total Tariff', 'year',
       'month', 'days', 'hours', 'Contracted energy', 'Declared energy',
       'Scheduled energy', 'CPAF', 'PAFm', 'CC_on_NA', 'Cum_CC_on_NA',
       'CC_on_Actual_Availability', 'Cum_CC_on_Actual_Availability',
       'Cum.Capacity Charge till this month', 'Cum.Capacity Charge till prev. month', 'Capacity charge for this month',
       'fiscal_month', 'Cum_incentive(Rs.)', 'Cum_penalty(Rs.)',
       'Rate of Incentive', 'Rate of Penalty',
       'Energy_applicable_for_incentive', 'Energy_applicable_for_penalty',
       'Cum_Monthly_Incentive/Penalty', 'Monthly_Incentive/Penalty',
       'Net Incentive for this month', 'Net Penalty for this month',
       'Cum_Incentive/Penalty', 'Energy Charge for this month',
       'Cum_Scheduled_energy', 'Cum_Declared_energy', 'Cum_Contracted_energy',
       'Cum_Total_capacity_charge', 'Total Tariff Payable(Cap.+En.+/-Incentive/Penalty)']
		#st.write(df_copy.columns)
		feat = ('All','Period','MECPn','MEEPn','MEITPn', 'Non esc. Capacity charge', 'Non esc. Energy charge', 'Non esc. Inland Tr. charge',
	    'Total Capacity charge','Total Energy charge','Total Inland Tr. charge','Contracted energy', 'Declared energy',
       'Scheduled energy','CPAF', 'PAFm','Rate of Incentive', 'Rate of Penalty','Net Incentive for this month', 'Net Penalty for this month',
       'Energy Charge for this month','Capacity charge for this month','Cum.Capacity Charge till prev. month','Cum.Capacity Charge till this month',
       'Total Tariff Payable(Cap.+En.+/-Incentive/Penalty)')

		st.write('')
		st.write('')
		st.write('')
		selected_feat = st.multiselect("Select features",feat,default=['Period','Energy Charge for this month','Capacity charge for this month','Total Tariff Payable(Cap.+En.+/-Incentive/Penalty)'])#,"PAFm","CPAF",
		df_copy.loc[location3,'Total Tariff Payable(Cap.+En.+/-Incentive/Penalty)'] = df_copy['Capacity charge for this month'][location3] + df_copy['Energy Charge for this month'][location3] + df_copy['Net Incentive for this month'][location3] - df_copy['Net Penalty for this month'][location3]	
		st.write('')
		st.write('')
		st.write('')
		if st.button('Submit',key='new05'):
			with st.spinner('Loading data...'):
				time.sleep(0.8)
				st.success('Done!')     
				st.write('')	
				df_copy['CPAF'] = round(df_copy['CPAF']*100,2)
				df_copy['PAFm'] = round(df_copy['PAFm']*100,2)
				if 'All' in selected_feat:
					ff = ['Period','MECPn','MEEPn','MEITPn', 'Non esc. Capacity charge', 'Non esc. Energy charge', 'Non esc. Inland Tr. charge',
	    'Total Capacity charge','Total Energy charge','Total Inland Tr. charge','Contracted energy', 'Declared energy',
       'Scheduled energy','CPAF', 'PAFm','Rate of Incentive', 'Rate of Penalty','Net Incentive for this month', 'Net Penalty for this month',
       'Energy Charge for this month','Capacity charge for this month','Cum.Capacity Charge till prev. month','Cum.Capacity Charge till this month',
       'Total Tariff Payable(Cap.+En.+/-Incentive/Penalty)']
					st.dataframe(df_copy.loc[location3,ff])
					csv_downloader(df_copy.loc[location3,ff])
				else:	
					st.dataframe(df_copy.loc[location3,selected_feat])
					csv_downloader(df_copy.loc[location3,selected_feat])			
			
	else:
		col12,col13,col14 =   st.beta_columns([2.4,3,1])
		with col13:
			st.header("PPA Synopsis")
			st.write('')
			st.write('')
		
		menu2 = ["Home","Major Terms/Dates","Conditions to be satisfied","Supply of Power","Billing and Payment",
			"Force Majeure","Change in Law","Events of Defaults and Termination","Dispute Resolution","Monthly Tariff"]
		choice2 = st.sidebar.selectbox('Subjects',menu2)

		if choice2 == "Major Terms/Dates":
			img15 = Image.open("s15.png")
			st.image(img15,width = 120,use_column_width=True)

		elif choice2 =='Home':
			img0 = Image.open("img0.png")
			st.image(img0,width = 120,use_column_width=True)	

		elif choice2 == "Conditions to be satisfied":
			img14 = Image.open("s14.png")
			st.image(img14,width = 120,use_column_width=True)

		elif choice2 == "Supply of Power":
			img13 = Image.open("s13.png")
			st.image(img13,width = 120,use_column_width=True)	

		elif choice2 == "Billing and Payment":
			img12 = Image.open("s12.png")
			st.image(img12,width = 120,use_column_width=True)	
			st.write('')
			st.write('')
			img11 = Image.open("s11.png")
			st.image(img11,width = 120,use_column_width=True)
			st.write('')
			st.write('')
			img10 = Image.open("s10.png")
			st.image(img10,width = 120,use_column_width=True)	
			
		elif choice2 == "Force Majeure":
			img9 = Image.open("s9.png")
			st.image(img9,width = 120,use_column_width=True)	
			st.write('')
			st.write('')
			img8 = Image.open("s8.png")
			st.image(img8,width = 120,use_column_width=True)
		
		elif choice2 == "Change in Law":
			img7 = Image.open("s7.png")
			st.image(img7,width = 120,use_column_width=True)

		elif choice2 == "Events of Defaults and Termination":
			img6 = Image.open("s6.png")
			st.image(img6,width = 120,use_column_width=True)	
			st.write('')
			st.write('')
			img5 = Image.open("s5.png")
			st.image(img5,width = 120,use_column_width=True)

		elif choice2 == "Dispute Resolution":
			img4 = Image.open("s4.png")
			st.image(img4,width = 120,use_column_width=True)

		elif choice2 == "Monthly Tariff":
			img3 = Image.open("s3.png")
			st.image(img3,width = 120,use_column_width=True)	
			st.write('')
			st.write('')
			img2 = Image.open("s2.png")
			st.image(img2,width = 120,use_column_width=True)
			st.write('')
			st.write('')
			img1 = Image.open("s1.png")
			st.image(img1,width = 120,use_column_width=True)

		# img15 = Image.open("s15.png")
		# st.image(imgs15,width = 120,use_column_width=True)
###Take care MEITPPn 











		# Working with File Upload

		# uploaded_file = st.file_uploader("Choose an XLSX file", type="xlsx")
		# if uploaded_file is not None:
		# 	file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type}
		# 	df = pd.read_excel(uploaded_file)
		# 	st.dataframe(df)
		# 	save_uploaded_file(uploaded_file)
		

		



		#if uploaded_file:
    	#	df = pd.read_excel(uploaded_file)
    	#	st.dataframe(df)
    	#	st.table(df)
		#df1 = pd.read_excel(file)
		#uploaded_file = st.file_uploader("Upload Files",type=["xlsx"])
		#st.write(df1)



		#file_type = st.selectbox("Select File Type",["excel","txt","pdf","docx","csv"])
	

		#st.write(processed_file)

























if __name__=='__main__':
	main()	