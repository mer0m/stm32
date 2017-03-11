import pyb, micropython, ujson
micropython.alloc_emergency_exception_buf(100)
from IIR import IIR

class main():
    def __init__(self):
        self.adc = pyb.ADC(pyb.Pin('PC5'))
        self.dac = pyb.DAC(2, bits = 12)
        self.myIIR = IIR(1, 1, -1022)
        self.timer = pyb.Timer(2, freq = 1000)

    def cb(self, tim):
        x0 = self.adc.read()
        y0 = min(4095, max(0, self.myIIR.compute(x0)))
        self.dac.write(y0)

    def start(self):
        print('Start')
        self.timer.callback(self.cb)

    def stop(self):
        self.timer.callback(None)
        self.dac.write(0)
        print('Stop')

if __name__=='__main__':
    myLoop = main()
    myLoop.start()
