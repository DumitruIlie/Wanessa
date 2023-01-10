class v128:
    def __init__(self,type,list):
        self._type = type
        self._v = [int(x) for x in list]
        if(int(type.split("x")[1])==16):
            self._v += [0 for _ in range(8)]
    def __str__(self):
        strr = ""
        for x in self._v:
            strr += str(x) + " "
        strr = strr[:-1]
        return f"{self._type} {strr}"

