import sys
import tokenizer
import ASTChecker
import wasmFunc
import AST
import i8
import i16
import i32
import i64
import i16x8
import f32
import v128

#date importante globale, nu are sens sa le stocam altundeva
wasmAritateFunctii={"i32.add":2, "i32.sub":2, "i32.mul":2, "i32.div_s":2, "i32.div_u":2, "i32.rem_s":2, "i32.rem_u":2, "i32.and":2, "i32.or":2, "i32.xor":2, "i32.shl":2, "i32.shr_s":2, "i32.shr_u":2, "i32.rotl":2, "i32.rotr":2,\
				"i32.clz":1, "i32.ctz":1, "i32.popcnt":1, "i32.extend8_s":1, "i32.extend16_s":1, "i32.wrap_i64":1, "i32.eqz":1, "i32.eq":2, "i32.ne":2, "i32.lt_s":2, "i32.lt_u":2, "i32.le_s":2, "i32.le_u":2, "i32.gt_s":2, "i32.gt_u":2, "i32.ge_s":2, "i32.ge_u":2,\
				"i64.add":2, "i64.sub":2, "i64.mul":2, "i64.div_s":2, "i64.div_u":2, "i64.rem_s":2, "i64.rem_u":2, "i64.and":2, "i64.or":2, "i64.xor":2, "i64.shl":2, "i64.shr_s":2, "i64.shr_u":2, "i64.rotl":2, "i64.rotr":2,\
				"i64.clz":1, "i64.ctz":1, "i64.popcnt":1, "i64.extend8_s":1, "i64.extend16_s":1, "i64.eqz":1, "i64.eq":2, "i64.ne":2, "i64.lt_s":2, "i64.lt_u":2, "i64.le_s":2, "i64.le_u":2, "i64.gt_s":2, "i64.gt_u":2, "i64.ge_s":2, "i64.ge_u":2,\
				"i64.extend32_s":1}
wasmFunctiiBaza={"i32.add":i32.i32.add, "i32.sub":i32.i32.sub, "i32.mul":i32.i32.mul, "i32.div_s":i32.i32.div_s, "i32.div_u":i32.i32.div_u, "i32.rem_s":i32.i32.rem_s, "i32.rem_u":i32.i32.rem_u, "i32.and":i32.i32._and, "i32.or":i32.i32._or, "i32.xor":i32.i32._xor, "i32.shl":i32.i32.shl, "i32.shr_s":i32.i32.shr_s, "i32.shr_u":i32.i32.shr_u, "i32.rotl":i32.i32.rotl, "i32.rotr":i32.i32.rotr,\
			 "i32.clz":i32.i32.clz, "i32.ctz":i32.i32.ctz, "i32.popcnt":i32.i32.popcnt, "i32.extend8_s":i32.i32.extend8_s, "i32.extend16_s":i32.i32.extend16_s, "i32.wrap_i64":i32.i32.wrap_i64, "i32.eqz":i32.i32.eqz, "i32.eq":i32.i32.eq, "i32.ne":i32.i32.ne, "i32.lt_s":i32.i32.lt_s, "i32.lt_u":i32.i32.lt_u, "i32.le_s":i32.i32.le_s, "i32.le_u":i32.i32.le_u, "i32.gt_s":i32.i32.gt_s, "i32.gt_u":i32.i32.gt_u, "i32.ge_s":i32.i32.ge_s, "i32.ge_u":i32.i32.ge_u,\
			 "i64.add":i64.i64.add, "i64.sub":i64.i64.sub, "i64.mul":i64.i64.mul, "i64.div_s":i64.i64.div_s, "i64.div_u":i64.i64.div_u, "i64.rem_s":i64.i64.rem_s, "i64.rem_u":i64.i64.rem_u, "i64.and":i64.i64._and, "i64.or":i64.i64._or, "i64.xor":i64.i64._xor, "i64.shl":i64.i64.shl, "i64.shr_s":i64.i64.shr_s, "i64.shr_u":i64.i64.shr_u, "i64.rotl":i64.i64.rotl, "i64.rotr":i64.i64.rotr,\
			 "i64.clz":i64.i64.clz, "i64.ctz":i64.i64.ctz, "i64.popcnt":i64.i64.popcnt, "i64.extend8_s":i64.i64.extend8_s, "i64.extend16_s":i64.i64.extend16_s, "i64.eqz":i64.i64.eqz, "i64.eq":i64.i64.eq, "i64.ne":i64.i64.ne, "i64.lt_s":i64.i64.lt_s, "i64.lt_u":i64.i64.lt_u, "i64.le_s":i64.i64.le_s, "i64.le_u":i64.i64.le_u, "i64.gt_s":i64.i64.gt_s, "i64.gt_u":i64.i64.gt_u, "i64.ge_s":i64.i64.ge_s, "i64.ge_u":i64.i64.ge_u,\
			 "i64.extend32_s":i64.i64.extend32_s}
wasmSimdFuncs={"i16x8.extadd_pairwise_i8x16_s":i16x8.i16x8.extadd_pairwise_i8x16_s, "i16x8.extadd_pairwise_i8x16_u":i16x8.i16x8.extadd_pairwise_i8x16_u}
wasmDataTypes={"i32":i32.i32, "i64":i64.i64, "v128":v128.v128, "f32":f32.f32}


class Interpretor:
	def __init__(self):
		self.wasmStack=[[]]
		self.variabileLocale=[]
		self.functiiWasm=dict()
		self.wasmPozEval=[0]
		self.wasmBlockAlias=dict()
		self.wasmBlocksCount=0
		self.wasmDataTypesVariabileLocale=[]
		sys.setrecursionlimit(10**5)

	#functie de test, ajuta la debug, TREBUIE NEAPARAT STEARSA INAINTE SA TRIMITEM PROIECTUL
	def wasmLogStack(self):
		print('[')
		for i in range(len(self.wasmStack)):
			print(' [', *self.wasmStack[i], ']')
		print(']')

	#adauga pe stiva un element
	def wasmPush(self, x):
		self.wasmStack[-1].append(x)

	#scoate si returneaza ultimul obiect de pe stiva
	def wasmPop(self):
		if len(self.wasmStack[-1])==0:
			return "type mismatch"
		return self.wasmStack[-1].pop()

	def wasmEvalNumber(self, ast):
		if len(ast.children)<=self.wasmPozEval[-1]:
			return "\"type mismatch\""
		if isinstance(ast.children[self.wasmPozEval[-1]], AST.AST):
			self.wasmPozEval.append(0)
			ans=self.wasmEval(ast.children[self.wasmPozEval[-2]])
			self.wasmPozEval.pop()
			self.wasmPozEval[-1]+=1
			if ans!="":
				return ans
			return ""
		if ast is None:
			return "\"type mismatch\""
		if ast.children[self.wasmPozEval[-1]].tokType=="keyword":
			return self.wasmEvalKeyword(ast)
		if ast.children[self.wasmPozEval[-1]].tokType=="block":
			return self.wasmEvalBlock(ast)
		if ast.children[self.wasmPozEval[-1]].tokType=="number":
			if ast.children[self.wasmPozEval[-1]].token=="unknown operator":
				return ast.children[self.wasmPozEval[-1]].token
			self.wasmPush(Interpretor.wasmTokenToNumber(ast.children[self.wasmPozEval[-1]]))
			return ""
		return "unknown operator"

	#transforma un token intr-un numar (int)
	
	def wasmTokenToNumber(t):
		t = t.token.replace('_', '')
		if(t[1] == "x"):
			return int(t, 16)
		else:
			return int(t)
		
	#functie pentru incarcat parametri si variabile locale + apel la functie
	def wasmCallFunc(self, ast, F):
		locVar=[]
		locVarTypes=[]
		
		while len(locVar)<len(F.paramTypes):
			retType=wasmDataTypes[F.paramTypes[len(locVar)]]
			
			if isinstance(ast.children[self.wasmPozEval[-1]], AST.AST):
				self.wasmPozEval.append(0)
				x=self.wasmEvalNumber(ast.children[self.wasmPozEval[-2]])
				self.wasmPozEval.pop()
				self.wasmPozEval[-1]+=1
				if x!="":
					return x
			else:
				x=self.wasmEvalKeyword(ast)
				if x!="":
					return x
			x=self.wasmPop()
			if not isinstance(x, retType):
				return "type mismatch"
			locVar.append(x)
			locVarTypes.append(retType)
		
		for x in F.localTypes:
			locVar.append(wasmDataTypes[x](0))
			locVarTypes.append(wasmDataTypes[x])
		
		if isinstance(F.AST, AST.AST):
			self.variabileLocale.append(locVar)
			self.wasmDataTypesVariabileLocale.append(locVarTypes)
			self.wasmStack.append([])
			self.wasmPozEval.append(0)
			error=self.wasmEval(F.AST)
			self.wasmPozEval.pop()
			self.wasmDataTypesVariabileLocale.pop()
			self.variabileLocale.pop()
			x=self.wasmStack.pop()
			if error!="":
				if isinstance(error, tuple) and error[0]=="return from function":
					#rezultatul este strict ce primim din error
					x=error[1]
				else:
					return error
			if len(F.results)!=(l:=len(x)):
				return f"function is expected to return {len(F.results)} values but returns {l}"
			for i in range(l):
				if wasmDataTypes[F.results[i]]!=type(x[i]):
					return f"function is expected to return {F.results[i]} but returns (type={type(x[i])}, value={x})"
			self.wasmStack[-1].extend(x)
			return ""
		
		if F.results!=[]:
			return "function is expected to return, but has no implementation"
		return ""

	#verifica un assert
	def wasmEvalAssert(self, ast):
		#momentan nu sunt toate aici, incerc sa le fac pe toate dar dureaza
		if ast.children[self.wasmPozEval[-1]].token=="assert_return":
			self.wasmPozEval[-1]+=1
			#calculam cele 2 rezultate si daca sunt diferite ne oprim
			if isinstance(ast.children[self.wasmPozEval[-1]], AST.AST):
				self.wasmStack.append([])
				self.wasmPozEval.append(0)
				x=self.wasmEval(ast.children[self.wasmPozEval[-2]])
				self.wasmPozEval.pop()
				self.wasmPozEval[-1]+=1
				if x!="":
					return "assert fail because of "+str(x)
			else:
				return f"assert fail because expected expresion after assert_return"
			self.wasmStack.append([])
			for i in range(self.wasmPozEval[-1], len(ast.children)):
				if isinstance(ast.children[i], AST.AST):
					self.wasmPozEval.append(0)
					x=self.wasmEval(ast.children[i])
					self.wasmPozEval.pop()
					if x!="":
						return "assert fail because of "+str(x)
				else:
					return "assert fail because expected expresion after assert_return"
			self.wasmPozEval[-1]=len(ast.children)
			y=self.wasmStack.pop()
			x=self.wasmStack.pop()
			if len(x)!=len(y):
				return f"assert fail because expected {len(y)} values but only got {len(x)} values"
			for i in range(len(x)):
				if type(x[i])!=type(y[i]):
					return f"assert fail because {i}-th values differ in type: ({type(x[i])}, {x[i]}) != ({type(y[i])}, {y[i]})"
				if isinstance(x[i], v128.v128):
					if len(x[i]._val)!=len(y[i]._val):
						return f"assert fail because {i}-th values have different length"
					for j in range(len(x[i]._val)):
						if type(x[i]._val[j])!=type(y[i]._val[j]) or x[i]._val[j]._val!=y[i]._val[j]._val:
							return f"assert fail because {i}-th value (simd vector) differs at {j}-th position: ({type(x[i]._val[j])}, {x[i]._val[j]}) != ({type(y[i]._val[j])}, {y[i]._val[j]})"
				elif x[i]._val!=y[i]._val:
					return f"assert fail because {i}-th values differ: ({type(x[i])}, {x[i]}) != ({type(y[i])}, {y[i]})"
			return "ok"
		
		if ast.children[self.wasmPozEval[-1]].token=="assert_invalid" or ast.children[self.wasmPozEval[-1]].token=="assert_trap":
			self.wasmPozEval[-1]+=1
			#ne asteptam la o eroare, daca eroarea primita este cea la care ne asteptam, assert-ul trece, altfel pica
			#dupa assert_invalid urmeaza un modulul ce trebuie sa dea eroare si dupa un string indicand eroarea ce ar trebui ridicata
			if not isinstance(ast.children[self.wasmPozEval[-1]], AST.AST):
				return "assert fail because expected expresion after assert_return"
			self.wasmPozEval.append(0)
			eroare=self.wasmEval(ast.children[self.wasmPozEval[-2]])
			self.wasmPozEval.pop()
			self.wasmPozEval[-1]+=1
			y=ast.children[self.wasmPozEval[-1]].token
			self.wasmPozEval[-1]+=1
			if y!=eroare:
				#erorile asteptata si primita sunt diferite, assert-ul pica
				return f"assert fail because expected error {y} but received {eroare}"
			#assert-ul merge perfect
			return "ok"
		
		if ast.children[self.wasmPozEval[-1]].token=="assert_malformed": # verificam daca ceea ce e pus intre ghilimele in modulul cu quote e ok
			#	--- unul dintre cazuri e urmatorul:
			#
			#	(assert_malformed 
			#		(module quote 
			#			"ceva cod"
			#			"alt cod"
			#			"etc"
			#			"etc bis"
			#		)
			# 		"unexpected token"
			#	)
			# 
			# date fiind formularile din fisiere, plecam de la presupunerea ca singurele noduri urmase in contextul asta sunt nodul cu modulul urmator si token-ul cu eroarea (in ordinea asta)
			# 
			# cazul in care avem "inline function type" poate fi tratat doar dupa implementarea unei tabele pentru tinerea evidentei de signaturi pentru functii
			codNou = ""
			for x in ast.children:
				if isinstance(x, AST.AST):
					codNou = Interpretor.getCodeFromQuoteModule(x)
					break # are sens existenta unui singur nod de ast
			
			# codul nou reprezinta echivalentul a ceea ce am in nodul de "module quote"
			# il interpretam folosind aceeasi logica din main
			codNou = codNou.splitlines()
			codNou = tokenizer.reformat(codNou)
			
			codEroare = interpret(codNou, printExecutionEnd=False)
			self.wasmPozEval[-1] += 3
			if codEroare == "unexpected token" or codEroare == "inline function type":
				return "ok"
				
			return "assert not validated"
		
		return ast.children[self.wasmPozEval[-1]].token+" not implemented"

	def getCodeFromQuoteModule(ast : AST.AST): # dat fiind un nod de ast, functia returneaza concatenarea token-urilor (cu endline-uri) urmase ale nodului respectiv intr-un bloc de tip modul
		return  "(module\n" + "\n".join([ x.token[1:-1] for x in ast.children if isinstance(x, tokenizer.Token) and x.token[0] == '"']) + "\n)\n"

	#helper, spune ce tip de structura este ast-ul pentru if
	def wasmEvalIfHelper(ast):
		if isinstance(ast, tokenizer.Token):
			if ast.tokType=="alias":
				return "ignore"
			return f"unexpected {ast.token} after if"
		if isinstance(ast.children[0], tokenizer.Token):
			if ast.children[0].token=="then":
				return "then"
			if ast.children[0].token=="else":
				return "else"
			if ast.children[0].token=="result":
				return "result"
			if ast.children[0].token == "param":
				return f"unexpected {ast} after if" 
			return "conditie"
		return f"unexpected {ast} after if"

	#interpreteaza if cu toate nebuniile lui
	def wasmEvalIf(self, ast):
		#forma cea mai generala de if:
		#(if [(result ...)] [(conditie)] (then ...) [(else ...)])
		resultType=[]
		conditie=""
		thenInstr=""
		elseInstr=""
		
		#am trecut peste if deja
		part=Interpretor.wasmEvalIfHelper(ast.children[self.wasmPozEval[-1]])
		if part=="ignore":
			self.wasmPozEval[-1]+=1
			part=Interpretor.wasmEvalIfHelper(ast.children[self.wasmPozEval[-1]])
		if part=="result":
			for i in range(1, len(ast.children[self.wasmPozEval[-1]].children)):
				resultType.append(wasmDataTypes[ast.children[self.wasmPozEval[-1]].children[i].token])
			self.wasmPozEval[-1]+=1
			part=Interpretor.wasmEvalIfHelper(ast.children[self.wasmPozEval[-1]])
		if part=="conditie":
			conditie=ast.children[self.wasmPozEval[-1]]
			self.wasmPozEval[-1]+=1
			part=Interpretor.wasmEvalIfHelper(ast.children[self.wasmPozEval[-1]])
		if part=="then":
			thenInstr=ast.children[self.wasmPozEval[-1]]
			self.wasmPozEval[-1]+=1
			if self.wasmPozEval[-1]<len(ast.children):
				part=Interpretor.wasmEvalIfHelper(ast.children[self.wasmPozEval[-1]])
			else:
				part="done"
		if part=="else":
			elseInstr=ast.children[self.wasmPozEval[-1]]
			self.wasmPozEval[-1]+=1
			part="done"
		
		if part!="done":
			if part[:10]=="unexpected":
				return part
			return "unexpected order, "+part+" after if should be earlier"
		
		#done reading the instructions, can interpret them now
		if conditie!="":
			self.wasmPozEval.append(0)
			error=self.wasmEval(conditie)
			self.wasmPozEval.pop()
			if error!="":
				return error
		x=self.wasmPop()
		if x=="type mismatch":
			return x
		
		if x._val!=0:
			#True
			if thenInstr!="":
				self.wasmPozEval.append(0)
				error=self.wasmEval(thenInstr)
				self.wasmPozEval.pop()
				if error!="":
					return error
				return ""
			return "expected then after if"
		elif elseInstr!="":
			#False
			self.wasmPozEval.append(0)
			error=self.wasmEval(elseInstr)
			self.wasmPozEval.pop()
			if error!="":
				return error
		#returnez din if simplu deoarece se pune automat pe stiva
		return ""

	#interpreteaza block
	def wasmEvalBlock(self, ast: AST.AST):
		#sar de block
		self.wasmPozEval[-1]+=1
		
		if self.wasmPozEval[-1]>=len(ast.children):
			return ""
		
		indexBlock=self.wasmBlocksCount
		self.wasmBlocksCount+=1
		myName=""
		tipuriReturn=[]
		
		if isinstance(ast.children[self.wasmPozEval[-1]], tokenizer.Token):
			if ast.children[self.wasmPozEval[-1]].tokType=="alias":
				myName=ast.children[self.wasmPozEval[-1]].token
				if myName in self.wasmBlockAlias:
					return "block label already declared"
				self.wasmBlockAlias[myName]=indexBlock
				self.wasmPozEval[-1]+=1
			else:
				return "unexpected token "+ast.children[self.wasmPozEval[-1]].token
		
		self.wasmStack.append([])
		
		if self.wasmPozEval[-1]<len(ast.children):
			rezultat=Interpretor.wasmEvalIfHelper(ast.children[self.wasmPozEval[-1]])
			if rezultat=="result":
				for i in range(1, len(ast.children[self.wasmPozEval[-1]].children)):
					tipuriReturn.append(wasmDataTypes[ast.children[self.wasmPozEval[-1]].children[i].token])
				self.wasmPozEval[-1]+=1
		
		while self.wasmPozEval[-1]<len(ast.children):
			#conventia este ca daca trebuie sa ma intorc dintr-un block o sa am un tuplu: ("skip to block index", index_block, rezultat_block_branching)
			error=self.wasmEval(ast)
			if error!="":
				if isinstance(error, tuple):
					if error[0]=="skip to block index":
						if error[1]<indexBlock:
							#trecem peste cateva block-uri, ai grija sa faci cleanup
							if myName!="":
								del self.wasmBlockAlias[myName]
							self.wasmStack.pop()
							self.wasmBlocksCount-=1
							return error
						else:
							#sunt block-ul din care se vrea iesirea
							if myName!="":
								del self.wasmBlockAlias[myName]
							self.wasmStack.pop()
							self.wasmStack[-1]=error[2]
							self.wasmBlocksCount-=1
							self.wasmPozEval[-1]=len(ast.children)
							return ""
					else:
						if myName!="":
							del self.wasmBlockAlias[myName]
						self.wasmStack.pop()
						self.wasmBlocksCount-=1
						return error
					
				else:
					self.wasmStack.pop()
					if myName!="":
						del self.wasmBlockAlias[myName]
					self.wasmBlocksCount-=1
					return error
		
		x=self.wasmStack.pop()
		if len(x)!=len(tipuriReturn):
			self.wasmBlocksCount-=1
			return f"expected {len(tipuriReturn)} returns from block got {len(x)}"
		for i in range(len(x)):
			if type(x[i])!=tipuriReturn[i]:
				self.wasmBlocksCount-=1
				return f"block is meant to return {tipuriReturn[i]} as it's {i}-th return but returns (type={type(x)}, value={x})"
		self.wasmStack[-1].extend(x)
		if myName!="":
			del self.wasmBlockAlias[myName]
		self.wasmBlocksCount-=1
		return ""

	#keywords
	def wasmEvalKeyword(self, ast):
		t=ast.children[self.wasmPozEval[-1]]
		self.wasmPozEval[-1]+=1
		
		#verific care tip de keyword este ca sa stiu cum sa continui
		if t.token in {"module", "then", "else", "nop", "result"}:
			return ""
		
		if t.token=="drop":
			#scoate de pe stiva si nu returneaza sau executa ce urmeaza si scoate de pe stiva
			if len(ast.children)!=1:
				#executa ce urmeaza
				error=self.wasmEval(ast)
				if error!="":
					return error
			#scoate de pe stiva
			x=self.wasmPop()
			if x=="type mismatch":
				return x
			return ""
		
		if t.token=="local.get":
			#nu mai exista aliase, daca exista atunci e o eroare
			if ast.children[self.wasmPozEval[-1]].tokType=="alias":
				return "unknown label"
			self.wasmPush(self.variabileLocale[-1][Interpretor.wasmTokenToNumber(ast.children[self.wasmPozEval[-1]])])
			self.wasmPozEval[-1]+=1
			return ""
		
		if t.token=="local.tee":
			#nu mai exista aliase, daca exista atunci e o eroare
			if ast.children[self.wasmPozEval[-1]].tokType=="alias":
				return "unknown label"
			i=Interpretor.wasmTokenToNumber(ast.children[self.wasmPozEval[-1]])
			self.wasmPozEval[-1]+=1
			if len(ast.children)==self.wasmPozEval[-1]:
				#setam variabila la valoarea de pe stiva
				x=self.wasmPop()
				if isinstance(x, self.wasmDataTypesVariabileLocale[-1][i]):
					self.variabileLocale[-1][i]=x
					return ""
				return "type mismatch"
			#evaluam urmatoarea expresie si setam variabila la aceasta valoarea
			if not isinstance(ast.children[self.wasmPozEval[-1]], AST.AST):
				return "expected expresion after local.set"
			self.wasmPozEval.append(0)
			error=self.wasmEval(ast.children[self.wasmPozEval[-2]])
			self.wasmPozEval.pop()
			self.wasmPozEval[-1]+=1
			x=self.wasmPop()
			if error!="":
				return error
			if self.wasmDataTypesVariabileLocale[-1][i]!=type(x):
				return "type mismatch"
			self.variabileLocale[-1][i]=x
			self.wasmPush(x)
			return ""
		
		if t.token=="local.set":
			#nu mai exista aliase, daca exista atunci e o eroare
			if ast.children[self.wasmPozEval[-1]].tokType=="alias":
				return "unknown label"
			i=Interpretor.wasmTokenToNumber(ast.children[self.wasmPozEval[-1]])
			self.wasmPozEval[-1]+=1
			if len(ast.children)==self.wasmPozEval[-1]:
				#setam variabila la valoarea de pe stiva
				x=self.wasmPop()
				if isinstance(x, self.wasmDataTypesVariabileLocale[-1][i]):
					self.variabileLocale[-1][i]=x
					return ""
				return "type mismatch"
			#evaluam urmatoarea expresie si setam variabila la aceasta valoarea
			if not isinstance(ast.children[self.wasmPozEval[-1]], AST.AST):
				return "expected expresion after local.set"
			self.wasmPozEval.append(0)
			error=self.wasmEval(ast.children[self.wasmPozEval[-2]])
			self.wasmPozEval.pop()
			self.wasmPozEval[-1]+=1
			x=self.wasmPop()
			if error!="":
				return error
			if self.wasmDataTypesVariabileLocale[-1][i]!=type(x):
				return "type mismatch"
			self.variabileLocale[-1][i]=x
			return ""
		
		if t.token=="func":
			#definire functie
			F=wasmFunc.wasmFunc()
			ans=F.make(ast.toTokenList())
			if ans!="":
				return ans
			if F.invokeName!="":
				self.functiiWasm[F.invokeName]=F
			if F.callName!="":
				self.functiiWasm[F.callName]=F
			self.wasmPozEval[-1]=len(ast.children)
			return ""
		
		if t.token=="invoke":
			#apel functie "exemplu"
			if ast.children[self.wasmPozEval[-1]].tokType!="string":
				return "expected function name string after function invoke"
			F=self.functiiWasm[ast.children[self.wasmPozEval[-1]].token]
			self.wasmPozEval[-1]+=1
			ans=self.wasmCallFunc(ast, F)
			return ans
		
		if t.token=="call":
			#apel functie $exemplu
			if ast.children[self.wasmPozEval[-1]].tokType!="alias":
				return "expected function label after function call"
			F=self.functiiWasm[ast.children[self.wasmPozEval[-1]].token]
			self.wasmPozEval[-1]+=1
			ans=self.wasmCallFunc(ast, F)
			return ans
		
		if t.token=="i32.const":
			#va trebui sa le adaugam si pe celelalte
			self.wasmPush(i32.i32(Interpretor.wasmTokenToNumber(ast.children[self.wasmPozEval[-1]])))
			self.wasmPozEval[-1]+=1
			return ""
		
		if t.token=="i64.const":
			self.wasmPush(i64.i64(Interpretor.wasmTokenToNumber(ast.children[self.wasmPozEval[-1]])))
			self.wasmPozEval[-1]+=1
			return ""
		
		if t.token=="v128.const":
			if ast.children[self.wasmPozEval[-1]].token=="i16x8":
				#read 8 values
				self.wasmPozEval[-1]+=1
				l=[]
				for _ in range(8):
					x=Interpretor.wasmTokenToNumber(ast.children[self.wasmPozEval[-1]])
					if not isinstance(x, int):
						return x
					l.append(i16.i16(x))
					self.wasmPozEval[-1]+=1
				self.wasmPush(v128.v128(l))
				return ""
			if ast.children[self.wasmPozEval[-1]].token=="i8x16":
				#read 16 values
				self.wasmPozEval[-1]+=1
				l=[]
				for _ in range(16):
					x=Interpretor.wasmTokenToNumber(ast.children[self.wasmPozEval[-1]])
					if not isinstance(x, int):
						return x
					l.append(i8.i8(x))
					self.wasmPozEval[-1]+=1
				self.wasmPush(v128.v128(l))
				return ""
			return "expected simd type for vector"
		
		if t.token in wasmFunctiiBaza:
			#o functie aplicata pe i32 sau i64
			if isinstance(ast.children[self.wasmPozEval[-1]], AST.AST):
				self.wasmPozEval.append(0)
				x=self.wasmEvalNumber(ast.children[self.wasmPozEval[-2]])
				self.wasmPozEval.pop()
				self.wasmPozEval[-1]+=1
				if x!="":
					return x
			else:
				self.wasmEvalKeyword(ast)
			x=self.wasmPop()
			if x=="type mismatch":
				return x
			
			if wasmAritateFunctii[t.token]==2:
				if isinstance(ast.children[self.wasmPozEval[-1]], AST.AST):
					self.wasmPozEval.append(0)
					y=self.wasmEvalNumber(ast.children[self.wasmPozEval[-2]])
					self.wasmPozEval.pop()
					self.wasmPozEval[-1]+=1
					if y!="":
						return y
				else:
					self.wasmEvalKeyword(ast)
				y=self.wasmPop()
				if y=="\"type mismatch\"":
					return y
				ans=wasmFunctiiBaza[t.token](x, y)
				
				if ans=="TYPE MISMATCH":
					return "\"type mismatch\""
				if ans=="INTEGER DIVIDE BY ZERO":
					return "\"integer divide by zero\""
				if ans=="INTEGER OVERFLOW":
					return "\"integer overflow\""
				self.wasmPush(ans)
				return ""
			ans=wasmFunctiiBaza[t.token](x)
			if ans=="TYPE MISMATCH":
				return "\"type mismatch\""
			self.wasmPush(ans)
			return ""
		
		if t.token in wasmSimdFuncs:
			error=self.wasmEval(ast)
			if error!="":
				return error
			v=self.wasmPop()
			if v=="type mismatch":
				return v
			self.wasmPush(wasmSimdFuncs[t.token](v))
			return ""
		
		if t.token=="if":
			ans=self.wasmEvalIf(ast)
			return ans
		
		if t.token=="select":
			#evaluam 3 chestii, a 3-a spune care din cele 2 este pusa pe stiva/returnata
			if self.wasmPozEval[-1]+3!=len(ast.children):
				return f"expected exactly 3 expresions after select but found {len(ast.children)-self.wasmPozEval[-1]-3}"
			if not isinstance(ast.children[self.wasmPozEval[-1]], AST.AST) or not isinstance(ast.children[self.wasmPozEval[-1]+1], AST.AST) or not isinstance(ast.children[self.wasmPozEval[-1]+2], AST.AST):
				return "expected brace enclosed expresion after select"
			self.wasmPozEval.append(0)
			error=self.wasmEval(ast.children[self.wasmPozEval[-2]])
			self.wasmPozEval.pop()
			if error!="":
				return error
			self.wasmPozEval.append(0)
			error=self.wasmEval(ast.children[self.wasmPozEval[-2]+1])
			self.wasmPozEval.pop()
			if error!="":
				return error
			self.wasmPozEval.append(0)
			error=self.wasmEval(ast.children[self.wasmPozEval[-2]+2])
			self.wasmPozEval.pop()
			if error!="":
				return error
			self.wasmPozEval[-1]+=3
			z=self.wasmPop()
			if z=="type mismatch":
				return z
			y=self.wasmPop()
			if y=="type mismatch":
				return y
			x=self.wasmPop()
			if x=="type mismatch":
				return x
			if z._val:
				self.wasmPush(x)
			else:
				self.wasmPush(y)
			return ""
		
		if t.token=="return":
			self.wasmStack.append([])
			while self.wasmPozEval[-1]<len(ast.children):
				error=self.wasmEval(ast)
				if error!="":
					self.wasmStack.pop()
					return error
			return ("return from function", self.wasmStack.pop())
		
		if t.token=="br":
			if not isinstance(ast.children[self.wasmPozEval[-1]], tokenizer.Token):
				return "unspecified label or index for br"
			if ast.children[self.wasmPozEval[-1]].tokType=="alias":
				brName=ast.children[self.wasmPozEval[-1]].token
				if brName in self.wasmBlockAlias:
					brIndex=self.wasmBlockAlias[brName]
				else:
					return "unknown label"
			elif ast.children[self.wasmPozEval[-1]].tokType=="number":
				brIndex=Interpretor.wasmTokenToNumber(ast.children[self.wasmPozEval[-1]])
			else:
				return "unspecified label or index for branch"
			self.wasmPozEval[-1]+=1
			
			#evaluare rezultat
			while self.wasmPozEval[-1]<len(ast.children):
				error=self.wasmEval(ast)
				if error!="":
					return error
			
			x=self.wasmStack[-1]
			return ("skip to block index", brIndex, x)
		
		if t.token=="br_if":
			if not isinstance(ast.children[self.wasmPozEval[-1]], tokenizer.Token):
				return "unspecified label or index for branch"
			if ast.children[self.wasmPozEval[-1]].tokType=="alias":
				brName=ast.children[self.wasmPozEval[-1]].token
				if brName in self.wasmBlockAlias:
					brIndex=self.wasmBlockAlias[brName]
				else:
					return "unknown label"
			elif ast.children[self.wasmPozEval[-1]].tokType=="number":
				brIndex=Interpretor.wasmTokenToNumber(ast.children[self.wasmPozEval[-1]])
			else:
				return "unspecified label or index for br_if"
			self.wasmPozEval[-1]+=1
			
			#evaluare rezultat
			cntRez=0
			while self.wasmPozEval[-1]<len(ast.children):
				error=self.wasmEval(ast)
				cntRez+=1
				if error!="":
					return error
			
			x=self.wasmPop()
			if x=="type mismatch":
				return x
			if x._val:
				return ("skip to block index", brIndex, self.wasmStack[-1])
			for _ in range(cntRez-1):
				self.wasmPop()
			return ""
		
		if t.token=="br_table":
			if not isinstance(ast.children[self.wasmPozEval[-1]], tokenizer.Token):
				return "unspecified label or index for br_table"
			brIndices=[]
			while self.wasmPozEval[-1]<len(ast.children) and isinstance(ast.children[self.wasmPozEval[-1]], tokenizer.Token) and ast.children[self.wasmPozEval[-1]].tokType in {"alias", "number"}:
				if ast.children[self.wasmPozEval[-1]].tokType=="number":
					brIndices.append(Interpretor.wasmTokenToNumber(ast.children[self.wasmPozEval[-1]]))
				else:
					if ast.children[self.wasmPozEval[-1]].token in self.wasmBlockAlias:
						brIndices.append(self.wasmBlockAlias[ast.children[self.wasmPozEval[-1]].token])
					else:
						return "unknown label"
				self.wasmPozEval[-1]+=1
			if not len(brIndices):
				return "unspecified label or index for br_table"
			
			#evaluare rezultat
			while self.wasmPozEval[-1]<len(ast.children):
				error=self.wasmEval(ast)
				if error!="":
					return error
			
			x=self.wasmPop()
			if x=="type mismatch":
				return x
			if -1<x._val<len(brIndices):
				return ("skip to block index", brIndices[x._val], self.wasmStack[-1])
			return ("skip to block index", brIndices[-1], self.wasmStack[-1])
		
		#operatii de debug si ajutor pentru debug; se pot scoate la cerere
		if t.token=="print":
			self.wasmLogStack()
			return ""
		
		if t.token=="fulldrop":
			self.wasmStack=[]
			return ""
		
		if t.token=="leveldrop":
			self.wasmStack[-1]=[]
			return ""
		
		return "not implemented "+t.token

	#functie generala
	def wasmEval(self, ast):
		while self.wasmPozEval[-1]<len(ast.children):
			t=ast.children[self.wasmPozEval[-1]]
			#pentru debug se poate decomenta urmatoarea linie
			#print(f"Eval {t}")
			
			if isinstance(t, tokenizer.Token):
				if t.tokType=="number":
					if t.token=="unknown operator":
						return "unknown operator"
					#un numar razlet
					print(f"skipped random number encounter {t.token}")
					self.wasmPozEval[-1]+=1
				
				elif t.tokType=="assert":
					ans=self.wasmEvalAssert(ast)
					if ans!="ok":
						return ans
				
				elif t.tokType=="keyword":
					ans=self.wasmEvalKeyword(ast)
					if ans!="":
						return ans
				
				elif t.tokType=="block":
					ans=self.wasmEvalBlock(ast)
					if ans!="":
						return ans
				
				else:
					print(f"skipped {t.token} cannot interpret it")
					self.wasmPozEval[-1]+=1
				
			else:
				self.wasmPozEval.append(0)
				ans=self.wasmEval(t)
				self.wasmPozEval.pop()
				self.wasmPozEval[-1]+=1
				if ans!="":
					return ans
		return ""

#functia generala, se apeleaza o data pentru un text/cod sursa.
def interpret(code, printExecutionEnd=True):
	T=tokenizer.Tokenizer(code)
	A=AST.makeAST(T.tokens)
	errCode = ASTChecker.ASTChecker().checkAST(A)
	if errCode != "seems fine":
		print(errCode)
		return errCode

	
	if not isinstance(A, AST.AST):
		print("code cannot be interpreted because "+A)
		return A
	if not A.correct:
		print("code returns error: "+A.assertError)
		return A.assertError
	interpretor=Interpretor()
	ans=interpretor.wasmEval(A)
	if ans!="":
		print(ans)
		return ans
	if printExecutionEnd:
		print("smooth sailing")
	return ""

def interpretMultipleFiles(fisiere, printExecutionEnd=True):
	ASTs=[]
	for i in range(len(fisiere)):
		f=open(fisiere[i])
		code=tokenizer.reformat(f.readlines())
		T=tokenizer.Tokenizer(code)
		A=AST.makeAST(T.tokens)
		errCode = ASTChecker.ASTChecker().checkAST(A)
		if errCode != "seems fine":
			print(errCode)
			return errCode

		if not isinstance(A, AST.AST):
			print("code cannot be interpreted because "+A)
			return A
		if not A.correct:
			print("code returns error: "+A.assertError)
			return A.assertError
		ASTs.append(A)
	interpretor=Interpretor()
	for ast in ASTs:
		print(len(ASTs))
		ans=interpretor.wasmEval(ast)
		if ans!="":
			print(ans)
			return ans
	if printExecutionEnd:
		print("smooth sailing")
	return ""
