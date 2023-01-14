from v128 import v128
import i16
import i8

class i16x8:
	def __init__(self):
		#???
		self._x = 0
	def extadd_pairwise_i8x16_s(t):
		if not isinstance(t, v128) or len(t._val)!=16:
			return "type mismatch"
		for i in t._val:
			if not isinstance(i, i8.i8):
				return "type mismatch"
		list_zero=[0]*8
		ans=v128(list_zero)
		for i in range(8):
			ans._val[i]=i16.i16.add_s(t._val[i*2], t._val[i*2+1])
		return ans
	def extadd_pairwise_i8x16_u(t):
		if not isinstance(t, v128) or len(t._val)!=16:
			return "type mismatch"
		for i in t._val:
			if not isinstance(i, i8.i8):
				return "type mismatch"
		list_zero=[0]*8
		ans=v128(list_zero)
		for i in range(8):
			ans._val[i]=i16.i16.add_u(i16.i16((t._val[i*2]._val+256)%256), i16.i16((t._val[i*2+1]._val+256)%256))
		return ans