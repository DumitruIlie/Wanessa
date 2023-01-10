from v128 import v128
class i16x8:
    def __init__(self):
        #???
        self._x = 0
    def extadd_pairwise_i8x16_s(t):
        list_zero = [0 for _ in range(8)]
        type_resulted = "16x8"
        ans = v128(type_resulted,list_zero)
        for i in range(0,8):
            ans._v[i] = t._v[i*2] + t._v[i*2+1]
        for i in range(0,len(ans._v)):
            ans._v[i] = ans._v[i] & (2**9 - 1)
            if ans._v[i] & 2**8:
                ans._v[i] -= 2**9
        return ans
    def extadd_pairwise_i8x16_u(t):
        list_zero = [0 for _ in range(8)]
        type_resulted = "16x8"
        ans = v128(type_resulted,list_zero)
        for i in range(0,8):
            ans._v[i] = t._v[i*2] + t._v[i*2+1]
        return ans