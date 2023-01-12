import tokenizer

class AST:
	def __init__(self):
		self.children=[]
		self.correct=True
		self.assertCorrect=True
		self.assertError=""
	
	def myStr(self, indentCnt):
		if not self.correct:
			if self.assertError!="":
				return self.assertError
			return "Not correct"
		return ' '*indentCnt+'(\n'+"\n".join([(x.myStr(indentCnt+1) if isinstance(x, AST) else (' '*(indentCnt+1))+str(x)) for x in self.children])+'\n'+' '*indentCnt+')'
	
	def __str__(self):
		return self.myStr(0)
	
	def make(self, tokens, pozStart, pozEnd, paranthesis):
		self.children=[]
		self.correct=True
		self.assertError=""
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
					self.assertCorrect=False
					self.assertError="expected )"
					self.children=[]
					break
				A=AST()
				A.make(tokens, i+1, j-2, paranthesis)
				self.children.append(A)
				if not A.correct:
					if not A.assertCorrect:
						self.assertCorrect=False
						self.assertError=A.assertError
						self.correct=False
						self.children=[]
						break
					if isinstance(self.children[0], AST) or self.children[0].token!="assert_malformed":
						self.correct=False
						self.assertError=A.assertError
						self.children=[]
						break
				i=j
			elif tokens[i].tokType=="number" and tokens[i].token=="unknown operator":
				self.children=[]
				self.correct=False
				self.assertError="\"unknown operator\""
				break
			else:
				self.children.append(tokens[i])
				i+=1
		if len(self.children)==1 and isinstance(self.children[0], AST):
			self.children=self.children[0].children
	
	def toTokenList(self):
		tokens=[tokenizer.getToken('(')]
		for child in self.children:
			if isinstance(child, AST):
				tokens.extend(child.toTokenList())
			else:
				tokens.append(child)
		tokens.append(tokenizer.getToken(')'))
		return tokens

def makeAST(tokens):
	A=AST()
	paranthesis=[-1]*len(tokens)
	st=[]
	for i in range(len(tokens)-1, -1, -1):
		if tokens[i].tokType=="end":
			st.append(i)
		elif tokens[i].tokType=="start":
			if len(st):
				paranthesis[i]=st.pop()
			else:
				return "missing matching )"
	if len(st):
		return "missing matching ("
	A.make(tokens, 0, len(tokens)-1, paranthesis)
	return A