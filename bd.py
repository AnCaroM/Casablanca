# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 22:44:16 2023

@author: Carlos Camilo Caro
"""

from datetime import datetime
import streamlit as st
import pandas as pd
from io import BytesIO

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

now = datetime.now()
st.title("REGISTROS CASABLANCA MUEBLES TUNJA") 

st.write("Ingrese gasto nuevo")
lista_tipos = ["Muebles","Casa","Tapiceria"]
lista_tipos.insert(0, "-")
if st.checkbox("Agregar gasto"):
    df = pd.read_excel('df.xlsx')
    col1, col2, col3= st.columns(3)
    with col1:
        gasto = st.text_input('Gasto',"-")
    with col2:
        costo = st.text_input('Costo',"-")
    with col3:
        tipo=st.selectbox("Tipo", ((lista_tipos)))
        
    if st.button("Agregue registro"):
        if tipo == "-" or gasto == "-" or costo == "-":
            st.error('Por favor ingrese datos')
        else:
            df = df.append({'Gasto':gasto, 'Costo':float(costo), 'Tipo':tipo, 'fecha':now}, ignore_index=True)
            df.to_excel("df.xlsx",index=False)
            st.success('Registro insertado')

if st.checkbox("Ver tabla"):
    df = pd.read_excel('df.xlsx')
    df.loc[:, 'Precio'] ='$'+ df['Costo'].map('{:,.0f}'.format)
    dff =df[['Gasto', 'Precio', 'Tipo', 'fecha']]
    st.dataframe(dff)
    st.download_button(label='📥 Descargar DATAFRAME GENERADO', data=to_excel(df) ,file_name= "df.xlsx")
    

