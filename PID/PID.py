class PID(object):
    def __init__(self, Kp = 0, Ki = 0, sp = 0, imax = 100000):
        self.setKp(int(Kp))
        self.setKi(int(Ki))
        self.resetInt()
        self.setSp(int(sp))
        self.setIntSat(int(imax))
        self.ON = True

    def compute(self, y0):
        if self.ON:
            eps = self.setpoint - y0
            #if abs(eps) < 10:
            #    self.Sum = 0
            #else:
            self.Sum = min(self.imax, max(-self.imax, self.Sum + eps))
            return (self.Kp * eps + self.Ki * self.Sum)//1000
        else:
            return 0

    def setKp(self, Kp):
        self.Kp = Kp

    def setKi(self, Ki):
        self.Ki = Ki

    def resetInt(self):
        self.Sum = 0

    def setSp(self, Sp):
        self.setpoint = Sp

    def setIntSat(self, imax):
        self.imax = imax

    def status(self):
        print('%s\t%s\t%s\t%s\t%s'%(self.setpoint, self.Kp, self.Ki, self.Sum, self.ON))

    def stop(self):
        self.ON = False
        self.setKp(0)
        self.setKi(0)
        self.resetInt()

    def start(self):
        self.ON = True

    def set(self, Kp = 0, Ki = 0, sp = 2000):
        self.setKp(Kp)
        self.setKi(Ki)
        self.setSp(sp)
