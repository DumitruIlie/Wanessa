import interpretor as interp
import tokenizer
import AST

def main():
	interpretedFileName=input("the file to interpret: ")
	interpretedFile=open(interpretedFileName)
	code=tokenizer.reformat(interpretedFile.readlines())
	interp.interpret(code)

if __name__=="__main__":
	main()