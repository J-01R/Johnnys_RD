//Jonatan Rassekhnia
//Linnaeus Univeristy
//Professor Fredrick A
// 6-23-2022
#include "PubSubClient.h"
#include <ESP8266WiFi.h>


#include <DHT.h>


char ssid[] = "Jdog";  // wifi name
char pass[] = "kobe24LA";  //wifi password


#define DHTPIN 4 //Connect Out pin to D2 in NODE MCU
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);


// MQTT properties
const char* mqtt_server = "mqtt.datacake.co";  // IP address of the MQTT broker
const char* temp_topic = "dtck-pub/mqtt-tempdevice/fdf0f057-daf3-4716-a510-b8fee04f99ae/TEMPERATURE";
const char* humid_topic = "dtck-pub/mqtt-tempdevice/fdf0f057-daf3-4716-a510-b8fee04f99ae/HUMIDITY";
const char* mqtt_username = "01e5a5726352ca95607820f69d5d5f3a3566ebde"; // MQTT username safer to use API user
const char* mqtt_password = "01e5a5726352ca95607820f69d5d5f3a3566ebde"; // MQTT password safer to use API pass
const char* clientID = "arduino"; // MQTT client ID

WiFiClient wifiClient;

PubSubClient client(mqtt_server, 1883, wifiClient);


void setup()
{

  Serial.begin(115200);
  WiFi.begin(ssid, pass);

  // while wifi not connected yet, print '.'
  // then after it connected, get out of the loop
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  //print a new line, then print WiFi connected and the IP address
  Serial.println("");
  Serial.println("WiFi connected");
  // Print the IP address
  Serial.println(WiFi.localIP());


  dht.begin();


}

bool connect_MQTT() {
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, pass);
  // Wait until the connection has been confirmed before continuing
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  // Debugging - Output the IP Address
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  // Connect to MQTT Broker
  // client.connect returns a boolean value to let us know if the connection was successful.
  if (client.connect(clientID, mqtt_username, mqtt_password)) {
    Serial.println("Connected to MQTT Broker!");
    return true;
  }
  else {
    Serial.println("Connection to MQTT Broker failed...");
    return false;
  }
}

void(* resetFunc) (void) = 0;

void loop()
{

  if (connect_MQTT()) {
    delay(10); // This delay ensures that client.publish doesn't clash with the client.connect call
    float h = dht.readHumidity();
    float t = dht.readTemperature(); // or dht.readTemperature(true) for Fahrenheit

    if (isnan(h) || isnan(t)) {
      Serial.println("Failed to read from DHT sensor!");
      resetFunc();
    }
    char temp_buf[6];
    char hum_buf[6];

    //null terminator 

    String(t, 2).toCharArray(temp_buf, 6);
    String(h, 2).toCharArray(hum_buf, 6);

    

    // Publish all data to the MQTT
    if (client.publish(temp_topic, temp_buf, 6)) {
    delay(10); // This delay ensures that BME data upload is all good
      client.publish(humid_topic, hum_buf, 6);
      delay(10); // This delay ensures that BME data upload is all good
      Serial.print("Temperature: ");
      Serial.println(temp_buf);
      Serial.print("Humitidy: ");
      Serial.println(hum_buf);
      
      delay(300000);
    }

  }
  resetFunc();
}
