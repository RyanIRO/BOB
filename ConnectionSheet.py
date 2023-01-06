
from time import sleep
import gspread
import datetime
from decouple import config


refsall=[]
lotes=[]


credentials={
  "type": config('type').replace('\\n', '\n'),
  "project_id": config('project_id').replace('\\n', '\n'),
  "private_key_id":config('private_key_id').replace('\\n', '\n'),
  "private_key": config('private_key').replace('\\n', '\n'),
  "client_email":config('client_email').replace('\\n', '\n'),
  "client_id": config('client_id').replace('\\n', '\n'),
  "auth_uri": config('auth_uri').replace('\\n', '\n'),
  "token_uri": config('token_uri').replace('\\n', '\n'),
  "auth_provider_x509_cert_url": config('auth_provider_x509_cert_url').replace('\\n', '\n'),
  "client_x509_cert_url": config('client_x509_cert_url').replace('\\n', '\n')
}

gc = gspread.service_account_from_dict(credentials)
sh = gc.open_by_url(config('url'))

def getdata():
    #data=sh.sheet1.get_all_records()
    datatmpo=sh.worksheet('Oruro').get_all_records()
    keyo,valueo='SEDE','Oruro'
    for datao in datatmpo:
        datao[keyo]=valueo
    datatmpp=sh.worksheet('Potosí').get_all_records()
    keyp,valuep='SEDE','Potosí'
    for datap in datatmpp:
        datap[keyp]=valuep
    datatmpt=sh.worksheet('Iska Iska').get_all_records()
    keyt,valuet='SEDE','Iska Iska'
    for datat in datatmpt:
        datat[keyt]=valuet

    data=datatmpp+datatmpo+datatmpt
    return data
    
    
getdata()

def getcontacts():
    contactstp=sh.worksheet('Clasificación').col_values(1)
    contactsor=sh.worksheet('Clasificación').col_values(2)
    contactspt=sh.worksheet('Clasificación').col_values(3)
    contactspt.pop(0)
    contactsor.pop(0)
    contactstp.pop(0)
    contactspt.pop(0)
    contactsor.pop(0)
    contactstp.pop(0)
    
    return contactstp,contactsor,contactspt
