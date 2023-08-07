import firebase_admin, time
from firebase_admin import credentials
from firebase_admin import db
from datetime import date
import RPi.GPIO as GPIO

databaseURL = 'https://iot-wattsaura-default-rtdb.firebaseio.com/'
department = 'department/'
institute = 'SRIMCA/'

RELAY_1 = 19
RELAY_2 = 13
rooms = {"B105":0, "B106":1}
POWER = [RELAY_1, RELAY_2]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RELAY_1, GPIO.OUT)
GPIO.setup(RELAY_2, GPIO.OUT)
ref = None # db reference

def init() :
    if not firebase_admin._apps:
        cred_obj = credentials.Certificate('/home/pi/Desktop/Team 7/private/iot-wattsaura-firebase-adminsdk-xa9dd-df6762ca44.json')
        default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL':databaseURL})
    
init()

def getData() :
    global ref
    ref = db.reference(department+institute)
    return dict(ref.order_by_key().get())

def run() :
    for block, v in getData().items() :
        for roomNo, v1 in v.items() :
            data = ref.child(block+"/"+roomNo+"/"+str(date.today())).get()
            if data is not None :
                data = list(data.keys())[-1]
                r = ref.child(block+"/"+roomNo+"/"+str(date.today())+"/"+data).get()
                if r['status'] == 1 :
                    #print("Relay 1 - On")
                    GPIO.output(POWER[rooms[block+roomNo]], False)
                else :
                    #print("Relay 1 - Off")
                    GPIO.output(POWER[rooms[block+roomNo]], True)

while True :
    run()
    #time.sleep(2)

