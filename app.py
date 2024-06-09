import random
import string
import threading
import time
import requests
from bitai import BitAi
from flask import Flask, request
app = Flask(__name__)
autocron = False
bitai = BitAi()
def cronjob(host):
    while True:
        time.sleep(30)
        requests.get("https://"+host)
def gentoken():
    caracteres = string.ascii_letters+string.digits
    return ''.join(random.choices(caracteres, k=30))
procesos = []
users = [{"username":"techdev", "password":"@A1a2a3mo", "token":"@A1a2a3mo"}]
print("Token del administrador: "+users[0]["token"])
def callback(json, args):
    global users
    print(json)
    for p in procesos:
        if p["ide"] == args["ide"]:
            p["data"] = str(json)
@app.route("/")
def home():
    global autocron
    if not autocron:
        t = threading.Thread(target=cronjob, args=(request.host,))
        t.start()
        autocron = True
    return ''':)'''
@app.route("/api/process")
def process():
    url = request.args.get("url")
    token = request.args.get("token")
    invalid_token = True
    for u in users:
        if u["token"] == token:
            invalid_token = False
            user = u
    if invalid_token:
        return '''Token invalido'''
    ide = str(random.randint(10000,99999))
    t = threading.Thread(target=bitai.download, args=(url, callback, {"ide":ide}))
    t.start()
    procesos.append({"ide":ide, "data":{"process":"loading"}})
    return ide
@app.route("/api/getide")
def getide():
    ide = request.args.get("ide")
    token = request.args.get("token")
    invalid_token = True
    for u in users:
        if u["token"] == token:
            invalid_token = False
            user = u
    if invalid_token:
        return '''Token invalido'''
    for i in procesos:
        if i["ide"] == ide:
            return i["data"]
    return "Proceso no encontrado"
if __name__ == "__main__":
    app.run()