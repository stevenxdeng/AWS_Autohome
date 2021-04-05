#Copyright (c) 2021 Hsien-Wen "Steven" Deng
#This is a client program for AWS-based "Autohome" Project
#--------------------------------------------------------------------------------------------------
#In Autohome, there are two types of devices: light and thermostats
#This client program can:
#   1. Add a light
#   2. Remove a light
#   3. Switch a light
#   4. Set temperature for a thermostat
#   5. See devices status
#   6. See Events
#
#For interacting with devices, this client use Kinesis Data Stream (KDS) to
#deliver a command to AWS, while a Lambda function deployed in AWS will react
#based on KDS data, here is the KDS data format: "Component_ID,Status,Temperature,Action"
#   Component_ID: A string describe device ID. Light starts with 'L' and thermostat with 'T'.
#       e.g. L1, T4
#   Status: A specific string descibe current status of a light. Light used only.
#       e.g. 0, 1 (these two are only legal digits for Status)
#   Temperature: A number describe current temperature setting for a thermostat. Thermostat usd only.
#       e.g. 85, 74 (temperature is in range 30~120)
#   Action: A specific string describe action of this event.
#       ADD: Add a light
#       REMV: Remove a light
#       ON: Turn on a light
#       OFF: Turn off a light
#       SET: Set a temperature for a thermostat
#
#For searching databases, this client program directly scan the target database and print results
#--------------------------------------------------------------------------------------------------
#Instruction:
#   Run the program using: 'python Autohome_Client.py'(Linux/OS X)
#                          'py Autohome_Client.py'(Windows)
#   Selection:
#       1) Add or Remove a Light
#           1) Add a Light (Input with your new light name starts with 'L')
#           2) Remove a Light (Input with your target light name)
#       2) Switch a light (Input with your target light name)
#       3) Set Temperature (Input with your target thermostat then temperature)
#       4) See Device Database
#       5) See Event Database
#       x) Exit
#--------------------------------------------------------------------------------------------------


import time
import boto3
import botocore
import datetime
from datetime import timezone
from decimal import *

kinesis_client = boto3.client('kinesis',region_name='us-east-1')
dynamodb = boto3.resource("dynamodb", config=botocore.client.Config(max_pool_connections=100))
Autohome_collection_Table = dynamodb.Table('Autohome_collection') #Device Database
Autohome_logs_Table = dynamodb.Table('Autohome_logs') #Event Database

IDs = []
L_status = {}
flag = True

#Scan Device Database
def Table_scan():
    IDs = []
    status = {}
    L_message = []
    T_message = []
    items = Autohome_collection_Table.scan()['Items']
    for item in items:
        IDs.append(item['Component_ID'])
        if item['Component_ID'][0] == 'L':
            L_message.append('Light ID: '+ item['Component_ID'] + ' Status: ' + str(item['Status']))
            status[item['Component_ID']]=item['Status']
        elif item['Component_ID'][0] == 'T':
            T_message.append('Thermostat ID: '+ item['Component_ID'] + ' Temperature: ' + str(item['Temperature']) + 'F')
    #Print devices by categories
    print('             Device Database\n----------------------------------------')
    for L_info in L_message:
        print(L_info)
    for T_info in T_message:
        print(T_info)
    print('----------------------------------------')
    return (IDs,status)

#Scan Event Database
def Log_scan():
    time_stamp = []
    component_ID = {}
    action = {}
    items = Autohome_logs_Table.scan()['Items']
    #Categorize event logs
    for item in items:
        time_stamp.append(item['Time_Stamp'])
        component_ID[item['Time_Stamp']] = item['Component_ID']
        action[item['Time_Stamp']] = item['Action']
    #Sort event logs by time then print
    time_stamp.sort()
    print('               Event Database\nDate       Time           Device   Action\n---------------------------------------------')
    for event in time_stamp:
        print(event, '   ', component_ID[event], '     ', action[event])
    print('---------------------------------------------')

#Upload a KDS with  corresponding dara
def kinesis_upload(data):
    response = kinesis_client.put_record(
        StreamName='Autohome_Stream',
        Data=data.encode(),
        PartitionKey='0',
        ExplicitHashKey='0',
        SequenceNumberForOrdering='0'
    )
    return

#Custom functions for specific purposes
def add_light(component_ID):
    record = component_ID + ',0,0,ADD'
    kinesis_upload(record)

def remove_light(component_ID):
    record = component_ID + ',0,0,REMV'
    kinesis_upload(record)

def on_light(component_ID):
    record = component_ID + ',1,0,ON'
    kinesis_upload(record)

def off_light(component_ID):
    record = component_ID + ',0,0,OFF'
    kinesis_upload(record)

def set_temperature(component_ID,temperature):
    record = str(component_ID) + ',1,' + str(temperature) + ',SET'
    kinesis_upload(record)

IDs,L_status = Table_scan()#Start program with a device database scan

while flag:
    x = input('\nActions\n1)Add/Remove Light 2)Switch light 3)Set Temperatue 4)See Device Database 5)See Event Database x)Exit\nEnter action:')
    if x == 'x':#Exit
        flag = False
    elif x == '1':#Add or remove a device
        y = input('\n1)Add Light 2)Remove Light x)Back\nEnter action:')
        while y != '1' and y != '2' and y != 'x':
            y = input('Illegal input\n1)Add Light 2)Remove Light x)Back\nEnter action:')
        if y == '1':#Add a device
            z = input('\nLight ID to add (x for cancel):')
            #Exclude inproper input
            while (z[0] != 'L' and z != 'x') or z in IDs or (z[0] == 'L' and len(z) == 1):
                if z[0] == 'L' and z in IDs:
                    z = input('Light already exist!\nLight ID to be add (x for back):')
                else:
                    z = input('Illegal light name format!\nLight ID to be add (x for back):')
            if z[0] == 'L' and len(z) > 1:
                print('Add light ', z)
                add_light(z)
        elif y == '2':#Remove a device
            z = input('\nLight ID to remove (x for back):')
            #Exclude inproper input
            while (z[0] != 'L' and z != 'x') or (z[0] == 'L' and z not in IDs):
                if z[0] == 'L' and z not in IDs:
                    z = input('Light does not exist!\nLight ID to be add (x for back):')
                else:
                    z = input('Illegal light name format!\nLight ID to be add (x for back):')
            if z[0] == 'L' and z in IDs:
                print('Remove light ', z)
                remove_light(z)
        else:
            pass

    elif x == '2':#Switch a light
        y = input('\nLight to switch x)back\nEnter action:')
        #Exclude inproper input
        while y not in IDs and y != 'x' or (y[0] == 'T' and y in IDs):
            if y[0] == 'L' and y not in IDs:
                y = input('Light does not exist!\nLight to switch x)back\nEnter action:')
            else:
                y = input('Illegal light name format!\nLight to switch x)back\nEnter action:')
        #Switch light based on its current status
        if y[0] == 'L' and y in IDs:
            if L_status[y] == True:
                print('Turn off light ', y)
                off_light(y)
            else:
                print('Turn on light ', y)
                on_light(y)

    elif x == '3':#Set a temperature
        y = input('\nThermostat to set x)back\nEnter action:')
        #Exclude inproper input
        while y not in IDs and y != 'x' or (y[0] == 'L' and y in IDs):
            if y[0] == 'T' and y not in IDs:
                y = input('Thermostat does not exist!\nThermostat to set x)back\nEnter action:')
            else:
                y = input('Illegal thermostat name format!\nThermostat to set x)back\nEnter action:')
        if y[0] == 'T' and y in IDs:
            z = input('Set temperature: ')
            while not z.isdigit() or (int(z) > 120 or int(z) < 30):
                z = input('Illegal temperature\nSet temperature: ')
            print('Set thermostat ', y, ': ', z, 'F')
            set_temperature(y,z)
    elif x == '4':#Get Device Database
        IDs,L_status = Table_scan()
    elif x == '5':#Get Event Database
        Log_scan()

print('Finished')




