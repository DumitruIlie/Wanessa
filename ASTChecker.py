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
        for nodUrmas in nod.children:
            if isinstance(nodUrmas, AST.AST):
                tipToken = Interpretor.Interpretor.wasmEvalIfHelper(nodUrmas)
                if "unexpected" in tipToken:
                    return "unexpected token"
                
        return "seems fine"

    def checkConstToken(self, nod : AST):
        # un nod cu label-ul const ar trebui sa primeasca doar un numar, deci 2 tokeni
        if len(nod.children) < 2 or \
            not isinstance(nod.children[0], tokenizer.Token) or not isinstance(nod.children[1], tokenizer.Token):
            
            return "unexpected end of node"
        
        
        # daca const-ul e de tip int si numarul e float atunci returneaza "unexpected token"
        if nod.children[0].token[0] == "i" and nod.children[1].token[:3] == "nan":
            return "unexpected token"
        return "seems fine"

    def checkAST(self, nod : AST):
        # primeste un nod de AST, il incadreaza 
        # intr-un tip de bloc de control si ii verifica structura
    
        
        # daca nodul este de tip "if"
        # atunci verifica daca structura e buna
        if not isinstance(nod, AST.AST):
            return "expected expresion but found "+nod
        errUrm = "seems fine"
        if len(nod.children) > 0 and isinstance(nod.children[0], tokenizer.Token):
            # are label nodul actual
            if nod.children[0].token == "if":
                errUrm = self.checkIfToken(nod)
            elif nod.children[0].token[-5:] == "const": # daca avem de extras un numar dintr-un string
                errUrm = self.checkConstToken(nod)

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
