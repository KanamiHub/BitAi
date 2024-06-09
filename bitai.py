import requests
from bs4 import BeautifulSoup
import os
import base64
import shutil
import re
import time
import threading
import random
class BitAi:
    def __init__(self, proxy=""):
        self.host = "https://revtecnologia.sld.cu/index.php/tec/"
        self.username = "techdev"
        self.password = "@A1a2a3mo"
        self.repository = "4086"
        self.key = base64.b64encode(self.host.encode("utf-8")).decode("utf-8").replace("==","@").replace("=","#")+"-"+base64.b64encode(self.username.encode("utf-8")).decode("utf-8").replace("==","@").replace("=","#")+"-"+base64.b64encode(self.password.encode("utf-8")).decode("utf-8").replace("==","@").replace("=","#")+"-"+base64.b64encode(str(self.repository).encode("utf-8")).decode("utf-8").replace("==","@").replace("=","#")
        self.bitlevel = 1
        self.proxy = proxy
        self.session = requests.Session()
    def download(self, url, callback, callback_args=""):
        times = time.time()
        response = requests.get(url, stream=True)
        filename = response.headers.get('Content-Disposition').split('"')[1]
        if not filename:
            filename = url.split('/')[-1]
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                downloaded += len(chunk)
                timec = time.time()
                if (timec - times) > 3.0:
                    file.write(chunk)
                    times = time.time()
                    t = threading.Thread(target=callback, args=({"process":"download","progress":round((downloaded/total_size)*100,2),"filename":filename}, callback_args))
                    t.start()
        self.upload(filename, callback, callback_args)
    def upload(self,file, callback, callback_args, proxy=""):
        ver = self.session.get(self.host,proxies={"http":self.proxy,"https":self.proxy})
        logindata = {"username":self.username,"password":self.password}
        login = self.session.post(self.host+"/login/signIn",data=logindata,allow_redirects=True,stream=True,proxies={"http":self.proxy,"https":self.proxy})
        if "Salir" in ver.text or "Log Out" in ver.text:
            self.session_state = '''{"success":True,"message":"Sesión iniciada correctamente"}'''
        else:
            self.session_state = '''{"success":False,"message":"No se pudo iniciar sesión"}'''
        callback({"process":"zipper", "progress":0}, callback_args)
        filename = file.split("/")[-1]
        fileRename = file.replace(".","_")
        os.rename(file, fileRename)
        file = fileRename
        files = []
        tamano_parte_bytes = 10 * 1024 * 1024
        tamano_archivo = os.path.getsize(file)
        current = 0
        numero_partes = (tamano_archivo + tamano_parte_bytes - 1) // tamano_parte_bytes
        if tamano_archivo < tamano_parte_bytes:
            files.append(file)
            callback({"process":"zipper", "progress":100}, callback_args)
        else:
            with open(file, 'rb') as archivo_original:
                numero_parte = 1
                while True:
                    contenido_parte = archivo_original.read(tamano_parte_bytes)
                    if not contenido_parte:
                        break
                    nombre_parte = f"{file}_xatis_{numero_parte}"
                    with open(nombre_parte, 'wb') as archivo_parte:
                        if self.bitlevel == 0:
                            archivo_parte.write(contenido_parte)
                        elif self.bitlevel == 1:
                            png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf6\x178U\x00\x00\x00\x00IEND\xaeB`\x82'
                            archivo_parte.write(png+contenido_parte)
                    files.append(nombre_parte)
                    numero_parte += 1
                    current += 1
            os.unlink(file)
            callback({"process":"zipper", "progress":(current/numero_partes)*100}, callback_args)
        callback({"process":"zipper", "progress":100,"result":files}, callback_args)
        ideslist = []
        callback({"process":"upload", "progress":0}, callback_args)
        current = 0
        for f in files:
            data = {"articleId":self.repository,"formLocale":"es_Es","title[es_ES]":random.randint(100000,999999),"creator[es_ES]":"TechDev","subject[es_ES]":"","type":"Herramienta de investigación","typeOther[es_ES]":"","description[es_ES]":"Subido por TechDev","publisher[es_ES]":"","sponsor[es_ES]":"TechDev","dateCreated":"","source[es_ES]":"","language":"es"}
            filek = {"uploadSuppFile": open(f,"rb")}
            upFile = self.session.post(self.host+"/author/saveSuppFile?path=",data=data,files=filek,allow_redirects=True,stream=True,proxies=dict(http=self.proxy,https=self.proxy))
            current += 1
            callback({"process":"upload", "progress":(current/len(files))*100}, callback_args)
            getLink = self.session.get(self.host+"/author/submission/"+self.repository,proxies=dict(http=self.proxy,https=self.proxy))
            soup = BeautifulSoup(getLink.text, "html.parser")
            entradas = soup.find_all('a',{'class':'file'})
            regex1 = str(entradas).split(",")
            regex2 = regex1[-1]
            regex3 = regex2.replace("]","")
            regex4 = regex3.split("-")[1]
            getid = self.session.get(self.host+"/author/submit/4?articleId="+self.repository)
            soup = BeautifulSoup(getid.text, 'html.parser')
            ultimo_tr = soup.find_all('tr', {'valign': 'top'})[-1]
            primer_td = ultimo_tr.find('td')
            try:
                os.unlink(f)
            except:
                None
            textid = primer_td.text
            ides = textid+"-"+regex4
            ideslist.append(ides)
        callback({"process":"upload", "progress":100,"result":ideslist, "filename":filename,"filesize":tamano_archivo, "code":str(self.bitlevel)+"/"+'_'.join(ideslist)+"/"+str(base64.b64encode(filename.encode('utf-8')).decode('utf-8'))+"/"+str(tamano_archivo)+"/"+self.key}, callback_args)