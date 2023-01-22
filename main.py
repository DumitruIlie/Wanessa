import Interpretor
import sys

def main():
	argv=sys.argv
	argc=len(argv)
	
	if argc==1:
		interpretedFileName=input("the file to interpret: ")
		Interpretor.interpretMultipleFiles([interpretedFileName])
	else:
		Interpretor.interpretMultipleFiles(argv[1:])

if __name__=="__main__":
	main()