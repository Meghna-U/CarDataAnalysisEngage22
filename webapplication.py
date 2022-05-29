# importing required libraries
import pandas as pd
import streamlit as st
import plotly.express as px

# setting up the website
st.set_page_config(page_title='Automotive Industry')
st.header('Automobile Industry Data Analysis')

# reading the excel file
file_exc='cars_engage_2022.xlsx'
sheet='Worksheet'
df=pd.read_excel(file_exc,sheet_name=sheet,usecols='A:Z',header=0)
find=pd.read_excel(file_exc,sheet_name=sheet,usecols='AD:AE',header=0)
# dropping rows which have null values to make the information consistent
df.dropna(inplace=True)
find.dropna(inplace=True)
# display a dataframe showing the Make,Model and Variant
df1=df[['Make','Model','Variant']]
d1=df1.astype(str)
st.dataframe(d1)

make=df['Make'].unique().tolist()
model=df['Model'].unique().tolist()
variant=df['Variant'].unique().tolist()
fuel_type=df['Fuel_Type'].unique().tolist()
body_type=df['Body_Type'].unique().tolist()
showroomprice=df['Showroom_Price'].unique().tolist()
type=df['Type'].unique().tolist()

# making the slider for showroom price
srprice_select=st.slider('Showroom_Price:',min_value=min(showroomprice),max_value=max(showroomprice),value=(min(showroomprice),max(showroomprice)))
# making the multiselect choose options
make_select=st.multiselect('Make:',make,default=make)
model_select=st.multiselect('Model:',model,default=model)
variant_select=st.multiselect('Variant:',variant,default=variant)
fuel_type_select=st.multiselect('Fuel_Type:',fuel_type,default=fuel_type)
body_type_select=st.multiselect('Body_Type:',body_type,default=body_type)
type_select=st.multiselect('Type:',type,default=type)

# taking the intersection of the slider and multiselect options
mask=(df['Showroom_Price'].between(*srprice_select)) & (df['Make'].isin(make_select)) & (df['Model'].isin(model_select)) & (df['Variant'].isin(variant_select)) &(df['Fuel_Type'].isin(fuel_type_select)) & (df['Body_Type'].isin(body_type_select)) & (df['Type'].isin(type_select))
no_res=df[mask].shape[0]
# displaying the number of available choices based on the selected options
st.markdown(f'Available choices: {no_res}')
# grouping the dataframe based on selection
dfg=df[mask].groupby(by=['Model']).mean()[['Showroom_Price']]
dfg=dfg.reset_index()

# plotting bar graphs
bc=px.bar(dfg,x='Model',y='Showroom_Price',text='Showroom_Price',color_discrete_sequence=['#F63366']*len(dfg),template='plotly_white')
st.plotly_chart(bc)

dfg1=df[mask].groupby(by=['Model']).mean()[['Fuel_Tank_Capacity']]
dfg1=dfg1.reset_index()
bc1=px.bar(dfg1,x='Model',y='Fuel_Tank_Capacity',text='Fuel_Tank_Capacity')
st.plotly_chart(bc1)
# grouping the dataframe based on selection
df['City_Mileage']=df['City_Mileage'].astype(float)
df['Highway_Mileage']=df['Highway_Mileage'].astype(float)
dfg2=df[mask].groupby(by=['Model']).mean()[['City_Mileage','Highway_Mileage']]
dfg2=dfg2.reset_index()
bc2=px.bar(dfg2,x='Model',y=['City_Mileage','Highway_Mileage'],text='Model',color_discrete_sequence=['#F63366','#262730']*len(dfg2),template='plotly_white')
st.plotly_chart(bc2)

# other important information
dfp=df.astype(str)
ot=dfp[mask][['Make','Model','Variant','Cylinders','Drivetrain','Engine_Location','Fuel_Type','Body_Type','Seating_Capacity','Seats_Material','Power','Torque','Basic_Warranty','Airbags','Child_Safety_Locks']]
st.dataframe(ot)

dim=dfp[mask][['Make','Model','Variant','Height','Width','Length','Kerb_Weight','Doors']]
st.dataframe(dim)

# plotting pie chart
pc=px.pie(find,title='Customer segmentation on different brands of cars',values='Number_of_Customers',names='Brand')
st.plotly_chart(pc)
