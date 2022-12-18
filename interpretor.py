#citeste un element din cod: pana acum are functionalitate pentru '(', ')' si siruri de caractere care nu contin ' ' sau '\t'
#returneaza un tuplu format dintr-un string ce reprezinta elementul citit si pozitia din cod la care a ramas citirea.
def readElement(code, pos):
	while pos<len(code) and (code[pos]==' ' or code[pos]=='\t'):
		pos+=1
	if pos==len(code):
		return -1
	#un element incepe aici
	if code[pos]=='(' or code[pos]==')':
		return (code[pos], pos+1)
	L=[]
	while pos<len(code) and code[pos]!=' ' and code[pos]!='\t' and code[pos]!='(' and code[pos]!=')':
		L.append(code[pos])
		pos+=1
	return ("".join(L), pos)

StivaProgram=[]

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

#functie recursiva, returneaza pozitia din cod unde a ramas cu interpretarea
def interpretCode(code, pos):
	while (x:=readElement(code, pos))!=-1:
		if x[0]=="i32.add":
			#ceva de genul "citeste termen" "citeste termen" "adauga termen0 si termen1"
			#momentan e tarziu, nu mai stau sa fac ca lumea
			pushStiva(1)
			pushStiva(2)
			i32add()
			print(popStiva(), end='')
			#cumva trebuie sa discutam despre ce si cum facem prostiile astea de automate
		print(x[0])
		pos=x[1];
		if x[0]=='(':
			pos=interpretCode(code, pos)
		elif x[0]==')':
			return pos

def interpret(code):
	initStiva()
	interpretCode(code, 0)