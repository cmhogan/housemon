# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 15:23:19 2021

@author: Chad
"""

import mysql.connector as mariadb
import housemon_tools as hmt
import time
import os
import sys
import glob

cnx_details = ["USER", "PASSWORD", "housemon_db", "192.168.0.6", "3306"]

#%%

import RPi.GPIO as GPIO

GPIO_PIN_NUMBER=14
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN_NUMBER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def ds18b20_read_sensors():
    rtn = {}
    w1_devices = []
    w1_devices = os.listdir("/sys/bus/w1/devices/")
    for deviceid in w1_devices:
        rtn[deviceid] = {}
        rtn[deviceid]['temp_c'] = None
        device_data_file = "/sys/bus/w1/devices/" + deviceid + "/w1_slave"
        if os.path.isfile(device_data_file):
            try:
                f = open(device_data_file, "r")
                data = f.read()
                f.close()
                if "YES" in data:
                    (discard, sep, reading) = data.partition(' t=')
                    rtn[deviceid]['temp_c'] = float(reading) / float(1000.0)
                else:
                    rtn[deviceid]['error'] = 'No YES flag: bad data.'
            except Exception as e:
                rtn[deviceid]['error'] = 'Exception during file parsing: ' + str(e)
        else:
            rtn[deviceid]['error'] = 'w1_slave file not found.'
    return rtn;

while True:
    temp_readings = ds18b20_read_sensors()
    for t in temp_readings:
        if not 'error' in temp_readings[t]:
            sensor_id = hmt.get_sensor_id(cnx_details, t)
            record = [time.time(), sensor_id, temp_readings[t]['temp_c']]
            hmt.add_temperature(cnx_details, record)
    time.sleep(60.0)

