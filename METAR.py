import urllib.request
"""
Petite permettant de lire un fichier contenant (presque) tous les noms d'aéroports
(il fait 620 lignes, soit autant d'aéroports répertoriés)
"""
fichier=open("./codes.txt",'r',encoding="utf-8")
donnees=[]
for ligne in fichier.readlines():
    donnees.append(ligne.strip().split(';'))
fichier.close()

def décoder(code):
    for i in range (len(code)):
        if code[i]=='"':
            return code[:i]
    return code
        
def print_massif(liste_a_imprimer: list):
    for element in liste_a_imprimer:
        print(element)

def decodage(t,METAR):
    """
    La fonction décodage permet de dissocier les elements "utiles" des codes météorologiques METAR et TAF afin de les traiter un par un et par groupe d'éléments.
    L'argument à rentrer s'apelle METAR car initialement, j'ai développé ce code pour ce code mais comme le TAF reprends plus ou moins la même syntaxe je vais lui dédier une fonction, mais ça ne change rien de mettre un code TAF dans l'argument METAR :)
    La valeur d'entrée doit être une chaîne de caractère
    La valeur renvoyée en sortie sera une liste
    """
    if t.upper()=="M":
        code=[]
        partie=""
        for i in range (len(METAR)):
            if METAR[i]!=' ':
                partie+=METAR[i] #Nous cherchons tous les éléments, delimités par les espaces (donc certains seront reliés après)
            elif (i+4<len(METAR) and METAR[i+4]=="V" and METAR[i+5]!="V") or (len(partie)>5 and any(chr.isdigit() for chr in partie)==True and (METAR[i+1:i+4]=="FEW" or METAR[i+1:i+4]=="BKN" or METAR[i+1:i+4]=="SCT" or METAR[i+1:i+4]=="OVC" or METAR[i+1:i+4]=='///')): #Nous cherchons à savoir si le code indique un vent variable pouvent être confondu plus tard dans le code ou s'il y a plusieurs couches nuageuses.
                continue #Nous le mettons dans le même groupe
            elif i+4<len(METAR) and METAR[i+1]=='R' and METAR[i+4]=='/': #Nous cherchons si il y a un indicateur de visibilité de piste afin de le mettre avec la visibilité "classique"
                partie+=' ' #Ici on dit de ne pas continuer mais de rajouter un espace pour ne pas interférer avec la méthode de séparation de la fonction dédiée
            elif partie=='9999' and METAR[i+2].isdigit() and METAR[i+4].isdigit():
                continue
            else:
                if partie!='AUTO' and partie!='METAR': #À l'heure actuelle, (presque) tous les aéroports émettent des METARs et TAFs automatiquement, et de plus nous aideront pas pour déterminer le temps qu'il fait (ou fera)
                    code.append(partie) #On ajoute la partie différente d'AUTO dans la liste finale
                partie='' #On réinitialise la variable "partie"
        code.append(partie) #À la fin in n'y a pas d'espaces pour rajouter donc la dèrnière partie du code est ajouté en dehors de la boucle
        if code[-1][-1]=="=": #Les codes TAFs et certains METARs ont un "=" pour signifier la fin du code et nous informent rien des situations météorologiques
            code[-1]=code[-1][:-2]#La dernière partie du code se verra enlever le dernier caractère.
        return code
    else:
        Code=METAR
        chaine=""
        liste=[]
        ind=0
        
        while Code[ind] not in '0987654321':
            chaine+=Code[ind]
            mini_liste=[]
            ind+=1
        if chaine[-1]==" ":
            liste.append(chaine[:-1])
        else:
            liste.append(chaine)
        chaine=""

        while ind<len(Code):
            if Code[ind]==" " and ind<len(Code)-5 and (Code[ind+1:ind+5]=='PROB' or (not chaine[:4]=='PROB' and Code[ind+1:ind+6]=="TEMPO" or Code[ind+1:ind+6]=="BECMG")):
                mini_liste.append(chaine)
                liste.append(mini_liste)
                chaine,mini_liste="",[]
            elif Code[ind]==" ":
                mini_liste.append(chaine)
                chaine=""
            else:
                chaine+=Code[ind]
            ind+=1
        mini_liste.append(chaine)
        liste.append(mini_liste)
        return liste

def aeroport(OACI):
    """
    Le code international OACI nous permet de code les aéroports en fonction de leur zone géographique puis pays (et enfin les deux dernières lettres donnent la ville)
    La valeur rentrée doit être une chaîne de caractère contenant que 4 lettres
    la valeur de sortie elle aussi sera une chaîne de caractères
    """
    for i in range(len(donnees)):
        if donnees[i][0]==OACI:
            return (("Code "),("pour "+donnees[i][3]+", "+donnees[i][5]))
    return None
        
def horaire(h):
    """
    La syntaxe horaire se definit comme telle JJHHMMz (Z se prononce zulu, singifiant ici UTC)
    Le code sort pour le JJ du mois à HH:MM UTC
    La valeur d'entrée doit être une chaîne de caractrère
    La valeur de sortie sera elle aussi une chaîne de caractère
    """
    jour=h[0:2] #Conformément à la syntaxe, les deux premiers chiffres désignent le jour de sortie
    h=h[2:6] #Je supprime le reste pour ne garder que les 4 chiffres désignant l'heure
    heure=h[:2]+":"+h[2:] #Les deux premiers chiffres désignent l'heure et les deux derniers les minutes (00 ou 30)
    return "Publié le "+jour+" du mois, à "+heure+" UTC"

def vent(v):
    """
    La syntaxe du vent est sssvvKT (S pour sens et V pour vitesse, Kt designant l'unité, en noeuds) quand tout va bien
    La valeur entrée est une chaîne de caratère
    la valeur de sortie est aussi une chaîne de caractères
    """
    #Recherche de cas particuliers
    if "G" in v: #G signifie "Gust" (rafale en français), la syntaxe devient sssvvGrrKT, où les arrivants sont G informant la rafale et r la vitesse de cette rafale
        return ("Vent de direction "+v[0:3]+"°, la force est de "+str(int(int(v[3:5])*1.852))+" km/h et les rafales sont de "+str(int(int(v[6:8])*1.852))+' km/h')
    elif "VRB" in v: #Les systèmes automatiques sont incapable de savoir d'où vient le vent (parce que la direction change beaucoup), les valeurs designant le sens sont remplacé par les 3 lettres voulant dire "Variable"
        return "Vent de direction variable, la force de ce vent est de "+str(int(int(v[3:5])*1.852))+' km/h'
    elif "0V" in v: #Le vent peut avoir un sens variable, détectable c'est pourquoi le code se verra ajouter 7 lettres (2 fois les directions séparé par un V) 
        return "Vent de direction "+v[0:3]+"° pouvant varier de "+v[-7:-4]+" à "+v[-3:]+"°, de la force est "+str(int(int(v[3:5])*1.852))+' km/h'
    elif "00000KT" in v: #RIen ne se passe donc tout passe à 0
        return "Vent calme"
    else: #aucun cas particulier n'a été détecté donc on utilise la version "classique"
        return "Vent de direction "+v[0:3]+"°, la force est de "+str(int(int(v[3:5])*1.852))+' km/h'

def visibilite(d):
    """
    La fonction visu permet de rendre la valeur de visibilité et si défini la visibilité des piste (RVR, Runway Visual Range)
    Si la visibilité de la piste est mentionnée, la fonction Visual_Range sera invoquée
    La valeur d'entrée est la distance, une chaîne de caractères
    La valeur de sortie sera aussi une chaîne de caractères
    """
    visu=""
    RVR=""
    code=""
    r=0
    if "R" in d: #détection des informations concernant les pistes et séparation si nécéssaire
        for i in range (len(d)):
            if d[i]=="R":
                RVR=d[i:]
                d=d[:i-1]
                break
    if "SM" in d: #Unité de ceux qui utilisent les Semi-Miles et non pas les mètres.
        for i in range (len(d)):
            if d[i:i+2]=="SM":
                if d[i-3]!=" ":
                    visu="La visibilité est de "+d[i-3:i+2]
                elif d[i-3]==" ":
                    visu="La visibilité est de"+d[i-3:i+2]
    elif "CAVOK" in d: #Signifie Clear And Visibility OK (regroupe la visibilité, les nuages et le temps (un ciel bleu en gros))
        return "Visibilité parfaite et ciel degagé" #il n'y a aucune info sur la visibilité des pistes si tout est parfait
    elif "9999" in d: #Je dis que c'est la visibilité parfaite mais signifie en réalité 10 Km ou plus
        if len(d)==8:
            visu="La visibilité est de "+d[4]+","+d[5]+" km"' km ou plus'
        else:
            visu="visibilité parfaite"
    elif "000" in d: #Je cherche à savoir si ce sont des kilomètres tout ronds ou s'il y a des hectomètres
        visu="La visibilité est de : "+d[0]+" km"
    elif "00" in d:
        visu="La visibilité est de : "+d[0]+","+d[1]+" km"
    for i in range (len(RVR)):
        if RVR[i]=="R":
            r+=1 #Compteur d'informations de piste
    if r!=0: #Si diférent de 0, des informations ont été données donc il faut les traduire
        for j in range (r):
            code=""
            for car in RVR:
                if car==" ": #Séparation des informations de pistes, une par une (car une information ne concerne qu'une seule piste), séparée par des espaces
                    RVR=RVR[len(code)+1:] #On raccourci le code afin de chercher si après il y en a d'autres
                    break
                else:
                    code+=car
            code=Visual_Range(code) #invocation de la fonction
            visu+=code #Rajout des informations de piste aux informations de visibilité
    return visu

def Visual_Range(RVR):
    """
    Runway visual Range (Portée visuelle de la piste) est donnée, généralement quand il y a un brouillard ou une averse de pluie forte
    La valeur d'entrée et de sortie sont de type str
    """
    piste=""
    piste=RVR[1:4] #Les numéros de piste sont d'indice 1 et 2 mais parfois il nous est précisé si c'est de gauche (L) ou de droite (R)
    RVR=RVR[4:]+"m"
    if "/" in piste: #Recherche d'indicateur supplémentaire de piste et s'il n'y en a pas, / permet de séparer l'indentifié et les informations le concernant
        piste=piste[:-1]
    else:
        RVR=RVR[1:]
    if "M" in RVR:
        RVR="moins de "+RVR[1:]
    if "P" in RVR:
        RVR="plus de "+RVR[1:]
    if "D" in RVR:
        RVR=RVR[:-2]+" m en baisse"
    if "U" in RVR:
        RVR=RVR[:-2]+" m en hausse"
    return ("; la portée visuelle de la piste "+piste+" est de "+RVR)

def nuages(n):
    """
    Les couches nuageuses (nébulosité) est définie en octas (le ciel est donc découpé en huit et on regarde le nombre de "parts" qui sont encombrés par les nuages:
    0 : ciel dégagé (non mentionné du coup)
    1 et 2 : FEW, Peu de nuages
    3 et 4 : SCT, Scattered, Nuages éparpillés (si on suit la traduction)
    5 et 6 : BKN, Broken, ciel fragmenté
    7 et 8 : OVC, Overcast, ciel couvert
    Il ne peut y avoir que 3 couches maximum sauf pour signaler les TCU et CB
    La Valeur d'entrée est une chaîne de caractères, contenant toutes les couches, non séparées par les espaces (sinon ça ne marche pas)
    la valeur de sortie est une chaîne de caractères aussi
    """
    Cn=""
    Nuages=[] #J'ai séparé les couches nuageuses en couches afin de les distinguer
    while n!='': #Je sais pas ce que je voulais faire mdr
        if len(n)>4 and n[4]=='/':
            if len(n)==9 and n[:10]=="//////TCU":
                Nuages.append(n[:10])
                n=n[10:]
            elif len(n)==6 and n[5]=='/':
                Nuages.append(n[:6])
                n=n[6:]
            else:
                Nuages.append(n[:5])
                n=n[5:]
                
        elif len(n)>=8 and n[6:8]=='CB':
            Nuages.append(n[:8])
            n=n[8:]
            
        elif len(n)>=9 and n[6:9]=='TCU':
            Nuages.append(n)
            n=n[9:]
            
        elif len(n)>=9 and n[8]=='/':
            Nuages.append(n[:9])
            n=""
        else:
            Nuages.append(n[:6])
            n=n[6:]
    couches=len(Nuages)
    for i in range(len(Nuages)):
        base=""
        if Nuages[i]=="VV///": #Le ciel est invisible donc l'invisibilité du ciel est annoncé, les couches nuageuses ne peuvent être détectées
            Cn+="Ciel invisible"
        elif Nuages[i]=="CB///" or Nuages[i]=='///CB': #CumulonimBus, nuage d'orage, pouvant altérer les conditions d'attérissages.
            Cn+="Présence de cumulonimbus"
        elif Nuages[i]=="TCU///" or Nuages[i]=="///TCU": #Towering CUmulus, nuage naissant d'une instabilité
            Cn+="Présence de cumulus bourgeonnants"
        elif Nuages[i]=="//////TCU":
            Cn+="Présence de cumulus bourgeonnants de nébulosité et altitude inconnus"
        elif Nuages[i][0]=="F": #F, première lettre de FEW
            Cn+="Quelques nuages "
        elif Nuages[i][0]=="S": #S, première lettre de SCT, SCaTtered
            Cn+="Nuages éparpillés "
        elif Nuages[i][0]=="B": #B, Première lettre de BKN, BroKeN
            Cn+="Ciel fragmenté "
        elif Nuages[i][0]=="O": #O première lettre de OVC, OVerCast
            Cn+="Ciel couvert "
        Nuages[i]=Nuages[i][3:] #les 3 premières lettres designent le "taux d'encombrement" du ciel, les trois chiffres suivant, la base de la couche nuageuse en centaines de pieds
        if Nuages[i][3:]=="CB":
            Cn+="dont des cumulonimbus "
        elif Nuages[i][-3:]=='///':
            if Cn[-3:]=='es ':
                Cn+='inconnus '
            else:
                Cn+='de nuages inconnus '
        if Nuages[i][0].isdigit():
            if Nuages[i][0]!="0": #On regarde si la première valeur designant la base est différente de 0
                base+='à '+Nuages[i][0]+Nuages[i][1]+"."+Nuages[i][2]+"00 pieds"
            else:
                base+='à '+Nuages[i][1]+"."+Nuages[i][2]+"00 pieds"
            Cn+=base
        if Nuages[i][-3:]=="TCU":
            Cn+=", noter la présence de cumulus bourgeonnants"
        if couches-1>i:
            Cn+="\n" #Si plusieurs couches il y a, pour rendre la lecture plus agréable, j'ai séparé les couches 
    return Cn

def température(t):
    """
    L'Organisation aérienne civile internationale et l'organisation météorologique mondiale ont défini la température des codes METAR et TAF comme étant les unités métriques (°C)
    La valeur d'entrée et de sortie sont des chaînes de caractères
    """
    tp="La température est "
    for l in t: #On prend les chiffres et on laisse le séparateur de température - point de rosée à part
        if l=="M":#M comme Moins donc la valeur associée est négative
            tp+="-"
        elif l=="/":
            tp+="°C et le point de rosée vaut : " #Je n'ai toujours pas compris à ça donc ne me demandez pas...
        else:
            tp+=l
    tp+='°C'
    return tp

def temps(meteo):
    """
    C'est le plus important du code, quand il est la, il peut se composer d'un indicateur d'intensité ou de proximité, d'un descripteur,
    se composera toujours de phénomène de précipitation ou d'obscurcissement
    - indique que c'est faible,
    rien indique que c'est modéré,
    + met en valeur la force.
    la valeur d'entrée et de sortie sont des chaînes de caractères
    """
    phen={"RA":"Pluie ", "DZ":"Bruine ", "FG":"Brouillard ", "BR":"Brume ", "BC":"Bancs de ", "SH":"Averses de ", "TS":"Orages ", "SN":"Neige ", "HZ":"Brume sèche ", "FZ":"Se congelant, ", "GS":"Grêle"}
    tps=""
    it=""
    if len(meteo)%2==1:
        if meteo[0]=="-":
            it="faible"
            meteo=meteo[1:]
        if meteo[0]=="+":
            it="fort(e)"
            meteo=meteo[1:]
    else:
        it="modéré(e)"
        
    #Cas Particuliers
        
    if meteo=="NSC":
        return "Pas de nuages significatifs"
    elif meteo=="NSW":
        return "Pas de temps significatif"
    if meteo=="VV///":
        return "Ciel invisible"
    #Desc. du temps
    for i in range (0,len(meteo),2):
        try:
            tps+=phen[meteo[i:i+2]]
    
        except KeyError: #S'il y a une erreur, c'est que je n'ai pas pris en compte un phen. décodable
            return "Phénomène non décodé ("+meteo+")"
        
    tps=tps+it
    return tps

def pression(QNH):
    """
    Le QNH est la presion au niveau de la mer (NH=Nautical Height)
    Ici la pression est arrondie au hPa inférieur
    Les valeurs d'entrée/sortie sont des chaines de caractères
    """
    return "La pression est de "+QNH[1:]+"hPa"

def futur(ftr):
    """
    Le temps futur est représenté par trois types d'indicateurs d'evolution:
    -TEMPO: Temporairement, une evolution durant moins d'1 heure et couvrant moins de la moitié de la période avec les indicateur horaires:
    FM... TL... (From... until...)
    - BECMG (Becoming): évolution régulière ou irrégulière des conditions et où l'heure de début de tendence reste incertaine, l'heure prévue
    est mentionnée avec l'indicateur AT
    -NOSIG: Pas de cahngements à prevoir dans les deux heures
    """
    proch=""
    a=[]
    for element in ftr:
        if element=="NOSIG":
            return "Pas de changements à prévoir dans les deux heures à venir"
        elif element=='TEMPO':
            if element[0:2]=="FM" and element[0:2]=="TL":#recherche d'indicateurs
                proch+=("De "+element[2:4]+":"+ftr[4:]+" à "+element[2:4]+":"+element[4:]+",\n     ")
            else:#Pas d'indicateurs
                proch+=('Temporairement,\n     ')
        elif element=="BECMG":
            if element[0:2]=="AT":#recherche d'indicateurs
                proch+=("Devient à "+element[2:4]+":"+element[4:]+":\n     ")
            else:
                proch+=("Devient,\n     ")#pas d'indicateurs
        elif any(chr.isdigit() for chr in element)==True: #Petite fonction que j'ai decouvert qui dit si il y a (ou non) des chiffres dans la chaîne de caractères
            if "KT" in element: #recherches de phénomènes avec des lettres à l'intérieur
                a.append(vent(element))
            elif "FEW" in element[0:3] or "SCT" in element[0:3] or "BKN" in element[0:3] or "OVC" in element[0:3]:
                a.append(nuages(element))
            else:#seul phénomène n'utilisant pas de lettres
                a.append(visibilite(element))
        else: #seul phénomènes sans chiffres dedans
            a.append(temps(element))
    for i in range (len(a)):
        proch+=a[i]
        if i<len(a)-1:
            proch+=",\n     "#Je sépare les différents phénomènes avec afin de rendre ça plus confortable à voir
    return proch
            
    

def METAR(code):
    """
    Resultat final
    La valeur entrée est le code METAR en chaîne de caractères
    """
    a_imprimer=[]
    code=decodage("m",code)
    ICAO=code[0]
    ICAO=aeroport(ICAO)
    a_imprimer.append(ICAO[0]+"METAR "+ICAO[1])
    code=code[1:]
    a_imprimer.append(horaire(code[0]))
    code=code[1:]
    a_imprimer.append(vent(code[0]))
    code=code[1:]
    a_imprimer.append(visibilite(code[0]))
    code=code[1:]
    while '///' not in code[0] and not(any(chr.isdigit() for chr in code[0])):
        a_imprimer.append(temps(code[0]))
        code=code[1:]
    if "FEW" in code[0] or "SCT" in code[0] or "BKN" in code[0] or "OVC" in code[0] or "VV" in code[0]:
        print(code[0])
        a_imprimer.append(nuages(code[0]))
        code=code[1:]
    a_imprimer.append(température(code[0]))
    code=code[1:]
    a_imprimer.append(pression(code[0]))
    if len(code)>1:
        code=code[1:]
        a_imprimer.append(futur(code))
    return a_imprimer

        
def TAF(code):
    a_imprimer=[]
    code=decodage("T",code)
    ICAO=code[0][-4:]
    ICAO=aeroport(ICAO)
    a_imprimer.append(ICAO[0]+"TAF "+ICAO[1])
    a_imprimer.append(horaire(code[1][0]))
    a_imprimer.append("Valable du "+code[1][1][:2]+" à "+code[1][1][2:4]+" heures, jusqu'au "+code[1][1][5:7]+" à "+code[1][1][7:]+" heures")
    print()
    code=code[1:]
    code[0]=code[0][2:]
    ###
    for liste in code:
        if liste[0][:4]=="PROB":
            a_imprimer.append("Avec une probabilité de "+liste[0][4:6]+" % :")
            liste=liste[1:]
        if liste!=code[0]:
            a_imprimer.append("Du "+liste[1][:2]+" à "+liste[1][2:4]+" heures, jusqu'au "+liste[1][5:7]+" à "+liste[1][7:]+" heures :")
            del liste[1]
        a_imprimer.append(futur(liste))
        a_imprimer.append('')
    return a_imprimer

        
def recherche(t="", code_aero="", to_print=True):
    if t=="":
        t=input("Que voulez vous déchifffrer ? ")
    t=t.upper()
    if code_aero=="":
        code_aero=input("Entrer le code OACI de l'aéroport dont les codes METAR et TAF sont à décoder ") 
        print()
    
    if t=="METAR":
        URL="https://tgftp.nws.noaa.gov/data/observations/metar/stations/"+code_aero.upper()+".TXT" 
        request_url = urllib.request.urlopen(URL)
        ligne=request_url.readlines()[1].decode("utf-8").strip()
        Metar=METAR(ligne)
        if to_print:
            print_massif(Metar)
        else:
            return Metar
        
    elif t.upper() == "TAF":
        URL="https://aerometeo.fr/web_taf.php?st="+code_aero.upper()
        request_url = urllib.request.urlopen(URL)
        ligne=request_url.readlines()[0][23:].decode()
        ligne=décoder(ligne)
        Taf=TAF(ligne)
        if to_print:
            print_massif(Taf)
        else:
            return Taf
        
    elif t=="TOUT":
        URL="https://tgftp.nws.noaa.gov/data/observations/metar/stations/"+code_aero.upper()+".TXT" #Le lien en question
        request_url = urllib.request.urlopen(URL)
        ligne=request_url.readlines()[1].decode("utf-8").strip()
        Metar=METAR(ligne)
        
        #####
        
        URL="https://aerometeo.fr/web_taf.php?st="+code_aero.upper()
        request_url = urllib.request.urlopen(URL)
        ligne=request_url.readlines()[0][23:].decode()
        ligne=décoder(ligne)
        Taf=TAF(ligne)
        if to_print:
            print_massif(Metar)
            print()
            print("____________________________________________________________________________________________________")
            print()
            print_massif(Taf)
        else:
            return Metar,Taf
    else:
        print("pas faisable")

if __name__=="__main__":
    #recherche()
    print_massif(recherche("TAF", "LFRQ"))