import threading
import time

class Test:
   test = 1
   def threadFunc(self):
      print(self.test)
      for i in range(5):
         print('Hello from new Thread ')
         print(self.test)
         time.sleep(1)
      self.test = 3

   def go(self):
      th = threading.Thread(target=self.threadFunc)
      th.start()
      self.test = 2
      while self.test == 2:
         print("Esperando")
         time.sleep(1)
      print("Cambiado: ", self.test)

t = Test()
t.go()

