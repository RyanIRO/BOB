
from time import sleep
import logging
import gspread
import datetime
refsall=[]
lotes=[]
credentials = {
  "type": "service_account",
  "project_id": "administracionoperaciones",
  "private_key_id": "6a19af9548c6fb75a627504f1825eb52330530e2",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCzGbAWOQNj3aEB\ntLd0sjijT2YnPf9LvKSk6q1qtqTfd295EWFzpdSZPIfQR86zeHwrdSAVhp5bxpNZ\nLzOhfLIqkPv16fUTzpYLC/vZwHFLBOHt6SNFNBY0dgv8Wk1KU5HmYmMHHi1fKQOB\n8CKl1MYh+PYOpMFAIFR39h5kf3AlZ1c9u6eb+IW+QkR27IOYGAPuiHD8pPcp4y7V\nYRt4AJ3DqLdwUeTwml/9HkqB2vs7LW7o1Nf4PayFryGJknh4IzwTCw/LPXCTxFuI\nAeliAL74vlfLaGY2y+F2otWG0ZBX6J2XyTsgrIkgzeabenFh+JYp2xQrrLTHoHL8\nBcveKqTbAgMBAAECggEAEmmOJkK3PAGRZ1z+TUNzOirT/C3N/KnInWG48VMUkRq0\nvZQRWjPOrvA/oCR5tg6paUhRw5TC2/mGtXD6VFw+7sxX8tiaBu7CkyEow6KaoxU9\n6tkAdMFdlQgbxFY+QuljgvVTa+xoyrMrNqUK0tSUh/KRzUCX03FfbbPCPR+y1k1k\nrj/Ld+OEcUx2o8JgeQhIbIZPLunjQn/c7tGDznxCWnTqsMgA5+jWhn7/7Q2XD/UR\n1QZViDS39BCEjB848CRLf1mMW0A30JZJ3uObA6NRvGzhm3Wlej3MVn9EDHJGSLum\nS/R7UuCQfRJh5NEdpnTUKo1w6dNxJwFfgEu5dxNIfQKBgQDuM3XHiDHWKyHSKG4P\nEy6h9GjpF8cTKaWVpFhQt4G3xBvzktPXBX74wWwAaQ9pfB570Oa1eHzhTNz5dKqO\naS8ssljf2YaDvUK9NvDEep1RHvUkDwAPWqIqV9+ZhFUIsPtW2z7apL1kz9oGaPhX\nXW7NuHiaBhYsHvLm7/nRUsgpdwKBgQDAe7FbyUQUexkAZ36xfNjC0WHdTRtcrnLt\nw67Zm8UQkJwD1+snUnxVkjtm6j/GzmxB6ccD8tC6K3w+IhlwrzZ9xTuEXE9wlBW6\nxOZJu2Uf7hcrU2oIU3EbeeSOMAgel49UUPGGtrf58feBdwi+I9Q2iqrJDhLlgTyf\nMNZul744vQKBgBNvKWXdK8vAeyLtX4VlWEGockLKSNi8ZiEeZoI3ZqL6ohkuWpBJ\nh4F+LnSeHb7KfKY3dgtKSE4Nel3z8dJqrImmB3BEDCCFeYN8jwpIwrsSnoeRnbyi\n9WYlAz5AOLvbzLXab3dhR36JIs2xFMnz+o1YRqayZm61G7ZRz/0PFvujAoGAetc1\n9G75LNz2ssRaHamgqIx6GYLZIIgQvt7wmt4HoS+48db9syW4ReBCWsbKlvUsL9Cj\ne0ienwGblAetFrYrX47dEfbbl+xaBc0dbxbSTdNkI/ljJRcjizZ6f6f1tphhF51k\n1uWLek9K9uvhv38cMwbCQffiZWfaKXpAj2n2Mz0CgYAd8hcuOGzZYm6t9kATaAAZ\ndO0cLlqvxCvS3qEZf1H/vvdKMW+q4ZDbRgL5SttOm806W/iYY1sjU5cxhlmExe/h\nbie/ZG6fCUdEYf/gvodtnIWlBUgoobW/VxpUs9XT0JXZIuS4pKATJ7U+YeU5evN7\ngUG5s3B11J/qxFix/2FxUw==\n-----END PRIVATE KEY-----\n",
  "client_email": "whatsappbot@administracionoperaciones.iam.gserviceaccount.com",
  "client_id": "106876150400762948680",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/whatsappbot%40administracionoperaciones.iam.gserviceaccount.com"
}
gc = gspread.service_account_from_dict(credentials)
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/19RGpz5pBD-ZaTzQapQgQIW9LNAyFJ1AIPpVmxBD2BFM")
"""def getdata(flag):
    global  refsall
    global lotes
    if flag==False:
        refsall=sh.sheet1.col_values(1)
        refsall.pop(0)
        return refsall
    else:
        lotes=sh.sheet1.col_values(2)
        lotes.pop(0)
        return lotes"""
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
