import pyb, micropython, ujson
micropython.alloc_emergency_exception_buf(100)

class main():
    def __init__(self):
        self.timer = pyb.Timer(1, freq = 2*1000)
        self.flag = False
        self.led = pyb.LED(4)

    def cb(self, tim):
        self.flag = True

    def start(self):
        print('Start')
        self.timer.callback(self.cb)
        while True:
            pyb.udelay(1)
            if self.flag == True:
                self.led.toggle()
                self.flag = False

if __name__=='__main__':
    myLoop = main()
    myLoop.start()
