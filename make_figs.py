# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 22:53:18 2021

@author: Chad
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import housemon_tools as hmt
import mysql.connector as mariadb
import numpy as np
import time

cnx_details = ["USER", "PASSWORD", "housemon_db", "192.168.0.6", "3306"]

connection = mariadb.connect(
    user = cnx_details[0],
    password = cnx_details[1],
    database = cnx_details[2],
    host = cnx_details[3],
    port = cnx_details[4])
        
cursor = connection.cursor()

query = "SELECT * FROM sensor"

cursor.execute(query)
count = 0;

for sensor in cursor:
    this_id = sensor[0]
    this_type = sensor[1]
    this_loc = sensor[2]

    if (count==0):
        sens_id = np.array(this_id)
        sens_type = np.array(this_type)
        sens_loc = np.array(this_loc)             
    else:
        sens_id = np.append(sens_id, this_id)
        sens_type = np.append(sens_type, this_type)
        sens_loc = np.append(sens_loc, this_loc)
    count = count + 1

count = 0

for lid in sens_loc:
    query = "SELECT description FROM location WHERE id=%d"%lid
    cursor.execute(query)
    
    if (count==0):
        locnames = np.array(cursor.next()[0])
    else:
        locnames = np.append(locnames, cursor.next()[0])
    count = count + 1

plotnum = 0;
fig = plt.figure(1);
plt.clf()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
for this_sid in sens_id:
    seconds, data = hmt.get_last_days(cnx_details, this_sid, 1.25)
    #seconds, data = hmt.get_last_days(cnx_details, this_sid)
    now = time.localtime()
    midnight = "%d %d %d"%(now.tm_mday, now.tm_mon, now.tm_year)
    midn_str = time.strptime(midnight, "%d %m %Y")
    midn_sec = time.mktime(midn_str)
    
    sec = seconds - midn_sec
    hr = sec/60/60
    
    #fig = plt.figure(this_sid)
    #plt.clf()
    
    #ax = fig.add_subplot(111)
    if np.max(data) > 10:
        ax1.plot(hr, data, label=locnames[plotnum])
    else:
        ax2.plot(hr, data, label=locnames[plotnum])
        
    #ax.legend()
    
    plotnum = plotnum+1;
        
title_string = "Generated at %d:%02d"%(now.tm_hour, now.tm_min)    
degree_sign = u'\N{DEGREE SIGN}'

ax1.set(ylabel="temp (%sC)"%degree_sign, title=title_string)
ax2.set(xlabel="hour", ylabel="temp (%sC)"%degree_sign)
#ax1.set_ylim(16,29)

ax1.grid()
ax2.grid()

ax1.legend()
ax2.legend()
plt.draw()

# ax1.yaxis.set_label_position('right')
# ax1.yaxis.tick_right()
# ax2.yaxis.set_label_position('right')
# ax2.yaxis.tick_right()

fig.canvas.draw()

hmt.labels_to_24h(ax1)
hmt.labels_to_24h(ax2)
plt.savefig("/home/pi/python/24hr.png")
cursor.close()
connection.close()

