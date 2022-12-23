import tokenizer
import wasmFunc
import i32
wasmStack=[]
variabileLocale=[]
aliasVariabileLocale=[]
functiiWasm=dict()
aritateFunctii={"i32.add":2, "i32.sub":2, "i32.mul":2, "i32.div_s":2, "i32.div_u":2, "i32.rem_s":2, "i32.rem_u":2, "i32.and":2, "i32.or":2, "i32.xor":2, "i32.shl":2, "i32.shr_s":2, "i32.shr_u":2, "i32.rotl":2, "i32.rotr":2,\
				"i32.clz":1, "i32.ctz":1, "i32.popcnt":1, "i32.extend8_s":1, "i32.extend16_s":1, "i32.eqz":1, "i32.eq":2, "i32.ne":2, "i32.lt_s":2, "i32.lt_u":2, "i32.le_s":2, "i32.le_u":2, "i32.gt_s":2, "i32.gt_u":2, "i32.ge_s":2, "ge_u":2}
functiiBaza={"i32.add":i32.i32.add, "i32.sub":i32.i32.sub, "i32.mul":i32.i32.mul, "i32.div_s":i32.i32.div_s, "i32.div_u":i32.i32.div_u, "i32.rem_s":i32.i32.rem_s, "i32.rem_u":i32.i32.rem_u, "i32.and":i32.i32._and, "i32.or":i32.i32._or, "i32.xor":i32.i32._xor}#, "i32.shl":i32.i32.shl, "i32.shr_s":i32.i32.shr_s, "i32.shr_u":i32.i32.shr_u, "i32.rotl":i32.i32.rotl, "i32.rotr":i32.i32.rotr,\
#				"i32.clz":i32.i32.clz, "i32.ctz":i32.i32.ctz, "i32.popcnt":i32.i32.popcnt, "i32.extend8_s":i32.i32.extend8_s, "i32.extend16_s":i32.i32.extend16_s, "i32.eqz":i32.i32.eqz, "i32.eq":i32.i32.eq, "i32.ne":i32.i32.ne, "i32.lt_s":i32.i32.lt_s, "i32.lt_u":i32.i32.lt_u, "i32.le_s":i32.i32.le_s, "i32.le_u":i32.i32.le_u, "i32.gt_s":i32.i32.gt_s, "i32.gt_u":i32.i32.gt_u, "i32.ge_s":i32.i32.ge_s, "ge_u":i32.i32.ge_u}

#initializeaza stiva programului
def initWasm():
	global wasmStack, veriabileLocale, functiiWasm
	wasmStack=[]
	variabileLocale=[]
	functiiWasm=dict()

#adauga pe stiva un element
def wasmPush(x):
	wasmStack.append(x)

#scoate si returneaza ultimul obiect de pe stiva
def wasmPop():
	return wasmStack.pop()

#numere in baza 10 si 16
#va trebui modificat cand integram si i64
def wasmEvalNumar(T, poz):
	t=T[poz].token
	if T[poz].tokType=="start":
		poz=wasmEval(T, poz+1)
		x=wasmPop()
		return (x, poz)
	sign=1
	if t[0]=='-':
		sign=-1
		t=t[1:]
	if len(t)<3:
		#baza 10 sigur
		return (i32.i32(int(t)*sign), poz+1)
	if t[1]=='x' or t[1]=='X':
		#baza 16
		x=0
		for i in range(2, len(t)):
			if '0'<=t[i]<='9':
				x=x*16+ord(t[i])-ord('0')
			elif 'a'<=t[i]<='f':
				x=x*16+10+ord(t[i])-ord('a')
			elif 'A'<=t[i]<='F':
				x=x*16+10+ord(t[i])-ord('A')
			else:
				return f"Number error, {T[poz].token} is not OK."
		return (i32.i32(x*sign), poz+1)
	return (i32.i32(int(t)*sign), poz+1)

#functie pentru incarcarea parametrilor si "apel" functieWasm
def wasmEvalFunc(T, poz, F):
	variabileLocale.append([])
	aliasVariabileLocale.append(F.params)
	while len(variabileLocale[-1])<len(F.paramTypes):
		x=wasmEvalNumar(T, poz)
		poz=x[1]
		variabileLocale[-1].append(x[0])
	#trebuie modificat aici cu tipurile de date din variabilele locale ale functiei
	variabileLocale[-1].extend([i32.i32(0)]*len(F.localTypes))
	wasmEval(F.tokens, 0)
	aliasVariabileLocale.pop()
	variabileLocale.pop()
	return poz

#keywords
def wasmEvalKeyword(T, poz):
	global variabileLocale
	t=T[poz]
	#verific care tip de keyword este ca sa stiu cum sa continui
	if t.token=="local.get":
		#alias sau numar
		poz+=1
		if T[poz].tokType=="alias":
			x=aliasVariabileLocale[-1][T[poz].token]
			poz+=1
			wasmPush(variabileLocale[-1][x])
		else:
			x=wasmEvalNumar(T, poz)
			poz=x[1]
			wasmPush(variabileLocale[-1][x[0]])
		return poz
	
	if t.token=="func":
		#definire functie
		F=wasmFunc.wasmFunc()
		poz=F.make(T, poz)
		functiiWasm[F.name]=F
		return poz
	
	if t.token=="invoke":
		#apel functie
		poz+=1
		F=functiiWasm[T[poz].token.strip('\"')]
		poz+=1
		poz=wasmEvalFunc(T, poz, F)
		return poz
	
	if t.token=="i32.const":
		#va trebui sa le adaugam si pe celelalte
		x=wasmEvalNumar(T, poz+1)
		poz=x[1]
		#aici trebuie facut apel la un constructor de i32 dintr-un numar
		y=x[0]#y=i32.i32(x[0])
		wasmPush(y)
		return poz
	
	if t.token[:3]=="i32":
		#o functie aplicata pe i32
		#va trebui modificat astfel incat sa poata face toate functiile respective, pentru moment nu avem decat add deci folosim o implementare simpla
		#x=wasmEvalNumar(T, poz+1)#x=i32.i32(wasmEvalNumar(T, poz+1))
		#y=wasmEvalNumar(T, x[1])#y=i32.i32(wasmEvalNumar(T, x[1]))
		#wasmPush(x[0]+y[0])#wasmPush(i32.i32.add(x[0]+y[0]))
		#return y[1]
		
		#aici incerc o implementare generala, dar nu pot testa pana nu am clasa i32
		X=wasmEvalNumar(T, poz+1)
		if aritateFunctii[t.token]==2:
			Y=wasmEvalNumar(T, X[1])
			wasmPush(functiiBaza[t.token](X[0], Y[0]))
			return Y[1]
		wasmPush(functiiBaza[t.token](i32.i32(X[0])))
		return X[1]
	
	return poz+1

#functia generala a interpretorului T este lista de tokene, iar poz este pozitia de la care se incepe
def wasmEval(T, poz):
	while poz<len(T):
		t=T[poz]
		#pentru debug se poate decomenta urmatoarea linie
		#print(f"Eval {T[poz]}")
		
		if t.tokType=="start":
			poz=wasmEval(T, poz+1)
			if poz==-1:
				return -1
		
		elif t.tokType=="end":
			return poz+1
		
		elif t.tokType=="number":
			x=wasmEvalNumar(T, poz)
			poz=x[1]
			wasmPush(x[0])
		
		elif t.tokType=="keyword":
			poz=wasmEvalKeyword(T, poz)
		
		else:
			poz+=1
	return -1

#functia generala, se apeleaza o data pentru un text/cod sursa.
def interpret(code):
	initWasm()
	T=tokenizer.Tokenizer(code, tokenizer.listaTipuriTokene())
	poz=0
	while poz<len(T.tokens):
		poz=wasmEval(T.tokens, poz)
		if poz==-1:
			break
	print(*wasmStack, sep='\n')