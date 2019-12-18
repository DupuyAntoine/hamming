# coding: utf-8

# TP Maths Hamming
# Réalisé par Thomas COLETTE et Antoine DUPUY
# Master 1 ICE (2019-2020)

# Consignes :
# [Réalisé] Deux fonctions MatriceH et MatriceG qui étant donné l calculant une matrice de parité et génératrice du code de Hamming pour l
# [Réalisé] Une fonction Encodage d'une bloc de taille 2^l-l-1
# [Réalisé] Une fonction Bruitage qui altère un bit parmi 2^l-1
# [Réalisé] Une fonction Coorection qui corrige un mot de taille 2^l-1
# [Réalisé] Une fonction Hachage qui découpe un bloc quelconque en sous blocs de taille 2^l-l-1
# Bonus : Pour n, k implémenter la fonction qui calcule le nombre max d'erreurs corrigibles qui provient de l'empilement des sphères

from random import randint

# Fonctions générales

def dec_to_binary(nb, nbBits):
    """ Converti un nombre décimal en binaire """
    binary = []
    binaryString = format(nb, '0' + str(nbBits) + 'b')
    for elt in binaryString:
        binary.append(int(elt))
    return binary

def buildIdentite(nb):
    """ Crée une matrice identité de la taille donnée """
    identite = []
    for i in range(2**nb - 1, 0, -1):
        if (is_power_two(i)):
            identite.append(dec_to_binary(i, nb))
    return identite

def transpose(mat):
    """ Transpose une matrice donnée """
    return [[mat[j][i] for j in range(len(mat))] for i in range(len(mat[0]))] 


def is_power_two(nb):
    """ Vérifie si un nombre est une puissance de 2 """
    return (nb & (nb-1) == 0) and (nb != 0)  

def matmul2D(mot, mat):
    """ Multiplie un mot par une matrice """
    col = []
    for i in range(len(mat)):
        tmp = 0
        for j in range(len(mot)):
            tmp = (tmp + mot[j] * mat[i][j]) % 2
        col.append(tmp)
    return col


class Hamming:

    def __init__(self, l):
        self.n = 2**l - 1
        self.k = 2**l - l - 1


    def matriceH(self):
        """ Génère une matrice H """
        identite = buildIdentite(self.n - self.k)
        matriceH = []
        for i in range(self.n, 0, -1):
            if (is_power_two(i)):
                continue
            else:
                matriceH.append(dec_to_binary(i, self.n - self.k))
        for elt in identite:
            matriceH.append(elt)
        return transpose(matriceH)

    def matriceG(self, matriceH):
        """ Génère une matrice G avec une matrice H donnée """
        matriceG = buildIdentite(self.k)
        temp = []
        for elt in transpose(matriceH):
            if sum(elt) != 1:
                temp.append(elt)
        transposeTemp = transpose(temp)
        for elt in transposeTemp:
            matriceG.append(elt)
        return transpose(matriceG)

    def encodage(self, mot, matGen):
        """ Encode un mot de taille 2^l - l - 1 """
        tmp = [0] * (len(matGen[0]))
        for i in range(len(mot)):
            for j in range(len(matGen[0])):
                tmp[j] = (tmp[j] + (mot[i] * matGen[i][j])) % 2
        return tmp

    def bruitage(self, mot):
        """ Altère un bit au hasard dans un mot """
        index = randint(0, len(mot) - 1)
        bruit = mot[:]
        bruit[index] = (bruit[index] + 1) % 2
        return bruit

    def correction(self, mot, matPar):
        """ Corrige un mot possiblement erroné """
        col = []
        index = 0
        # H * le mot en colonne
        col = matmul2D(mot, matPar)
        matParTrans = transpose(matPar)
        # trouver la position de la colonne de H correspondante à la colonne trouvée
        for i in range(len(matParTrans)):
            if(col == matParTrans[i]):
                index = i
        # changer le bit se trouvant à cet index
        decode = mot[:]
        decode[index] = (decode[index] + 1) % 2
        return decode

    def hachage(self, mot, longueur):
        """ Hache une longue donnée et la transforme en tableau de données décodables """
        hashed = []
        tmp = []
        for i in range(len(mot)):
            if(i % longueur != 0 or i == 0):
                tmp.append(mot[i])
            else:
                hashed.append(tmp)
                tmp = []
                tmp.append(mot[i])
        return hashed        


if __name__ == '__main__':
    #Variables
    l = 3
    m = [1, 1, 0, 0]
    hash = [1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1]


    # Création d'un code de Hamming de taille l = 3
    print("Création d'un code de Hamming de taille l = 3..." + '\n')
    hamming = Hamming(l)

    # Génération de la matrice H
    print("Génération de la matrice H : " + '\n')
    h = hamming.matriceH()
    print(h)

    print('\n')

    # Génération de la matrice G
    print("Génération de la matrice G :" + '\n')
    g = hamming.matriceG(h)
    print(g)

    print('\n')    

    # Encodage d'un mot m = (1100)
    print("Encodage d'un mot m = (1100) :" + '\n')
    md = hamming.encodage(m, g)
    print(md)

    print('\n')

    # Bruitage du mot encodé précédent
    print("Bruitage du mot encodé précédent :" + '\n')
    mb = hamming.bruitage(md)
    print(mb)

    print('\n')

    # Correction du mot bruité précédent
    print("Correction du mot bruité précédent :" + '\n')
    mdd = hamming.correction(mb, h)
    print(mdd)

    print('\n')

    # Hachage de la donnée suivante
    print("Hachage de la donnée suivante :" + '\n')
    print(hash)
    print('\n' + "Résultat : " + '\n')
    hashed = hamming.hachage(hash, hamming.n)
    print(hashed)

    print('\n')

    # Correction de la donnée hachée
    print("Correction de la donnée hachée :" + '\n')
    for i in range(len(hashed)):
        print(hamming.correction(hashed[i], h))