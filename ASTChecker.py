import Interpretor
import tokenizer
import AST

class ASTChecker:
    def __init__(self):
        pass

    def checkIfToken(self, nod : AST):
        # se uita la urmasii unui nod de AST de tip "if";
        # daca gaseste token-uri care nu se potrivesc cu structura if-ului returneaza
        # "unexpected token"
        for nodUrmas in nod.children[1:]:
            tipToken = Interpretor.Interpretor.wasmEvalIfHelper(nodUrmas)
            if "unexpected" in tipToken:
                return "unexpected token"
                
        
        return "seems fine"


    def checkAST(self, nod : AST):
        # primeste un nod de AST, il incadreaza 
        # intr-un tip de bloc de control si ii verifica structura
        if not isinstance(nod.children[0], tokenizer.Token):
            return "unexpected token"
        
        # daca nodul este de tip "if"
        # atunci verifica daca structura e buna
        errUrm = "seems fine"
        if nod.children[0].token == "if":
            errUrm = self.checkIfToken(nod)
        if errUrm != "seems fine":
            return errUrm

        # pentru fiecare nod AST urmas al nodului actual se 
        # verifica recursiv validitatea sa
        for nodUrmator in nod.children:
            if isinstance(nodUrmator, AST.AST):
                errUrm = self.checkAST(nodUrmator)
                if errUrm != "seems fine":
                    return errUrm

        return "seems fine"
