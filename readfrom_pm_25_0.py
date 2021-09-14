# -*- coding: utf-8 -*-

import socket, re
import housemon_tools as hmt
import time

sock = socket.socket()

sock.connect(("192.168.0.23", 80))

request_text = "GET / HTTP/1.1"

sock.sendall(request_text.encode('ascii'))
raw_reply = b''

while True:
    more = sock.recv(4096)
    if not more: 
        break
    raw_reply += more

raw_text = raw_reply.decode('utf-8')

split_up = raw_text.split()

cnx_details = ["USERNAME", "PASSWORD", "housemon_db", "192.168.0.6", "3306"]

sensor_name = "bedroom_pm2.5"

sensor_id = hmt.get_sensor_id(cnx_details, sensor_name)
record = [time.time(), sensor_id, float(split_up[14])]
hmt.add_temperature(cnx_details, record)
