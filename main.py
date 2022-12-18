import interpretor as interp

interpretedFileName=input("the file to interpret: ")
interpretedFile=open(interpretedFileName)
interp.interpret("".join(interpretedFile.readlines()))