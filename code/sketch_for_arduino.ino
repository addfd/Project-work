#include <Adafruit_NeoPixel.h>
#include <Servo.h>


const int num = 5;
Adafruit_NeoPixel* strips[num];
Servo* stripsservo[num];


bool isInitialized = false;
String message;


void setup()
{
  Serial.begin(9600);
  Serial.println("BEGIN"); 

  while (!isInitialized) 
  {
    if (Serial.available() > 0) {
      String message = Serial.readString();
      if (message == "done") {
        isInitialized = true;
      }
      else{




        String inputString = message;
        char delimiter = ' ';
        String outputArray[10];
        int outputArraySize = 10;
        int outputArrayLength;

        splitString(inputString, delimiter, outputArray, outputArraySize, outputArrayLength);
        
        if (outputArray[0] == "0"){
          strips[outputArray[3].toInt()] = new Adafruit_NeoPixel(outputArray[2].toInt(), outputArray[1].toInt(), NEO_GRB + NEO_KHZ800);
          strips[outputArray[3].toInt()]->begin();
          strips[outputArray[3].toInt()]->show();
          for(int i = 0; i < strips[outputArray[3].toInt()]->numPixels(); i++) {
            strips[outputArray[3].toInt()]->setPixelColor(i, strips[outputArray[3].toInt()]->Color(255, 0, 0));
          }
          strips[outputArray[3].toInt()]->setBrightness(200);
          strips[outputArray[3].toInt()]->show();
        }else if (outputArray[0] == "1"){
          stripsservo[outputArray[2].toInt()] = new Servo();
          stripsservo[outputArray[2].toInt()]->attach(outputArray[1].toInt());
        }
      
      
      
    }




  }
  Serial.println("DONE!"); 
  }
}

void loop()
{
  while (Serial.available())
  { 
    message += char(Serial.read()); //сохраняем строку от входящих сообщений
  }
  if (!Serial.available())
  {
    if (message != "")
    { //если данные доступны

      Serial.println(message); 

      String inputString = message;
      char delimiter = ' ';
      String outputArray[10];
      int outputArraySize = 10;
      int outputArrayLength;

      splitString(inputString, delimiter, outputArray, outputArraySize, outputArrayLength);
        
      if (outputArray[0] == "0"){
        switch (outputArray[2].toInt()) {
        case 0: 
          strips[outputArray[1].toInt()]->setBrightness(outputArray[3].toInt());
          strips[outputArray[1].toInt()]->show();
          break;
        case 1:
          int r = outputArray[3].toInt();
          int g = outputArray[4].toInt();
          int b = outputArray[5].toInt();
          for(int i = 0; i < strips[outputArray[1].toInt()]->numPixels(); i++) {
            strips[outputArray[1].toInt()]->setPixelColor(i, strips[outputArray[1].toInt()]->Color(r, g, b));
          }
          strips[outputArray[1].toInt()]->show();
          break;
        default:
          break;
        }
      }else if (outputArray[0] == "1"){
        stripsservo[outputArray[1].toInt()]->write(outputArray[2].toInt());
      }
        
      }
      message = ""; //очищаем данные
    }
  
  delay(100); //delay
}



void splitString(String inputString, char delimiter, String* outputArray, int outputArraySize, int& outputArrayLength) { // 
  outputArrayLength = 0; // сбросим длину массива на всякий случай
  
  // Итерируемся по символам строки
  int startIndex = 0;
  for (int i = 0; i < inputString.length(); i++) {
    // Если текущий символ - разделитель, то вырезаем подстроку и добавляем ее в массив
    if (inputString.charAt(i) == delimiter) {
      outputArray[outputArrayLength++] = inputString.substring(startIndex, i);
      startIndex = i + 1;
      
      // Если массив заполнен, то завершаем функцию
      if (outputArrayLength >= outputArraySize) {
        return;
      }
    }
  }
  
  // Добавляем последний элемент, если он есть
  if (startIndex < inputString.length()) {
    outputArray[outputArrayLength++] = inputString.substring(startIndex);
  }
}