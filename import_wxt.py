# from requests import Session
import requests as rq
import time as time
import json
import re
from datetime import datetime, timedelta, timezone
import pandas as pd
import re
# from email_script import email_me

# disable warnings
import warnings
warnings.filterwarnings("ignore")

def main():
    # get today's datetime
    today = datetime.now().strftime("%Y-%m-%d")
    
    # open the last data sent by the weather station
    dados = pd.read_csv('dados_wxt_upto_%s.csv' % today,sep=';',header=None,quoting=3)

    # read the last value of the weather station
    dados1 = dados[[0,13,14,15,16,17,18,19]]
    dados1[0] = dados1[0].str.replace('"','')
    dados1[0] = pd.to_datetime(dados1[0]).astype(str)
    list_dados = [13,14,15,16,17,18]

    dados_met = pd.DataFrame({'Data': dados1[0], #dados[0].str.split(' ', expand=True)[0],
                            #   'Hora': dados[0].str.split(' ', expand=True)[1],
                            'Pressão atmosférica (bar)': dados1[13],
                            'Temperatura do ar (°C)': dados1[14],
                            'Umidade relativa do ar (%)': dados1[15],
                            'Precipitação (mm)': dados1[16],
                            'Velocidade do vento (m/s)': dados1[17],
                            'Direção do vento (˚)': dados1[18],
                            'Bateria (v)': dados1[19]})

    dados_met['Data'] = pd.to_datetime(dados_met['Data']) - timedelta(hours=4)
    dados_met['Pressão atmosférica (bar)'] = dados_met['Pressão atmosférica (bar)'].str[-5:]

    for i in dados_met: #range(1,dados.shape[1]-1):
        if i == 'Data':
            dados_met[i] = dados_met[i].astype('datetime64[ns]')
        else:
            dados_met[i] = pd.to_numeric(dados_met[i], errors='coerce')

    # read the last-1 value of the weather station
    dados2 = dados[[0,7,8,9,10,11,12,13]]

    dados2[0] = dados2[0].str.replace('"','')
    dados2[0] = pd.to_datetime(dados2[0]).astype(str)
    list_dados = [7,8,9,10,11,12,13]

    dados_met2 = pd.DataFrame({'Data': dados2[0], #dados[0].str.split(' ', expand=True)[0],
                            #   'Hora': dados[0].str.split(' ', expand=True)[1],
                            'Pressão atmosférica (bar)': dados2[7],
                            'Temperatura do ar (°C)': dados2[8],
                            'Umidade relativa do ar (%)': dados2[9],
                            'Precipitação (mm)': dados2[10],
                            'Velocidade do vento (m/s)': dados2[11],
                            'Direção do vento (˚)': dados2[12],
                            'Bateria (v)': dados2[13]})

    dados_met2['Data'] = pd.to_datetime(dados_met2['Data']) - timedelta(hours=5)
    dados_met2['Pressão atmosférica (bar)'] = dados_met2['Pressão atmosférica (bar)'].str[-5:]

    for i in dados_met2: #range(1,dados.shape[1]-1):
        if i == 'Data':
            dados_met2[i] = dados_met2[i].astype('datetime64[ns]')
        else:
            dados_met2[i] = pd.to_numeric(dados_met2[i], errors='coerce')

    # read the last-2 value of the weather station
    dados3 = dados[[0,1,2,3,4,5,6,7]]

    dados3[0] = dados3[0].str.replace('"','')
    dados3[0] = pd.to_datetime(dados3[0]).astype(str)
    list_dados = [1,2,3,4,5,6,7]

    dados_met3 = pd.DataFrame({'Data': dados3[0], #dados[0].str.split(' ', expand=True)[0],
                            #   'Hora': dados[0].str.split(' ', expand=True)[1],
                            'Pressão atmosférica (bar)': dados3[1],
                            'Temperatura do ar (°C)': dados3[2],
                            'Umidade relativa do ar (%)': dados3[3],
                            'Precipitação (mm)': dados3[4],
                            'Velocidade do vento (m/s)': dados3[5],
                            'Direção do vento (˚)': dados3[6],
                            'Bateria (v)': dados3[7]})

    dados_met3['Data'] = pd.to_datetime(dados_met3['Data']) - timedelta(hours=6)
    dados_met3['Pressão atmosférica (bar)'] = dados_met3['Pressão atmosférica (bar)'][-5:]

    for i in dados_met3:
        if i == 'Data':
            dados_met3[i] = dados_met3[i].astype('datetime64[ns]')
        else:
            dados_met3[i] = pd.to_numeric(dados_met3[i], errors='coerce')

    dados_met = dados_met.set_index('Data')
    dados_met2 = dados_met2.set_index('Data')
    dados_met3 = dados_met3.set_index('Data')

    dados_met = dados_met.combine_first(dados_met2)
    dados_met = dados_met.combine_first(dados_met3)

    dados_met = dados_met.reset_index()

    dados = pd.read_csv('~/hydronet/dados_met_updated.txt', sep=';')

    dados_full = pd.concat([dados,dados_met], ignore_index=True).drop_duplicates(subset='Data', keep='last').reset_index(drop=True)
    dados_full['Data'] = pd.to_datetime(dados_full['Data'])
    dados_full = dados_full.drop_duplicates(subset='Data', keep='last').reset_index(drop=True)

    dados_full.to_csv('~/hydronet/dados_met_updated.txt', sep=';', index=False)

    df_unique_dates = dados_met[~dados_met['Data'].isin(dados['Data'])]
    df_unique_dates.to_csv('~/hydronet/dados_met_upload.txt', sep=';', index=False)

if __name__ == '__main__':
    main()