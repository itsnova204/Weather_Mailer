###############
#By Nova_Delta#
###############

#1.1 patch - fixed data de amanha

import requests
import os
from datetime import datetime, timedelta
import smtplib, ssl


sender = "user@gmail.com"
receiver = "user@gmail.com"
user = input("Introduzir nome: ")

#fonte: https://api.ipma.pt/#services
codigo_id = "1131200"

main_api_link = "https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/" + codigo_id + ".json"
weaClass_api_link = "https://api.ipma.pt/open-data/weather-type-classe.json"
precClass_api_link = "https://api.ipma.pt/open-data/precipitation-classe.json"
winSpeed_api_link = "https://api.ipma.pt/open-data/wind-speed-daily-classe.json"

main_api_link = requests.get(main_api_link)
main_api_data = main_api_link.json()
weaClass_api_link = requests.get(weaClass_api_link)
weaClass_api_data = weaClass_api_link.json()
precClass_api_link = requests.get(precClass_api_link)
precClass_api_data = precClass_api_link.json()
winSpeed_api_link = requests.get(winSpeed_api_link)
winSpeed_api_data = winSpeed_api_link.json()


precipitaProb = main_api_data['data'][1]['precipitaProb']
tMax = main_api_data['data'][1]['tMax']
tMin = main_api_data['data'][1]['tMin']
predWindDir = main_api_data['data'][1]['predWindDir']
idWeatherType = main_api_data['data'][1]['idWeatherType']
classWindSpeed = main_api_data['data'][1]['classWindSpeed']
forecastDate = main_api_data['data'][1]['forecastDate']
longitude = main_api_data['data'][1]['longitude']
latitude = main_api_data['data'][1]['latitude']

descIdWeatherTypePT = weaClass_api_data['data'][idWeatherType + 1]['descIdWeatherTypePT']
descClassPrecIntPT = precClass_api_data['data'][classWindSpeed + 1]['descClassPrecIntPT']

switcher = {
'N': "Norte",
'S': "Sul",
'E': "Este",
'O': "Oeste"
}

mensage = list("""Boa noite.

Aqui vao as informacoes meteorologicas para amanha:
- Durante o dia, no Porto estara """ + descIdWeatherTypePT + """, sendo que a temperatura maxima prevista sera de """ + tMax + """_C e o vento estara """ + descClassPrecIntPT + """, soprara na direcao """ + switcher.get(predWindDir, "ERRO! Falta de cardial") + """, a probabilidade de precipitacao sera de """ + precipitaProb + """ %.

- Durante a noite, a temperatura minima sera de """ + tMin + """C.

Saudacoes,

""" + user)

for i in range(len(mensage)):
    if mensage[i] == 'í':
        mensage[i] = 'i'
    elif mensage[i] == 'é':
        mensage[i] = 'e'

mensagem = "".join(mensage)
print(mensagem)

#---------------------------------------------Email sending stuffs---------------------------------------------------------------------
import smtplib, ssl

tomorrow = str(datetime.today() + timedelta(days=1))
tomorrow = tomorrow[:10]

subject = "Meteorologia de " + tomorrow
password = input("Pass da gmail para confirmação (crtl + c para abortar): ")

def enviaremail(usuario,senha,destinatario,subject,mesg):
    from smtplib import SMTP
    from email.mime.text import MIMEText

    msg=MIMEText(mensagem)
    msg['From']=usuario
    msg['To']=destinatario
    msg['Subject']=subject

    smtp=SMTP('smtp.gmail.com',587)
    smtp.starttls()
    smtp.login(usuario,senha)
    smtp.sendmail(usuario,destinatario,msg.as_string())
    smtp.quit()
    print('E-mail sent')

enviaremail(sender,password,sender,subject,mensagem)
