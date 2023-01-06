#include "WiFi.h"
int ledPin = 2;
const char* ssid = "Pixel6a";
const char* pwd = "Carotte:)";

int JoyStick_X = 35; // Signal de l'axe X
int JoyStick_Y = 32; // Signal de l'axe Y
int Button = 33; // Bouton

void setup() 
{
  pinMode(ledPin, OUTPUT);

  pinMode(JoyStick_X, INPUT);
  pinMode(JoyStick_Y, INPUT);
  pinMode(Button, INPUT);

  // Lorsqu'on pousse sur le bouton, la mise à la masse
  // active la résistance de PullUp.
  digitalWrite(Button, HIGH); 
  
  Serial.begin(9600);
  Serial.println("Configuration du WiFi");
  
  WiFi.begin(ssid, pwd);

  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.println("Connexion au WiFi..");
  }

  Serial.print("Est connecte au reseau avec ");
  Serial.println(WiFi.localIP());
}

void loop() 
{
  delay(500);

  int x, y, btn;

  x = ceil(analogRead (JoyStick_X) * (5.0 / 1023.0)); 
  y = ceil(analogRead (JoyStick_Y) * (5.0 / 1023.0));
  btn = digitalRead (Button);
  
  if (WiFi.status() == WL_CONNECTED) 
  {    
    digitalWrite(ledPin, HIGH);
    WiFiClient curl;

    int xValue = abs(10 - x);
    int yValue = abs(10 - y);
    
    if(xValue > 5 || yValue > 5)
    {
      int xCmd = xValue > 5 ? 10 - x > 0 ? 2 : 3 : -1;
      int yCmd = yValue > 5 ? 10 - y > 0 ? 0 : 1 : -1;
      
      if(curl.connect("192.168.233.89", 5000)) 
      {
        Serial.println("Connected");

        String endCmd = "  HTTP/1.1";
        String startCmd = "GET /commande/";

        String strCmd = startCmd + + (xCmd > -1 ? xCmd : yCmd) + endCmd;

        Serial.println(strCmd);
        
        curl.println(strCmd);
        curl.println("Host:192.168.233.89");
        curl.println("Connection: close");
        curl.println();
      } 
      else 
      {
        Serial.println("ConnectionFailed");
      }
    }
  } 
  else 
  {
    Serial.println("N'est pas connecte au reseau");
    digitalWrite(ledPin, LOW);
  }
}
