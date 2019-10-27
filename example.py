#! /usr/bin/python3
import subprocess
from cursesmenu import *
from cursesmenu.items import *
from miband import miband
from bluepy.btle import BTLEDisconnectError
import argparse
import time
from datetime import datetime
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mac', required=True, help='Set mac address of the device')
args = parser.parse_args()

MAC_ADDR= args.mac

#ADD YOUR AUTH KEY HERE
#mine was 3505642c77773c07e52efc326b58d9a0
AUTH_KEY= b'\x35\x05\x64\x2c\x77\x77\x3c\x07\xe5\x2e\xfc\x32\x6b\x58\xd9\xa0'

#Needs Auth
def get_step_count():
    binfo = band.get_steps()
    print ('Number of steps: ', binfo['steps'])
    print ('Fat Burned: ', binfo['fat_burned'])
    print ('Calories: ', binfo['calories'])
    print ('Distance travelled in meters: ', binfo['meters'])
    input('Press a key to continue')
def general_info():
    print ('MiBand')
    print ('Soft revision:',band.get_revision())
    print ('Hardware revision:',band.get_hrdw_revision())
    print ('Serial:',band.get_serial())
    print ('Battery:', band.get_battery_info()['level'])
    print ('Time:', band.get_current_time()['date'].isoformat())
    input('Press a key to continue')

def send_notif():
    msg = input ("Enter message or phone number to be displayed: ")
    ty= int(input ("1 for Message / 2 for Missed Call / 3 for Call: "))
    if(ty > 3 or ty < 1):
        print ('Invalid choice')
        time.sleep(2)
        return
    a=[5,4,3]
    band.send_custom_alert(a[ty-1],msg)

#Needs Auth
def get_heart_rate():
    print ('Latest heart rate is : %i' % band.get_heart_rate_one_time())
    input('Press a key to continue')

def logger(data):
    print ('Realtime heart BPM:', data)

#Needs Auth
def get_realtime():
    band.start_heart_rate_realtime(heart_measure_callback=logger)
    input('Press Enter to continue')

#Needs Auth.This feature has the potential to brick your Mi Band 4. You are doing this at your own risk.
def restore_firmware():
    path = input("Enter the path of the firmware file :")
    band.dfuUpdate(path)
    
#Needs Auths
def set_time():
    now = datetime.now()
    print ('Set time to:', now)
    band.set_current_time(now)

if __name__ == "__main__":
    while True :
        try:
            if (AUTH_KEY):
                band = miband(MAC_ADDR,AUTH_KEY,debug=True)
                band.initialize()
            else:
                band=miband(MAC_ADDR,debug=True)
            break
        except BTLEDisconnectError:
            print('connection to the MIBand failed. Trying out again')
            continue

    menu = CursesMenu("MIBand4", "Some of the feature requires authentication.")
    info_item = FunctionItem ("Get general info of the device",general_info)
    steps_item = FunctionItem ("Get Steps/Meters/Calories/Fat Burned",get_step_count)
    call_item = FunctionItem ("Send Call/ Missed Call/Message",send_notif)
    single_heart_rate_item = FunctionItem ("Get Heart Rate",get_heart_rate)
    real_time_heart_rate_item = FunctionItem ("Get realtime heart rate data", get_realtime)
    set_time_item= FunctionItem ("Set the band's time to system time", set_time)
    dfu_update_item = FunctionItem ("Restore/Update Firmware", restore_firmware )



    menu.append_item(info_item)
    menu.append_item(steps_item)
    menu.append_item(call_item)
    menu.append_item(single_heart_rate_item)
    menu.append_item(real_time_heart_rate_item)
    menu.append_item(set_time_item)
    menu.append_item(dfu_update_item)
    menu.show()