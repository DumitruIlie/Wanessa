# Wanessa

Proiect realizat pentru cursul de Arhitectura Sistemelor de Calcul predat de domnul profesor Cristian Rusu pentru anul intai de facultate la FMI Unibuc.
Proiectul consta in construirea unui program in limbajul de programare python care sa interpreteze (cateva programe) WebAssembly.

## Cuprins

1) Utilizare
2) Functionalitate
3) Limitari
4) Echipa
5) Surse

## Utilizare

Doua moduri de utilizare, depinzand de numarul de surse ce se doreste interpretat:

Pentru interpretarea unei singure surse se ruleaza din consola:

`python3 main.py`

Veti fi intampinati de mesajul: "the file to interpret: ". Introduceti numele (cu extensie) fisierului pe care doriti sa il interpretati.

Pentru interpretarea mai multor surse se ruleaza tot din consola:

`python3 main.py nume_sursa_1 nume_sursa_2 ... nume_sursa_n`

Fisierele sunt interpretate in ordinea primita. Aceasta metoda poate de asemenea fi folosita pentru interpretarea unui singur fisier fara probleme.

## Functionalitate

Programul are cateva stagii:

1) Reformatarea codului pentru a face interpretarea mai usoara.
2) Transformarea codului reformatat in lista de tokene.
3) Transformarea listei de tokene intr-un abstract syntax tree (AST).
4) Interpretarea codului folosind o parcurgere in preordine a AST-ului.

### Reformatarea

Reformatarea codului se refera la eliminarea caracterelor de tip newLine si inlocuirea lor cu caractere spatiu, adaugarea a unui caracter spatiu inainte si dupa paranteze si eliminarea comentariilor.

### Marea tokenizare

Codul reformatat primit ca input se desparte in bucatile componente prin despartirea acestuia dupa caracterele spatiu si tab. De mentionat ca se acorda atentie la caracterele escape si caracterele whitespace in interiorul sirurilor de caractere definite in cod. Tokenele sunt perechi de forma (tip token, token) si sunt alipite intr-o lista.

### AST

Lista de tokene se proceseaza si se transforma intr-un AST in care o secventa de forma `(secventa_cod)` reprezinta un fiu al nodului curent din AST. De mentionat ca fisierul poate fi gandit drept radacina deoarece pot fi mai multe module in interiorul unui fisier, fiecare putand fi considerat un fiu al radacinii.

### Interpretarea

Pentru interpretare folosim o clasa Interpretor care contine tot codul ce tine de interpretare. Am decis sa folosim acest model pentru a permite sa rulam cod din cod (keywordul quote) si pentru a nu polua scope-ul unui fisier cu un altul in cazul link-ingului si al verificarii validitatii unor proceduri (assert_invalid).

Functia principala este interpret, aceasta se apeleaza o singura data pentru lista de linii ce reprezinta codul de executat. Aceasta face cei 3 pasi mentionati anterior si in cazul in care nu apare nici o problema creaza un obiect din clasa Interpretor care este apoi folosit pentru interpretare. In mare clasa Interpretor interpreteze un AST in mai multi pasi apeland recursiv metodele clasei.

## Limitari

Standardul WebAssembly permite definirea unor semnaturi speciale pentru functii care pot deveni mai departe tipuri de date (un fel de pointer la functie din C declarat cu typedef). Programul nostru nu permite asa ceva si la intalnirea unei asemenea definiri va returna o eroare.

Operatiile in virgula mobila nu sunt definite, programul nostru nu are functionalitatea de a interpreta alte tipuri de date decat numere intregi (cu sau fara semn), totusi am creat o librarie cu fixed point ce poate fi folosita (destul de rudimentara, lipseste impartirea, momentan). Blocurile de loop nu sunt implementate (inca). Nu exista pointeri, deci nici vectori. Nu exista conceptul de memorie, memorie globala.

## Echipa

Echipa noastra este formata din:

1) Brabete Marius-Stelian - Restructurarea codului intr-un mod object oriented
2) Buzatu Giulian - Ajutor la reverse engineering pe teste
3) Ilie Dumitru - Interpretorul si teste aditionale
4) Popescu Stefan-Alexandru - Documentare si lucru cu erori "ciudate"

Toti suntem din grupa 152.

## Surse

[Documentatia WebAssembly](https://webassembly.github.io/spec/core/)
[Interpretor Tom Stuart](https://github.com/tomstuart/wasminna)
[YouTube Tom Stuart](https://www.youtube.com/@tom.stuart)
