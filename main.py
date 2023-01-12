import interpretor
import tokenizer
import AST

def main():
	interpretedFileName=input("the file to interpret: ")
	interpretedFile=open(interpretedFileName)
	code=interpretedFile.readlines()
	code=tokenizer.reformat(code)
	interpretor.interpret(code)

def dbgmain():
	interpretedFileName=input("the file to interpret: ")
	interpretedFile=open(interpretedFileName)
	code=interpretedFile.readlines()
	code=tokenizer.reformat(code)
	print(AST.makeAST(tokenizer.Tokenizer(code).tokens))

if __name__=="__main__":
	main()
	#dbgmain()