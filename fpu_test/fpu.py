@micropython.asm_thumb
def add(r0, r1):
    vmov(s0, r0)
    vmov(s1, r1)
    vadd(s2, s0, s1)
    vmov(r0, s2)

@staticmethod
@micropython.asm_thumb
def mul(r0, r1, r2):
    vmov(s1, r1)
    vmov(s2, r2)
    vmul(s0, s1, s2)
    vstr(s0, [r0, 0])

@micropython.asm_thumb
def div(r0, r1):
    data(2, 0xfb90, 0xf0f1)
