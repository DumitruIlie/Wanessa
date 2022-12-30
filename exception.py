def NumberException(Exception):
	def __init__(self, text):
		self.text=text

	def __str__(self):
		return self.text

def StringException(Exception):
	def __init__(self, text):
		self.text=text

	def __str__(self):
		return self.text

def TypeMismatchException(Exception):
	def __init__(self, text):
		self.text=text

	def __str__(self):
		return self.text

def LogicException(Exception):
	def __init__(self, text):
		self.text=text

	def __str__(self):
		return self.text

def FormatException(Exception):
	def __init__(self, text):
		self.text=text

	def __str__(self):
		return self.text