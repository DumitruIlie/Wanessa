import AST

class wasmFunc:
	def __init__(self):
		self.params=dict()
		self.paramTypes=[]
		self.localVars=dict()
		self.localTypes=[]
		self.results=[]
		self.name=""
		self.tokens=[]
		self.AST=None
		
	#aici setez parametri, returnType-urile si lista de tokene(instructiunile pe care le executa functia)
	def make(self, T, poz):
		if T[poz].token!='func':
			return -1
		poz+=1
		if T[poz].tokType!='start':
			return -1
		while T[poz].tokType=='start':
			poz+=1
			if T[poz].token=='export':
				#numele functiei, folosit la apel
				poz+=1
				self.name=T[poz].token.strip("\"")
				poz+=2
			
			elif T[poz].token=='param':
				#parametrii(tip si alias)
				poz+=1
				while T[poz].tokType!='end':
					if T[poz].tokType=='alias':
						#parametru cu alias
						self.params[T[poz].token]=len(self.paramTypes)
						poz+=1
					self.paramTypes.append(T[poz].token)
					poz+=1
				poz+=1
			
			elif T[poz].token=='local':
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
			
			elif T[poz].token=='result':
				#tip de return
				poz+=1
				while T[poz].tokType!='end':
					self.results[len(self.results)]=T[poz].token
					poz+=1
				poz+=1
			
			else:
				#instructiunile functiei, le stochez ca o lista ca sa pot folosi aceeasi functie de evaluare
				cntParant=1
				while poz<len(T):
					if cntParant==1 and T[poz].tokType=='end':
						#sfarsit corp functie
						self.params=dict()
						self.localVars=dict()
						self.AST=AST.makeAST(self.tokens)
						self.tokens=[]
						return poz+1
					
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
				return -1
			
		return -1