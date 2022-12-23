f = open("cod_wasm.txt")
s = ""
for line in f:
    line = line.replace("(", " ")
    line = line.replace(")", " ")
    line.replace("'\n'", " ")
    s += " " + line + " "
f.close()
# acum avem in s toate cuvintele din fisier, fara paranteze
L = s.split()
d = {x: L.count(x) for x in L}
# am mutat toate cuvintele care apar in dictionarul de forma cuvant:frecventa
g = open("decodare.txt", "w")
for x in d.keys():
    g.write(x + "\n")
g.close()
