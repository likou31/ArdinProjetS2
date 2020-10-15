# coding:utf-8
import os
from time import sleep
from random import randint

# !! Il y a un bug d'affichage quand une partie est gagnée, je n'ai pas réussi à résoudre ce problème. !!

type_jeu = "0"
#les types de jeux correspondent a : 
#pvp = joueur contre joueur
#pve = joueur contre ia faible (ia = joueur 2)
#eve = ia faible contre ia faible, elle ne sera pas utilisé dans ce fichier
#le type de jeu sera déterminé dans le menu à partir du choix du joueur.

grille = [["x", "x", "x", "x", "x"], ["x", "x", "x", "x", "x"], ["x", "x", " ", "o", "o"], ["o", "o", "o", "o", "o"],
          ["o", "o", "o", "o", "o"]]

#fonction ia faible, qui renvoie un deplacement aleatoire (selon le niveau de l'ia)
def ia_guide(grille, joueur, second_tour):
    sleep(2)
    niveau_ia = 1 #si on la remplace par 0, elle fait du hazard complet
    deplacements_possibles = depl_possibles(grille,joueur,second_tour)
    index_deplacement = randint(0,len(deplacements_possibles)-1)
    depl = deplacements_possibles[index_deplacement]
    if niveau_ia != 0: #si on met un niveau a l'ia superieur a 0 elle va choisir avec preference pour les actions qui lui font manger un pion
        deplacements_opti = [depl]
        for depl in deplacements_possibles:
            if max(abs(depl[0]-depl[2]),abs(depl[1]-depl[3])) == 2: #si on a déplacé un pion de 2 c'est qu'on a mangé un pion adverse
                deplacements_opti.append(depl)
        index_deplacement_opti = randint(0,len(deplacements_opti)-1)
        depl = deplacements_opti[index_deplacement_opti]
    mange = False
    if max(abs(depl[0]-depl[2]),abs(depl[1]-depl[3])) == 2: #si on a déplacé un pion de 2 c'est qu'on a mangé un pion adverse
        mange = True
    return depl,mange


def icone_joueurs(joueur): #fonction qui renvoie l'icone d'un joueur donné
    if joueur == 1:
        player = 'x'
        adversaire = 'o'
    else:
        player = 'o'
        adversaire = 'x'
    return (player,adversaire)


def depl_possibles(grille,joueur,second_tour): #fonction qui renvoie tous les deplacements possibles pour un joueur donné 
    player, adversaire = icone_joueurs(joueur)
    liste_depl_possibles = []
    for ligne in range(5):
        for colonne in range(5):
            if grille[ligne][colonne] == player: #si le pion qui occupe la case appartient au joueur
                coordonnees_arrivees_valides = coordonnes_arrivee_valides(ligne,colonne,grille,adversaire,second_tour) #on regarde ou ce pion peut aller en respectant les regles
                for position in coordonnees_arrivees_valides:
                    liste_depl_possibles.append((ligne,colonne,position[0],position[1]))
    return liste_depl_possibles
                
def deplacement_simple_valide(deplacement, grille): #cette fonction regarde si un deplacement simple donné respecte les regles du jeu (la case d'arrivée est vide)
    if grille[deplacement[0]][deplacement[1]] == ' ':
        return True
    return False

#cette fonction teste si un deplacement double respecte les règles (case d'arrivee vide + case "survolée" occupee par un adversaire)
def deplacement_double_valide(dep_x,dep_y,deplacement, grille, adversaire):
    milieu_x = (deplacement[0]+dep_x)//2
    milieu_y = (deplacement[1]+dep_y)//2
    if grille[deplacement[0]][deplacement[1]] == ' ':
        if grille[milieu_x][milieu_y] == adversaire:
            return True
    return False

def coordonnes_arrivee_valides(coordonnee_depart_x,coordonnee_depart_y,grille,adversaire,second_tour):
    positions_arrivee_valide = []

    #si c'est le second tour du joueur, les déplacements simples ne sont pas autorisés
    if (not second_tour):
        deplacements_relatifs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]#déplacements simples
        position_absolue = []
        for deplacement in deplacements_relatifs: #on passe les coordonnes en absolu
            if deplacement[0]+coordonnee_depart_x >= 0 and deplacement[0]+coordonnee_depart_x < 5:
                if deplacement[1]+coordonnee_depart_y >= 0 and deplacement[1]+coordonnee_depart_y < 5:
                    position_absolue.append((deplacement[0]+coordonnee_depart_x,deplacement[1]+coordonnee_depart_y))
        for deplacement in position_absolue:
            if deplacement_simple_valide(deplacement,grille):
                positions_arrivee_valide.append(deplacement)
    
    #on regarde ensuite les deplacements doubles
    deplacements_relatifs_doubles = [(-2,-2),(-2,0),(-2,2),(0,-2),(0,2),(2,-2),(2,0),(2,2)] #déplacements doubles

    position_absolue_double = []
    for deplacement in deplacements_relatifs_doubles: #on passe les coordonnes en absolu
        if deplacement[0]+coordonnee_depart_x >= 0 and deplacement[0]+coordonnee_depart_x < 5:
            if deplacement[1]+coordonnee_depart_y >= 0 and deplacement[1]+coordonnee_depart_y < 5:
                position_absolue_double.append((deplacement[0]+coordonnee_depart_x,deplacement[1]+coordonnee_depart_y))

    for deplacement_double in position_absolue_double:
        if deplacement_double_valide(coordonnee_depart_x,coordonnee_depart_y,deplacement_double,grille,adversaire):
            positions_arrivee_valide.append(deplacement_double)

    return positions_arrivee_valide


def format_saisie_valide(entree):
    lettres = ['A', 'B', 'C', 'D', 'E']
    chiffres = ['1', '2', '3', '4', '5']

    return (entree[0] in lettres) and (entree[1] in chiffres) #vérifier que le format rentré est bien le bon
 

# transforme une saisie en coordonnées exploitables ex: A1, A2 -> (0,0,0,1)
def saisie_2_deplacement(pionin, pionout):
    lettres = ['A', 'B', 'C', 'D', 'E']
    chiffres = ['1', '2', '3', '4', '5']

    return (lettres.index(pionin[0]),chiffres.index(pionin[1]),lettres.index(pionout[0]),chiffres.index(pionout[1]))


# transforme des coordonnées dans un format lisible par l'utilisateur ex: (0,0,0,1) -> "A1 -> A2"
def deplacement_2_saisie(depl):
    lettres = ['A', 'B', 'C', 'D', 'E']
    chiffres = ['1', '2', '3', '4', '5']

    return lettres[depl[0]]+chiffres[depl[1]]+" -> "+lettres[depl[2]]+chiffres[depl[3]]


def saisie(joueur, grille, second_tour):
    mange = False
    deplacements_possibles = depl_possibles(grille,joueur,second_tour) #on recupere tous les déplacements possibles
    depl = (0,0,0,0)
    #le deplacement (0,0,0,0)=(A1, A1) n'est jamais valide 
    #tant que le deplacement n'est pas  autorisé, l'utilisateur doit entrer un nouveau deplacement
    while not depl in deplacements_possibles:

        pionin = ''
        format_depart_valide = False
        #on teste d'abord que l'entrée de l'utilisateur soit au bon format pour etre traitée comme les coordonnées d'une case
        while not format_depart_valide:
            if pionin != '': #le message d'erreur ne doit pas s'afficher des le debut
                print("Le format entré est invalide")
            print("Rentrer le pion à déplacer (ex : A3) :")
            pionin = input().upper() #prends en compte les minuscules et les majuscules
            pionin = pionin + "  " #il faut une chaine de caractères de longueur 2 minimum pour ne pas faire planter le programme
            format_depart_valide = format_saisie_valide(pionin)
            if format_depart_valide:
                format_arrivee_valide = False
                pionout = ''
                while not format_arrivee_valide:
                    if pionout != '':
                        print("Le format entré est invalide")
                    print("Rentrer l'emplacement d'arrivée (ex : C3) :")
                    pionout = input().upper() #prends en compte les minuscules et les majuscules
                    pionout = pionout + "  " #pareil que pour le précédent
                    format_arrivee_valide = format_saisie_valide(pionout)
        depl = saisie_2_deplacement(pionin,pionout)
        if not depl in deplacements_possibles:
            print("Le déplacement "+deplacement_2_saisie(depl)+" n'est pas possible")
            print("Les déplacements autorisés sont :")
            for deplacement in deplacements_possibles:
                print(deplacement_2_saisie(deplacement))
            print(" ")
    if max(abs(depl[0]-depl[2]),abs(depl[1]-depl[3])) == 2: #si on a déplacé un pion de 2 c'est qu'on a mangé un pion adverse
        mange = True
    return depl,mange

def modif_terrain(deplacement,grille,mange):
    grille[deplacement[2]][deplacement[3]] = grille[deplacement[0]][deplacement[1]]
    grille[deplacement[0]][deplacement[1]] = ' '
    if mange:
        milieu_x = (deplacement[0]+deplacement[2])//2
        milieu_y = (deplacement[1]+deplacement[3])//2
        grille[milieu_x][milieu_y] = ' '
    return grille

    

def finPartie(grille): #fonction pour assurer la fin de partie quand un des joueurs n'a plus de pions
    pion_a = 0
    pion_b = 0
    for x in range(5):
        for y in range(5):
            if grille[x][y] == 'x': #compter le nombre de x dans la grille
                pion_a += 1
            if grille[x][y] == 'o': #compter le nombre de o dans la grille
                pion_b += 1
    if pion_a == 0: #s'il n'y a plus de x en premier, cela veut dire que le joueur 2 a gagné
        return 2
    if pion_b == 0: #s'il n'y a plus de o en premier, cela veut dire que le joueur 1 a gagné
        return 1
    return 0 #retourner 0 tant qu'il y 1 pion de chaque joueur dans la grille

def changement_joueur(ancien_joueur):
    if ancien_joueur == 1:
        return 2
    else:
        return 1

def affGrillePartie(grillet, player): #grillet = grille_temporaire
    os.system("cls") #effacer la grille à la fin de chaque tour afin qu'une nouvelle mise à jour apparaisse à son tour
    print()
    player_icone, adversaire = icone_joueurs(player)
    print("   Tour du joueur " + str(player) + " : " + player_icone)
    print()
    print("     A   B   C   D   E  ")
    print(" 1 |", grillet[0][0], "|", grillet[1][0], "|", grillet[2][0], "|", grillet[3][0], "|", grillet[4][0], "|")
    print(" 2 |", grillet[0][1], "|", grillet[1][1], "|", grillet[2][1], "|", grillet[3][1], "|", grillet[4][1], "|")
    print(" 3 |", grillet[0][2], "|", grillet[1][2], "|", grillet[2][2], "|", grillet[3][2], "|", grillet[4][2], "|")
    print(" 4 |", grillet[0][3], "|", grillet[1][3], "|", grillet[2][3], "|", grillet[3][3], "|", grillet[4][3], "|")
    print(" 5 |", grillet[0][4 ], "|", grillet[1][4], "|", grillet[2][4], "|", grillet[4][4], "|", grillet[4][4], "|")
    print()

def jeuEnCours(grille):
    joueur = 1
    affGrillePartie(grille, joueur)
    mange = False
    while finPartie(grille) == 0:
        if type_jeu == "pve":
            if joueur == 1:
                deplacement, mange = saisie(joueur, grille, mange)
            else:
                deplacement, mange = ia_guide(grille ,joueur ,mange)
        elif type_jeu == "pvp":
            deplacement, mange = saisie(joueur, grille, mange)
        elif type_jeu == "eve":
            deplacement, mange = ia_guide(grille ,joueur ,mange)
        grille = modif_terrain(deplacement,grille,mange)
        if mange:
            if depl_possibles(grille,joueur,True) == []:
                joueur = changement_joueur(joueur)
                mange = False
        else:
            joueur = changement_joueur(joueur)
        affGrillePartie(grille, joueur)
    print("Le joueur " + str(finPartie(grille)) + " a gagné!")
    
    

def menu2(type_jeu) :
    grille_1 = [["x", "x", "x", "x", "x"], ["x", "x", "x", "x", "x"], ["x", "x", " ", "o", "o"], ["o", "o", "o", "o", "o"],
["o", "o", "o", "o", "o"]]
    grille_2 = [[" ", " ", "x", "x", " "], [" ", "x", "x", " ", "x"], ["x", " ", " ", "o", " "], ["o", "o", " ", " ", "o"],
["o", " ", "o", "o", " "]]
    grille_3 = [[" ", " ", "x", " ", " "], [" ", "x", " ", " ", " "], [" ", " ", " ", " ", " "], [" ", "o", " ", " ", " "],
[" ", " ", " ", " ", " "]]
    print(" ____________________________________ ")
    print("|                                    |")
    print("|  1. Debut de partie                |")
    print("|                                    |")
    print("|  2. Milieu de partie               |")
    print("|                                    |")
    print("|  3. Fin de partie                  |")
    print("|____________________________________|")
    choix = int(input())
    while choix != 1 or choix != 2 or choix != 3 :
        if choix == 1:
            os.system("cls")
            jeuEnCours(grille_1)
        elif choix == 2 :
            os.system("cls")
            jeuEnCours(grille_2)
        elif choix == 3 :
            os.system("cls")
            jeuEnCours(grille_3)
        else :
            print("Mauvais choix, veuillez remettre un choix")
            choix = int(input()) 
    


def menu() :
    print(" ____________________________________ ")
    print("|                                    |")
    print("|  1. Joueur VS Joueur               |")
    print("|                                    |")
    print("|  2. Joueur VS IA Faible            |")
    print("|____________________________________|")
    choix = int(input())
    global type_jeu
    while choix != 1 or choix != 2 :
        if choix == 1 :
            os.system("cls")
            type_jeu = "pvp"
            menu2(type_jeu)
        elif choix == 2 :
            os.system("cls")
            type_jeu = "pve"
            menu2(type_jeu)
        else :
            print("Mauvais choix, veuillez remettre un choix")
            choix = int(input())


menu()
