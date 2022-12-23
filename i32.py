ERROR_TYPE_MISMATCH = "TYPE MISMATCH"
ERROR_TYPE_DIVIDEBY0 = "INTEGER DIVIDE BY ZERO"
BITMASK_32 = 0xFFFFFFFF
BITMASK_64 = 0XFFFFFFFFFFFFFFFF
OVERFLOW_FLAG = False
class i32:
    ### 
    ### i32 CLASS
    ### Constructor
    def __init__(self, val):  
        self._val = val
    ### OVERFLOW
    def check_overflow(self): 
        try:
            global OVERFLOW_FLAG
            OVERFLOW_FLAG = False 
            self._val=int.from_bytes(self._val.to_bytes(4, 'little', signed=True), 'little', signed=True)
            ###Incearca sa-l reconstruiasca, da eroare de overflow in caz ca nu reuseste
        except OverflowError:
            ###Handle la eroare, pune flag si returneaza numarul cu bitii ramasi
            OVERFLOW_FLAG = True
            self._val = self._val & (2**32 - 1)
            if self._val & 2**31:
                self._val -= 2**32
    ### ADD - adunare
    def add(t1, t2):
        global OVERFLOW_FLAG
        OVERFLOW_FLAG = False
        if (isinstance(t1,i32) & isinstance(t2,i32)) != 1: 
            return ERROR_TYPE_MISMATCH
        ans = i32(0)
        ans._val = (t1._val + t2._val)
        ans.check_overflow()
        return ans
    ### SUB - scadere
    def sub(t1,t2):
        global OVERFLOW_FLAG
        OVERFLOW_FLAG = False
        if (isinstance(t1,i32) & isinstance(t2,i32)) != 1: 
            return ERROR_TYPE_MISMATCH
        ans = i32(0)
        ans._val = (t1._val - t2._val)
        ans.check_overflow()
        return ans
    ### MUL - inmultire
    def mul(t1,t2):
        global OVERFLOW_FLAG
        OVERFLOW_FLAG = False
        if (isinstance(t1,i32) & isinstance(t2,i32)) != 1: 
            return ERROR_TYPE_MISMATCH
        ans = i32(0)
        ans._val = (t1._val * t2._val)
        ans.check_overflow()
        return ans
    ### div_s - impartire cu semn
    def div_s(t1,t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) != 1: 
            return ERROR_TYPE_MISMATCH
        if (t2._val == 0):
            return ERROR_TYPE_DIVIDEBY0
        ans = i32(0)
        ans._val = (t1._val // t2._val)
        ans.check_overflow()
        return ans
    ### div_u - impartire fara semn
    def div_u(t1, t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) != 1: 
            return ERROR_TYPE_MISMATCH
        if (t2._val == 0):
            return ERROR_TYPE_DIVIDEBY0
        ans = i32(0)
        ans._val = (t1._val // t2._val)
        ans.check_overflow()
        ans._val = ans._val & BITMASK_32
        return ans
    def __str__(self):
        return f"{self._val}"

#Faci teste
'''
a = i32(-50)
b = i32(25)
c = i32.div_u(a,b)
print(c._val)
'''