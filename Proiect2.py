
#facem citirea din fisier si creem un dictionar de date
f=open("inputNFA4..txt")
s=f.readline()
stari_finale=s.strip().split()
print("stari finale="+s)
dictionardedate={}
s=f.readline()
while s!='':
    lista=s.strip().split()
    primel=lista[0]
    if primel not in dictionardedate:
        dictionardedate[primel]={}
    if lista[2] not in dictionardedate:
        dictionardedate[lista[2]]={}
    if lista[1] not in dictionardedate[primel]:
        dictionardedate[primel][lista[1]]=[lista[2]]
    else:
        dictionardedate[primel][lista[1]].append(lista[2])
    s=f.readline()

#retinem starea initiala
for x in dictionardedate:
    stareinitiala=x
    break
# #citim un cuvant
# #creem o variabila in care sa retinem starea curenta si un sir in care sa retin drumurile
drumuri=stareinitiala
starecurenta=stareinitiala
b=1
ok=0
i=0
listadrumuri=[]

print(f"dictionardedate: {dictionardedate}")

#ma folosesc de dictionarul creat pentru a retine datele despe nfa pt primul
#pas din transformare

#pasul 2:calculez lambda inchiderile pentru fiecare stare
Lambdainchideri={}
for stare in dictionardedate:
    if stare not in Lambdainchideri:
        Lambdainchideri[stare]=[stare]

def Lambda_closures(dictionardedate, starecurenta,listastari):
    if 'lambda' in dictionardedate[starecurenta]:  # parcurgem lista de tranzitii pentru fiecare stare
        for drum_posibil in dictionardedate[starecurenta]['lambda']:
            if drum_posibil not in listastari:
                listastari.append(drum_posibil)
                Lambda_closures(dictionardedate, drum_posibil,listastari)
    return listastari
for starecurenta in dictionardedate:
    listastari=[]
    listaa=[]
    if Lambda_closures(dictionardedate, starecurenta, listastari) is not None:
        listaa=Lambda_closures(dictionardedate,starecurenta,listastari)
    for x in listaa:
        if x!=starecurenta:
            Lambdainchideri[starecurenta].append(x)
            Lambdainchideri[starecurenta].sort()
print(f"Lambdainchideri: {Lambdainchideri}")

#pasul 3:calculez tabelul
#retin tipurile de tranzitii
tranzitii=[]
for stari in dictionardedate:
    for tranzitie in dictionardedate[stari]:
        if tranzitie!='lambda' and tranzitie not in tranzitii:
            tranzitii.append(tranzitie)

#creez tabelul
dictionartranzitii={}
for stare in dictionardedate:
    dictionartranzitii[stare] = {}
    for x in tranzitii:
        dictionartranzitii[stare][x]=[]

#calculez valorile din tabel
listacuvinte=[]
for stare in dictionartranzitii:
        drumuri=set()
        aux=set()
        for tranzitie in dictionartranzitii[stare]:#dictionartranzitii[stare]: #suntem pe coloanele tabelei
            cuvinte=''
            for x in Lambdainchideri[stare]: #parcurgem lambdatranzitiile pt fiecare stare
                if tranzitie in dictionardedate[x]:
                    for y in dictionardedate[x][tranzitie]:
                        drumuri.add(y)
            for z in list(drumuri):
                for l in Lambdainchideri[z]:
                    aux.add(l)
            dictionartranzitii[stare][tranzitie]=sorted(aux)
            for x in dictionartranzitii[stare][tranzitie]:
                cuvinte=cuvinte+x
            listacuvinte.append(cuvinte)
            cuvinte=''
            drumuri=set()
            aux=set()
print(f"dictionartranzitii: {dictionartranzitii}")
#pasul 4
#obtinem starile noului automat
stariDFA={}
stareinitialaDFA=''
stivaDFA=[]
ok=0
listastarilorfinaleDFA=[]
for x in Lambdainchideri[stareinitiala]:
    stareinitialaDFA=stareinitialaDFA+x
    if x in stari_finale:
        ok=1
if ok == 1:
    listastarilorfinaleDFA.append(stareinitialaDFA)

stivaDFA.append(stareinitialaDFA)
stariDFA[stareinitialaDFA]={}
for x in tranzitii:
    cuvinte=''
    stariDFA[stareinitialaDFA][x]=dictionartranzitii[stareinitiala][x]
    for y in stariDFA[stareinitialaDFA][x]:
        cuvinte = cuvinte + y

while len(stivaDFA)>0:
    stare_curenta=stivaDFA.pop(0)
    # pentru fiecare tranzitie existenta din starea curenta
    for tranzitie_ in stariDFA[stare_curenta]:
        stare_din_tranzitie = ''.join(stariDFA[stare_curenta][tranzitie_])

        if stare_din_tranzitie not in stariDFA and stare_din_tranzitie!='':
            # daca starea pe care a gasit-o nu a fost deja calculata,
            # se adauga in dictionar si in coada
            stariDFA[stare_din_tranzitie] = {}
            stivaDFA.append(stare_din_tranzitie)

            #verific care sunt starile finale cu un ok
            ok=0
            for l in stariDFA[stare_curenta][tranzitie_]:
                if l in stari_finale:
                    ok=1
                    break
            if ok==1:
                listastarilorfinaleDFA.append(stare_din_tranzitie)

            # calculeaza starile in care poate sa ajunga starea adaugata
            drumuri = set()
            aux = set()
            for tr in tranzitii:  # dictionartranzitii[stare]: #suntem pe coloanele tabelei
                for ministare in stariDFA[stare_curenta][tranzitie_]:
                    for x in Lambdainchideri[ministare]:  # parcurgem lambdatranzitiile pt fiecare stare
                        if tr in dictionardedate[x]:
                            for y in dictionardedate[x][tr]:
                                drumuri.add(y)
                    for z in list(drumuri):
                        for l in Lambdainchideri[z]:
                            aux.add(l)
                    stariDFA[stare_din_tranzitie][tr] = sorted(aux)
                drumuri = set()
                aux = set()

print(listastarilorfinaleDFA)
print(stariDFA)


