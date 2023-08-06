from serial import Serial
from time import sleep

class WallDisplay(Serial):
  def __init__(self, device):
    Serial.__init__(self, device)
    self.baudrate = 2400

  def safeWrite(self, msg):
    for char in msg:
      self.write(char.encode())
      sleep(0.02)

  def sendAllOn(self):
    self.safeWrite("allon\n")

  def sendAllOff(self):
    self.safeWrite("alloff\n")

  def sendAllFlash(self):
    self.safeWrite("allflash\n")

  def sendMessage(self, msg):
    self.safeWrite("\"%s\n"%(msg))
