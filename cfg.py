#functie de incarcare date din fisier

def load_grammar(file):

    grammar = {} #dictionar pentru gramatica CFG-ului

    with open(file, "r") as f:

        for line in f:

            line = line.strip() #stergem \n

            if line:

                lefts, rights = line.split("->") #dam split in variabila si lista de terminali

                lefts = lefts.strip()

                rights = [x.strip() if x.strip() != "epsilon" else '' for x in rights.split("|")] #luam fiecare terminal daca exista mai multi (de ex "dog | cat" sa fie luate separat)

                if lefts in grammar: #daca variabila e deja in dict

                    grammar[lefts].extend(rights) #adaugam elementele in continuarea listei

                else:

                    grammar[lefts] = rights #altfel lista respectiva devine chiar lista de terminali

    print("Dictionarul cu regulile CFG-ului: ", grammar)

    return grammar



#functia de validare a gramaticii

def validate_grammar(grammar):

    start_symbol = list(grammar.keys())[0] #prima cheie din dict este simbolul de start (variabila din prima regula)

    visited = set() #facem o multime visited care ne arata pe unde am fost pana acum

    visited.add(start_symbol)

    stack = [start_symbol]

    while stack:

        symbol = stack.pop() #cat timp stiva nu e goala, scoatem un simbol din ea

        if symbol in grammar: #daca simbolul este variabila (nu e terminal)

            for e in grammar[symbol]: #luam lista de terminali

                if e == '':

                    continue

                for s in e.split(): #ii dam split in simboluri ca sa le luam individual

                    if s not in visited: #daca nu am trecut pana acm prin simbol

                        visited.add(s) #il adaugam multimii

                        stack.append(s) #si il si punem pe stiva

    for symbol in grammar.keys(): #luam fiecare simbol dintre cheile dictionarului (variabile nu terminali)

        if symbol not in visited: #daca simbolul respectiv nu se afla si in multimea visited inseamna ca nu se poate ajunge la el => invalid

            raise ValueError(f"La simbolul {symbol} nu se poate ajunge") #ridicam eroare ca sa nu mai continue programul

    print(visited)



# Load the grammar from a file

file = "2.4_g"

grammar = load_grammar(file)



print("Grammar:")

for lefts, rights in grammar.items(): #mergem in dictionar simultan si cu cheie si cu valoare ca sa le printam cum le-am primit in input file

    print(f"{lefts} -> {' | '.join(rights)}") #printam variabila apoi -> apoi concatenam cu "|" toate simbolurile din dreapta



# Validate the grammar

validate_grammar(grammar) #apelam functia si daca e valid poate trece la urmatoarea linie si deci o sa afiseze valid

print("CFG valid!")

