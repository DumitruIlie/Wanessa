import tokenizer

class AST:
	def __init__(self):
		self.children=[]
		self.correct=True
	
	def myStr(self, indentCnt):
		if not self.correct:
			return "Not correct"
		return '\t'*indentCnt+'(\n'+"\n".join([(x.myStr(indentCnt+1) if isinstance(x, AST) else ('\t'*(indentCnt+1))+str(x)) for x in self.children])+'\n'+'\t'*indentCnt+')'
	
	def __str__(self):
		return self.myStr(0)
	
	def make(self, tokens, pozStart, pozEnd):
		self.children=[]
		self.correct=True
		i=pozStart
		while i<=pozEnd:
			if tokens[i].tokType=="start":
				j=i+1
				countPrnt=1
				while j<=pozEnd and countPrnt:
					if tokens[j].tokType=="end":
						countPrnt-=1
					elif tokens[j].tokType=="start":
						countPrnt+=1
					j+=1
				if countPrnt:
					self.correct=False
					self.children=[]
					break
				A=AST()
				A.make(tokens, i+1, j-2)
				if not A.correct:
					self.correct=False
					self.children=[]
					break
				self.children.append(A)
				i=j
			else:
				self.children.append(tokens[i])
				i+=1
		if len(self.children)==1 and isinstance(self.children[0], AST):
			self.children=self.children[0].children
	
	def toTokenList(self):
		tokens=[]
		for child in self.children:
			tokens.extend(child.toTokenList() if isinstance(child, AST) else [child])
		return tokens

def makeAST(tokens):
	A=AST()
	A.make(tokens, 0, len(tokens)-1)
	return A