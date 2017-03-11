import pyb, micropython, ujson
micropython.alloc_emergency_exception_buf(100)
from VNH5019 import VNH5019
from PID import PID

class controller(object):
    def __init__(self, config_filename = 'pid_config.json'):
        self.mesTemp = pyb.ADC(pyb.Pin('PC4'))
        self.mesPh = pyb.ADC(pyb.Pin('PC5'))
        self.vnh = VNH5019()
        self.config_filename = config_filename
        self.configure()

    def cb(self, tim):
        self.y01 = self.mesPh.read()
        self.u1 = min(4000, max(-4000, self.myPID1.compute(self.y01)))
        self.vnh.setPWM1(self.u1)
        self.y02 = self.mesTemp.read()
        self.u2 = min(4000, max(-4000, self.myPID2.compute(self.y02)))
        self.vnh.setPWM2(self.u2)

    def start(self):
        print('Start')
        self.timer.callback(self.cb)
        #self.wait_for_restart()

    def stop(self):
        self.timer.callback(None)
        #self.debug.callback(None)
        self.vnh.setPWM1(0)
        self.vnh.setPWM2(0)
        print('Stop')

    def wait_for_restart(self):
        while pyb.Switch()() == False:
            pyb.delay(20)
        self.restart()

    def restart(self):
        self.stop()
        pyb.delay(1000)
        self.configure()
        self.start()

    def configure(self):
        self.load_config()
        #self.myPID1 = PID(self.config['kp1'], self.config['ki1'], self.config['sp1'])
        self.myPID1 = PID(2000, 5, 1125)
        self.myPID2 = PID(self.config['kp2'], self.config['ki2'], self.config['sp2'])
        self.myPID2.stop()
        self.u1 = 0
        self.y01 = 0
        self.u2 = 0
        self.y02 = 0
        self.timer = pyb.Timer(1, freq = 1000)
        #self.debug = pyb.Timer(3, freq=10)
        #self.debug.callback(lambda t:print(self.config['sp1'], self.y01, self.u1, self.config['sp2'], self.y02, self.u2))

    def disp(self, tim = None):
        print(self.config['sp1'], self.y01, self.u1, self.config['sp2'], self.y02, self.u2)

    def logON(self, f = 1):
        self.debug = pyb.Timer(3, freq = int(f))
        self.debug.callback(self.disp)

    def logOFF(self):
        self.debug.callback(None)

    def load_config(self):
        try:
            with open(self.config_filename, 'r') as f:
                self.config = ujson.loads(f.read())
        except:
            config = {'kp1': 0, 'ki1': 0, 'sp1': 1450, 'kp2': 0, 'ki2': 0, 'sp2': 1500}
            with open(self.config_filename, 'w') as f:
                config_json = ujson.dumps(config)
                f.write("%s" % config_json)
        finally:
            with open(self.config_filename, 'r') as f:
                self.config = ujson.loads(f.read())

if __name__=='__main__':
    myLock = controller()
    myLock.start()
