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
        global OVERFLOW_FLAG
        OVERFLOW_FLAG = False  
        self._val = val
        self.check_overflow()
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
    def rem_s(t1, t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) != 1: 
            return ERROR_TYPE_MISMATCH
        if (t2._val == 0):
            return ERROR_TYPE_DIVIDEBY0
        ans = i32(i32.div_s(t1,t2))
        ans._val = i32.mul(i32.sub(t1,ans),t2)
        return ans
    def rem_u(t1,t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) != 1: 
            return ERROR_TYPE_MISMATCH
        if (t2._val == 0):
            return ERROR_TYPE_DIVIDEBY0
        ans = i32(i32.div_u(t1,t2))
        ans._val = i32.mul(i32.sub(t1,ans),t2)
        return ans
    def _and(t1,t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) != 1: 
            return ERROR_TYPE_MISMATCH
        ans = i32(t1._val & t2._val)
        return ans
    def _or(t1,t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) != 1: 
            return ERROR_TYPE_MISMATCH
        ans = i32(t1._val | t2._val)
        return ans
    def _xor(t1,t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) != 1: 
            return ERROR_TYPE_MISMATCH
        ans = i32(t1._val ^ t2._val)
        return ans
    def shl(t1, t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        ans = i32(t1._val >> t2._val)
        return ans
    ### Nu stiu care e diferenta intre shift right signed si shift right unsigned, le fac la fel si le modifici tu cuz I really have no idea
    def shr_s(t1,t2):
        global OVERFLOW_FLAG
        OVERFLOW_FLAG = False
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        ans = i32(t1._val << t2._val)
        ans.check_overflow()
        return ans
    def shr_u(t1,t2):
        global OVERFLOW_FLAG
        OVERFLOW_FLAG = False
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        ans = i32(t1._val << t2._val)
        ans.check_overflow()
        return ans
    def rotl(t1,t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        ans = i32(int(f"{t1._val:032b}"[t2._val:] + f"{t1._val:032b}"[:t2._val], 2))
        return ans
    def rotr(t1,t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        ans = i32(int(f"{t1._val:032b}"[-t2._val:] + f"{t1._val:032b}"[:-t2._val], 2))
        return ans
    def clz(t1,t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        base = 1 << 31
        t2._val = 0
        while(base & t1._val == 0 and base>=1):
            t2._val += 1
            base = base >> 1
    def ctz(t1,t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        base = 1
        t2._val = 0
        while(base & t1._val == 0  and base<=(1<<31)):
            t2._val += 1
            base = base << 1
    def popcnt(t1, t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        base = 1
        t2._val = 0
        while base<=(1<<31):
            if t1._val & base: t2._val+=1
            base = base << 1
    ### Nu inteleg extend-urile le las pt mai incolo ca sa le termin pe restul
    def eqz(t1):
        if isinstance(t1,i32) !=1:
            return ERROR_TYPE_MISMATCH
        if t1._val == 0: return i32(1)
        return i32(0)
    def eq(t1, t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        if t1._val == t2._val: return i32(1)
        return i32(0)
    def ne(t1, t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        if t1._val != t2._val: return i32(1)
        return i32(0)
    def lt_s(t1, t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        if t1._val < t2._val: return i32(1)
        return i32(0)
    def lt_u(t1, t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        if t1._val < 0 : comp1 = t1._val + 1<<32
        else: comp1 = t1._val
        if t2._val < 0 : comp2 = t2._val + 1<<32
        else: comp2 = t2._val
        if comp1 < comp2: return i32(1)
        return i32(0)
    def le_s(t1,t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        return i32(i32._or(i32.eq(t1,t2),i32.lt_s(t1,t2)))
    def le_u(t1,t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        return i32(i32._or(i32.eq(t1,t2),i32.lt_u(t1,t2)))
    def gt_s(t1,t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        if t1._val > t2._val: return i32(1)
        return i32(0)
    def gt_u(t1, t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        if t1._val < 0 : comp1 = t1._val + 1<<32
        else: comp1 = t1._val
        if t2._val < 0 : comp2 = t2._val + 1<<32
        else: comp2 = t2._val
        if comp1 > comp2: return i32(1)
        return i32(0)
    def ge_s(t1,t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        return i32(i32._or(i32.eq(t1,t2),i32.gt_s(t1,t2)))
    def ge_u(t1,t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        return i32(i32._or(i32.eq(t1,t2),i32.gt_u(t1,t2)))
    def __str__(self):
        return f"{self._val}"

#Faci teste

a = i32(-1)
b = i32(0)
c = i32.lt_u(b,a)
print(c)