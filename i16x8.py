from v128 import v128
class i16x8:
    def __init__(self):
        #???
        self._x = 0
    def extadd_pairwise_i8x16_s(t):
        t._type = "16x8"
        for i in range(0,16,2):
            t._v[i//2] = t._v[i] + t._v[i+1]
        t._v = t._v[:8]
        for i in range(0,len(t._v)):
            t._v[i] = t._v[i] & (2**9 - 1)
            if t._v[i] & 2**8:
                t._v[i] -= 2**9
    def extadd_pairwise_i8x16_u(t):
        t._type = "16x8"
        for i in range(0,16,2):
            t._v[i//2] = t._v[i] + t._v[i+1]
        t._v = t._v[:8]


aj = v128("8x16",[255,255,127,127,0,0,0,0,0,0,0,0,0,0,0,0])
i16x8.extadd_pairwise_i8x16_u(aj)
print(aj)