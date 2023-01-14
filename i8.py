class i8:
	def __init__(self, val):
		self._val = (val%256+256)%256
		if self._val>127:
			self._val-=256
	def __str__(self):
		return f"{self._val}"