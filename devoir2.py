#coding:utf-8

import csv
#pour importer les fichiers csv

import re 
#Pour les expression régulières dans 3e partie

#Pour les chiffres romains, trouvé par Shannon sur Stackoverflow (internet) 
def rom_to_int(value):
    s = 0;
    a = dict();
    b = dict();
    r = value;
    
    a['CM'] = 900;
    a['IX'] = 9;
    a['IV'] = 4;
    a['XL'] = 40;
    a['CD'] = 400;
    a['XC'] = 90;
    
    b['M'] = 1000;
    b['C'] = 100;
    b['D'] = 500;
    b['X'] = 10;
    b['V'] = 5;
    b['L'] = 50;
    b['I'] = 1;
    
    #pour les chiffres romains
    for key in a:
            if key in r:
                r = re.sub(key,'',r)
                s+=a[key];
                
    #Enlever les 4 et les 9            
                
    #pour évirer les mauvaises additions des nombres.             
    for key in b:
            s+= r.count(key) * b[key];
             
    #pour retourner à la "solution" nombre entier
    return s 

fichier="concordia1.csv"
#Nommer le fichier
concordia=open(fichier)
#Ouvrir le fichier
lignes=csv.reader(concordia)
   
   
#pour sauter à la deuxième ligne
next(lignes)

#Placer le titre, le nom et le prénom de chaque ligne dans une colone distincte pour pouvoir bien les différencier
titre=[]
nom=[]
prenom=[]

#ajouter (append) les bonnes colones aux bonnes lignes 
for ligne in lignes:
    titre.append(ligne[2])
    nom.append(ligne[0])
    prenom.append(ligne[1])
# print(titre) pour voir si ça fonctionne

#Pour que le "curseur" csv retourne au début par lui même. Il faut l'utiliser pour chaque for "ligne in lignes"

concordia.seek(0)
next(lignes)

#Première question : Longueur du titre


#Titre est à la 3e ligne, soit colone 2 dans le CSV.

longTitre=[]

#utilité du "append" ici, pour que tout soit entre "[]", et donc dans la liste 

for ligne in lignes:
   longTitre.append(len(ligne[2]))
#la ligne [2] = colone 3
# print(longTitre)

#Pour que le "curseur" du CSV retourne au début.
concordia.seek(0)
next(lignes)

#fin de la première question

#Deuxième question : Type (Mémoire ou Thèse)
#nom de la colone : thesis_degree_name (que ce soit Maîtrise ou Doctorat), colone 6 (7 en vrai)
#Création d'une liste ("typedoc") pour diviser les noms des travaux, s'ils sont dans maîtrise ou Doctorat
typedoc=[]
#je ne l'appelle pas seulement "type", car ça peut créer un problème de confusion dans les fonctions, donc "typedoc"
for ligne in lignes:
    #Pour chaque ligne dans les lignes, on veut "Doctorat" pour chaque appellation liée au doctorat 
    #c'est à dire : "D.""PhD""Ph.D"
    #ne pas oublier le "el" (else if) devant les if 
    #Pour la Maîtrise, c'est juste "M.", pas d'autres appellations.
    #append!! Pour ajouter le doctorat (rappel)
    if "D." in ligne[6]:
        typedoc.append("Doctorat")
    elif "PhD" in ligne[6]:
        typedoc.append("Doctorat")
    elif "Ph.D" in ligne[6]:
        typedoc.append("Doctorat")
    #Doctorat est fait, maîtrise maintenant
    elif "M." in ligne[6]:
        typedoc.append("Maîtrise")
    #Sinon, s'il y a un autre truc que je n'ai pas remarqué, ça va me dire où le "bobo" se trouve
    else : 
        typedoc.append("BOBO")
        print(ligne)
        #le print ici est pour me dire où il y a le "bobo", pas sensé rien afficher. Bon Cloud9. :)
# print(typedoc)
#ça fonctionne yay!

#Troisième question : Nombre de pages
#Colone : "pages_aacr", soit la 5e colone (la 6e en vrai)
#C'est ici que s'applique le code des nombres romains mis au début
#numéros Romains + numéros Arabes = nombre total de pages
#la formule a été trouvée sur le site de stackoverflow
#ne pas oublier de remettre le "curseur" du CSV au début car nouvelle étape
concordia.seek(0)
next(lignes)

#Créer la liste pour mieux classer le nombre de pages
nbpages=[]

for ligne in lignes:
    n=ligne[5]
    #création d'une boucle pour la colone "pages_aacr" du fichier CSV
    #Étape 1: séparer la ligne avec le nombre de pages en deux, pour les deux types de nombres
    #La méthode utilisée est une fonction avec des expressions régulières (regular expressions)
    #si jamais je rencontre "leaves" ou "p."" ou "l."" ou ":"" : ça coupe
    #on va appeler ça "lignecoupee" suivie de 1, 2 ou 3
    #la ligne droite "|" est la séparation
    # le \ sert à indiquer que le "." fait partie du "p" 
    leaves=re.split("leaves|p\.|1\.|:", n)
    #On veut la première valeur du "re.split" La deuxième valeur : on ne la veut pas
    brutlignecoupee2=leaves[0]
    #Dans "lignecoupee2" il y a toujours deux infos, mais séparées par une virgule. On les sépare à la virgule
    netpages=brutlignecoupee2.split(",")
    #On intègre les chiffres romains à la formule
    #fonction : "rom_to_int". Comme au début du script
    # print(netpages)
    if len(netpages)==2:
        traduit=rom_to_int(netpages[0]) #les nombres romains sont traduits
        #création de variable : nombre de pages sans espaces : nbpasspace
        #avec .strip()
        netnbpasspace=netpages[1].strip()
        if netnbpasspace.isdigit() is True: # Le bash va dire True si tous les caractères sont numériques et qu'il y en a au moins un. Sinon ça va dire False.
        #C'est pour s'assurer que l'écriture respecte le «[chiffres romains si nécessaire], [chiffres arabes] ["leaves" ou "p." ou "l." ou ":"]»
        #nbpasspace devrait avoir que des chiffres, sinon BOBO   
        #SINON : on met "GROS BOBO parce que"
            
        #Il faudra tout additionner. Mais on veut que nbpages devienne un nombre entier (int) pour pouvoir additionner.
            nbrpages=int(netnbpasspace) 
            total=traduit+nbrpages 
            nbpages.append(total)#le résultat de cette addition sera ajouté à la liste créée au début.
        else : 
            nbpages.append("### type1(GROS BOBO parce que : {})".format(n))

    elif len(netpages)==1: #pas de nombre romain
        netnbpasspace=netpages[0].strip() #strip va enlever les espaces
        if netnbpasspace.isdigit() is False : 
            nbpages.append("### type2(GROS BOBO parce que : {})".format(n))    #s'il y a une erreur, GROS BOBO va le dire.
        else : 
            nbrpages=int(netnbpasspace) #il faut encore le mettre en nombre entier
            nbpages.append(nbrpages) #ajout du total à la liste
    
# print(nbpages)  #On vérifie. On devrait avoir le nombre de pages des thèses ou des mémoires

#remise du curseur au début à ne pas oublier
concordia.seek(0)
next(lignes)

#Dernière étape : regrouper les informations ensemble. On veut faire une phrase
# du genre : 
#Le document {thèse ou mémoire} de {nom complet de l'auteur} compte {tant} de pages. Son titre est {ceci ou cela} ({tant} de caratères)

for index in range(len(longTitre)): #le nombre d'éléments est le même partout. Alors on peut mettre le titre de chaque ligne d'élément dans les parenthèses
    # print(index) je commente. espace.
    print("Le document de {} de {} {} compte {} de pages. Son titre est {} ({} caractères).".format(typedoc[index],nom[index],prenom[index],nbpages[index],titre[index],longTitre[index]))
    
    #c'est fini.
