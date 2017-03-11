import pyb, micropython
micropython.alloc_emergency_exception_buf(100)

class VNH5019(object):
    def __init__(self, m1inA = 'PC0', m1inB = 'PC2', m1pwm = 'PA2', m2inA = 'PC1', m2inB = 'PC3', m2pwm = 'PA3'):
        self.m1inA = pyb.Pin(m1inA, pyb.Pin.OUT_PP)
        self.m1inB = pyb.Pin(m1inB, pyb.Pin.OUT_PP)
        self.m2inA = pyb.Pin(m2inA, pyb.Pin.OUT_PP)
        self.m2inB = pyb.Pin(m2inB, pyb.Pin.OUT_PP)
        self.timer = pyb.Timer(2, freq = 20000)
        self.m1pwm = self.timer.channel(3, pyb.Timer.PWM, pin = pyb.Pin(m1pwm))
        self.m2pwm = self.timer.channel(4, pyb.Timer.PWM, pin = pyb.Pin(m2pwm))
        self.setPWM1(0)
        self.setPWM2(0)

    def setPWM1_percent(self, value = 0):
        if value >=0:
            self.setDir1(1)
            self.m1pwm.pulse_width_percent(value)
        else:
            self.setDir1(-1)
            self.m1pwm.pulse_width_percent(-value)

    def setPWM1(self, value = 0):
        if value >=0:
            self.setDir1(1)
            self.m1pwm.pulse_width(value)
        else:
            self.setDir1(-1)
            self.m1pwm.pulse_width(-value)

    def setDir1(self, val = 1):
        if val == 1:
            self.m1inA.low()
            self.m1inB.high()
        elif val == -1:
            self.m1inA.high()
            self.m1inB.low()

    def setPWM2_percent(self, value = 0):
        if value >=0:
            self.setDir2(1)
            self.m2pwm.pulse_width_percent(value)
        else:
            self.setDir2(-1)
            self.m2pwm.pulse_width_percent(-value)

    def setPWM2(self, value = 0):
        if value >=0:
            self.setDir2(1)
            self.m2pwm.pulse_width(value)
        else:
            self.setDir2(-1)
            self.m2pwm.pulse_width(-value)

    def setDir2(self, val = 1):
        if val == 1:
            self.m2inA.low()
            self.m2inB.high()
        elif val == -1:
            self.m2inA.high()
            self.m2inB.low()
