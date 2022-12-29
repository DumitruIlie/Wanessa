def listaTipuriTokene():
	return {"i32":"data type",\
			"(":"start",\
			")":"end",\
			"drop":"keyword",\
			"func":"keyword",\
			"param":"keyword",\
			"export":"keyword",\
			"invoke":"keyword",\
			"call":"keyword",\
			"local.get":"keyword",\
			"assert_return":"keyword",\
			"assert_trap":"keyword",\
			"assert_invalid":"keyword",\
			"assert_malformed":"keyword",\
			"i32.const":"keyword",\
			"i32.add":"keyword",\
			"i32.sub":"keyword",\
			"i32.mul":"keyword",\
			"i32.div_s":"keyword",\
			"i32.div_u":"keyword",\
			"i32.rem_s":"keyword",\
			"i32.rem_u":"keyword",\
			"i32.and":"keyword",\
			"i32.or":"keyword",\
			"i32.xor":"keyword",\
			"i32.shl":"keyword",\
			"i32.shr_s":"keyword",\
			"i32.shr_u":"keyword",\
			"i32.rotl":"keyword",\
			"i32.rotr":"keyword",\
			"i32.clz":"keyword",\
			"i32.ctz":"keyword",\
			"i32.popcnt":"keyword",\
			"i32.extend8_s":"keyword",\
			"i32.extend16_s":"keyword",\
			"i32.eqz":"keyword",\
			"i32.eq":"keyword",\
			"i32.ne":"keyword",\
			"i32.lt_s":"keyword",\
			"i32.lt_u":"keyword",\
			"i32.le_s":"keyword",\
			"i32.le_u":"keyword",\
			"i32.gt_s":"keyword",\
			"i32.gt_u":"keyword",\
			"i32.ge_s":"keyword",\
			"i32.ge_u":"keyword",\
			"module":"keyword"}

#functie pentru ignorarea comentariilor si reformatarea codului original la anumite standarde
def reformat(code):
	#exista posibilitatea ca un comentariu sa fie scris intre ghilimele ceea ce il face sa nu mai fie un comentariu, asa ca trebuie sa fim atenti cu ele
	#comentariile par a incepe cu ;; si a se termina la sfarsitul liniei
	for i in range(len(code)):
		j=0
		string=0
		while j<len(code[i]):
			if code[i][j]=='\"':
				string=1-string
			elif code[i][j]=='\\' and j+1<len(code[i]) and code[i][j+1]=='\"':
				j+=1
			elif code[i][j]==';' and j+1<len(code[i]) and code[i][j+1]==';' and string==0:
				code[i]=code[i][:j]
				break
			j+=1
		if len(code[i])==0:
			code[i]=""
	#pana aici sterg comentariile
	#alipesc tot codul intr-un singur string, dar vreau sa stim in continuare faptul ca acolo se separa codul, iar pentru asta facem join cu un caracter spatiu
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
	def __init__(self, text):
		tokenTypes=listaTipuriTokene()
		curr=[]
		self.tokens=[]
		
		i=0
		while i<len(text):
			if text[i]==' ' or text[i]=='\t' or text[i]=='\n':
				if curr!=[]:
					curr="".join(curr)
					tkType=tokenTypes.get(curr, "word")
					
					if tkType=="word":
						#tipuri aditionale, generale care nu pot fi reprezentate intr-un dictionar
						if curr[0]=='$':
							tkType="alias"
						elif '0'<=curr[0]<='9' or curr[0]=='-':
							tkType="number"
						elif curr[0]=='\"':
							tkType="string"
					
					self.tokens.append(Token(tkType, curr))
					curr=[]
			elif text[i]=='\"':
				#string
				curr=[text[i]]
				i+=1
				while i<len(text):
					if text[i]=='\\' and i+1<len(text) and text[i+1]=='\"':
						curr.append(text[i])
						i+=1
					elif text[i]=='\"':
						curr.append(text[i])
						i+=1
						break
					curr.append(text[i])
					i+=1
				tkType="string"
				self.tokens.append(Token(tkType, "".join(curr)))
				curr=[]
			
			else:
				curr.append(text[i])
			
			i+=1
		if curr!=[]:
			curr="".join(curr)
			tkType=tokenTypes.get(curr, "Word")
			self.tokens.append(Token(tkType, curr))

	def __str__(self):
		return "\n".join([str(x) for x in self.tokens])