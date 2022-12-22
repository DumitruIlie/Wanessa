class wasmFunc:
	def __init__(self):
		self.params=dict()
		self.paramTypes=[]
		self.localVars=dict()
		self.localTypes=[]
		self.results=dict()
		self.name=""
		self.tokens=[]
		
	#aici setez parametri, returnType-urile si tokenele specifice
	def make(self, T, poz):
		if T[poz].token!='func':
			return -1
		poz+=1
		if T[poz].tokType!='start':
			return -1
		while T[poz].tokType=='start':
			poz+=1
			#nume
			if T[poz].token=='export':
				poz+=1
				self.name=T[poz].token.strip("\"")
				poz+=2
			#parametrii
			elif T[poz].token=='param':
				poz+=1
				while T[poz].tokType!='end':
					if T[poz].tokType=='alias':
						#parametru cu alias
						self.params[T[poz].token]=len(self.paramTypes)-1
						poz+=1
					self.paramTypes.append(T[poz].token)
					poz+=1
				poz+=1
			#variabile locale
			elif T[poz].token=='local':
				poz+=1
				while T[poz].tokType!='end':
					if T[poz].tokType=='alias':
						#parametru cu alias
						self.params[T[poz].token]=len(self.paramTypes)-1
						poz+=1
					self.paramTypes.append(T[poz].token)
					poz+=1
				poz+=1
			#results
			elif T[poz].token=='result':
				poz+=1
				while T[poz].tokType!='end':
					self.results[len(self.results)]=T[poz].token
					poz+=1
				poz+=1
			#tokene
			else:
				cntParant=1
				while poz<len(T):
					if cntParant==1 and T[poz].tokType=='end':
						return poz+1
					if T[poz].tokType=='start':
						cntParant+=1
					elif T[poz].tokType=='end':
						cntParant-=1
					self.tokens.append(T[poz])
					poz+=1
				return -1
		return -1