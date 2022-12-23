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
def wasmEvalNumber(T, poz, returnType):
	t=T[poz].token
	if T[poz].tokType=="start":
		poz=wasmEval(T, poz+1)
		if isinstance(poz, tuple):
			#a aparut o eroare undeva in cod
			return poz
		x=wasmPop()
		if returnType is None or isinstance(x, returnType):
			return (x, poz)
		if isinstance(x, int) and (returnType==i32.i32): #or returnType==i64.i64):
			return (returnType(x), poz)
		#if (isinstance(x, float) or isinstance(x, int)) and returnType==f32.f32:
		#	return (retType(x), poz)
		return "type mismatch"
	sign=1
	if t[0]=='-':
		sign=-1
		t=t[1:]
	if len(t)<3:
		#baza 10 sigur
		if returnType is None:
			return (int(t)*sign, poz+1)
		return (returnType(int(t)*sign), poz+1)
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
		if returnType is None:
			return (x*sign, poz+1)
		return (returnType(x*sign), poz+1)
	if returnType is None:
		return (int(t)*sign, poz+1)
	return (returnType(int(t)*sign), poz+1)

#functie pentru incarcarea parametrilor si "apel" functieWasm
def wasmEvalFunc(T, poz, F):
	variabileLocale.append([])
	aliasVariabileLocale.append(F.params)
	while len(variabileLocale[-1])<len(F.paramTypes):
		retType=None
		if F.paramTypes[len(variabileLocale[-1])]=="i32":
			retType=i32.i32
		elif F.paramTypes[len(variabileLocale[-1])]=="i64":
			#retType=i64.i64
			pass
		elif F.paramTypes[len(variabileLocale[-1])]=="f32":
			#retType=f32.f32
			pass
		x=wasmEvalNumber(T, poz, retType)
		if isinstance(x[0], str):
			return x
		poz=x[1]
		variabileLocale[-1].append(x[0])
	#trebuie modificat aici cu tipurile de date din variabilele locale ale functiei
	variabileLocale[-1].extend([i32.i32(0)]*len(F.localTypes))
	x=wasmEval(F.tokens, 0)
	aliasVariabileLocale.pop()
	variabileLocale.pop()
	if isinstance(x, tuple):
		return x
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
			x=wasmEvalNumber(T, poz, None)
			if isinstance(x[0], str):
				return x
			poz=x[1]
			wasmPush(variabileLocale[-1][x[0]])
		return poz
	
	if t.token=="func":
		#definire functie
		F=wasmFunc.wasmFunc()
		poz=F.make(T, poz)
		functiiWasm[F.name]=F
		return poz
	
	if t.token=="invoke" or t.token=="call":
		#apel functie
		poz+=1
		F=functiiWasm[T[poz].token.strip('\"')]
		poz+=1
		poz=wasmEvalFunc(T, poz, F)
		return poz
	
	if t.token[:6]=="assert":
		#assert-uri
		#momentan nu sunt toate aici, incerc sa le fac pe toate dar dureaza
		if t.token=="assert_return":
			#calculam cele 2 rezultate si daca sunt diferite ne oprim
			poz=wasmEval(T, poz+1)
			if isinstance(poz, tuple):
				return poz
			poz=wasmEval(T, poz)
			if isinstance(poz, tuple):
				return poz
			x=wasmPop()
			y=wasmPop()
			#cred ca va trebui sa modific cate ceva pe aici dar nu mai pot sa mai fac acum
			if type(x)!=type(y):
				return (f"Answers have different types, {type(x)}!={type(y)}", poz)
			if x._val!=y._val:
				return (f"Answers aren't the same, {x}!={y}", poz)
			return poz
	
	if t.token=="i32.const":
		#va trebui sa le adaugam si pe celelalte
		x=wasmEvalNumber(T, poz+1, i32.i32)
		if isinstance(x[0], str):
			return x
		wasmPush(x[0])
		return x[1]
	
	if t.token[:3]=="i32":
		#o functie aplicata pe i32
		X=wasmEvalNumber(T, poz+1, i32.i32)
		if isinstance(X[0], str):
			return X
		if aritateFunctii[t.token]==2:
			Y=wasmEvalNumber(T, X[1], i32.i32)
			if isinstance(Y[0], str):
				return Y
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
		print(f"Eval {T[poz]}")
		
		if t.tokType=="start":
			poz=wasmEval(T, poz+1)
			if isinstance(poz, tuple):
				return poz
			if poz==-1:
				return -1
		
		elif t.tokType=="end":
			return poz+1
		
		if t.tokType=="number":
			x=wasmEvalNumber(T, poz, None)
			if isinstance(x[0], str):
				return x
			poz=x[1]
			wasmPush(x[0])
		
		elif t.tokType=="keyword":
			poz=wasmEvalKeyword(T, poz)
			if isinstance(poz, tuple):
				return poz
		
		else:
			poz+=1
	return -1

#functia generala, se apeleaza o data pentru un text/cod sursa.
def interpret(code):
	initWasm()
	T=tokenizer.Tokenizer(code)
	poz=0
	while poz<len(T.tokens):
		poz=wasmEval(T.tokens, poz)
		if isinstance(poz, tuple):
			print(poz[0])
			return None
		if poz==-1:
			break
	print(*wasmStack, sep='\n')