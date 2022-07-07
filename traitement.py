import timeit
start= timeit.default_timer()
import re
import lexique as lex
filename = './resource/Token.txt'

#Écrir tous les token dans le liste
with open(filename,encoding='utf-8-sig') as f:
	tokenListe=[]
	for i in f.readlines():
		tokenListe.append(i.strip('\n'))


def chunker(liste):
    '''<=== parcourir le texte de token par l'indice de l'élément ===>'''
    for i in range(len(liste)):
        '''<=== Commencez à identifier les "chunk_N", "chunk_PN" et "chunk_SV" par la localisation assistée par marqueur. ===>'''
        if liste[i] in lex.dico_marq:
            '''<-------------------- Commencer à identifier -------------------->'''
            '''
            Parce que la longueur maximale du chunk d'article est de 2 tokens.
            Pour éviter que le parcours de l'indice ne dépasse la longueur de l'élément pour signaler une erreur,
            la longueur de l'élément est avancée de -2.
            '''
            if i <= len(liste)-5:
                #<-------------------- Commencer à identifier "chun_N" -------------------->
                #====>localisé par le marqueur,existent "chunk_N" seul c'est "unaire N".
                N1 = lex.dico[liste[i]]
                #====>localisé par le marqueur,existent "chunk_N" NOM ou NAM précédé d'un article coronal ou numérique, c'est "dualiste N".
                N2 = lex.dico[liste[i]]+lex.dico[liste[i+1]]
                #régle de unaire N
                re_regleN1 = 'NOM|NAM'
                regleN1 = re.search(re_regleN1,N1)
                #régle de dualiste N
                re_regleN2 = '(NUM|DET).*?(NOM|NAM).*?(ADJ)?'
                regleN2 = re.search(re_regleN2,N2)

                #<-------------------- Commencer à identifier "chunk_N" unaire/dualiste/ternaire -------------------->
                '''
                Pour "regleN2", il y a 3 cas:
                1.Le token précédent d'un token avec cat NOM|NAM ne peut pas être lesPRP et PRO, et le mot suivant n'est pas ADJ
                2.cat pour le token "NOM|NAM" a PRO(ex.Tout) avant la préposition précédente [ternaire]
                3.cat pour le token "NOM|NAM" a token après qui est "ADJ" [ternaire]
                '''
                if regleN2:
                    #cas 1
                    if not re.search('PRP|PRO',lex.dico[liste[i-1]]) and not re.search('ADJ',lex.dico[liste[i+2]]):
                        print('【' + 'Règle:',re_regleN2,'[Chunk:N',liste[i],liste[i+1] + ']'+"】", file = open ("Output.txt","a"))
                    #cas 2
                    elif re.search('PRO',lex.dico[liste[i-1]]):
                        print('【' + 'Règle:',re_regleN2,'[Chunk:N',liste[i-1],liste[i],liste[i+1]+ ']'+"】", file = open ("Output.txt","a"))
                    #cas 3
                    elif re.search('ADJ',lex.dico[liste[i+2]]):
                        print('【' + 'Règle:',re_regleN2,'[Chunk:N',liste[i],liste[i+1],liste[i+2]+ ']'+"】", file = open ("Output.txt","a"))

                #regleN1 identifie monadique N "chunk_N"
                elif regleN1 and not re.search('DET',lex.dico[liste[i-1]]):
                    '''
                    Identifier seulement les cas où "NOM|NAM" se produit seul
                    Donc en excluant le cas où le premier est "DET"
                    Parce que c'est le seul cas où ce texte monadique N se produit
                    La reconnaissance est donc plus dépendante du texte
                    '''
                    print('【' + 'Règle:',re_regleN1,'[Chunk:N',liste[i]+ ']'+"】", file = open ("Output.txt","a"))


                #<-------------------- Commencer à identifier le "chunk_PN " -------------------->
                #====>"Chunk_PN","dualiste"et "ternaire" => localisé par le marqueur (PRP ou KON)
                #dualiste
                Pn2 = lex.dico[liste[i]]+lex.dico[liste[i+1]]
                #ternaire
                Pn3 = lex.dico[liste[i]]+lex.dico[liste[i+1]]+lex.dico[liste[i+2]]
                #PL'expression régulière des règles de "PN"
                re_reglePN = '(PRP|KON).*?(NOM|NAM).*?(ADJ)?'
                #Identification et recherche
                reglePN2 = re.search(re_reglePN,Pn2)
                reglePN3 = re.search(re_reglePN,Pn3)

                '''
                Trois cas existent :
                1.dualiste "PN" et sans modificateur "ADJ"
                2.ternaire PN", avec modificateur "ADJ"
                3.Après une identification réussie du "PN" ternaire,
                le "KON: est exclu en tant que conjonction (et, and), 
                et s'il y a un verbe dans la structure, et si le premier token est un nom.
                '''

                #Cas 1:
                if reglePN2 and lex.dico[liste[i+2]] != 'ADJ':
                    print('【' + 'Règle:',re_reglePN,'[Chunk:PN',liste[i],liste[i+1]+ ']'+"】", file = open ("Output.txt","a"))
                    #Cas 2:
                    if lex.dico[liste[i+2]] == 'ADJ':
                        print('【' + 'Règle:',re_reglePN,'[Chunk:PN',liste[i],liste[i+1],liste[i+2]+ ']'+"】", file = open ("Output.txt","a"))
                #Cas 3:
                elif reglePN3:
                    if liste[i] != 'et' and liste[i] != 'and' and lex.dico[liste[i+1]] != 'VER_infi' and lex.dico[liste[i]] != 'NOM':
                        print('【' + 'Règle:',re_reglePN,'[Chunk:PN',liste[i],liste[i+1],liste[i+2]+ ']'+"】", file = open ("Output.txt","a"))





                #<-------------------- Commencer à identifier le "chunk_SV" -------------------->
                #====> "Chunk_PN" localisé par le marqueur (PRP ou KON)
                Sv2 = lex.dico[liste[i]] + lex.dico[liste[i+1]]
                Sv4 = lex.dico[liste[i]] + lex.dico[liste[i+1]] + lex.dico[liste[i+2]] + lex.dico[liste[i+3]]
                Sv5 = lex.dico[liste[i]] + lex.dico[liste[i+1]] + lex.dico[liste[i+2]] + lex.dico[liste[i+3]]+ lex.dico[liste[i+4]]
                #"SVregle" dualiste
                re_regleSV2 = 'PRO_PERVER_pres'
                #"Vregle" quadratique
                re_regleSV4 = 'PRO.*?ADV_negVER.*?ADV'
                #"SVregle" quintuplet
                re_regleSV5 = 'PRO.*?ADV_negPRO.*?ADV'
                #Identification par règles
                regleSV2 = re.search(re_regleSV2,Sv2)
                regleSV4 = re.search(re_regleSV4,Sv4)
                regleSV5 = re.search(re_regleSV5,Sv5)

                '''
                Trois cas existent ::
                1. PRO + verbe conjugué VER
                2. PRO + verbe conjugué VER+ verbe initial+(modificateur (ADV ou et ADJ))
                3. Il y a des pronoms autoréflexifs
                4. Présence d'adverbes négatifs
                5. Présence de pronoms et d'adverbes négatifs (y)
                '''
                #La composition des pronoms autoréflexifs n'est pas prise en compte
                if regleSV2 and liste[i] != 'se':
                    #Pas de modificateur ADJ|ADV
                    if not re.search(r'ADJ|ADV',lex.dico[liste[i+3]]):
                        #case 2(Pas de modificateur "ADJ|ADV")
                        if lex.dico[liste[i+2]] == 'VER_infi':
                            print('【' + 'Règle:',re_regleSV2,'[Chunk:SV',liste[i],liste[i+1],liste[i+2]+ ']'+"】", file = open ("Output.txt","a"))
                        #case 1(Pas de verbe initial)
                        else:
                            print('【' + 'Règle:',re_regleSV2,'[Chunk:SV',liste[i],liste[i+1]+ ']'+"】", file = open ("Output.txt","a"))
                    #case 2(Présence du modificateur "ADJ|ADV")
                    else:
                        #Présence du modificateur "ADJ"
                        if re.search(r'ADJ',lex.dico[liste[i+3]]):
                            print('【' + 'Règle:',re_regleSV2,'[Chunk:SV',liste[i],liste[i+1],liste[i+2],liste[i+3]+ ']'+"】", file = open ("Output.txt","a"))
                        #Présence du modificateur "ADV"
                        elif re.search(r'ADV',lex.dico[liste[i+3]]):
                            print('【' + 'Règle:',re_regleSV2,'[Chunk:SV',liste[i],liste[i+1],liste[i+2],liste[i+3],liste[i+4],liste[i+5]+ ']'+"】", file = open ("Output.txt","a"))
                #case 3
                elif regleSV2 and liste[i] == 'se' and re.search(r'PRO',lex.dico[liste[i-1]]):
                    print('【' + 'Règle:',re_regleSV2,'[Chunk:SV',liste[i-1],liste[i],liste[i+1],liste[i+2]+ ']'+"】", file = open ("Output.txt","a"))
                #case 4
                elif regleSV4:
                    print('【' + 'Règle:',re_regleSV4,'[Chunk:SV',liste[i],liste[i+1],liste[i+2],liste[i+3]+ ']'+"】", file = open ("Output.txt","a"))
                #case 5
                elif regleSV5:
                    print('【' + 'Règle:',re_regleSV5,'[Chunk:SV',liste[i],liste[i+1],liste[i+2],liste[i+3],liste[i+4]+ ']'+"】", file = open ("Output.txt","a"))

        #<-------------------- Commencer à identifier "chunk_Pvant", "chunk_Pver" et "chunk_V" -------------------->
        #Parce que la structure de "Pvant", "Pver" et "V" est simple, le noyau est "VER"
        #Donc seule cette règle est nécessaire, et ensuite selon le mot avant et après pour déterminer qui appartient à chacun.
        re_regleVx = 'VER'
        Vx = lex.dico[liste[i]]
        regleVx = re.search(re_regleVx,Vx)
        #Tout d'abord, il doit correspondre aux règles, et le token précédent ne doit pas être "PRO|ADV|VER"
        if regleVx and not re.search(r'PRO|ADV|VER',lex.dico[liste[i-1]]):
            #si le token précédent est "PRP"
            if re.search(r'PRP',lex.dico[liste[i-1]]):
                #Et si le token lui-même est au participe présent, alors c'est tout "Pvant"
                if lex.dico[liste[i]].endswith('ppre'):
                    #"Pvant" avec modifications "ADJ"
                    if re.search(r'ADJ',lex.dico[liste[i+1]]):
                        print('【' + 'Règle:',re_regleVx,'[Chunk:PVant',liste[i-1],liste[i],liste[i+1] + ']'+"】", file = open ("Output.txt","a"))
                    #"Pvant" sans modifications "ADJ"
                    else:
                        print('【' + 'Règle:',re_regleVx,'[Chunk:PVant',liste[i-1],liste[i] + ']'+"】", file = open ("Output.txt","a"))
                #如Si le token lui-même n'est pas un participe présent, alors c'est "Pver"
                else:
                    print('【' + 'Règle:',re_regleVx,'[Chunk:PVer',liste[i-1],liste[i] + ']'+"】", file = open ("Output.txt","a"))
            #A l'exclusion des cas où le token suivant  est "VER|ADJ"
            elif re.search(r'ADJ|VER|ADV',lex.dico[liste[i+1]]):
                #Si ce dernier token est "ADV" pour le modifier
                if re.search(r'ADV',lex.dico[liste[i+1]]):
                    print('【' + 'Règle:',re_regleVx,'[Chunk:V',liste[i],liste[i+1],liste[i+2] + ']'+"】", file = open ("Output.txt","a"))
                #Si le dernier token n'est pas "ADV" pour le modifier
                else:
                    print('【' + 'Règle:',re_regleVx,'[Chunk:V',liste[i],liste[i+1] + ']'+"】", file = open ("Output.txt","a"))
            #Ce qui reste est la "VER" qui existe distinctement 
            else:
                print('【' + 'Règle:',re_regleVx,'[Chunk:V',liste[i] + ']'+"】", file = open ("Output.txt","a"))


        #<-------------------- Commencer à identifier les "chunk_ADV" qui apparaissent distinctement-------------------->
        re_regleADV = 'ADV'
        Adv = lex.dico[liste[i]]
        regleADV = re.search(re_regleADV,Adv)
        if regleADV and not lex.dico[liste[i]].endswith('fon') and not lex.dico[liste[i]].endswith('neg') and not re.search('ADV|ADJ|VER|PRO|KON',lex.dico[liste[i+1]]):
            print('【' + 'Règle:',re_regleADV,'[Chunk:ADV',liste[i] + '】', file = open ("Output.txt","a"))

        #<-------------------- Commencer à identifier les "chunk_CO,chunk_CS" qui apparaissent distinctement -------------------->
        re_regleCoCs = 'KON'
        CoCs = lex.dico[liste[i]]
        regleCOCS = re.search(re_regleCoCs,CoCs)
        if regleCOCS:
            if liste[i] == 'et' or liste[i] == 'and':
                print('【' + 'Règle:',re_regleCoCs,'[Chunk:CO]',liste[i] + '】', file = open ("Output.txt","a"))
            elif liste[i] == 'mais':
                print('【' + 'Règle:',re_regleCoCs,'[Chunk:CS]',liste[i] + '】', file = open ("Output.txt","a"))
            elif re.search('KON|ADV',lex.dico[liste[i-1]]) and not lex.dico[liste[i-1]].endswith('neg'):
                print('【' + 'Règle:',re_regleCoCs,'[Chunk:CS]',liste[i-1],liste[i] + '】', file = open ("Output.txt","a"))
        
        #<-------------------- Commencer à identifier les "PRelS" qui apparaissent distinctement -------------------->
        re_reglePRelS= 'PRelS'
        PRelS = lex.dico[liste[i]]
        reglePRelS = re.search(re_reglePRelS,PRelS)
        if reglePRelS:
            print('【' + 'Règle:',re_reglePRelS,'[Chunk:PRelS',liste[i] + ']'+ '】', file = open ("Output.txt","a"))


        #<-------------------- Reconnaissance directe de la ponctuation  -------------------->
        if liste[i] in lex.dico_punc:
            print('【' +'[Chunk:PCT(N)F',liste[i] + ']'+ '】', file = open ("Output.txt","a"))



        #<--------------------  Commencer à identifier les "Vse" qui apparaissent distinctement.-------------------->
        re_regleVse = 'PRO'
        Vse = lex.dico[liste[i-1]]
        regleVse = re.search(re_regleVse,Vse)
        if liste[i] == "s'" or liste[i] == "se" and not regleVse:
            print('【' + 'Règle:',re_regleVse,'[Chunk:Vse',liste[i],liste[i+1] + ']'+ '】',file = open ("Output.txt","a"))


chunker(tokenListe)
# <--si vous voulez lancer 2ème fois de programme, veuillez d'abord supprimer le "Output.txt" de la première exécution.-->

#Calcluer la durée du processus
end= timeit.default_timer()
time = str(end-start)
print('Durée du processus:',end-start)

#Ajouter le contenu du texte dans le fichier "Output.txt"
with open("Texte original.txt","r",encoding="utf-8") as f:
    data = f.read()
    text = "Texte origianl: "+ "\n"+ data + "\n"

#Ajouter les résultats de Chunk dans le fichier "Output.txt"
with open("Output.txt","r+") as f:
    old = f.read()
    f.seek(0)
    f.write(text)
    f.write(old)

#Ajouter le durée du processus dans le fichier "Output.txt"
with open("Output.txt","r+") as f:
    old = f.read()
    f.seek(0)
    f.write('Durée du processus:'+time+"\n"+"\n")
    f.write(old)

#Ouvrir le fichier "Output.txt", pour calculer des nombres
with open("Output.txt","r",encoding="utf-8") as f:
    Text = f.read()

#calculer les nombres et les ajouter dans le fichier "Output.txt"
file = open("Output.txt",'a')
file.write("----------------"*5+"\n")

#nombre total de Chunk  
num1=Text.count("Chunk:")
num=str(num1)
print("Nombre de Chunk: ", num)
t1 = "Nombre de Chunk :"+num
file.write(t1+"\n")

#nombre de "Chunk:N"
c1=Text.count("Chunk:N")
cp1= "%.2f%%" % (c1/num1 * 100)
c1=str(c1)
print("Nombre de 'Chunk:N': ",c1,"\t","Pourcentage: ",cp1)
ct1 = "Nombre de 'Chunk:N':"+c1+"\t"+"Pourcentage: "+"("+cp1+")"
file.write(ct1+"\n")

#nombre de "Chunk:V"
"""
Attention: ici on un espace après le V.
Sinon le programme va aussi calculer les autres Chunk.
【Chunk:Vse】
"""
c2=Text.count("Chunk:V ")
cp2= "%.2f%%" % (c2/num1 * 100)
c2=str(c2)
print("Nombre de 'Chunk:V': ",c2,"\t","Pourcentage: ",cp2)
ct2 = "Nombre de 'Chunk:V':"+c2+"\t"+"Pourcentage: "+"("+cp2+")"
file.write(ct2+"\n")

#nombre de "Chunk:PVer"
c3=Text.count("Chunk:PVer")
cp3= "%.2f%%" % (c3/num1 * 100)
c3=str(c3)
print("Nombre de 'Chunk:PVer': ",c3,"\t","Pourcentage: ",cp3)
ct3 = "Nombre de 'Chunk:PVer':"+c3+"\t"+"\t"+"Pourcentage: "+"("+cp3+")"
file.write(ct3+"\n")

#nombre de "Chunk:PCT(N)F"
c4=Text.count("Chunk:PCT(N)F")
cp4= "%.2f%%" % (c4/num1 * 100)
c4=str(c4)
print("Nombre de 'Chunk:PCT(N)F': ",c4,"\t","Pourcentage: ",cp4)
ct4 = "Nombre de 'Chunk:PCT(N)F':"+c4+"\t"+"Pourcentage: "+"("+cp4+")"
file.write(ct4+"\n")

#nombre de "Chunk:PN"
c5=Text.count("Chunk:PN")
cp5= "%.2f%%" % (c5/num1 * 100)
c5=str(c5)
print("Nombre de 'Chunk:PN': ",c5,"\t","Pourcentage: ",cp5)
ct5 = "Nombre de 'Chunk:PN':"+c5+"\t"+"Pourcentage: "+"("+cp5+")"
file.write(ct5+"\n")

#nombre de "Chunk:PRelS"
c6=Text.count("Chunk:PRelS")
cp6= "%.2f%%" % (c6/num1 * 100)
c6=str(c6)
print("Nombre de 'Chunk:PRelS': ",c6,"\t","Pourcentage: ",cp6)
ct6 = "Nombre de 'Chunk:PRelS':"+c6+"\t"+"\t"+"Pourcentage: "+"("+cp6+")"
file.write(ct6+"\n")

#nombre de "Chunk:CO"
c7=Text.count("Chunk:CO")
cp7= "%.2f%%" % (c7/num1 * 100)
c7=str(c7)
print("Nombre de 'Chunk:CO': ",c7,"\t","Pourcentage: ",cp7)
ct7 = "Nombre de 'Chunk:CO':"+c7+"\t"+"Pourcentage: "+"("+cp7+")"
file.write(ct7+"\n")

#nombre de "Chunk:CS"
c8=Text.count("Chunk:CS")
cp8= "%.2f%%" % (c8/num1 * 100)
c8=str(c8)
print("Nombre de 'Chunk:CS': ",c8,"\t","Pourcentage: ",cp8)
ct8 = "Nombre de 'Chunk:CS':"+c8+"\t"+"Pourcentage: "+"("+cp8+")"
file.write(ct8+"\n")

#nombre de "Chunk:SV"
c9=Text.count("Chunk:SV")
cp9= "%.2f%%" % (c9/num1 * 100)
c9=str(c9)
print("Nombre de 'Chunk:SV': ",c9,"\t","Pourcentage: ",cp9)
ct9 = "Nombre de 'Chunk:SV':"+c9+"\t"+"Pourcentage: "+"("+cp9+")"
file.write(ct9+"\n")

#nombre de "Chunk:ADV"
c10=Text.count("Chunk:ADV")
cp10= "%.2f%%" % (c10/num1 * 100)
c10=str(c10)
print("Nombre de 'Chunk:ADV': ",c10,"\t","Pourcentage: ",cp10)
ct10 ="Nombre de 'Chunk:ADV':"+c10+"\t"+"Pourcentage: "+"("+cp10+")"
file.write(ct10+"\n")

#nombre de "Chunk:Vse"
c11=Text.count("Chunk:Vse")
cp11= "%.2f%%" % (c11/num1 * 100)
c11=str(c11)
print("Nombre de 'Chunk:Vse': ",c11,"\t","Pourcentage: ",cp11)
ct11 = "Nombre de 'Chunk:Vse':"+c11+"\t"+"Pourcentage: "+"("+cp11+")"
file.write(ct11+"\n")

#nombre de "Chunk:PVant"
c12=Text.count("Chunk:PVant")
cp12= "%.2f%%" % (c12/num1 * 100)
c12=str(c12)
print("Nombre de 'Chunk:PVant': ",c12,"\t","Pourcentage: ",cp12)
ct12 = "Nombre de 'Chunk:PVant':"+c12+"\t"+"\t"+"Pourcentage: "+"("+cp12+")"
file.write(ct12+"\n")

file.write("----------------"*5+"\n")

#nombre total d'utilisation de règle "NOM|NAM"
num2=Text.count("Règle: NOM|NAM")
p2 = "%.2f%%" % (num2/num1 * 100)
num2=str(num2)
print("Nombre de règle 'NOM|NAM': ", num2,"\t","Pourcentage: ",p2)
t2 = "Nombre de règle 'NOM|NAM': "+num2+"\t"+"Pourcentage: "+"("+p2+")"
file.write(t2+"\n")

#nombre total d'utilisation de règle "(NUM|DET).*?(NOM|NAM).*?(ADJ)?"
num3=Text.count("Règle: (NUM|DET).*?(NOM|NAM).*?(ADJ)?")
p3 = "%.2f%%" % (num3/num1 * 100)
num3=str(num3)
print("Nombre de règle '(NUM|DET).*?(NOM|NAM).*?(ADJ)?': ", num3,"\t","Pourcentage: ",p3)
t3 = "Nombre de règle '(NUM|DET).*?(NOM|NAM).*?(ADJ)?': "+num3+"\t"+"Pourcentage: "+"("+p3+")"
file.write(t3+"\n")

#nombre total d'utilisation de règle "(PRP|KON).*?(NOM|NAM).*?(ADJ)?"
num4=Text.count("Règle: (PRP|KON).*?(NOM|NAM).*?(ADJ)?")
p4 = "%.2f%%" % (num4/num1 * 100)
num4=str(num4)
print("Nombre de règle '(PRP|KON).*?(NOM|NAM).*?(ADJ)?': ", num4,"\t","Pourcentage: ",p4)
t4 = "Nombre de règle '(PRP|KON).*?(NOM|NAM).*?(ADJ)?': "+num4+"\t"+"Pourcentage: "+"("+p4+")"
file.write(t4+"\n")

#nombre total d'utilisation de règle "PRO_PERVER_pres"
num5=Text.count("Règle: PRO_PERVER_pres")
p5 = "%.2f%%" % (num5/num1 * 100)
num5=str(num5)
print("Nombre de règle 'PRO_PERVER_pres': ", num5,"\t","Pourcentage: ",p5)
t5 = "Nombre de règle 'PRO_PERVER_pres': "+num5+"\t"+"Pourcentage: "+"("+p5+")"
file.write(t5+"\n")

#nombre total d'utilisation de règle "PRO.*?ADV_negVER.*?ADV"
num6=Text.count("Règle: PRO.*?ADV_negVER.*?ADV")
p6 = "%.2f%%" % (num6/num1 * 100)
num6=str(num6)
print("Nombre de règle 'PRO.*?ADV_negVER.*?ADV': ", num6,"\t","Pourcentage: ",p6)
t6 = "Nombre de règle 'PRO.*?ADV_negVER.*?ADV': "+num6+"\t"+"Pourcentage: "+"("+p6+")"
file.write(t6+"\n")

#nombre total d'utilisation de règle "PRO.*?ADV_negPRO.*?ADV"
num7=Text.count("Règle: PRO.*?ADV_negPRO.*?ADV")
p7 = "%.2f%%" % (num7/num1 * 100)
num7=str(num7)
print("Nombre de règle 'PRO.*?ADV_negPRO.*?ADV': ", num7,"\t","Pourcentage: ",p7)
t7 = "Nombre de règle 'PRO.*?ADV_negPRO.*?ADV': "+num7+"\t"+"Pourcentage: "+"("+p7+")"
file.write(t7+"\n")

#nombre total d'utilisation de règle "VER"
num8=Text.count("Règle: VER")
p8 = "%.2f%%" % (num8/num1 * 100)
num8=str(num8)
print("Nombre de règle 'VER': ", num8,"\t","Pourcentage: ",p8)
t8 = "Nombre de règle 'VER': "+num8+"\t"+"\t"+"Pourcentage: "+"("+p8+")"
file.write(t8+"\n")

#nombre total d'utilisation de règle "ADV"
num9=Text.count("Règle: ADV")
p9 = "%.2f%%" % (num9/num1 * 100)
num9=str(num9)
print("Nombre de règle 'ADV': ", num9,"\t","Pourcentage: ",p9)
t9 = "Nombre de règle 'ADV': "+num9+"\t"+"\t"+"Pourcentage: "+"("+p9+")"
file.write(t9+"\n")

#nombre total d'utilisation de règle "KON"
num10=Text.count("Règle: KON")
p10 = "%.2f%%" % (num10/num1 * 100)
num10=str(num10)
print("Nombre de règle 'KON': ", num10,"\t","Pourcentage: ",p10)
t10 = "Nombre de règle 'KON': "+num10+"\t"+"\t"+"Pourcentage: "+"("+p10+")"
file.write(t10+"\n")

#nombre total d'utilisation de règle "PRelS"
num11=Text.count("Règle: PRelS")
p11 = "%.2f%%" % (num11/num1 * 100)
num11=str(num11)
print("Nombre de règle 'PRelS': ", num11,"\t","Pourcentage: ",p11)
t11 = "Nombre de règle 'PRelS': "+num11+"\t"+"Pourcentage: "+"("+p11+")"
file.write(t11+"\n")

#nombre total d'utilisation de règle "PRO"
"""
Attention: ici on un espace après le PRO.
Sinon le programme va aussi calculer les autres règles.
【PRO_PERVER_pres】
【Règle: PRO.*?ADV_negPRO.*?ADV"】
【PRO.*?ADV_negVER.*?ADV】
"""
num12=Text.count("Règle: PRO ")
p12 = "%.2f%%" % (num12/num1 * 100)
num12=str(num12)
print("Nombre de règle 'PRO': ", num12,"\t","Pourcentage: ",p12)
t12 = "Nombre de règle 'PRO': "+num12+"\t"+"\t"+"Pourcentage: "+"("+p12+")"
file.write(t12+"\n")

#nombre total d'utilisation de règle "PCT(N)F"
num13=Text.count("Chunk:PCT(N)F")
p13 = "%.2f%%" % (num13/num1 * 100)
num13=str(num13)
print("Nombre de règle 'PCT(N)F': ", num13,"\t","Pourcentage: ",p13)
t13 = "Nombre de règle 'PCT(N)F': "+num13+"\t"+"Pourcentage: "+"("+p13+")"
file.write(t13+"\n")

file.close()

