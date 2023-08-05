#! /usr/local/bin/python3.6
# -*- coding: utf-8 -*-
####################################################################################################

import argparse
import datetime
import os
import sys
import time

##################################################

sys.path.append(os.path.join(sys.path[0], 'etc'))    

import paho.mqtt.client as mqtt

try:
    import DeviceList
except:
    import DemoDeviceList as DeviceList

####################################################################################################

def getResponse(p_Client, p_UserData, p_Message):
    C_TimeStampLength = 4

#    print(f'''\nResponse: {p_Message.topic} -> {p_Message.payload} ''')

    l_Status  = p_Message.payload[0] == ord('T')
    l_Payload = p_Message.payload[1:]
    
    try:        
        l_Topic = p_Message.topic    
        
        l_TopicParts = l_Topic.split('/')
        
        l_Target = l_TopicParts[2]
        l_Id     = l_TopicParts[3]
        l_Tag    = l_TopicParts[4]
        
        l_Payload = l_Payload.decode()
        
        if g_Arguments.datestamp:
            l_Datestamp = f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S}  '
        else:
            l_Datestamp = ''
        
        print(f'''{l_Datestamp}{l_Target:10s} : {l_Tag:15s}({l_Id:5s}) -> {l_Payload}''')
        
    except Exception as l_Exception:
        print (l_Exception)
        
####################################################################################################
if __name__ == '__main__':
    l_ArgumentParser = argparse.ArgumentParser(description='Communicate with an ESP6288 board via MQTT')
    
    l_ArgumentParser.add_argument('-v', '--verbose',    required=False,  action='store_true',          help='Verbose user info')
    l_ArgumentParser.add_argument('-d', '--datestamp',  required=False,  action='store_true',          help='Prepend datestamp')
    
    l_ArgumentParser.add_argument('-b', '--broker',     required=True,   action='store',               help='Broker to access ESP.')
    l_ArgumentParser.add_argument('-f', '--filter',     required=False,  action='store', default=None, help='Only show these targets')
    
    g_Arguments  = l_ArgumentParser.parse_args()    
        
    l_Broker = g_Arguments.broker
    l_UserName = DeviceList.C_MQTTCredentials[l_Broker][0]
    l_Password = DeviceList.C_MQTTCredentials[l_Broker][1]
    l_Target   = '+' if g_Arguments.filter == None else g_Arguments.filter
    
    l_Client     = mqtt.Client()
        
    if l_UserName is not None:
        l_Client.username_pw_set(l_UserName, l_Password)
        
    l_Client.connect(l_Broker, 1883,60)
    
    l_Client.on_message = getResponse
    l_Client.subscribe(f'sensors/esp/{l_Target}/#',  qos=0)
    l_Client.loop_start()

    while True:
        time.sleep(0.01)
