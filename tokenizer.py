def listaTipuriTokene():
	return {
			#i think this is done
			"if":"keyword",\
			"then":"keyword",\
			"else":"keyword",\
			"select":"keyword",\
			"i32":"data type",\
			"(":"start",\
			")":"end",\
			"nan:canonical":"unexpected token",\
			"nan:arithmetic":"unexpected token",\
			"drop":"keyword",\
			"func":"keyword",\
			"param":"keyword",\
			"result":"keyword",\
			"export":"keyword",\
			"invoke":"keyword",\
			"call":"keyword",\
			"local.get":"keyword",\
			"local.set":"keyword",\
			"assert_return":"keyword",\
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
			"i64.const":"keyword",\
			"i64.add":"keyword",\
			"i64.sub":"keyword",\
			"i64.mul":"keyword",\
			"i64.div_s":"keyword",\
			"i64.div_u":"keyword",\
			"i64.rem_s":"keyword",\
			"i64.rem_u":"keyword",\
			"i64.and":"keyword",\
			"i64.or":"keyword",\
			"i64.xor":"keyword",\
			"i64.shl":"keyword",\
			"i64.shr_s":"keyword",\
			"i64.shr_u":"keyword",\
			"i64.rotl":"keyword",\
			"i64.rotr":"keyword",\
			"i64.clz":"keyword",\
			"i64.ctz":"keyword",\
			"i64.popcnt":"keyword",\
			"i64.extend8_s":"keyword",\
			"i64.extend16_s":"keyword",\
			"i64.eqz":"keyword",\
			"i64.eq":"keyword",\
			"i64.ne":"keyword",\
			"i64.lt_s":"keyword",\
			"i64.lt_u":"keyword",\
			"i64.le_s":"keyword",\
			"i64.le_u":"keyword",\
			"i64.gt_s":"keyword",\
			"i64.gt_u":"keyword",\
			"i64.ge_s":"keyword",\
			"i64.ge_u":"keyword",\
			"nop":"keyword",\
			"module":"keyword",\
			
			#working on
			
			#to do
			"assert_trap":"keyword",\
			"assert_invalid":"keyword",\
			"assert_malformed":"keyword",\
			
			#to find workaround
			"loop":"ignored",\
			"br":"ignored",\
			"br_if":"ignored",\
			"br_table":"ignored",\
			"return":"ignored",\
			"memory":"ignored",\
			
			#ASTEA TREBUIE SCOS INAINTE SA TRIMITEM PROIECTUL
			"print":"keyword",\
			"fulldrop":"keyword",\
			"leveldrop":"keyword"\
			}

#functie pentru ignorarea comentariilor si reformatarea codului original la anumite standarde
def reformat(code):
	#exista posibilitatea ca un comentariu sa fie scris intre ghilimele ceea ce il face sa nu mai fie un comentariu, asa ca trebuie sa fim atenti cu ele
	#comentariile par a incepe cu ;; si a se termina la sfarsitul liniei
	#pentru a face treaba mai usoara, modificam codul pentru a avea un spatiu inainte si dupa caracterele '(' si ')'.
	#si aici pot aparea probleme din cauza ghilimelelor
	for i in range(len(code)):
		j=0
		string=0
		aux=[]
		while j<len(code[i]):
			if code[i][j]=='\"':
				string=1-string
				aux.append(code[i][j])
			elif code[i][j]=='\\' and j+1<len(code[i]) and code[i][j+1]=='\"':
				aux.append(code[i][j])
				aux.append(code[i][j+1])
				j+=1
			elif code[i][j]==';' and j+1<len(code[i]) and code[i][j+1]==';' and string==0:
				break
			elif code[i][j]=='(' and string==0:
				aux.append(' ( ')
			elif code[i][j]==')' and string==0:
				aux.append(' ) ')
			else:
				aux.append(code[i][j])
			j+=1
		code[i]="".join(aux).strip('\n')
	#alipesc tot codul intr-un singur string, dar vreau sa stim in continuare faptul ca acolo se separa codul, iar pentru asta facem join cu un caracter spatiu
	code=" ".join(code)
	return code

#class Token, retine tipul de token si string-ul reprezentand 
class Token:
	def __init__(self, tokType, token):
		self.tokType=tokType
		self.token=token

	def __str__(self):
		return f"{{{self.tokType}, {self.token}}}"

#functie, primeste un string returneaza un Token ce reprezinta tipul stringului si stringul in sine
def getToken(s):
	tkType=listaTipuriTokene().get(s, "word")
	if tkType=="word":
		#tipuri aditionale, generale care nu pot fi reprezentate intr-un dictionar
		if s[0]=='$':
			tkType="alias"
		
		elif '0'<=s[0]<='9' or s[0]=='-' or s[0]=='+':
			aux=""
			if s[0]=='-' or s[0]=='+':
				aux=s[0]
				s=s[1:]
			tkType="number"
			if len(s)>2:
				#posibil hexa
				if s[1]=='x':
					for i in range(2, len(s)):
						if s[i] not in "0123456789abcdef_ABCDEF":
							s="unknown operator"
							break
				else:
					for i in range(1, len(s)):
						if s[i] not in "0123456789_":
							s="unknown operator"
							break
			elif len(s)==2 and not ('0'<=s[1]<='9'):
				s="unknown operator"
			if '0'<=s[0]<='9':
				s=aux+s
		
		elif s[0]=='\"':
			tkType="string"
	return Token(tkType, s)

class Tokenizer:
	def __init__(self, text):
		tokenTypes=listaTipuriTokene()
		curr=[]
		self.tokens=[]
		
		i=0
		while i<len(text):
			if text[i]==' ' or text[i]=='\t' or text[i]=='\n':
				if curr!=[]:
					self.tokens.append(getToken("".join(curr)))
					curr=[]
			elif text[i]=='\"':
				#string
				if curr==[]:
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
					if i==len(text) or text[i]==' ':
						tkType="string"
						self.tokens.append(Token(tkType, "".join(curr)))
						curr=[]
					else:
						curr=[]
						self.tokens.append(Token("number", "unknown operator"))
						while i<len(text):
							if text[i]==' ':
								break
							if text[i]=='\"':
								while i<len(text):
									if text[i]=='\\' and i+1<len(text) and text[i+1]=='\"':
										i+=1
									elif text[i]=='\"':
										i+=1
										break
									i+=1
							else:
								i+=1
				else:
					curr=[]
					self.tokens.append(Token("number", "unknown operator"))
					i+=1
					while i<len(text):
						if text[i]=='\\' and i+1<len(text) and text[i+1]=='\"':
							i+=1
						elif text[i]=='\"':
							i+=1
							break
						i+=1
					ok=(text[i]==' ')
					i+=1 if ok else 0
					while not ok and i<len(text):
						if text[i]==' ':
							ok=True
						elif text[i]=='\"':
							while i<len(text):
								if text[i]=='\\' and i+1<len(text) and text[i+1]=='\"':
									i+=1
								elif text[i]=='\"':
									i+=1
									break
								i+=1
			
			else:
				curr.append(text[i])
			
			i+=1
		if curr!=[]:
			curr="".join(curr)
			tkType=tokenTypes.get(curr, "Word")
			self.tokens.append(Token(tkType, curr))

	def __str__(self):
		return "\n".join([str(x) for x in self.tokens])