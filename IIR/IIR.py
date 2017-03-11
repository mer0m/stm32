class IIR(object):
    def __init__(self, m0, m1, n1):
        self.m0 = m0
        self.m1 = m1
        self.n1 = n1
        self.y1 = 0
        self.x1 = 0

    def compute(self, x0):
        '''y0 = m0*x0+m1*x1-n1*y1
        '''
        self.y1 = min(4095<<10, max(0, self.m0*x0 + self.m1*self.x1 - self.n1*self.y1))
        self.x1 = x0
        return self.y1>>10
