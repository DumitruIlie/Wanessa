def listaTipuriTokene():
	return {"i32":"data type",\
			"(":"start",\
			")":"end",\
			"i32.add":"keyword",\
			"func":"keyword",\
			"local.get":"keyword",\
			"param":"keyword",\
			"module":"keyword"}

#functie pentru ignorarea comentariilor si reformatarea codului original la anumite standarde
def reformat(code):
	#comentariile par a incepe cu ;; si a se termina la sfarsitul liniei
	for i in range(len(code)):
		cmnt=code[i].find(';;')
		if cmnt!=-1:
			code[i]=code[:cmnt]
	#pana aici sterg comentariile
	#alipesc tot codul intr-un singur string, dar vreau sa stim in continuare faptul ca acolo se separa codul, iar pentru asta facem join cu un caracter spatiu
	code=[c for c in code if c!=[]]
	code=" ".join(code)
	#pentru a face treaba mai usoara, modificam codul pentru a avea un spatiu inainte si dupa caracterele '(' si ')'.
	code=code.replace('(', ' ( ').replace(')', ' ) ')
	return code

#class Token, retine tipul de token si string-ul reprezentand 
class Token:
	def __init__(self, tokType, token):
		self.tokType=tokType
		self.token=token

	def __str__(self):
		return f"{{{self.tokType}, {self.token}}}"

class Tokenizer:
	def __init__(self, text, tokenTypes):
		curr=[]
		self.tokens=[]
		
		for i in range(len(text)):
			if text[i]==' ' or text[i]=='\t' or text[i]=='\n':
				if curr!=[]:
					curr="".join(curr)
					tkType=tokenTypes.get(curr, "word")
					
					if tkType=="word":
						#tipuri aditionale, mai greu de facut intr-un dictionar
						if curr[0]=='$':
							tkType="alias"
						elif '0'<=curr[0]<='9':
							tkType="number"
						#de facut: string-uri si (poate) alte chestii daca mai apar
					
					self.tokens.append(Token(tkType, curr))
					curr=[]
			else:
				curr.append(text[i])
				
		if curr!=[]:
			curr="".join(curr)
			tkType=tokenTypes.get(curr, "Word")
			self.tokens.append(Token(tkType, curr))

	def __str__(self):
		return "\n".join([str(x) for x in self.tokens])