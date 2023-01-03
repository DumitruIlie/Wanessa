ERROR_TYPE_MISMATCH = "TYPE MISMATCH"
ERROR_TYPE_DIVIDEBY0 = "INTEGER DIVIDE BY ZERO"
BITMASK_32 = 0xFFFFFFFF
BITMASK_64 = 0XFFFFFFFFFFFFFFFF
OVERFLOW_FLAG = False
class i64:
    ### 
    ### i64 CLASS
    ### Constructor
    def __init__(self, val):
        global OVERFLOW_FLAG
        OVERFLOW_FLAG = False  
        self._val = val
        self.check_overflow()
    ### OVERFLOW
    def check_overflow(self): 
        try:
            global OVERFLOW_FLAG
            OVERFLOW_FLAG = False 
            self._val=int.from_bytes(self._val.to_bytes(8, 'little', signed=True), 'little', signed=True)
            ###Incearca sa-l reconstruiasca, da eroare de overflow in caz ca nu reuseste
        except OverflowError:
            ###Handle la eroare, pune flag si returneaza numarul cu bitii ramasi
            OVERFLOW_FLAG = True
            self._val = self._val & (2**64 - 1)
            if self._val & 2**63:
                self._val -= 2**64
    ### ADD - adunare
    def add(t1, t2):
        global OVERFLOW_FLAG
        OVERFLOW_FLAG = False
        if (isinstance(t1,i64) & isinstance(t2,i64)) != 1: 
            return ERROR_TYPE_MISMATCH
        ans = i64(0)
        ans._val = (t1._val + t2._val)
        ans.check_overflow()
        return ans
    ### SUB - scadere
    def sub(t1,t2):
        global OVERFLOW_FLAG
        OVERFLOW_FLAG = False
        if (isinstance(t1,i64) & isinstance(t2,i64)) != 1: 
            return ERROR_TYPE_MISMATCH
        ans = i64(0)
        ans._val = (t1._val - t2._val)
        ans.check_overflow()
        return ans
    ### MUL - inmultire
    def mul(t1,t2):
        global OVERFLOW_FLAG
        OVERFLOW_FLAG = False
        if (isinstance(t1,i64) & isinstance(t2,i64)) != 1: 
            return ERROR_TYPE_MISMATCH
        ans = i64(0)
        ans._val = (t1._val * t2._val)
        ans.check_overflow()
        return ans
    ### div_s - impartire cu semn
    def div_s(t1,t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) != 1: 
            return ERROR_TYPE_MISMATCH
        if (t2._val == 0):
            return ERROR_TYPE_DIVIDEBY0
        ans = i64(0)
        ans._val = (t1._val // t2._val)
        ans.check_overflow()
        return ans
    ### div_u - impartire fara semn
    def div_u(t1, t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) != 1: 
            return ERROR_TYPE_MISMATCH
        if (t2._val == 0):
            return ERROR_TYPE_DIVIDEBY0
        ans = i64(0)
        ans._val = (t1._val // t2._val)
        ans.check_overflow()
        ans._val = ans._val & BITMASK_64
        return ans
    def rem_s(t1, t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) != 1: 
            return ERROR_TYPE_MISMATCH
        if (t2._val == 0):
            return ERROR_TYPE_DIVIDEBY0
        ans = i64.div_s(t1,t2)
        ans._val = i64.mul(i64.sub(t1,ans),t2)
        return ans
    def rem_u(t1,t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) != 1: 
            return ERROR_TYPE_MISMATCH
        if (t2._val == 0):
            return ERROR_TYPE_DIVIDEBY0
        ans = i64.div_u(t1,t2)
        ans._val = i64.mul(i64.sub(t1,ans),t2)
        return ans
    def _and(t1,t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) != 1: 
            return ERROR_TYPE_MISMATCH
        ans = i64(t1._val & t2._val)
        return ans
    def _or(t1,t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) != 1: 
            return ERROR_TYPE_MISMATCH
        ans = i64(t1._val | t2._val)
        return ans
    def _xor(t1,t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) != 1: 
            return ERROR_TYPE_MISMATCH
        ans = i64(t1._val ^ t2._val)
        return ans
    def shl(t1, t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) !=1:
            return ERROR_TYPE_MISMATCH
        ans = i64(t1._val << t2._val)
        ans.check_overflow()
        return ans
    ### Nu stiu care e diferenta intre shift right signed si shift right unsigned, le fac la fel si le modifici tu cuz I really have no idea
    def shr_s(t1,t2):
        global OVERFLOW_FLAG
        OVERFLOW_FLAG = False
        if (isinstance(t1,i64) & isinstance(t2,i64)) !=1:
            return ERROR_TYPE_MISMATCH
        ans = i64(t1._val >> t2._val)
        return ans
    def shr_u(t1,t2):
        global OVERFLOW_FLAG
        OVERFLOW_FLAG = False
        if (isinstance(t1,i64) & isinstance(t2,i64)) !=1:
            return ERROR_TYPE_MISMATCH
        ans = i64(t1._val >> t2._val)
        return ans
    def rotl(t1,t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) !=1:
            return ERROR_TYPE_MISMATCH
        ans = i64(int(f"{t1._val:064b}"[t2._val:] + f"{t1._val:064b}"[:t2._val], 2))
        return ans
    def rotr(t1,t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) !=1:
            return ERROR_TYPE_MISMATCH
        ans = i64(int(f"{t1._val:064b}"[-t2._val:] + f"{t1._val:064b}"[:-t2._val], 2))
        return ans
    def clz(t1,t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) !=1:
            return ERROR_TYPE_MISMATCH
        base = 1 << 63
        t2._val = 0
        while(base & t1._val == 0 and base>=1):
            t2._val += 1
            base = base >> 1
    def ctz(t1,t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) !=1:
            return ERROR_TYPE_MISMATCH
        base = 1
        t2._val = 0
        while(base & t1._val == 0  and base<=(1<<63)):
            t2._val += 1
            base = base << 1
    def popcnt(t1, t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) !=1:
            return ERROR_TYPE_MISMATCH
        base = 1
        t2._val = 0
        while base<=(1<<63):
            if t1._val & base: t2._val+=1
            base = base << 1
    def extend8_s(t1):
        ans = i64(int.from_bytes(t1._val.to_bytes(1, 'little', signed=True), 'little', signed=True))
        return ans
    def extend16_s(t1):
        ans = i64(int.from_bytes(t1._val.to_bytes(2, 'little', signed=True), 'little', signed=True))
        return ans
    def extend32_s(t1):
        ans = i64(int.from_bytes(t1._val.to_bytes(4, 'little', signed=True), 'little', signed=True))
        return ans
    def eqz(t1):
        if isinstance(t1,i64) !=1:
            return ERROR_TYPE_MISMATCH
        if t1._val == 0: return i64(1)
        return i64(0)
    def eq(t1, t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) !=1:
            return ERROR_TYPE_MISMATCH
        if t1._val == t2._val: return i64(1)
        return i64(0)
    def ne(t1, t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) !=1:
            return ERROR_TYPE_MISMATCH
        if t1._val != t2._val: return i64(1)
        return i64(0)
    def lt_s(t1, t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) !=1:
            return ERROR_TYPE_MISMATCH
        if t1._val < t2._val: return i64(1)
        return i64(0)
    def lt_u(t1, t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) !=1:
            return ERROR_TYPE_MISMATCH
        if t1._val < 0 : comp1 = t1._val + 1<<64
        else: comp1 = t1._val
        if t2._val < 0 : comp2 = t2._val + 1<<64
        else: comp2 = t2._val
        if comp1 < comp2: return i64(1)
        return i64(0)
    def le_s(t1,t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) !=1:
            return ERROR_TYPE_MISMATCH
        return i64(i64._or(i64.eq(t1,t2),i64.lt_s(t1,t2)))
    def le_u(t1,t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) !=1:
            return ERROR_TYPE_MISMATCH
        return i64(i64._or(i64.eq(t1,t2),i64.lt_u(t1,t2)))
    def gt_s(t1,t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) !=1:
            return ERROR_TYPE_MISMATCH
        if t1._val > t2._val: return i64(1)
        return i64(0)
    def gt_u(t1, t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) !=1:
            return ERROR_TYPE_MISMATCH
        if t1._val < 0 : comp1 = t1._val + 1<<64
        else: comp1 = t1._val
        if t2._val < 0 : comp2 = t2._val + 1<<64
        else: comp2 = t2._val
        if comp1 > comp2: return i64(1)
        return i64(0)
    def ge_s(t1,t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) !=1:
            return ERROR_TYPE_MISMATCH
        return i64(i64._or(i64.eq(t1,t2),i64.gt_s(t1,t2)))
    def ge_u(t1,t2):
        if (isinstance(t1,i64) & isinstance(t2,i64)) !=1:
            return ERROR_TYPE_MISMATCH
        return i64(i64._or(i64.eq(t1,t2),i64.gt_u(t1,t2)))
    def __str__(self):
        return f"{self._val}"

#Faci teste

a = i64(-1)
b = i64(0)
c = i64.lt_u(b,a)
print(c)