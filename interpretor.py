import tokenizer
import wasmFunc
StivaProgram=[]
variabileLocale=[]
functiiWasm=dict()

#initializeaza stiva programului
def initStiva():
	global StivaProgram
	StivaProgram=[]

#adauga pe stiva un element
def pushStiva(x):
	StivaProgram.append(x)

#scoate si returneaza ultimul obiect de pe stiva
def popStiva():
	return StivaProgram.pop()

#functie de test, adauga 2 i32 de pe stiva pe stiva
def i32add():
	x=popStiva()
	y=popStiva()
	#trebuie facuta modificare ca sa mearga cu i32, dar facem clasa cred si iese usor cu operator overloading
	pushStiva(x+y)

#numere in baza 10 si 16
def wasmEvalNumar(T, poz):
	t=T[poz].token
	if T[poz].tokType=="start":
		poz=wasmEval(T, poz+1)
		x=popStiva()
		return (x, poz)
	sign=1
	if t[0]=='-':
		sign=-1
		t=t[1:]
	if len(t)<3:
		#baza 10 sigur
		return (int(t)*sign, poz+1)
	if t[1]=='x':
		#baza 16
		x=0
		for i in range(2, len(t)):
			if '0'<=t[i]<='9':
				x=x*16+ord(t[i])-ord('0')
			elif 'a'<=t[i]<='f':
				x=x*16+10+ord(t[i])-ord('a')
			else:
				return f"Number error, {T[poz].token} is not OK."
		return (x*sign, poz+1)
	return (int(t)*sign, poz+1)

#functie pentru incarcarea parametrilor si "apel" functieWasm
def wasmEvalFunc(T, poz, F):
	variabileLocale.append([])
	while len(variabileLocale[-1])<len(F.paramTypes):
		x=wasmEvalNumar(T, poz)
		poz=x[1]
		variabileLocale[-1].append(x[0])
	#trebuie modificat aici cu tipurile de date din variabilele locale ale functiei
	variabileLocale[-1].extend([0]*len(F.localTypes))
	return wasmEval(F.tokens)

#keywords
def wasmEvalKeyword(T, poz):
	global variabileLocale
	t=T[poz]
	#verific care tip de keyword este ca sa stiu cum sa continui
	if t.token=="local.get":
		x=wasmEvalNumar(T, poz+1)
		poz=x[1]
		pushStiva(variabileLocale[-1][x[0]])
		return poz
	if t.token[:3]=="i32":
		#o functie aplicata pe i32
		#va trebui modificat astfel incat sa poata face toate functiile respective, pentru moment nu avem decat add deci folosim o implementare simpla
		x=wasmEvalNumar(T, poz+1)
		y=wasmEvalNumar(T, x[1])
		pushStiva(x[0]+y[0])
		return y[1]
	if t.token=="func":
		#definire functie
		F=wasmFunc.wasmFunc()
		poz=F.make(T, poz)
		functiiWasm[F.name]=F
		return poz
	if t.token=="invoke":
		#apel functie
		poz+=1
		F=functiiWasm[T[poz].token.strip("\"")]
		poz+=1
		poz=wasmEvalFunc(T, poz, F)
		return poz
	return poz+1

#functia generala a interpretorului T este lista de tokene, iar poz este pozitia de la care se incepe
def wasmEval(T, poz=0):
	while poz<len(T):
		t=T[poz]
		print(f"Eval {T[poz]}")
		if t.tokType=="start":
			poz=wasmEval(T, poz+1)
			if poz==-1:
				return -1
		elif t.tokType=="end":
			return poz+1
		elif t.tokType=="number":
			x=wasmEvalNumar(T, poz)
			poz=x[1]
			pushStiva(x[0])
		elif t.tokType=="keyword":
			poz=wasmEvalKeyword(T, poz)
		else:
			poz+=1
	return -1

#functia generala, se apeleaza o data pentru un text/cod sursa.
def interpret(code):
	initStiva()
	T=tokenizer.Tokenizer(code, tokenizer.listaTipuriTokene())
	wasmEval(T.tokens)
	print(StivaProgram)