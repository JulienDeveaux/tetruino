#include "WiFi.h"
#include "WiFiUdp.h"
#include "ESPmDNS.h"
#include "WebServer.h"

int ledPin = 2; // pin info wifi (bleu)
const char* ssid = "Pixel6a";
const char* pwd = "Carotte:)";

void(* resetFunc) (void) = 0;

int JoyStick_X = 35; // Signal de l'axe X
int JoyStick_Y = 32; // Signal de l'axe Y

int ButtonReset = 33; // Bouton reset
int ButtonPause = 25; // Bouton pause

int LedPause = 26;
int LedOver = 27;
int LedLineCleared = 34;

char* serverAddr = "192.168.233.89"; // la clairvoyance n'a pas fonctionnée :'(

WiFiUDP Udp;
WiFiClient curl;
WebServer server(80);

void setup()
{
  pinMode(ledPin, OUTPUT);

  pinMode(JoyStick_X, INPUT);
  pinMode(JoyStick_Y, INPUT);

  pinMode(ButtonReset, INPUT);
  pinMode(ButtonPause, INPUT);

  pinMode(LedPause, OUTPUT);
  pinMode(LedOver, OUTPUT);
  pinMode(LedLineCleared, OUTPUT);

  // Lorsqu'on pousse sur le bouton, la mise à la masse
  // active la résistance de PullUp.
  digitalWrite(ButtonReset, HIGH);

  Serial.begin(9600);
  Serial.println("Configuration du WiFi");

  WiFi.begin(ssid, pwd);

  int cptTentWifi = 0;
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println("Connexion au WiFi..");

    if(cptTentWifi++ > 10)
      resetFunc();
  }

  Serial.print("Est connecte au reseau avec ");
  Serial.println(WiFi.localIP());

  if (!MDNS.begin("ESP32_Browser")) {
        Serial.println("Error setting up MDNS responder!");
        while(1){
            delay(1000);
        }
    }

    if(curl.connect(serverAddr, 5000))
    {
      String endCmd = "  HTTP/1.1";
      String startCmd = "GET /register_gamepad";

      Serial.println(startCmd);

      curl.println(startCmd);
      curl.println("Host:192.168.233.89");
      curl.println("Connection: close");
      curl.println();
    }


    server.on("/", onGet);
    server.onNotFound(onNotFound);
    server.begin();
}

void onGet()
{
  String data = server.arg("data");
  String score = server.arg("score");

  if(data == "0")
  {
    Serial.println("gameOver");

    digitalWrite(LedPause, LOW);
    digitalWrite(LedOver, HIGH);
    digitalWrite(LedLineCleared, LOW);
  }
  else if(data == "1")
  {
    Serial.println("paused");

    digitalWrite(LedPause, HIGH);
    digitalWrite(LedOver, LOW);
    digitalWrite(LedLineCleared, LOW);
  }
  else if(data == "2")
  {
    Serial.println("Line cleared");

    digitalWrite(LedPause, LOW);
    digitalWrite(LedOver, LOW);
    digitalWrite(LedLineCleared, HIGH);
  }

  Serial.println(score);

  server.send(200, "text/json", "ok");
}

void onNotFound()
{
  Serial.println("get but route not found");
  server.send(404, "text/html", "no");
}

void browseService(const char * service, const char * proto){
    Serial.printf("Browsing for service _%s._%s.local. ... ", service, proto);
    int n = MDNS.queryService(service, proto);
    if (n == 0) {
        Serial.println("no services found");
    } else {
        Serial.print(n);
        Serial.println(" service(s) found");
        for (int i = 0; i < n; ++i) {
            // Print details for each service found
            Serial.print("  ");
            Serial.print(i + 1);
            Serial.print(": ");
            Serial.print(MDNS.hostname(i));
            Serial.print(" (");
            Serial.print(MDNS.IP(i));
            Serial.print(":");
            Serial.print(MDNS.port(i));
            Serial.println(")");
        }
    }
    Serial.println();
}

void loop()
{
  delay(100);

  int x, y, btn;

  x = ceil(analogRead (JoyStick_X) * (5.0 / 1023.0));
  y = ceil(analogRead (JoyStick_Y) * (5.0 / 1023.0));
  btn = digitalRead (ButtonReset);

  if (WiFi.status() == WL_CONNECTED)
  {
    digitalWrite(ledPin, HIGH);

    int xValue = abs(10 - x);
    int yValue = abs(10 - y);

    if(strlen(serverAddr) == 0)
    {
      Serial.println("send broadcast");

      browseService("http", "tcp");
      // pas de suite pour le moment
    }
    else
    {
      server.handleClient();

      if(xValue > 5 || yValue > 5)
      {
        int xCmd = xValue > 5 ? 10 - x > 0 ? 2 : 3 : -1;
        int yCmd = yValue > 5 ? 10 - y > 0 ? 0 : 1 : -1;

        if(curl.connect(serverAddr, 5000))
        {
          String endCmd = "  HTTP/1.1";
          String startCmd = "GET /commande/";

          String strCmd = startCmd + + (xCmd > -1 ? xCmd : yCmd) + endCmd;

          curl.println(strCmd);
          curl.println("Host:192.168.233.89");
          curl.println("Connection: close");
          curl.println();

          Serial.println("cmd sended");
        }
        else
        {
          Serial.println("ConnectionFailed");
        }
      }


    }
  }
  else
  {
    Serial.println("N'est pas connecte au reseau");
    digitalWrite(ledPin, LOW);
  }
}