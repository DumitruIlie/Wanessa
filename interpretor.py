import tokenizer
import wasmFunc
import AST
import i32
import i64

wasmStack=[]
variabileLocale=[]
functiiWasm=dict()
wasmPozEval=[]
aritateFunctii={"i32.add":2, "i32.sub":2, "i32.mul":2, "i32.div_s":2, "i32.div_u":2, "i32.rem_s":2, "i32.rem_u":2, "i32.and":2, "i32.or":2, "i32.xor":2, "i32.shl":2, "i32.shr_s":2, "i32.shr_u":2, "i32.rotl":2, "i32.rotr":2,\
				"i32.clz":1, "i32.ctz":1, "i32.popcnt":1, "i32.extend8_s":1, "i32.extend16_s":1, "i32.eqz":1, "i32.eq":2, "i32.ne":2, "i32.lt_s":2, "i32.lt_u":2, "i32.le_s":2, "i32.le_u":2, "i32.gt_s":2, "i32.gt_u":2, "i32.ge_s":2, "i32.ge_u":2,\
				"i64.add":2, "i64.sub":2, "i64.mul":2, "i64.div_s":2, "i64.div_u":2, "i64.rem_s":2, "i64.rem_u":2, "i64.and":2, "i64.or":2, "i64.xor":2, "i64.shl":2, "i64.shr_s":2, "i64.shr_u":2, "i64.rotl":2, "i64.rotr":2,\
				"i64.clz":1, "i64.ctz":1, "i64.popcnt":1, "i64.extend8_s":1, "i64.extend16_s":1, "i64.eqz":1, "i64.eq":2, "i64.ne":2, "i64.lt_s":2, "i64.lt_u":2, "i64.le_s":2, "i64.le_u":2, "i64.gt_s":2, "i64.gt_u":2, "i64.ge_s":2, "i64.ge_u":2}
functiiBaza={"i32.add":i32.i32.add, "i32.sub":i32.i32.sub, "i32.mul":i32.i32.mul, "i32.div_s":i32.i32.div_s, "i32.div_u":i32.i32.div_u, "i32.rem_s":i32.i32.rem_s, "i32.rem_u":i32.i32.rem_u, "i32.and":i32.i32._and, "i32.or":i32.i32._or, "i32.xor":i32.i32._xor, "i32.shl":i32.i32.shl, "i32.shr_s":i32.i32.shr_s, "i32.shr_u":i32.i32.shr_u, "i32.rotl":i32.i32.rotl, "i32.rotr":i32.i32.rotr,\
			 "i32.clz":i32.i32.clz, "i32.ctz":i32.i32.ctz, "i32.popcnt":i32.i32.popcnt, "i32.extend8_s":i32.i32.extend8_s, "i32.extend16_s":i32.i32.extend16_s, "i32.eqz":i32.i32.eqz, "i32.eq":i32.i32.eq, "i32.ne":i32.i32.ne, "i32.lt_s":i32.i32.lt_s, "i32.lt_u":i32.i32.lt_u, "i32.le_s":i32.i32.le_s, "i32.le_u":i32.i32.le_u, "i32.gt_s":i32.i32.gt_s, "i32.gt_u":i32.i32.gt_u, "i32.ge_s":i32.i32.ge_s, "i32.ge_u":i32.i32.ge_u,\
			 "i64.add":i64.i64.add, "i64.sub":i64.i64.sub, "i64.mul":i64.i64.mul, "i64.div_s":i64.i64.div_s, "i64.div_u":i64.i64.div_u, "i64.rem_s":i64.i64.rem_s, "i64.rem_u":i64.i64.rem_u, "i64.and":i64.i64._and, "i64.or":i64.i64._or, "i64.xor":i64.i64._xor, "i64.shl":i64.i64.shl, "i64.shr_s":i64.i64.shr_s, "i64.shr_u":i64.i64.shr_u, "i64.rotl":i64.i64.rotl, "i64.rotr":i64.i64.rotr,\
			 "i64.clz":i64.i64.clz, "i64.ctz":i64.i64.ctz, "i64.popcnt":i64.i64.popcnt, "i64.extend8_s":i64.i64.extend8_s, "i64.extend16_s":i64.i64.extend16_s, "i64.eqz":i64.i64.eqz, "i64.eq":i64.i64.eq, "i64.ne":i64.i64.ne, "i64.lt_s":i64.i64.lt_s, "i64.lt_u":i64.i64.lt_u, "i64.le_s":i64.i64.le_s, "i64.le_u":i64.i64.le_u, "i64.gt_s":i64.i64.gt_s, "i64.gt_u":i64.i64.gt_u, "i64.ge_s":i64.i64.ge_s, "i64.ge_u":i64.i64.ge_u}
tipuriDate={"i32":i32.i32, "i64":i64.i64}#, "f32":f32.f32}

#initializeaza interpretorul
def initWasm():
	global wasmStack, veriabileLocale, functiiWasm, wasmPozEval
	wasmStack=[[]]
	variabileLocale=[]
	functiiWasm=dict()
	wasmPozEval=[0]

#functie de test, ajuta la debug, TREBUIE NEAPARAT STEARSA INAINTE SA TRIMITEM PROIECTUL
def wasmLogStack():
	print('[')
	for i in range(len(wasmStack)):
		print('[', *wasmStack[i], ']')
	print(']')

#adauga pe stiva un element
def wasmPush(x):
	wasmStack[-1].append(x)

#scoate si returneaza ultimul obiect de pe stiva
def wasmPop():
	return wasmStack[-1].pop()

#numere in baza 10 si 16
def wasmASTEvalNumber(ast):
	if isinstance(ast.children[wasmPozEval[-1]], AST.AST):
		wasmPozEval.append(0)
		wasmASTEval(ast.children[wasmPozEval[-2]])
		wasmPozEval.pop()
		wasmPozEval[-1]+=1
		return wasmPop()
	if ast is None:
		return wasmPop()
	if ast.children[wasmPozEval[-1]].tokType=="keyword":
		wasmASTEvalKeyword(ast)
		return wasmPop()
	if ast.children[wasmPozEval[-1]].tokType=="number":
		if ast.children[wasmPozEval[-1]].token=="unknown operator":
			return ast.children[wasmPozEval[-1]].token
		return wasmTokenToNumber(ast.children[wasmPozEval[-1]])
	return "unknown operator"

#transforma un token intr-un numar (int)
def wasmTokenToNumber(t):
	sign=1
	t=t.token.replace('_', '')
	if t[0]=='-':
		sign=-1
		t=t[1:]
	elif t[0]=='+':
		t=t[1:]
	if len(t)<3:
		#baza 10 sigur
		return int(t)*sign
	if t[1]=='x':
		#baza 16
		x=0
		for i in range(2, len(t)):
			if '0'<=t[i]<='9':
				x=x*16+ord(t[i])-ord('0')
			elif 'a'<=t[i]<='f':
				x=x*16+10+ord(t[i])-ord('a')
		return x*sign
	return int(t)*sign

#functie pentru incarcat parametri si variabile locale + apel la functie
def wasmASTCallFunc(ast, F):
	#variabileLocale.append([])
	#wasmStack.append([])
	locVar=[]
	
	while len(locVar)<len(F.paramTypes):
		retType=int
		if F.paramTypes[len(locVar)]=="i32":
			retType=i32.i32
		elif F.paramTypes[len(locVar)]=="i64":
			retType=i64.i64
		elif F.paramTypes[len(locVar)]=="f32":
			#retType=f32.f32
			pass
		
		if isinstance(ast.children[wasmPozEval[-1]], AST.AST):
			wasmPozEval.append(0)
			x=wasmASTEvalNumber(ast.children[wasmPozEval[-2]])
			wasmPozEval.pop()
			wasmPozEval[-1]+=1
			if isinstance(x, str):
				#trebuie modificat pe aici
				########################################################################################################################################
				return x
		else:
			wasmASTEvalKeyword(ast)
			x=wasmPop()
		if not isinstance(x, retType):
			return "type mismatch"
		locVar.append(x)
	
	variabileLocale.append(locVar)
	for x in F.localTypes:
		variabileLocale[-1].append(tipuriDate[x](0))
	
	if isinstance(F.AST, AST.AST):
		wasmStack.append([])
		wasmPozEval.append(0)
		wasmASTEval(F.AST)
		wasmPozEval.pop()
	
	if len(F.results)!=(l:=len(wasmStack[-1])):
		wasmStack.pop()
		return f"function is expected to return {len(F.results)} values but only returns {l}"
	for i in range(l):
		if tipuriDate[F.results[i]]!=type(wasmStack[-1][i]):
			x=wasmStack.pop()[i]
			return f"function is expected to return {F.results[i]} but returns {type(x)}"
	
	variabileLocale.pop()
	x=wasmStack.pop()
	wasmStack[-1].extend(x)
	return ""

#verifica un assert
def wasmASTEvalAssert(ast):
	#momentan nu sunt toate aici, incerc sa le fac pe toate dar dureaza
	if ast.children[wasmPozEval[-1]].token=="assert_return":
		wasmPozEval[-1]+=1
		#calculam cele 2 rezultate si daca sunt diferite ne oprim
		if isinstance(ast.children[wasmPozEval[-1]], AST.AST):
			wasmStack.append([])
			wasmPozEval.append(0)
			x=wasmASTEval(ast.children[wasmPozEval[-2]])
			wasmPozEval.pop()
			wasmPozEval[-1]+=1
			if x!="":
				return "assert fail because of "+x
		else:
			return f"assert fail"
		wasmStack.append([])
		for i in range(wasmPozEval[-1], len(ast.children)):
			if isinstance(ast.children[i], AST.AST):
				wasmPozEval.append(0)
				x=wasmASTEval(ast.children[i])
				wasmPozEval.pop()
				if x!="":
					return "assert fail because of "+x
			else:
				return "assert fail"
		wasmPozEval[-1]=len(ast.children)
		y=wasmStack.pop()
		x=wasmStack.pop()
		if len(x)!=len(y):
			return f"assert fail because expected {len(y)} values but only got {len(x)} values"
		for i in range(len(x)):
			if type(x[i])!=type(y[i]) or x[i]._val!=y[i]._val:
				return f"assert fail because {i}-th values differ ({type(x[i])}, {x[i]._val}) != ({type(y[i])}, {y[i]._val})"
		return "ok"
	
	if ast.children[wasmPozEval[-1]].token=="assert_invalid":
		wasmPozEval[-1]+=1
		#ne asteptam la o eroare, daca eroarea primita este cea la care ne asteptam, assert-ul trece, altfel pica
		#dupa assert_invalid urmeaza un modulul ce trebuie sa dea eroare si dupa un string indicand eroarea ce ar trebui ridicata
		if not isinstance(ast.children[wasmPozEval[-1]], AST.AST):
			return "assert fail"
		wasmPozEval.append(0)
		eroare=wasmASTEval(ast.children[wasmPozEval[-2]])
		wasmPozEval.pop()
		wasmPozEval[-1]+=1
		y=ast.children[wasmPozEval[-1]].token
		if y!=eroare:
			#erorile asteptata si primita sunt diferite, assert-ul pica
			return "assert fail"
		#assert-ul merge perfect
		return "ok"

#keywords
def wasmASTEvalKeyword(ast):
	t=ast.children[wasmPozEval[-1]]
	wasmPozEval[-1]+=1
	
	#verific care tip de keyword este ca sa stiu cum sa continui
	if t.token=="drop":
		#scoate de pe stiva si nu returneaza
		wasmPop()
		return ""
	
	if t.token=="local.get":
		#nu mai exista aliase, daca exista atunci e o eroare
		if ast.children[wasmPozEval[-1]].tokType=="alias":
			return "unknown label"
		wasmPush(variabileLocale[-1][wasmTokenToNumber(ast.children[wasmPozEval[-1]])])
		wasmPozEval[-1]+=1
		return ""
	
	if t.token=="func":
		#definire functie
		F=wasmFunc.wasmFunc()
		ans=F.make(ast.toTokenList())
		if ans!="":
			return ans
		if F.invokeName!="":
			functiiWasm[F.invokeName]=F
		if F.callName!="":
			functiiWasm[F.callName]=F
		wasmPozEval[-1]=len(ast.children)
		return ""
	
	if t.token=="invoke":
		#apel functie "exemplu"
		if ast.children[wasmPozEval[-1]].tokType!="string":
			return "expected function name string after function invoke"
		F=functiiWasm[ast.children[wasmPozEval[-1]].token]
		wasmPozEval[-1]+=1
		ans=wasmASTCallFunc(ast, F)
		return ans
	
	if t.token=="call":
		#apel functie $exemplu
		if ast.children[wasmPozEval[-1]].tokType!="alias":
			return "expected function alias after function call"
		F=functiiWasm[ast.children[wasmPozEval[-1]].token]
		wasmPozEval[-1]+=1
		ans=wasmASTCallFunc(ast, F)
		return ans
	
	if t.token[:6]=="assert":
		wasmPozEval[-1]-=1
		assertAns=wasmASTEvalAssert(ast)
		if assertAns!="ok":
			return assertAns
		return ""
	
	if t.token=="i32.const":
		#va trebui sa le adaugam si pe celelalte
		wasmPush(i32.i32(wasmTokenToNumber(ast.children[wasmPozEval[-1]])))
		wasmPozEval[-1]+=1
		return ""
	
	if t.token=="i64.const":
		wasmPush(i64.i64(wasmTokenToNumber(ast.children[wasmPozEval[-1]])))
		wasmPozEval[-1]+=1
		return ""
	
	#va trebui sa adaugam si celelalte tipuri de date
	if t.token[:3]=="i32" or t.token[:3]=="i64":
		#o functie aplicata pe i32 sau i64
		if isinstance(ast.children[wasmPozEval[-1]], AST.AST):
			wasmPozEval.append(0)
			x=wasmASTEvalNumber(ast.children[wasmPozEval[-2]])
			wasmPozEval.pop()
			wasmPozEval[-1]+=1
			if isinstance(x, str):
				return x
		else:
			wasmASTEvalKeyword(ast)
			x=wasmPop()
		
		if aritateFunctii[t.token]==2:
			if isinstance(ast.children[wasmPozEval[-1]], AST.AST):
				wasmPozEval.append(0)
				y=wasmASTEvalNumber(ast.children[wasmPozEval[-2]])
				wasmPozEval.pop()
				wasmPozEval[-1]+=1
				if isinstance(y, str):
					return y
			else:
				wasmASTEvalKeyword(ast)
				y=wasmPop()
			ans=functiiBaza[t.token](x, y)
			if ans=="TYPE MISMATCH":
				return "type mismatch"
			wasmPush(ans)
			return ""
		ans=functiiBaza[t.token](x)
		if ans=="TYPE MISMATCH":
			return "type mismatch"
		wasmPush(ans)
		return ""
		
	#ASTA TREBUIE SCOS INAINTE SA TRIMITEM PROIECTUL
	if t.token=="print":
		wasmLogStack()
	
	return ""

#functie generala
def wasmASTEval(ast):
	while wasmPozEval[-1]<len(ast.children):
		t=ast.children[wasmPozEval[-1]]
		#pentru debug se poate decomenta urmatoarea linie
		#print(f"Eval {t}")
		
		if isinstance(t, tokenizer.Token):
			if t.tokType=="number":
				if t.token=="unknown operator":
					return "unknown operator"
				#un numar razlet
				print(f"skipped random number encounter {t.token}")
				wasmPozEval[-1]+=1
				#wasmPush(wasmTokenToNumber(t))
			
			elif t.tokType=="keyword":
				ans=wasmASTEvalKeyword(ast)
				if ans!="":
					return ans
			
			else:
				print(f"skipped {t.token} cannot interpret it")
				wasmPozEval[-1]+=1
			
		else:
			wasmPozEval.append(0)
			ans=wasmASTEval(t)
			wasmPozEval.pop()
			wasmPozEval[-1]+=1
			if ans!="":
				return ans
	return ""

#functia generala, se apeleaza o data pentru un text/cod sursa.
def interpret(code):
	initWasm()
	T=tokenizer.Tokenizer(code)
	A=AST.makeAST(T.tokens)
	if not A.correct:
		print(A.assertError)
		return A.assertError
	ans=wasmASTEval(A)
	if ans!="":
		print(ans)