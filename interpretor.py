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
def wasmEvalNumber(T, poz):
	t=T[poz].token
	if T[poz].tokType=="start":
		poz=wasmEval(T, poz+1)
		if isinstance(poz, tuple):
			#a aparut o eroare undeva in cod
			return poz
		x=wasmPop()
		return (x, poz)
	if T[poz].tokType=="end":
		#ia din stiva
		x=wasmPop()
		if isinstance(x, str):
			#eroare, nu avem nimic in stiva
			return (x, poz+1)
		return (x, poz+1)
	sign=1
	if t[0]=='-':
		sign=-1
		t=t[1:]
	if len(t)<3:
		#baza 10 sigur
		return (int(t)*sign, poz+1)
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
		return (x*sign, poz+1)
	return (int(t)*sign, poz+1)

#functie "citire" string
def wasmEvalString(T, poz):
	if T[poz].tokType=="start":
		x=wasmEvalString(T, poz+1)
		if len(x)==3:
			#eroare
			return x
		#string
		return x
	if T[poz].tokType=="string":
		return (T[poz].token, poz+1)
	#altceva, eroare
	return (-1, f"expected string found {T[poz].token}", poz)

#functie pentru incarcarea parametrilor si "apel" functieWasm
def wasmEvalFunc(T, poz, F):
	variabileLocale.append([])
	aliasVariabileLocale.append(F.params)
	while len(variabileLocale[-1])<len(F.paramTypes):
		retType=int
		if F.paramTypes[len(variabileLocale[-1])]=="i32":
			retType=i32.i32
		elif F.paramTypes[len(variabileLocale[-1])]=="i64":
			#retType=i64.i64
			pass
		elif F.paramTypes[len(variabileLocale[-1])]=="f32":
			#retType=f32.f32
			pass
		x=wasmEvalNumber(T, poz)
		if isinstance(x[0], str):
			#eroare
			return x
		if not isinstance(x[0], retType):
			#eroare TYPE_MISMATCH
			return ("type mismatch", x[1])
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

def wasmEvalAssert(T, poz):
	#assert-uri
	#momentan nu sunt toate aici, incerc sa le fac pe toate dar dureaza
	if T[poz].token=="assert_return":
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
			return ("type mismatch", poz)
		if x._val!=y._val:
			return ("AssertFail", poz)
		return poz
	
	if T[poz].token=="assert_invalid":
		#ne asteptam la o eroare, daca eroarea primita este cea la care ne asteptam, continuam executia, altfel ne oprim
		#dupa assert_invalid urmeaza un modul si dupa asta un string indicand eroarea ce ar trebui returnata
		if poz+1>=len(T):
			return (f"unexpected end of file", poz)
		poz+=1
		if T[poz].tokType!="start":
			return (f"expected '(' found {T[poz].token}", poz+1)
		if poz+1>=len(T):
			return (f"unexpected end of file", poz)
		poz+=1
		if T[poz].token!="module":
			return (f"expected \'module\' found {T[poz].token}", poz+1)
		cntPrnt=1
		i=poz
		while cntPrnt and i<len(T):
			cntPrnt+=int(T[i].tokType=="start")-int(T[i].tokType=="end")
			i+=1
		poz+=1
		x=wasmEval(T, poz)
		if not isinstance(x, tuple):
			#nu a aparut vreo eroare, deci assert-ul pica
			print(x, " ", wasmStack[-1])
			return ("AssertFail", x)
		#a aparut o eroare, verific daca e cea dorita
		y=wasmEvalString(T, i)
		if len(y)==3:
			#eroare
			return (y[1], y[2])
		#string-ul s-a citit corespunzator
		if y[0].strip('\"')!=x[0]:
			#erorile asteptata si primita sunt diferite, assert-ul pica
			return ("AssertFail", y[1])
		#assert-ul merge perfect
		return y[1]

#keywords
def wasmEvalKeyword(T, poz):
	global variabileLocale
	t=T[poz]
	#verific care tip de keyword este ca sa stiu cum sa continui
	if t.token=="drop":
		#scoate de pe stiva si nu returneaza
		wasmPop()
		return poz+1
	
	if t.token=="local.get":
		#alias sau numar
		poz+=1
		if T[poz].tokType=="alias":
			x=aliasVariabileLocale[-1][T[poz].token]
			poz+=1
			wasmPush(variabileLocale[-1][x])
		else:
			x=wasmEvalNumber(T, poz)
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
		poz=wasmEvalAssert(T, poz)
		if isinstance(poz, tuple):
			#AssertFail
			return poz
		#AssertPass
		return poz
	
	if t.token=="i32.const":
		#va trebui sa le adaugam si pe celelalte
		x=wasmEvalNumber(T, poz+1)
		if isinstance(x[0], str):
			return x
		if not isinstance(x[0], i32.i32):
			if not isinstance(x[0], int):
				return ("type mismatch", x[1])
			x=(i32.i32(x[0]), x[1])
		wasmPush(x[0])
		return x[1]
	
	if t.token[:3]=="i32":
		#o functie aplicata pe i32
		X=wasmEvalNumber(T, poz+1)
		if isinstance(X[0], str):
			return X
		if aritateFunctii[t.token]==2:
			Y=wasmEvalNumber(T, X[1])
			if isinstance(Y[0], str):
				return Y
			ans=functiiBaza[t.token](X[0], Y[0])
			if ans=="TYPE MISMATCH":
				return ("type mismatch", Y[1])
			wasmPush(ans)
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
			x=wasmEvalNumber(T, poz)
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