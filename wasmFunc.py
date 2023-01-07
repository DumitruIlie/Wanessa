import AST
import tokenizer

class wasmFunc:
	def __init__(self):
		self.params=dict()
		self.paramTypes=[]
		self.localVars=dict()
		self.localTypes=[]
		self.results=[]
		self.invokeName=""
		self.callName=""
		self.tokens=[]
		self.AST=None
		
	#aici setez parametri, returnType-urile si lista de tokene(instructiunile pe care le executa functia)
	def make(self, T):
		poz=0
		while T[poz].tokType=='start':
			poz+=1
		if T[poz].token!='func':
			return ""
		poz+=1
		if T[poz].tokType=="alias":
			self.callName=T[poz].token
			poz+=1
		if poz>=len(T) or T[poz].tokType=='end':
			return ""
		if T[poz].tokType!='start':
			return f"unexpected {T[poz].token} in function declaration"
		
		poz+=1
		if T[poz].token=='export':
			poz+=1
			self.invokeName=T[poz].token
			poz+=3
		
		if poz>=len(T):
			return ""
		while T[poz].token=='param':
			#parametrii(tip si alias)
			poz+=1
			while T[poz].tokType!='end':
				if T[poz].tokType=='alias':
					#parametru cu alias
					self.params[T[poz].token]=len(self.paramTypes)
					poz+=1
				self.paramTypes.append(T[poz].token)
				poz+=1
			poz+=2
			if poz>=len(T):
				self.params=dict()
				return ""
		
		if T[poz].token=='result':
			#tip de return
			poz+=1
			while T[poz].tokType!='end':
				self.results.append(T[poz].token)
				poz+=1
			poz+=1
		
		
		if poz>=len(T):
			self.params=dict()
			self.localVars=dict()
			return ""
		
		if T[poz].token=='local' or (T[poz].tokType=='start' and T[poz+1].token=="local"):
			if T[poz].token!='local':
				poz+=1
			#variabile locale(tip si alias)
			poz+=1
			while T[poz].tokType!='end':
				if T[poz].tokType=='alias':
					#variabila locala cu alias
					self.localVars[T[poz].token]=len(self.paramTypes)+len(self.localTypes)
					poz+=1
				self.localTypes.append(T[poz].token)
				poz+=1
			poz+=1
		
		if poz>=len(T):
			self.params=dict()
			self.localVars=dict()
			return ""
		
		#instructiunile functiei, le stochez ca o lista si le transform in AST dupa
		cntParant=1
		self.tokens=[tokenizer.getToken('(')]
		while poz<len(T):
			if cntParant==1 and T[poz].tokType=='end':
				#sfarsit corp functie
				self.params=dict()
				self.localVars=dict()
				self.tokens.append(T[poz])
				self.AST=AST.makeAST(self.tokens)
				self.tokens=[]
				return ""
			
			if T[poz].tokType=='start':
				cntParant+=1
			elif T[poz].tokType=='end':
				cntParant-=1
			if T[poz].tokType=='alias' and T[poz].token in self.params:
				self.tokens.append(tokenizer.getToken(str(self.params[T[poz].token])))
			elif T[poz].tokType=='alias' and T[poz].token in self.localVars:
				self.tokens.append(tokenizer.getToken(str(self.localVars[T[poz].token])))
			else:
				self.tokens.append(T[poz])
			poz+=1
		
		#am epuizat lista de tokene dar nu am incheiat corpul functiei, eroare de sintaxa, lipseste )
		self.params=dict()
		self.paramTypes=[]
		self.localVars=dict()
		self.localTypes=[]
		self.tokens=[]
		self.invokeName=""
		self.callName=""
		self.result=[]
		return "expected ) after function implementation"