# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 18:53:44 2021

@author: Chad
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 22:53:18 2021

@author: Chad
"""
import socket, re
import housemon_tools as hmt
import time

sock = socket.socket()

sock.connect(("192.168.0.21", 80))

request_text = "GET / HTTP/1.1"

sock.sendall(request_text.encode('ascii'))
raw_reply = b''

while True:
    more = sock.recv(4096)
    if not more: 
        break
    raw_reply += more

raw_text = raw_reply.decode('utf-8')

p = re.compile("<html>[\d\.]*")

span = p.search(raw_text).span()

temp = float(raw_text[span[0]+6:span[1]])

cnx_details = ["USERNAME", "PASSWORD", "housemon_db", "192.168.0.6", "3306"]

sensor_name = "garage_esp"

sensor_id = hmt.get_sensor_id(cnx_details, sensor_name)
record = [time.time(), sensor_id, temp]
hmt.add_temperature(cnx_details, record)
