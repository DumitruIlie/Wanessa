import i64
ERROR_TYPE_MISMATCH = "TYPE MISMATCH"
ERROR_TYPE_DIVIDEBY0 = "INTEGER DIVIDE BY ZERO"
ERROR_TYPE_OVERFLOW = "INTEGER OVERFLOW"
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
        if (t1._val == -2_147_483_648 and t2._val == -1):
            return ERROR_TYPE_OVERFLOW
        ans = i32(0)
        semn=(t1._val>=0)^(t2._val>0)
        ans._val = (abs(t1._val) // abs(t2._val))
        if semn:
            ans._val=-ans._val
        ans.check_overflow()
        return ans
    ### div_u - impartire fara semn
    def div_u(t1, t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) != 1: 
            return ERROR_TYPE_MISMATCH
        if (t2._val == 0):
            return ERROR_TYPE_DIVIDEBY0
        
        x1=t1._val
        if x1<0:
            x1+=2_147_483_648*2
        x2=t2._val
        if x2<0:
            x2+=2_147_483_648*2
        
        ans = i32(0)
        ans._val = (x1 // x2)
        ans.check_overflow()
        ans._val = ans._val & BITMASK_32
        return ans
    def rem_s(t1, t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) != 1: 
            return ERROR_TYPE_MISMATCH
        if (t2._val == 0):
            return ERROR_TYPE_DIVIDEBY0
        if (t1._val == -2_147_483_648 and t2._val == -1):
            return i32(0)
        ans = i32.div_s(t1,t2)
        ans = i32.sub(t1, i32.mul(ans, t2)) # t1 - ans * t2
        return ans
    def rem_u(t1,t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) != 1: 
            return ERROR_TYPE_MISMATCH
        if (t2._val == 0):
            return ERROR_TYPE_DIVIDEBY0
        ans = i32.div_u(t1,t2)
        ans = i32.sub(t1, i32.mul(ans, t2)) # t1 - ans * t2
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
        x=(t2._val%32+32)%32
        ans = i32(t1._val << x)
        ans.check_overflow()
        return ans
    ### Nu stiu care e diferenta intre shift right signed si shift right unsigned, le fac la fel si le modifici tu cuz I really have no idea
    def shr_s(t1,t2):
        global OVERFLOW_FLAG
        OVERFLOW_FLAG = False
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        x=(t2._val%32+32)%32
        y=t1._val
        if sign:=(y<0):
            y+=2_147_483_648*2
        ans=~((1<<(32-x))-1)*int(sign)
        ans=i32(ans|(y>>x))
        return ans
    def shr_u(t1,t2):
        global OVERFLOW_FLAG
        OVERFLOW_FLAG = False
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        x=(t2._val%32+32)%32
        y=t1._val
        if y<0:
            y+=2_147_483_648*2
        ans=i32(y>>x)
        return ans
    def rotl(t1,t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        x=(t2._val%32+32)%32
        up=i32.shl(t1, i32(x))
        down=i32.shr_u(t1, i32((32-x)%32))
        ans = i32._or(up, down)
        return ans
    def rotr(t1,t2):
        return i32.rotl(t1, i32(-t2._val))
    def clz(t1):
        if isinstance(t1,i32) !=1:
            return ERROR_TYPE_MISMATCH
        base = 1 << 31
        ans = i32(0)
        while(base & t1._val == 0 and base>=1):
            ans._val += 1
            base = base >> 1
        return ans
    def ctz(t1):
        if isinstance(t1,i32) !=1:
            return ERROR_TYPE_MISMATCH
        base = 1
        ans = i32(0)
        while(base & t1._val == 0  and base<=(1<<31)):
            ans._val += 1
            base = base << 1
        return ans
    def popcnt(t1):
        if isinstance(t1,i32) !=1:
            return ERROR_TYPE_MISMATCH
        x=t1._val
        if x<0:
            x+=2_147_483_648*2
        ans = 0
        while x:
            ans+=1
            x-=(x & -x)
        return i32(ans)
    def extend8_s(t1):
        x=t1._val
        x&=0xff
        if x>=0x80:
            x-=256
        return i32(x)
    def extend16_s(t1):
        x=t1._val
        x&=0xffff
        if x>=0x8000:
            x-=0x10000
        return i32(x)
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
        comp1=t1._val
        if t1._val<0: comp1 = t1._val + 2_147_483_648*2
        comp2=t2._val
        if t2._val<0: comp2 = t2._val + 2_147_483_648*2
        if comp1 < comp2: return i32(1)
        return i32(0)
    def le_s(t1,t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        return i32._or(i32.eq(t1,t2),i32.lt_s(t1,t2))
    def le_u(t1,t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        return i32._or(i32.eq(t1,t2),i32.lt_u(t1,t2))
    def gt_s(t1,t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        if t1._val > t2._val: return i32(1)
        return i32(0)
    def gt_u(t1, t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        if t1._val < 0 : comp1 = t1._val + 2_147_483_648*2
        else: comp1 = t1._val
        if t2._val < 0 : comp2 = t2._val + 2_147_483_648*2
        else: comp2 = t2._val
        if comp1 > comp2: return i32(1)
        return i32(0)
    def ge_s(t1,t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        return i32._or(i32.eq(t1,t2),i32.gt_s(t1,t2))
    def ge_u(t1,t2):
        if (isinstance(t1,i32) & isinstance(t2,i32)) !=1:
            return ERROR_TYPE_MISMATCH
        return i32._or(i32.eq(t1,t2),i32.gt_u(t1,t2))
    def wrap_i64(t1):
        if not isinstance((t1,i64)):
            return ERROR_TYPE_MISMATCH
        ans = i32(t1)
        return ans
    def __str__(self):
        return f"{self._val}"