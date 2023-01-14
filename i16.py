import i8
ERROR_TYPE_MISMATCH = "TYPE MISMATCH"

class i16:
	def __init__(self, val):
		self._val = val
	def __str__(self):
		return f"{self._val}"
	def add_s(t1, t2):
		if type(t1)!=type(t2):
			return ERROR_TYPE_MISMATCH
		if not isinstance(t1, i16):
			if isinstance(t1, i8.i8):
				t1=i16(t1._val)
			else:
				return ERROR_TYPE_MISMATCH
		if not isinstance(t2, i16):
			if isinstance(t2, i8.i8):
				t2=i16(t2._val)
			else:
				return ERROR_TYPE_MISMATCH
		ans=i16(t1._val+t2._val)
		ans._val=(ans._val%65536+65536)%65536
		if ans._val>32767:
			ans._val-=65536
		return ans
	def add_u(t1, t2):
		if type(t1)!=type(t2):
			return ERROR_TYPE_MISMATCH
		if not isinstance(t1, i16):
			if isinstance(t1, i8.i8):
				t1=i16(t1._val)
			else:
				return ERROR_TYPE_MISMATCH
		if not isinstance(t2, i16):
			if isinstance(t2, i8.i8):
				t2=i16(t2._val)
			else:
				return ERROR_TYPE_MISMATCH
		ans=i16(t1._val+t2._val)
		ans._val=(ans._val%65536+65536)%65536
		if ans._val>65535:
			ans._val-=65536
		return ans