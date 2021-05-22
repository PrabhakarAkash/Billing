import pandas as pd
import math
import streamlit as st
import time
import numpy as np

def bill(DE,SE,location,df3):
    #st.write('bill executed')
    df3.loc[location,'Declared_energy'] = DE
    df3.loc[location,'Scheduled_energy'] = SE
    m_dict = {'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun','07':'Jul','08':'Aug','09':'Sept','10':'Oct','11':'Nov','12':'Dec'}
    not_entered = []
    
    #This will ask for Sch and Dec energy for all cum months
    for j in range(int(df3['Month_code'][location])-1): #-1 bcz bvalues already entered for location
        
        b = location - (df3['Month_code'][location])+j+1 
        #st.write(b)
        if df3['Declared_energy'][b]==0 or df3['Scheduled_energy'][b]==0:
            #st.write('Entered the loop')
            not_entered.append([m_dict.get(df3['Period'][b][-5:-3]),df3['Period'][b][:4]])
    if len(not_entered)!=0:
        st.write("Please enter Declared and Scheduled Energy for:")
        for i in not_entered:
            st.warning(str(i[0])+"'"+str(i[1]))

        ## This will check for CREC Rates               
    if math.isnan(df3['Escalated Energy'][location]) or math.isnan(df3['Escalated Inland Transportation'][location]) or math.isnan(df3['Escalated Capacity Charge'][location]):
        start_date = df3["Period"][location - df3['Month_code'][location] + 1]
        end_date = df3["Period"][location - df3['Month_code'][location] + 6]
        st.info("Please enter Escalation Rates for period {} to {} ".format(start_date[:7],end_date[:7] ))


    for i in range(139,len(df3)):

        df3.loc[i,'Base_energy'] = df3['ME_energy'][i - df3['Month_code'][i]]

        df3.loc[i,'ME_energy'] = round(df3['Base_energy'][i]*(1+((df3['Escalated Energy'][i])/12)*df3['Month_code'][i]),4)

        df3.loc[i,'MS_energy'] = df3['ME_energy'][i-1]

        df3.loc[i,'EI_energy'] = round(df3['MS_energy'][i]/100,4)
                ## Escalation Index Inland Transportation Charges
        df3.loc[i,'Base_inland'] = df3['ME_inland'][i - df3['Month_code'][i]]

        df3.loc[i,'ME_inland'] = round(df3['Base_inland'][i]*(1+((df3['Escalated Inland Transportation'][i])/12)*df3['Month_code'][i]),4)


        df3.loc[i,'MS_inland'] = df3['ME_inland'][i-1]

        df3.loc[i,'EI_inland'] = df3['MS_inland'][i]/100

        df3.loc[i,'EI_inland'] = round(df3.loc[i,'EI_inland'],4)

            ## Escalation Index Capacity Charges

    for i in range(139,len(df3)):

        df3.loc[i,'Base_capacity'] = df3['ME_capacity'][i - df3['Month_code'][i]]

        df3.loc[i,'ME_capacity'] = round(df3['Base_capacity'][i]*(1+((df3['Escalated Capacity Charge'][i])/12)*df3['Month_code'][i]),4)

        df3.loc[i,'MS_capacity'] = round(df3['ME_capacity'][i-1],4)

        df3.loc[i,'EI_capacity'] = round(df3['MS_capacity'][i]/100,4)

                 ## MEITPPn,MECPn,MEEPn   

    df3['MEITPPn'] = 0.4920 * df3['EI_inland']
    df3['MEITPPn']= np.floor(df3['MEITPPn']*10000)/10000
    df3['MECPn'] = 0.1820 * df3['EI_capacity']
    df3['MECPn']= np.floor(df3['MECPn']*10000)/10000         
    df3['MEEPn'] = 0.4560 * df3['EI_energy']
    df3['MEEPn']= np.floor(df3['MEEPn']*10000)/10000         


    ##########################################   Monthly Bill  ###########################################################             

    for j in range(int(df3['fiscal_month'][location])):

        a = location - (df3['fiscal_month'][location])+j+1  

        if df3['Declared_energy'][a] == 0:
            df3.loc[a,'Declared_energy'] = int(input('Please enter the Declared Energy(in kWh) for {} '.format(df3['Period'][a])))
            df3.loc[a,'Scheduled_energy'] = int(input('Please enter the Scheduled Energy(in kWh) for {} '.format(df3['Period'][a]))) 


        df3.loc[a,'PAFm'] = df3['Declared_energy'][a]/df3['Contracted_energy'][a]                                                    
        df3.loc[a,'Cum_Scheduled_energy'] = df3['Scheduled_energy'][location-df3['fiscal_month'][location]+1:a+1].sum()
        df3.loc[a,'Cum_Declared_energy'] = df3['Declared_energy'][location-df3['fiscal_month'][location]+1:a+1].sum()          
        df3.loc[a,'Cum_Contracted_energy'] = df3['Contracted_energy'][location-df3['fiscal_month'][location]+1:a+1].sum()


        df3.loc[a,'CPAF'] =      round(df3['Cum_Declared_energy'][a]/df3['Cum_Contracted_energy'][a],4)                                             

        df3.loc[a,'CC_on_NA'] = 0.85* df3['Total_capacity_charge'][a]*200000 * df3['hours'][a]   

        df3.loc[a,'Cum_CC_on_NA'] = df3['CC_on_NA'][location-df3['fiscal_month'][location]+1:a+1].sum()                                             

        #df3.loc[a,'Cum_CC_on_NA'] =   Cumulative_capacity_charge_on_NA

        df3.loc[a,'CC_on_Actual_Availability'] = df3['PAFm'][a] * df3['Total_capacity_charge'][a]*200000 * df3['hours'][a]                                           

        # Cum_cap_charge_on_actual_av += df3['CC_on_Actual_Availability'][a]  

        df3.loc[a,'Cum_CC_on_Actual_Availability'] =   df3['CC_on_Actual_Availability'][location-df3['fiscal_month'][location]+1:a+1].sum() 

        df3.loc[a,'Total_energy_charge_for_month'] = (df3['Total_energy_charge'][a]+df3['Total_inland_charge'][a])*df3['Scheduled_energy'][a]     

        df3.loc[a,'Cum_Total_capacity_charge']  = df3['Total_capacity_charge'][location-df3['fiscal_month'][location]+1:a+1].sum() 

        if df3['CPAF'][a] > 0.85:
            df3.loc[a,'Applicable_cum_CC'] = df3['Cum_CC_on_NA'][a]
            df3.loc[a,'Energy_applicable_for_incentive'] = df3['Cum_Declared_energy'][a] - (0.85*df3['Cum_Contracted_energy'][a])
            df3.loc[a,'Energy_applicable_for_penalty'] = 0
            df3.loc[a,'Rate_of_incentive'] = 0.4* df3['NE_capacity_charge'][location-df3['fiscal_month'][location]+1:a+1].sum()/df3['fiscal_month'][a] 
            if df3.loc[a,'Rate_of_incentive'] > 0.25: ## Condition on Incentive Rate
                df3.loc[a,'Rate_of_incentive'] = 0.25
        
        elif df3['CPAF'][a] < 0.80:
            df3.loc[a,'Energy_applicable_for_penalty'] = 0.8*df3['Cum_Contracted_energy'][a] - df3['Cum_Declared_energy'][a]
            df3.loc[a,'Rate_of_penalty'] = 0.2 * df3['Total_capacity_charge'][location-df3['fiscal_month'][location]+1:a+1].mean()

        else:
            df3.loc[a,'Applicable_cum_CC'] = df3['Cum_CC_on_Actual_Availability'][a]  
            df3.loc[a,'Energy_applicable_for_incentive'] = 0


        df3.loc[a,'Cum_incentive(Rs.)'] = df3['Rate_of_incentive'][a] * df3['Energy_applicable_for_incentive'][a]    
        df3.loc[a,'Cum_penalty(Rs.)'] = df3['Rate_of_penalty'][a] * df3['Energy_applicable_for_penalty'][a]                                     

        if df3['fiscal_month'][a] == 1:
            df3.loc[a,'Cum_CC_till_prev_month'] = 0
         
        else:

            df3.loc[a,'Cum_CC_till_prev_month'] = df3['Applicable_cum_CC'][a-1]                                        


        df3.loc[a,'Payable_CC_for_month'] =   df3['Applicable_cum_CC'][a] -  df3['Cum_CC_till_prev_month'][a]   
        df3.loc[a,'Cum_Incentive/Penalty'] =  df3['Cum_incentive(Rs.)'][a] - df3['Cum_penalty(Rs.)'][a]
       

        if df3['fiscal_month'][a] == 1:
            df3.loc[a,'Monthly_Incentive/Penalty'] = df3['Cum_Incentive/Penalty'][a]

        else: 
            df3.loc[a,'Monthly_Incentive/Penalty'] = df3['Cum_Incentive/Penalty'][a] - df3['Cum_Incentive/Penalty'][a-1]     

        if df3['Monthly_Incentive/Penalty'][a] > 0 :
            df3.loc[a,'Net_Incentive_for_this_month'] = df3['Monthly_Incentive/Penalty'][a] 
            df3.loc[a,'Net_Penalty_for_this_month'] = 0
        elif df3['Monthly_Incentive/Penalty'][a] < 0:
            df3.loc[a,'Net_Incentive_for_this_month'] = 0
            df3.loc[a,'Net_Penalty_for_this_month'] = df3['Monthly_Incentive/Penalty'][a] 

        df3.iloc[a,-1] = df3['Payable_CC_for_month'][a] + df3['Total_energy_charge_for_month'][a] + df3['Net_Incentive_for_this_month'][a] - df3['Net_Penalty_for_this_month'][a]
    
    
    
    
    
    calculated_df = pd.DataFrame({'Month':[str(m_dict.get(df3['Period'][location][-5:-3]))+"-"+str(df3['Period'][location][:4])],'Non Escalable Capacity Charge(ANEFCyn)':[df3['NE_capacity_charge'][location]],
        'Escalable Capacity Charge(AEFCyn)':[df3['MECPn'][location]],'Total Capacity Charge(AFCyn)':[df3['Total_capacity_charge'][location]],
        'Escalable Energy Charges(MEEPn)':[df3['MEEPn'][location]],'Escalable Inland Transporation Charges(MEITPn)':[df3['MEITPPn'][location]],
        'Total Energy Charges(MEPn)':[df3['Total_energy_charge'][a]+df3['Total_inland_charge'][a]],'Energy Corresponding to Contracted Capacity':[df3['Contracted_energy'][location]],
        'Energy Corresponding to Capacity Declared':[df3['Declared_energy'][location]],'Actual Availability %':[df3['PAFm'][location]*100],
        'Energy Scheduled to MSEDCL':[df3['Scheduled_energy'][location]],'Monthly Capacity Charge(FCm)':[df3['Payable_CC_for_month'][location]],
        "Monthly Energy Charges":[df3['Total_energy_charge_for_month'][location]],
        'Cumulative PAFm %':[df3['CPAF'][location]*100],'Rate of Penalty':[round(df3['Rate_of_penalty'][a],4)],"Rate of Incentive":[round(df3.loc[a,'Rate_of_incentive'],4)],
        'Net Incentive for month':[df3['Net_Incentive_for_this_month'][location]]
        ,'Net Penalty for month':[df3['Net_Penalty_for_this_month'][location]],
        'Total Tariff':[df3['Payable_CC_for_month'][location] + df3['Total_energy_charge_for_month'][location] + 
        df3['Net_Incentive_for_this_month'][location] - df3['Net_Penalty_for_this_month'][location]]})
    #st.write(m_dict.get(df3['Period'][location][-5:-3]),"-",df3['Period'][location][:4])
    calculated_df = calculated_df.T
    st.write('')
    st.write('')
    st.dataframe(calculated_df)#(Capacity charges + Energy charges +/- Incentive/Penalty)
    st.write('')
    st.write('')
    if st.button('Press to save the results'):
        df3.to_csv('final_end2.csv')    
    

    return calculated_df






























    with st.spinner('Generating the Report...'):
        time.sleep(0.8)
        st.success('Done!')     


    

