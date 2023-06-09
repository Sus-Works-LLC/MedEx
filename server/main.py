from flask import Flask, request
from flask_sock import Sock
import simple_websocket
import json
import time
import random
import mysql.connector as mariadb
import os
import string
import json
import math

#------------- importing configs -------//
if 'V_LOCAL' in os.environ:
    with open("lconfig.json","r") as f:
        config = json.load(f)
else:
    with open("lconfig.json","r") as f:
        config = json.load(f)

#------------- DB connections --------//

mdbp1 = mariadb.connect(user = config['mariaDB']['username'], password = config['mariaDB']['pass'], host=config['mariaDB']['host'], port=config['mariaDB']['port'], database='medex')
mcp1 = mdbp1.cursor()

#------- Creating some global vars ---//

mcp1.execute("SELECT * FROM users")
raw_users = mcp1.fetchall()
users = {user[0]:{'name':user[1],'password':user[2]} for user in raw_users}
print(users)


app = Flask(__name__)
sock = Sock(app)
tokens = []
drivers = {570017:{}}
clients = dict()
cevents = dict()
devents = dict()

def add_client_event(event):
    def predicatate(*args, **kwargs):
        cevents[event.__name__] = event
    return predicatate

def add_driver_event(event):
    def predicatate(*args, **kwargs):
        devents[event.__name__] = event
    return predicatate


@sock.route('/tests/ws')
def tests(sock:simple_websocket.ws.Server):
    print('Connected!')
    while sock.connected:
        print(sock.receive())
        sock.send("Got it")

@sock.route('/driver/ws')
def driver(sock:simple_websocket.ws.Server):
    data = json.loads(sock.receive())
    id = time.time()
    if data['data']['token'] in tokens:
        drivers[570017][id] = {"data":data['data'],"socket":sock,"busy":False}
        while sock.connected:
            sock.send("""{"event":"heartbeat","data":{}}""")
            r = sock.receive(timeout=55)
            if r:
                data = json.loads(r)
                if data['event'] in devents:
                    devents[data['event']](data)
        tokens.remove(drivers[570017][id]['token'])
        drivers[570017].pop(id)
    else:
        sock.close(reason=403,message='Invalid Token')

@sock.route('/client/ws')
def client(sock:simple_websocket.ws.Server):
    data = json.loads(sock.receive())
    id = time.time()
    if data['data']['token'] in tokens:
        clients[id] = data
        while sock.connected:
            sock.send(json.dumnps({"event":"avails","data":drivers[570017]}))
            r = sock.receive(timeout=55)
            if r:
                data = json.loads(r)
                if data['event'] in cevents:
                    cevents[data['event']](data,id)
    else:
        sock.close(reason=403,message='Invalid Token')

@app.route('/')
def home():
    return "HI"

@app.route('/login', methods = ['POST'])
def auth():
    data  = request.json
    if data['phone'] in users:
        if users[data['phone']]['password'] == data['password']:
            token = ''.join(random.choices(string.ascii_uppercase+string.digits, k=128))
            tokens.append(token)
            return {'status':200,'data':{'token':token,'user_data':{users[data['phone']]}}}
        else:
            return {'status':403,'data':{}}
    return {'status':403,'data':{}}


@add_client_event
def confirm(data,id):
    min_driver = (999,1)
    for driver in drivers[data['data']['location']['pincode']]:
        if not driver['busy']:
            d = math.dist(driver['data']['location'],data['data']['location'])
            if min_driver[0] < d:
                min_driver = (d,driver)
    min_driver['socket'].send(json.dumps({"event":"booked","data":data['data']}))
    min_driver['busy'] = True


if __name__ == "__main__":
    app.run(host='0.0.0.0')