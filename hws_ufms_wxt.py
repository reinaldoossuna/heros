# from requests import Session
import requests as rq
import time as time
import json
import re
from datetime import datetime, timedelta, timezone
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

# from email_script import email_me

def main():

    os.remove('data_test.csv') if os.path.exists('data_test.csv') else None

    size = 2000
    output_file = 'data_test.csv'

    s = rq.Session()
    login_url = 'https://dcs1.noaa.gov/ACCOUNT/Login'
    r = s.get(login_url)

    payload = {"__RequestVerificationToken": r.cookies["__RequestVerificationToken"],
               "UserName": "",
               "Password": ""
               }
    
    r = s.post(login_url, data=payload)

    r = s.get('https://dcs1.noaa.gov/Messages/List')

    payload = {"Grid-sort": "TblDcpDataDtMsgCar-desc",
               "Grid-page": 1,
               "Grid-pageSize": 20,
               "Grid-group": "",
               "Grid-filter": "",
               }
    
    r = s.get('https://dcs1.noaa.gov/Messages/List',params=payload)
    r = s.post("https://dcs1.noaa.gov/Messages/ExportSize",data={"size": size})
    r = s.post("https://dcs1.noaa.gov/Messages/LoadView",data={"index": 1, "types": "Messages"})

    payload = {"Grid-sort": "TblDcpDataDtMsgCar-desc",
               "Grid-page": 1,
               "Grid-pageSize": 20,
               "Grid-group": "",
               "Grid-filter": "",
               "__": int(round(time.time() * 1000))}
    
    headers = {"Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Encoding": "gzip, deflate, sdch",
               "Accept-Language": "en-US,en;q=0.8"}
    
    try:
        r = s.get("https://dcs1.noaa.gov/Messages/List", params=payload, headers=headers)
        data = json.loads(json.loads(r.content.decode('utf-8')))
    except ValueError:
        print('Problema encontrado no download dos dados. Enviar email.')
        # email_me()
        return
    
    csv_data = []
    sr_regex = re.compile(r"[\s'\"]")
    num_regex = re.compile(r"\d+")

    with open (output_file, mode='a+', encoding='UTF-8') as file:
        file.seek (0)
        if len(file.read() ) > 0:
            file.seek(0)
            last_line = file.readlines() [-1]
            last_line_parts = last_line.split(",")
            date = ",".join (last_line_parts[0:4])
            last_date = datetime.strptime(date,"%Y-%m-%d %H").replace(tzinfo=timezone.utc) + timedelta(hours=1)
            last_date = last_date.timestamp()
            
        else:
            last_date = 0
            last_line = ''

        for d in data:
            if "DADDS" not in d['TblDcpDataData']:
                ts = int(num_regex.search(d['TblDcpDataDtMsgCar']).group(0))/1000
                if ts > last_date:
                    date_str = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H")
                    csv_data.append("{};{}".format(date_str, sr_regex.sub("", d['TblDcpDataData'])))

        csv_data.reverse()
        
        if csv_data[0] == last_line:
            del csv_data[0]
        
        file.seek(0)
        if len(csv_data) > 0 and len(file.read()) > 0:
            file.write("\n")
        else:
            file.write("")

        teste = pd.DataFrame({'dados': csv_data})
        teste = teste.sort_values(by='dados', ascending=False)
        
        # file.write("\n".join(csv_data))
        file.write("\n".join(teste))

        today = datetime.now().strftime("%Y-%m-%d")
        teste.to_csv('dados_wxt_upto_%s.csv' % today, index=False, header=False, encoding='utf-8')

    r = s.get("https://dcs1.noaa.gov/ACCOUNT/SIGNOUT")

if __name__ == '__main__':
    main()
