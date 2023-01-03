import interpretor
import tokenizer
import AST

def main():
	interpretedFileName=input("the file to interpret: ")
	interpretedFile=open(interpretedFileName)
	code=interpretedFile.readlines()
	code=tokenizer.reformat(code)
	interpretor.interpret(code)

if __name__=="__main__":
	main()