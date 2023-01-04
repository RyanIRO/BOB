from asyncio.windows_events import NULL
from operator import concat
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pathlib,os 
import base64
import re as r
import hashlib
import datetime
from ConnectionSheet import getdata
import locale
#------------------------------locale------------------------------------------------------------
locale.setlocale(locale.LC_ALL,("es_ES","UTF-8"))
#-----------------------------txt----------------------------------------------------------------
ctcs=open("contacts.txt","r")

#----------------------------Settings-------------------------------------------------------------
#----------------------------ConnectionOptions----------------------------------------------------
options=webdriver.ChromeOptions()
user=pathlib.Path().home()
options.add_argument(f"user-data-dir={user}/AppData/Local/Google/Chrome/User Data/")
driver=webdriver.Chrome('chromedriver.exe',chrome_options=options)
wait=WebDriverWait(driver, 100)
#----------------------------vars-----------------------------------------------------------------
flaglotes=True
flagchat=True
menu=''
lotedir=''
saving_folderdownload=''
timetld=0
flagtr=True
refsall=[]
lotes=[]
lotesref=[]
mssg=['Estoy listo para comenzar','Envíe las imagenes Por favor, al finalizar ingrese un "#" indicando que desea iniciar la descarga']
listIMG = []
listHashIMG=[]
checkedIMGSBytes = []
#---------------------------------LogsConfig-----------------------------------------------------
#---------------------------------OtherConfigs----------------------------------------------------
abs_path = str(pathlib.Path().absolute())
#---------------------------------Regexs----------------------------------------------------------
refex= r.compile(r"^B+[0-9]+[0-9]+[0-9]+[0-9]")
regex1=r.compile(r"^[0-9]")
regexlote=r.compile(r"^L+[0-9]")
regex2=r.compile(r"^[0-9]+[0-9]")
regexhora=r.compile(r"[0-9]+:+[0-9]+[0-9]")
#-----------------------------------------Functions--------------------------------------------------
#-----------------------------------------Menus------------------------------------------------------
#-----------------------------------------MenuRefs--------------------------------
def makeMenu(refs):
    menumssg='Los trabajos disponibles hoy son:\n'
    finalmssg='\nSi la referencia que busca no se encuentra en la lista por favor envíe la palabra "actualizar", si desea cambiar de referencia envíe "cambiar referencia"'
    for refi in refs:
        indice=""+str(refs.index(refi))+':   '+refi+"\n"
        menumssg=concat(menumssg,indice)
    menumssg=concat(menumssg,finalmssg)
    return menumssg
#-----------------------------------------MenuLotes--------------------------------
def makeMenuLote(lotes,mssgrec):
    global refsall
    global flaglotes
    global lotesref
    global lotedir
    lotesref=[]
    finalmssg='\nSi desea cambiar de lote envíe "cambiar lote"'
    #if lotes[mssgrec] != '-' or lote[mssgrec]!='FECHA':
    lotes=lotes[mssgrec]
    if lotes!='-' and lotes!='FECHA':
        menulotemssg='La referencia   '+refsall[mssgrec]+'   tiene:\n'
        for lote in lotes.split(','):
            lotesref.append(lote)
        for lote in lotesref:
            indice=str(lotesref.index(lote))
            menulotemssg=menulotemssg+'L'+ indice +":  "+str(lote)+'\n'
        menulotemssg=menulotemssg+finalmssg
        flaglotes=True
        return menulotemssg
    else:
        flaglotes=False
        lotedir=lotes
#-------------------------------------------WPPUse-----------------------------------------------------
#----------------------------------------Validate------------------------------
def validate():
    try:
          validate=driver.find_element(By.XPATH,"//*[@class='_1RAKT']")
          if validate:
            return False
    except:
        return True
#-------------------------------------------SelectChat-----------------------------------                 
def selectChat(target):     
    try: 
        search_box= wait.until(EC.presence_of_element_located((By.XPATH,"//*[@data-testid='chat-list-search']")))
        search_box.send_keys(target)
        contact_path= f'//span[contains(@title,"{target}")]'
        sleep(1)
        contact_path = driver.find_element(By.XPATH,contact_path)
        driver.implicitly_wait(1)
        contact_path.click()
        print("chat abierto")
        sendMessage(mssg[0])
        return True
    except:
        
        return False                       
                

#----------------------------------------------GetBytes---------------------------------------------------
def GetData(uri):
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

    """,uri)
    if type(result)==int:
        raise Exception("Request failed with status %s"%result)
    return base64.b64decode(result)

#----------------------------------------------DownloadIMGS------------------------------------------------
def downloadIMG(path,ref,lote):
    global menu
    global refsall
    global regexhora
    global timetld
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
    firstpic_box[0].click()
    previouspic='//*[@id="app"]/div/span[3]/div/div/div[2]/div/div[2]/div[3]/div/div'
    previouspic = wait.until(EC.presence_of_element_located((By.XPATH,previouspic)))
    while previouspic.get_attribute('aria-disabled') == 'false':
        previouspic.click()
    hourimg=wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/span[3]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div[2]/div"))).text
    hourtocomp=regexhora.findall(hourimg)
    hora=datetime.datetime.strptime(hourtocomp[0],"%H:%M")
    horaofitc=hora.hour+hora.minute
    while True:
        img_box='//*[@id="app"]/div/span[3]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/div[2]/img'
        wait.until(EC.presence_of_element_located((By.XPATH,img_box)))
        img_box=driver.find_element(By.XPATH,img_box)
        src=img_box.get_attribute('src') 
        print("source: "+src) 
        hourimg=wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/span[3]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div[2]/div"))).text
        hourimgt=regexhora.findall(hourimg)
        hour=datetime.datetime.strptime(hourimgt[0],"%H:%M")
        hourimgtd=hour.hour+hour.minute
        if hourimgtd in range(timetld,horaofitc+1):
            img_bytes=GetData(src)
            listIMG.append(img_bytes)
            nextpic_box='/html/body/div[1]/div/span[3]/div/div/div[2]/div/div[2]/div[1]/div/div'
            nextpic_box = wait.until(EC.presence_of_element_located((By.XPATH,nextpic_box)))
            if nextpic_box.get_attribute('aria-disabled') == 'true':
                    close_button = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-testid='x-viewer']")))
                    driver.execute_script("arguments[0].click();", close_button)

                    back_button = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='_18eKe']")))
                    driver.execute_script("arguments[0].click();", back_button)
                    break
            else:
                    driver.execute_script("arguments[0].click();", nextpic_box)
        else: 
            break
    if bool(listIMG):
        for imgB in listIMG:
            hashBytes=hashlib.sha256(imgB).hexdigest()
            if hashBytes not in checkedIMGSBytes:
                    try:
                        if imgB==NULL:
                            continue
                        if len(ref)<=1:
                            ref="NoRef"
                        if lote=="FECHA":
                            lote=datetime.datetime.today().strftime('%d-%B-%Y').upper()
                        
                        file_path=path+'/AHK'+ref+'_'+lote+'_'+str(numb_file)+'.jpg'
                        print(file_path)
                        open(file_path,'wb').write(imgB)
                        numb_file=numb_file+1
                        checkedIMGSBytes.append(hashBytes)
                        
                    except Exception as e:
                        print(e)
        sendMessage("Descarga exitosa")
        timetld=0
        try:
            refsall=getdata(False)
            menu=makeMenu(refsall)
            print(refsall)
            
        except Exception as e:
            print(e)
        close_button = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-testid='x-viewer']")))
        driver.execute_script("arguments[0].click();", close_button)
        #ex=driver.find_element(By.XPATH,"/html/body/div[1]/div/span[3]/div/div/div[2]/div/div[1]/div[2]/div/div[6]/div/span")
        #ex.click()
        sleep(1)
        close_button2 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[5]/span/div/span/div/header/div/div[1]/div')))
        driver.execute_script("arguments[0].click();", close_button2)
#------------------------------------------Messages----------------------------------
#-------------------------------------------WhosendMssg?---------------------------------
def whosendmssg():
    try:
        #divelementch=driver.find_elements(By.XPATH," //*[@class='ItfyB _3nbHh'] ")
        divelementch=wait.until(EC.presence_of_all_elements_located((By.XPATH," //*[@class='ItfyB _3nbHh'] ")))
        text_element_box_message = driver.find_elements(By.CLASS_NAME,"_22Msk")
        position = len(text_element_box_message)-1
        text=divelementch[position].find_element(By.CSS_SELECTOR,'span').get_attribute("aria-label")
        print(text)
    except Exception as e:
        print(e)
#------------------------------------------IdentifyMessage---------------------------
def identifyMessage():
        global flagtr
        nonwordlist=["Tú:","You:", "None"]
        flagtr=True
        try:
            #divelementch=driver.find_elements(By.XPATH," //*[@class='ItfyB _3nbHh'] ")
            divelementch=wait.until(EC.presence_of_all_elements_located((By.XPATH," //*[@class='ItfyB _3nbHh'] ")))
            text_element_box_message = driver.find_elements(By.CLASS_NAME,"_22Msk")
            position = len(text_element_box_message)-1
            #color = divcolor[position].value_of_css_property("background-color")

            text=divelementch[position].find_element(By.CSS_SELECTOR,'span').get_attribute("aria-label")

            print(text)
            #if color == 'rgba(32, 44, 51, 1)' or color == 'rgba(255, 255, 255, 1)':
            #if text in nonwordlist:
            #    flagtr=False    
            #else:
             #   flagtr=True
            element_message=text_element_box_message[position].find_elements(By.CLASS_NAME,'_1Gy50') 
            mssgrec=element_message[0].text.upper().strip()
            print("received")
            print(str(mssgrec))
                
            return mssgrec   

        except Exception:
            sleep(2)
            mssgrec=''
            identifyMessage()

#------------------------------------------ResponseMessage---------------------------
def responsemssg(mssgrec,menumssg,regex):
    global refsall
    global menu
    global refdir
    global saving_folderdonwload
    global lotesref
    global lotedir
    global timetld
    global flaglotes
    print("thinking an answer ")
    messages=['HOLA BOB','HEY BOB','HELLO BOB','HI BOB']
    try:
        if mssgrec in messages:
            try:
                refsall=getdata(False)
                menu=makeMenu(refsall)
                print(refsall)
                
            except Exception as e:
                print(e)
        
            sendMessage(menumssg)
        elif mssgrec=='CAMBIAR REFERENCIA':
            sendMessage(menumssg)
            menulote=''
        elif mssgrec=='CAMBIAR LOTE':
            lotes=getdata(True)
            menulote=makeMenuLote(lotes,refdir)
            sendMessage(menulote)
        elif regex.search(mssgrec):
            refdir=int(mssgrec)
            
            lotes=getdata(True)
            menulote=makeMenuLote(lotes,refdir)
            if  not flaglotes:
                #lotedir= datetime.datetime.today().strftime('%d-%B-%Y').upper()
                saving_folderdonwload=makeDirectory(refsall[refdir],lotedir)
                sendMessage(mssg[1])
                hour=datetime.datetime.now()
                h=datetime.datetime.strftime(hour,"%I:%M %p")
                hh=datetime.datetime.strptime(h,"%H:%M %p")
                timetld=hh.hour+hh.minute
            else:
                sendMessage(menulote)
        elif regexlote.search(mssgrec):
            for lc in str(mssgrec):
                if lc.isdigit():
                    lotedir=lotesref[int(lc)] 
            sendMessage(mssg[1])
            hour=datetime.datetime.now()
            h=datetime.datetime.strftime(hour,"%I:%M %p")
            hh=datetime.datetime.strptime(h,"%H:%M %p")
            timetld=hh.hour+hh.minute
            saving_folderdonwload=makeDirectory(refsall[refdir],lotedir)        
            lotesref=[]

        elif mssgrec=="#":
            downloadIMG(saving_folderdonwload,refsall[refdir],lotedir)
        elif mssgrec=="ACTUALIZAR":
            refsall=getdata(False)
            menu=makeMenu(refsall)
            sendMessage(menu)
            
    except Exception as e:
        print(e)
        sleep(2)
        mssgrec=''
        responsemssg(mssgrec,menumssg,regex)
#----------------------------------------Directories--------------------------------------
#----------------------------------------Make/use Directory-------------------------------
def makeDirectory(ref,lotedir):
    if lotedir!='-':
        saving_folder=abs_path+'/'+ref+'/'+lotedir
    if lotedir=='-':
        saving_folder=abs_path+'/'+ref
    if lotedir=='FECHA':
        date=datetime.datetime.today().strftime('%d-%B-%Y').upper()
        saving_folder=abs_path+'/'+ref+'/'+date    
    if not os.path.exists(saving_folder): 
        try:
            os.makedirs(saving_folder)
            print(saving_folder)
            return saving_folder
        except Exception as e:
            print(e)
    else:
        print("alredy exists")
        return saving_folder
"""def makeDirectoryLote(lote,saving_folder,refdir):
    saving_folderlote=saving_folder+"/"+lote
    if not os.path.exists(saving_folderlote):
        try:
            os.makedirs(saving_folderlote)
            print(saving_folderlote)
            sleep(30)
            return downloadIMG(saving_folderlote,refdir,lote)
        except Exception as e:
            print(e)
    else:
        print("alredy exists")
        return downloadIMG(saving_folderlote,refdir,lote)"""
#----------------------------------------SendMessage--------------------------------------
def sendMessage(mssg):
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
#-------------------------------------------main-------------------------------------------
def botwpp():

    global refsall
    global menu
    refsall=getdata(False)
    menu=makeMenu(refsall)
    driver.get("https://web.whatsapp.com/")

    wait=True

    while wait:
        print("Waiting")
        wait=validate()
        sleep(2)
        if wait==False:
            print("ready")
            break
    selectChat(ctcs.readlines()[0])
    while True:
        #if not selectChat('"Prueba2"'):
        #   sleep(10) 
        #  continue
        mssg=identifyMessage()
        #if flagtr:
        responsemssg(mssg,menu,regex1)
        #else:
         # continue
        #mssg=identifyMessage()
  
while True:
    botwpp()