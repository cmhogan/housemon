# Setting up thermal sensor

import machine, onewire, ds18x20, time

ds_pin = machine.Pin(14)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()
print('Found DS devices: ', roms)

# set up webserver
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)

  # read temperature
  ds_sensor.convert_temp()
  time.sleep_ms(750)
  temps = []
  for rom in roms:
      this_temp = ds_sensor.read_temp(rom)
      print(this_temp)
      temps.append(this_temp)


  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('<html>')
  for this_t in temps:
      print("sending %s"%this_t)
      conn.sendall("%s\n"%this_t)
      
  conn.send("</html>")
  conn.send('Connection: close\n\n')
  conn.close()