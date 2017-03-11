class PIDfloat:
    def __init__(self, P = 0, I = 0, D = 0, N = 100, Ts=0.001, synth = 'Tustin', filtered = 'eps'):

        self.U = array('f', [0, 0, 0, 0, 0, 0, 0, 0]) #[u0, u1, e0, e1, e2, y0, y1, y2]

        if synth == 'BE':
            '''
            Backward Euler
            '''
            a0 = 1+N*Ts
            a1 = -(N*Ts+2)
            a2 = 1
            i0 = I*Ts*(1+N*Ts)
            i1 = -(I*Ts)
            i2 = 0
            p0 = P*(1+N*Ts)
            p1 = -P*(2+N*Ts)
            p2 = P
            d0 = D*N
            d1 = -2*D*N
            d2 = D*N
        if synth == 'Tustin':
            '''
            Tustin
            '''
            a0 = 2+N*Ts
            a1 = -4
            a2 = 2-N*Ts
            i0 = I*Ts*(1+N*Ts/2)
            i1 = I*Ts*Ts*N
            i2 = I*Ts*(N*Ts/2-1)
            p0 = P*(2+N*Ts)
            p1 = -4*P
            p2 = P*(2-N*Ts)
            d0 = 2*D*N
            d1 = -4*D*N
            d2 = 2*D*N

        ku1 = a1/a0
        ku2 = a2/a0

        if filtered == 'dpy':
            ke0 = i0/a0
            ke1 = i1/a0
            ke2 = i2/a0
            ky0 = (d0+p0)/a0
            ky1 = (d1+p1)/a0
            ky2 = (d2+p2)/a0
        if filtered == 'dy':
            ke0 = (p0+i0)/a0
            ke1 = (p1+i1)/a0
            ke2 = (p2+i2)/a0
            ky0 = d0/a0
            ky1 = d1/a0
            ky2 = d2/a0
        if filtered == 'eps':
            ke0 = (p0+i0+d0)/a0
            ke1 = (p1+i1+d1)/a0
            ke2 = (p2+i2+d2)/a0
            ky0 = 0
            ky1 = 0
            ky2 = 0

        self.K = array('f', [-ku1, -ku2, ke0, ke1, ke2, -ky0, -ky1, -ky2])

        self.Y = array('f', [0, 500, 0])

    def compute(self, y0 = 0):
        self.updY(self.Y, y0)
        self.asm_PID(self.K, self.U, self.Y)

        return self.Y

    @staticmethod
    @micropython.asm_thumb
    def asm_PID(r0, r1, r2):
        #load K array
        vldr(s0,[r0,0])    #-ku1
        vldr(s1,[r0,4])    #-ku2
        vldr(s2,[r0,8])    #ke0
        vldr(s3,[r0,12])   #ke1
        vldr(s4,[r0,16])   #ke2
        vldr(s5,[r0,20])   #ky0
        vldr(s6,[r0,24])   #ky1
        vldr(s7,[r0,28])   #ky2

        #load Y array
        vldr(s16,[r2,0])   #last u0
        vldr(s17,[r2,4])   #setpoint
        vldr(s13,[r2,8])   #new y0

        #load U array
        vldr(s8,[r1,0])    #u1
        vldr(s9,[r1,4])    #u2
        vsub(s10,s17,s13)  #new e0 = setpoint - new y0
        vldr(s11,[r1,8])   #e1 = last e0
        vldr(s12,[r1,12])   #e2 = last e1
        vldr(s14,[r1,20])  #y1 = last y0
        vldr(s15,[r1,24])  #y2 = last y1

        #compute new u0
        vmul(s0,s0,s8)
        vmul(s1,s1,s9)
        vmul(s2,s2,s10)
        vmul(s3,s3,s11)
        vmul(s4,s4,s12)
        vmul(s5,s5,s13)
        vmul(s6,s6,s14)
        vmul(s7,s7,s15)
        vadd(s0,s0,s1)
        vadd(s0,s0,s2)
        vadd(s0,s0,s3)
        vadd(s0,s0,s4)
        vadd(s0,s0,s5)
        vadd(s0,s0,s6)
        vadd(s0,s0,s7)

        #update U array
        vstr(s16,[r1,0])   #u1 = last u0
        vstr(s8,[r1,4])    #u2 = last u1
        vstr(s10,[r1,8])   #e0 = new e0
        vstr(s11,[r1,12])  #e1 = last e0
        vstr(s12,[r1,16])  #e2 = last e1
        vstr(s13,[r1,20])  #y0 = new y0
        vstr(s14,[r1,24])  #y1 = last y0
        vstr(s15,[r1,28])  #y2 = last y1

        #update u0 in Y array
        vstr(s0,[r2,0])    #u0 = new u0

    @staticmethod
    @micropython.asm_thumb
    def updY(r0, r1):
        #load y0 array
        vmov(s0,r1)    #new y0

        #update y0 in Y array
        vstr(s0,[r0,8])    #y0 = new y0
