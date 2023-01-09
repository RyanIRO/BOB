import base64
import datetime
import hashlib
import locale
import os
import pathlib
import re as r
from asyncio.windows_events import NULL
from operator import concat
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from ConnectionSheet import getcontacts, getdata

#----------------------------Locale---------------------------------------------------------------
locale. setlocale(locale.LC_ALL,("es_ES","UTF-8"))
#---------------------------txt-----------------------------------------------------------
log=open("BOBlogs.txt","w")
#----------------------------Settings-------------------------------------------------------------
#----------------------------ConnectionOptions----------------------------------------------------
options=webdriver.ChromeOptions()
user=pathlib.Path().home()
options.add_argument(f"user-data-dir={user}/AppData/Local/Google/Chrome/User Data/")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),chrome_options=options)
wait=WebDriverWait(driver, 100)
#----------------------------Data----------------------------------------------------------------
datadict=getdata()
datamenus={}
menusname=['Oruro','Tupiza','Potosi']
for menu in menusname:
    datamenus[menu]=[]
#----------------------------vars-----------------------------------------------------------------
flagchat=False
menu=''
lotedir=''
saving_folderdownload=''
timetld=0
flagtr=True
lotes=[]
lotesref=[]
CHAT_NAME = ''
CITY=''
DATA_GROUPS = {}
contacts=getcontacts()
tpg=contacts[0]
org=contacts[1]
ptg=contacts[2]
allowedChats=tpg+org+ptg
for chatGroupName in allowedChats:#TO DEFINE THE MATRIX AT START
    DATA_GROUPS[chatGroupName] = {}
print('Group chats allowed: ' + str(allowedChats))
nonwordlist=['Tú:','You:','']
mssg=['Estoy listo para comenzar','Envíe las imagenes por favor, al finalizar ingrese un *#* para completar el envío.']
listIMG = []
listHashIMG=[]
checkedIMGSBytes = []

#---------------------------------OtherConfigs----------------------------------------------------
abs_path = str(pathlib.Path().absolute())#Absolute Path
#---------------------------------Regexs----------------------------------------------------------
refex= r.compile(r"^B+[0-9]+[0-9]+[0-9]+[0-9]")#validate entered ref 
regex1=r.compile(r"^[0-9]") #validate ref selecction
regexlote=r.compile(r"^L+[0-9]") #validate batch selection
regex2=r.compile(r"^[0-9]+[0-9]")
regexhora=r.compile(r"[0-9]+:+[0-9]+[0-9]")#get time(HH:MM )
#-----------------------------------------Functions--------------------------------------------------
#-----------------------------------------city------------------------------------------------------
def citygroup(grupo):#check to witch city a gruop belongs
    global ptg#Potosí
    global org#Oruro
    global tpg#Tupiza

    #grupo= wait.until(EC.presence_of_element_located((By.XPATH,"//*[@class='_21nHd']"))).text
    if grupo in ptg:
        return 'pt'
    if grupo in org:
        return 'or'
    if grupo in tpg:
        return 'tp'
#-----------------------------------------actualizar------------------------------------------------
def update():#update and  organize references into arrays obtained from dictionaries
        global datamenus #dict
        datamenus['Potosi']=[]
        datamenus['Oruro']=[]
        datamenus['Tupiza']=[]
        datadict=getdata()
        for sede in datadict:

                        if sede['SEDE']=='Oruro':
                            datamenus['Oruro'].append(sede)
                        if sede['SEDE']=='Iska Iska':
                            datamenus['Tupiza'].append(sede)
                        if sede['SEDE']=='Potosí':
                            datamenus['Potosi'].append(sede)
                        else: 
                            continue
#-----------------------------------------Menus------------------------------------------------------
#-----------------------------------------MenuRefs--------------------------------
"""def makeMenu(refs):
    menumssg='Los trabajos disponibles son:\n'
    finalmssg='Si la referencia que busca no se encuentra en la lista por favor envíe la palabra "actualizar", si desea cambiar de referencia envíe "cambiar referencia"'
    for refi in refs:
        indice=""+str(refs.index(refi))+':   '+refi+"\n"
        menumssg=concat(menumssg,indice)
    menumssg=concat(menumssg,finalmssg)
    log.write("INFO: "+"menu refs made"+" "+menumssg+" "+str(datetime.datetime.now()))
    return menumssg"""

def makeMenu(datamenus,grupo):#make menu by city 
    menumssg='Los trabajos disponibles son:\n'
    finalmssg='Si desea cambiar de referencia envíe "cambiar referencia"'
    city=citygroup(grupo)
    if city=='pt':
         for pt in datamenus['Potosi']:
               indice=str(datamenus['Potosi'].index(pt))+': '# menu index
               menumssg=menumssg+indice+pt["REFERENCIA (CARPETA)"]+'\n' #menu message
    if city=='or':
         for pt in datamenus['Oruro']:
               indice=str(datamenus['Oruro'].index(pt))+': '
               menumssg=menumssg+indice+pt["REFERENCIA (CARPETA)"]+'\n' 
        
    if city=='tp':
        for pt in datamenus['Tupiza']:
               indice=str(datamenus['Tupiza'].index(pt))+': '
               menumssg=menumssg+indice+pt["REFERENCIA (CARPETA)"]+'\n' 
    menumssg=menumssg+finalmssg
    log.write("INFO: "+"menu refs made"+" "+menumssg+" "+str(datetime.datetime.now()))
    return menumssg
#-----------------------------------------MenuLotes--------------------------------
def makeMenuLote(index): #make batchs menu by ref selected 
    global datamenus
    global lotesref
    global lotedir
    global flaglotes
    lotesref=[]
    grupo=CHAT_NAME
    finalmssg='Si desea cambiar de lote envíe "cambiar lote"'
    city=citygroup(grupo)
    if city=='pt':#by city 
        lotes=datamenus['Potosi'][index]['LOTES/DETALLE (SUB-CARPETA)']
        if lotes != '-' and lotes!='FECHA' and lotes!='R':
            menulotemssg='La referencia *'+datamenus['Tupiza'][index]['REFERENCIA (CARPETA)']+'* tiene:\n'
            for lote in lotes.split(','):#put batches in an array
                lotesref.append(lote)
            for lote in lotesref:#loop batch array 
                indice=str(lotesref.index(lote))#batch menu index 
                menulotemssg=menulotemssg+'L'+ indice +":  "+str(lote)+'\n'
            menulotemssg=menulotemssg+finalmssg#batch menu message
            flaglotes=True
            return menulotemssg
        else:
            flaglotes=False
            lotedir=lotes
    if city=='or':#by city 
        lotes=datamenus['Oruro'][index]['LOTES/DETALLE (SUB-CARPETA)']
        if lotes != '-' and lotes!='FECHA'and lotes!='R':
            menulotemssg='La referencia *'+datamenus['Tupiza'][index]['REFERENCIA (CARPETA)']+'* tiene:\n'
            for lote in lotes.split(','):#put batches in an array
                lotesref.append(lote) 
            for lote in lotesref:#loop batch array
                indice=str(lotesref.index(lote))#batch menu index 
                menulotemssg=menulotemssg+'L'+ indice +":  "+str(lote)+'\n'
            menulotemssg=menulotemssg+finalmssg#batch menu message
            flaglotes=True
            return menulotemssg
        else:
            flaglotes=False
            lotedir=lotes
    if city=='tp':#by city 
        lotes=datamenus['Tupiza'][index]['LOTES/DETALLE (SUB-CARPETA)']
        if lotes != '-' and lotes!='FECHA'and lotes!='R':
            menulotemssg='La referencia *'+datamenus['Tupiza'][index]['REFERENCIA (CARPETA)']+'* tiene:\n'
            for lote in lotes.split(','):#put batches in an array
                lotesref.append(lote)
            for lote in lotesref:#loop batch array 
                indice=str(lotesref.index(lote))#batch menu index 
                menulotemssg=menulotemssg+'L'+ indice +":  "+str(lote)+'\n'
            menulotemssg=menulotemssg+finalmssg#batch menu message
            flaglotes=True
            return menulotemssg
        else:
            flaglotes=False
            lotedir=lotes
    
#-------------------------------------------WPPUse-----------------------------------------------------
#----------------------------------------Validate------------------------------
def validate():#validate upload of WhatsApp chats 
    try:
          validate=driver.find_element(By.XPATH,"//*[@class='_1RAKT']")
          if validate:
            return False
    except:
        log.write("INFO: "+"whatsapp starts" +str(datetime.datetime.now()))
        return True
#-------------------------------------------WhosendMssg?---------------------------------
"""def whosendmssg():
    try:
        #divelementch=driver.find_elements(By.XPATH," //*[@class='ItfyB _3nbHh'] ")
        divelementch=wait.until(EC.presence_of_all_elements_located((By.XPATH," //*[@class='ItfyB _3nbHh'] ")))
        text_element_box_message = driver.find_elements(By.CLASS_NAME,"_22Msk")
        position = len(text_element_box_message)-1
        text=divelementch[position].find_element(By.CSS_SELECTOR,'span').get_attribute("aria-label")
        print(f'Send msg: {text}')
        return text
    except Exception as e:
        print(e)"""
#-------------------------------------------SelectChat-----------------------------------
def selectChat2():#select authorized chat with new messages
    global flagchat
    global CHAT_NAME
    global CITY
    global nonwordlist
    if not flagchat :
        if len(driver.find_elements(By.XPATH,"//*[@class='WM0_u']"))==0:
            print("opened chat")
            contact=wait.until(EC.presence_of_element_located((By.XPATH,"//*[@class='_21nHd']")))
            contactname=contact.find_element(By.CSS_SELECTOR,'span').text
            if contactname in allowedChats:
                #who=whosendmssg()
                #if who not in nonwordlist:    
                    return True
                #if who in nonwordlist:
                    #webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                    #return False
            else:
                webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        
    #chatswithnewmms=wait.until(EC.presence_of_all_elements_located((By.XPATH,"//*[@class='_2nY6U vq6sj _3C4Vf']")))
    chatswithnewmms=driver.find_elements(By.XPATH,"//*[@class='_2nY6U vq6sj _3C4Vf']")
    for chat in chatswithnewmms:#loop in chats with new messages 
            #Pendingchats=chat.find_elements(By.XPATH,"//*[@class='_2nY6U vq6sj _3C4Vf']")
            #index=chatswithnewmms.index(chat)
            try:
                chat.find_element(By.XPATH,"//*[@class='_1pJ9J']")
                Pendingchat=chat.text.split("\n")#get the latest chat with new messages
                #Pendingchat=Pendingchats[index].find_element(By.CSS_SELECTOR,'span').get_attribute('title')
                #Pendingchat=Pendingchats[index].find_element(By.CSS_SELECTOR,'span').text
                # print(f'on chat list: {Pendingchat[0]}')
                if Pendingchat[0] in allowedChats:#check if it is an allowed chat 
                    target = Pendingchat[0]#define target
                    try: 
                            #search_box= wait.until(EC.presence_of_element_located((By.XPATH,"//*[@data-testid='chat-list-search']")))
                            #search_box.send_keys(target.replace('"',''))
                            contact_path= '//span[contains(@title,"'+ target +'")]'
                            sleep(1)
                            contact_path = driver.find_element(By.XPATH,contact_path)
                            driver.implicitly_wait(1)
                            contact_path.click()
                            print("Chat Opened.")
                            CHAT_NAME = target
                            city=citygroup(CHAT_NAME)
                            if city=='pt':
                                CITY='Potosi'
                            if city=='tp':
                                CITY='Tupiza'
                            if city=='or':
                                CITY='Oruro'
                                
                            log.write("INFO:"+"chat selected"+target+str(datetime.datetime.now()))
                            return True
                    except Exception as e:
                            print(e)
                            log.write("ERROR: "+e+ target+" "+str(datetime.datetime.now))
            except Exception as e:
                pass
    return False
#----------------------------------------------GetBytes---------------------------------------------------
def GetData(uri):#get Images Bytes from WhatsApp
    result= driver.execute_async_script("""
       var uri= arguments[0];
       var callback=arguments[1];
       var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
       var xhr = new XMLHttpRequest();
       xhr.responseType = 'arraybuffer';
       xhr.onload = function(){ callback(toBase64(xhr.response)) };
       xhr.onerror = function(){ callback(xhr.status) };
       xhr.open('GET', uri);
       xhr.send(); 

    """,uri)#request (img bytes)
    if type(result)==int:
        log.write("ERROR: "+"bad request"+result+" "+str(datetime.datetime.now()))
        raise Exception("Request failed with status %s"%result)
    log.write("INFO: "+"request succesfuly"+result+" "+str(datetime.datetime.now()))
    return base64.b64decode(result)#return decode info

#----------------------------------------------DownloadIMGS------------------------------------------------
def downloadIMG(path,ref,lote):#write images bytes  in set directory
    print(path)
    print(ref)
    print(lote)
    global menu
    global regexhora
    global timetld
    global datamenus
    lst=os.listdir(path)
    numb_file=len(lst)+1
    header_box='//*[@id="main"]/header'
    header_box=wait.until(EC.presence_of_element_located((By.XPATH,header_box)))
    header_box.click()
    #firstpic_box = '_1TLrW _1Y056'
    firstpic_boxpath='//*[@id="app"]/div/div/div[5]/span/div/span/div/div/section/div[3]/div[2]/div[1]/div[2]'
    firstpic_box = wait.until(EC.presence_of_element_located((By.XPATH, firstpic_boxpath)))
    firstpic_box = firstpic_box.find_elements(By.XPATH, "*")
    sleep(1)
    firstpic_box[0].click()# click on the first image sent
    previouspic='//*[@id="app"]/div/span[3]/div/div/div[2]/div/div[2]/div[3]/div/div'
    previouspic = wait.until(EC.presence_of_element_located((By.XPATH,previouspic)))
    while previouspic.get_attribute('aria-disabled') == 'false': #Check if it´s a first pic
        previouspic.click()
    hourimg=wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/span[3]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div[2]/div"))).text
    hourtocomp=regexhora.findall(hourimg)
    hora=datetime.datetime.strptime(hourtocomp[0],"%H:%M")
    horaofitc=hora.hour+hora.minute#get get shipping time
    while True:#loop in image carousel to get bytes
        
        img_box='//*[@id="app"]/div/span[3]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/div[2]/div/img'
        wait.until(EC.presence_of_element_located((By.XPATH,img_box)))
        img_box=driver.find_element(By.XPATH,img_box)
        src=img_box.get_attribute('src') 
        print("source: "+src) 
        hourimg=wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/span[3]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div[2]/div"))).text
        hourimgt=regexhora.findall(hourimg)
        hour=datetime.datetime.strptime(hourimgt[0],"%H:%M")
        hourimgtd=hour.hour+hour.minute
        if hourimgtd in range(DATA_GROUPS[CHAT_NAME]['TIMELIMIT'], horaofitc+1):#compare time to limit download
            img_bytes=GetData(src)#get bytes
            listIMG.append(img_bytes)
            nextpic_box='/html/body/div[1]/div/span[3]/div/div/div[2]/div/div[2]/div[1]/div/div'
            nextpic_box = wait.until(EC.presence_of_element_located((By.XPATH,nextpic_box)))
            if nextpic_box.get_attribute('aria-disabled') == 'true':#carousel exit
                    close_button = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-testid='x-viewer']")))
                    driver.execute_script("arguments[0].click();", close_button)

                    back_button = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='_18eKe']")))
                    driver.execute_script("arguments[0].click();", back_button)
                    break
            else:
                    driver.execute_script("arguments[0].click();", nextpic_box)
        else: 
            break   
    if bool(listIMG):#check if the list is not empty
        log.write("INFO: "+"images bytes fetched succesfuly"+str(len(listIMG))+" "+str(datetime.datetime.now()))
        for imgB in listIMG:
            hashBytes=hashlib.sha256(imgB).hexdigest()
            if hashBytes not in checkedIMGSBytes:#check if the image was already downloaded
                    try:
                        if imgB==NULL:#check existence of bytes
                            continue
                        if len(ref)<=1:#validate reference name
                            ref="NoRef"
                        if lote=="FECHA":#assign download date
                            lote=datetime.datetime.today().strftime('%d-%B-%Y').upper()
                        file_path=path+'/AHK'+ref+'_'+lote+'_'+str(numb_file)+'.jpg'#define path/name
                        print('file path:' + file_path)
                        open(file_path,'wb').write(imgB)#save img
                        numb_file=numb_file+1
                        checkedIMGSBytes.append(hashBytes)
                        log.write("INFO: "+"bytes write succesfuly"+file_path+" "+str(datetime.datetime.now()))
                    except Exception as e:
                        print(e)
                        log.write("ERROR: "+"can'/t write image bytes "+e+ hashBytes+" "+str(datetime.datetime.now()))
        sendMessage("Descarga exitosa")
        timetld=0
        try:
            update()#update menus
            menu=makeMenu(datamenus)
            log.write("INFO: "+"references updated succesfuly"+menu+" "+str(datetime.datetime.now()))
        except Exception as e:
            log.write("ERROR: "+"can'/t update references"+e+" "+str(datetime.datetime.now()))
            print(e)
        close_button = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-testid='x-viewer']")))
        driver.execute_script("arguments[0].click();", close_button)
        close_button2 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[5]/span/div/span/div/header/div/div[1]/div')))
        driver.execute_script("arguments[0].click();", close_button2)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()#close active chat 
#------------------------------------------Messages----------------------------------
#------------------------------------------IdentifyMessage---------------------------
def identifyMessage():#identify message sent by user
    
    try:
        text_element_box_message = driver.find_elements(By.CLASS_NAME,"_22Msk")
        position = len(text_element_box_message)-1
        element_message=text_element_box_message[position].find_elements(By.CLASS_NAME,'_1Gy50') 
        mssgrec=element_message[0].text.upper().strip()
        print('Identified msg: ' + str(mssgrec))
        return mssgrec   #return user message
        
    except Exception:
            mssgrec=''
            log.write("ERROR: "+"can'/t identify message, allocating blank space to continue operation"+" "+str(datetime.datetime.now()))
            identifyMessage()
#------------------------------------------ResponseMessage---------------------------
def responsemssg(mssgrec,menumssg,regex):#prepare response according to message sent by the user,execute action according to message
    global datamenus
    global menu
    global refdir
    global saving_folderdonwload
    global lotesref
    global lotedir
    global timetld
    global flagchat
    global DATA_GROUPS
    global CHAT_NAME
    global datamenus
    print("Thinking of an answer ")
    messages=['HOLA BOB','HEY BOB','HELLO BOB','HI BOB']
    try:
       
        if mssgrec in messages:
            try:
                update()
                menu=makeMenu(datamenus,CHAT_NAME)
                log.write("INFO: "+"references updated succesfuly"+menu+" "+str(datetime.datetime.now()))
            except Exception as e:
                log.write("ERROR: "+"can'/t update references"+e+" "+str(datetime.datetime.now()))
                print(e)
           
            sendMessage(menu)
        if mssgrec=='CAMBIAR REFERENCIA':#validate keyword
            update()
            menumssg=makeMenu(datamenus,CHAT_NAME)
            sendMessage(menumssg)
            menulote=''
        if mssgrec=='CAMBIAR LOTE':#validate keyword
            update()
            menulote=makeMenuLote(refdir)
            sendMessage(menulote)
        if regex.search(mssgrec):       #VALIDATE MSG WHEN IT'S A REF
            refdir=int(mssgrec)
           
            menulote=makeMenuLote(refdir)
            if CHAT_NAME in ptg:
                DATA_GROUPS[CHAT_NAME]['REF'] = datamenus['Potosi'][refdir]['REFERENCIA (CARPETA)']
            if CHAT_NAME in org:
                DATA_GROUPS[CHAT_NAME]['REF'] = datamenus['Oruro'][refdir]['REFERENCIA (CARPETA)']
            if CHAT_NAME in tpg:
                DATA_GROUPS[CHAT_NAME]['REF'] = datamenus['Tupiza'][refdir]['REFERENCIA (CARPETA)']
            
            DATA_GROUPS[CHAT_NAME]['LOT'] = lotedir
            print(lotedir)
            if  not flaglotes:      #VALIDATE MSG WHEN IT'S IS A REF BUT HAS NO LOTS
                #lotedir= datetime.datetime.today().strftime('%d-%B-%Y').upper()
                saving_folderdonwload=makeDirectory(DATA_GROUPS[CHAT_NAME]['REF'], lotedir)    
                DATA_GROUPS[CHAT_NAME]['FOLDER'] = saving_folderdonwload   
                DATA_GROUPS[CHAT_NAME]['LOT'] = lotedir
                sendMessage(mssg[1])
                hour=datetime.datetime.now()
                h=datetime.datetime.strftime(hour,"%I:%M %p")
                hh=datetime.datetime.strptime(h,"%H:%M %p")
                timetld=hh.hour+hh.minute
                DATA_GROUPS[CHAT_NAME]['TIMELIMIT'] = timetld
            else:
                sendMessage(menulote)
        if regexlote.search(mssgrec):       #VALIDATE MSG WHEN IT'S A LOT
            for lc in str(mssgrec):
                if lc.isdigit():
                    lotedir=lotesref[int(lc)]
                    DATA_GROUPS[CHAT_NAME]['LOT'] = lotedir
                    print(lotedir)
            sendMessage(mssg[1])
            hour=datetime.datetime.now()
            h=datetime.datetime.strftime(hour,"%I:%M %p")
            hh=datetime.datetime.strptime(h,"%H:%M %p")
            timetld=hh.hour+hh.minute
            DATA_GROUPS[CHAT_NAME]['TIMELIMIT'] = timetld
            saving_folderdonwload=makeDirectory(DATA_GROUPS[CHAT_NAME]['REF'], DATA_GROUPS[CHAT_NAME]['LOT'])     
            DATA_GROUPS[CHAT_NAME]['FOLDER'] = saving_folderdonwload   
            lotesref=[]
        if mssgrec=="#":#validate keyword
            flagchat=False
            downloadIMG(DATA_GROUPS[CHAT_NAME]['FOLDER'],DATA_GROUPS[CHAT_NAME]['REF'],DATA_GROUPS[CHAT_NAME]['LOT'])
        """if mssgrec=="ACTUALIZAR":
            update()
            menuact=makeMenu(datamenus, CHAT_NAME)
            sendMessage(menuact)
        else:
             webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        print(DATA_GROUPS)"""
    except Exception as e:
        print(e)
        mssgrec=''
        sleep(1)
        responsemssg(mssgrec,menumssg,regex)
#----------------------------------------SendMessage--------------------------------------
def sendMessage(mssg):#send messages to user
    chatbox_path='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'
    try:
        chatbox=wait.until(EC.presence_of_element_located((By.XPATH,chatbox_path)))
        driver.implicitly_wait(1)
        if mssg.__contains__('\n'):
            for line in mssg.split('\n'):
                chatbox.send_keys(line.replace('"',''))
                chatbox.send_keys(Keys.SHIFT + Keys.ENTER)

            chatbox.send_keys(Keys.ENTER)
        else:
            chatbox.send_keys(mssg.replace('"',''))
            chatbox.send_keys(Keys.ENTER)
        
    except Exception as e:
        print(e)
        log.write("ERROR: "+"can'/t send message"+mssg+str(datetime.datetime.now()))
#----------------------------------------Directories--------------------------------------
#----------------------------------------Make/use Directory-------------------------------
def makeDirectory(ref,lotedir):#create new directory or use an existent directory
    #define path according to work
    if lotedir!='-':
        saving_folder=abs_path+'/'+ref+'/'+lotedir
    if lotedir=='-' or lotedir == 'R':
        saving_folder=abs_path+'/'+ref
    if lotedir=='FECHA':
        date=datetime.datetime.today().strftime('%d-%B-%Y').upper()
        saving_folder=abs_path+'/'+ref+'/'+date    
    if not os.path.exists(saving_folder): 
        try:
            os.makedirs(saving_folder)
            print('Saving Path: ' + saving_folder)
            log.write("INFO: "+"directory created"+saving_folder+str(datetime.datetime.now()))
            return saving_folder
        except Exception as e:
            print(e)
            log.write("ERROR: "+"can'/t create directory "+saving_folder+str(datetime.datetime.now()))
    else:
        print("Saving Path already exists, ignore the creation of it.")
        log.write("INFO: "+"directory already exists"+saving_folder+str(datetime.datetime.now()))
        return saving_folder
#-------------------------------------------main-------------------------------------------
def botwpp():#main function
    log.write("INFO: "+"BOB starts workign"+str(datetime.datetime.now()))
    global menu
    global nonwordlist
    menu=makeMenu(datamenus,CHAT_NAME)
    driver.get("https://web.whatsapp.com/")
    update()
    wait=True
    while wait:
        print("Waiting for WhatsApp to load...")
        wait=validate()
        sleep(2)
        if wait==False:
            print("Ready to Work.")
            break
    while True:
        chat=selectChat2()
        if not chat:
            continue
        elif chat:
            
            mssg=identifyMessage()
            
            responsemssg(mssg,menu,regex1)
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            
while True:#continuous execution of main function
    botwpp()

