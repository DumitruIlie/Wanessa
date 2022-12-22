import interpretor as interp
import tokenizer

interpretedFileName=input("the file to interpret: ")
interpretedFile=open(interpretedFileName)
code=tokenizer.reformat(interpretedFile.readlines())
interp.interpret(code)

# de cautat Big number