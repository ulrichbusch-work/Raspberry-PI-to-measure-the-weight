import RPi.GPIO as gpio
import time
import smtplib
from email.message import EmailMessage

from_email_addr ="fromraspberry4@outlook.com"
from_email_pass = "khluwprjinfdhtespy"
to_email_addr ="1deliou10@gmail.com"

msg = EmailMessage()

msg['From'] = from_email_addr
msg['To'] = to_email_addr

msg['Subject'] = 'Warning'

server = smtplib.SMTP('smtp.office365.com', 587)

server.starttls()

server.login(from_email_addr, from_email_pass)

DT =5

SCK=6

HIGH=1

LOW=0

sample=0

redLedPin = 12

greenLedPin = 16

yellowLedPin = 21

gpio.setwarnings(False)

gpio.setmode(gpio.BCM)

gpio.setup(SCK, gpio.OUT)

gpio.setup(redLedPin, gpio.OUT)

gpio.setup(greenLedPin, gpio.OUT)

gpio.setup(yellowLedPin, gpio.OUT)

def measureWeight():

  i=0

  weight=0

 # print weight

 # time.sleep(0.001)

  gpio.setup(DT, gpio.OUT)

  gpio.output(DT,1)

  gpio.output(SCK,0)

  gpio.setup(DT, gpio.IN)

  while gpio.input(DT) == 1:

      i=0

  for i in range(24):

        gpio.output(SCK,1)

        weight=weight<<1

        gpio.output(SCK,0)

        #time.sleep(0.001)

        if gpio.input(DT) == 0: 

            weight=weight+1

            #print Weight

  gpio.output(SCK,1)

  weight=weight^0x800000

  #time.sleep(0.001)

  gpio.output(SCK,0)

  return weight  

time.sleep(3)

calibration = 416000

zeroValue = 8225000

#gpio.cleanup()

weightChanged = False

msg.set_content("Warning the holder cups is empty")

prevWeight = 0

while 1:
        
      measuredWeight = measureWeight()
      
      actualWeight= ( measuredWeight - zeroValue )/ calibration * 1000
      
      actualWeight = round(actualWeight)
      
      if abs(actualWeight - prevWeight) > 30:
          weightChanged = True
          prevWeight = actualWeight
          
      print(actualWeight, "g")  
    #  body ="Hello from Raspberry Pi"
      msg.set_content(str(actualWeight))
      
      delay = 20
      
      while delay:
          
          delay = delay - 1
          
          if actualWeight < 200:
          
              gpio.output(redLedPin, gpio.HIGH)
              
              gpio.output(greenLedPin, gpio.LOW)
              
              gpio.output(yellowLedPin, gpio.LOW)
              
              if weightChanged:
                  
                  weightChanged = False
                  
                  msg.set_content(str(actualWeight) + ":  Warning the holder cups is empty")
          
          elif 200 < actualWeight and actualWeight < 350:
              
              gpio.output(redLedPin, gpio.LOW)
              
              gpio.output(greenLedPin, gpio.LOW)
              
              gpio.output(yellowLedPin, gpio.HIGH)
              
              if weightChanged:
                  
                  weightChanged = False
              
                  msg.set_content("There is " + str(actualWeight) + "g")

              
          else:
              
              gpio.output(redLedPin, gpio.LOW)
              
              gpio.output(greenLedPin, gpio.HIGH)
              
              gpio.output(yellowLedPin, gpio.LOW)
              
              if weightChanged:
                  
                  weightChanged = False
              
                  msg.set_content("There is " + str(actualWeight) + "g")
      
      server.send_message(msg)
      print('Email sent')
      time.sleep(1)
server.quit()

    
