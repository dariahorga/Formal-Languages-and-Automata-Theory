#functia care citeste din fisier si memoreaza datele intr-un dictionar
def load_file(file_name):
file=file_name
f=open(file, "r") #deschidere pt read
d={} #initializare dictionar vid
ok=0
start=[]
final_states=[]
for line in f:
line=line.strip() #scoatem \n
if line[0]!="#": #ignoram comentariile
if line not in d and ok==0:
d[line]=[]
value=line
ok+=1
else:
if line == "End": #ajungem la capat de sectiune
ok=0 #reluam cu ok=0 pt urm sectiune
else:
if len(line.split(','))==3:
s1, s2, s3 = line.split(',')
if s2=='S':
d[value].append(s1)
start.append(s1)
final_states.append(s1)
else:
s=[s1,s3,s2]
d[value].append(s)
elif len(line.split(','))==2:
state,s=line.split(',')
if s== 'S':
start.append(state)
elif s== 'F':
final_states.append(state)
d[value].append(state)
else:
d[value].append(line)
f.close() #inchidere fisier
return (d,start,final_states)

res=load_file("nfa1.in") #dictionarul format din elementele fisierului parsat
d=res[0]
start=res[1]
final_states=res[2]
print(d)
print(start)
print(final_states)

def verify_letters(d):
if 'Sigma:' not in d or d['Sigma:']==[]: #verif daca exista letters
return False
else:
return True

def verify_states(d):
if 'States:' not in d or d['States:']==[]: #verif daca avem states
return False
else:
return True

#functie de verificare ca avem o singura stare initiala, o singura sau mai multe stari finale sau nu avem deloc stari finale/initiale
def verify_SF(start,final_states):
valid=True
if len(start)>1:
valid=False
if len(final_states)==0 and len(start)>0:
valid=False
if len(final_states)>0 and len(start)==0:
valid=False
return valid

def verify_file(d):
valid=True
for value in d['Transitions:']:
state1=value[0]
state2=value[1]
sigma=value[2] #s1=prima stare, l=litera, s2=a doua stare
if state1 not in d['States:'] or state2 not in d['States:'] or sigma not in d['Sigma:']: #verificam dc s1,s2 exista in states si l in sigma
valid=False
return valid

verify1=verify_letters(d)
verify2=verify_states(d)
verify3=verify_SF(start,final_states)
verify4=verify_file(d)


if verify1==True and verify2==True and verify3==True and verify4==True:
print ("Fisierul este in regula")
else:
print ("Fisierul nu este bun")


def dfa (string,start, d, final_states, path): #functia recursiva care verifica daca cuvantul este valid
if len(string) == 0:
for s in start:
if s in final_states:
return "accept"
else:
return "reject"
elif(len(string) != 0):
for k in range(0, len(d['Transitions:'])):
if string[0] == d['Transitions:'][k][2] and start==[d['Transitions:'][k][0]]: #verificam daca avem in ce stare sa ne ducem
path.append(d['Transitions:'][k])
start=[d['Transitions:'][k][1]]
return dfa(string[1:], start, d, final_states, path) #apelam functia pentru stringul ramas
return "reject"


f=open("input_string","r")
strings=[]
path=[]
display=[]
for line in f.readlines():
strings.append(line)
for string in strings:
display.append(dfa(string,start,d,final_states,path))
print(*display)

closure={}
for state in d['States:']:
closure[state]=[state]

print (closure)
def getClosure(d,closure,start):
closure_start=[]
for l in d['Transitions:']:
if l[2]=='e':
closure[l[0]].append(l[1])
return closure

closure=getClosure(d,closure,start)
print(closure)

nfa={}
nfa['Sigma:']=d['Sigma:']
nfa['States:']=d['States:']
nfa['Transitions:'] = []

def table_nfa(nfa,d): ##cream tabelul de transitions pt nfa
for s in nfa['States:']:
for i in nfa['Sigma:']:
transitions = []
for x in d['Transitions:']:
if x[0]==s and x[2]==i:
transitions.append(x[1])
if transitions!=[]: ##stergem dead states
nfa['Transitions:'].append([s, transitions, i])
return nfa


nfa=table_nfa(nfa,d)
print(nfa)
dfa={}
dfa['Sigma:']=nfa['Sigma:']
dfa['Transitions:']=[]
dfa['States:']=[]
def dfa_table(final_states,start,nfa,dfa):
new_start=[]
ok=False
for state in start:
if state not in dfa['States:']:
dfa['States:'].append(state)
for state in dfa['States:']:
for s in final_states:
if s in state:
ok=True
for s in start:
for sigma in nfa['Sigma:']:
transitions=[]
for t in nfa['Transitions:']:
if len(s)!=1:
for j in s:
if t[0]==j and t[2]==sigma:
for i in t[1]:
transitions.append(i)
else:
if t[0]==s and t[2]==sigma:
for i in t[1]:
transitions.append(i)
if transitions!=[] and [s,transitions,sigma] not in dfa['Transitions:']:
if len(transitions)>1:
dfa['Transitions:'].append([s,transitions,sigma])
new_start.append(transitions)
else:
dfa['Transitions:'].append([s,''.join(transitions), sigma])
new_start.append(''.join(transitions))
if ok==False:
dfa_table(final_states,new_start,nfa,dfa)
else:
return dfa


dfa=dfa_table(final_states,start,nfa,dfa)
print(dfa)
