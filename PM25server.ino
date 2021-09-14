#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include <ESPmDNS.h>
#include <Seeed_HM330X.h>

const char* ssid = "SSID";
const char* password = "PASSWORD";

WebServer server(80);

HM330X sensor;
u8 buf[30];

const int led = 13;

void handleRoot() {
  char HM_output[100];
  u16 values[4];

  digitalWrite(led, 1);
  if(sensor.read_sensor_value(buf,29))
    {
      Serial.println("HM330X read result failed!!!");
      server.send(200, "text/plain", "HM330X read result failed!!!");
    }
   else
    {
      for(int i=1;i<5;i++)
      {
        values[i-1] = (u16)buf[i*2]<<8|buf[i*2+1];      
      }
      
      sprintf(HM_output, "Sensor: %d PM1.0: %d PM2.5: %d PM10: %d", values[0], values[1], values[2], values[3]);

      server.send(200, "text/plain", HM_output);
    }
  digitalWrite(led, 0);
}

void handleNotFound() {
  digitalWrite(led, 1);
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
  digitalWrite(led, 0);
}

void setup(void) {
  pinMode(led, OUTPUT);
  digitalWrite(led, 0);
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("esp32")) {
    Serial.println("MDNS responder started");
  }

  server.on("/", handleRoot);

  server.on("/inline", []() {
    server.send(200, "text/plain", "this works as well");
  });

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");

  if(sensor.init())
    {
        Serial.println("HM330X init failed!!!");
        while(1);
    }
  else
    {
      Serial.println("HM330X init succeeded.");
    }
}

void loop(void) {
  server.handleClient();
  delay(2);//allow the cpu to switch to other tasks
}
