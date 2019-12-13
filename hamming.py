# coding: utf-8

# Deux fonctions MatriceH et MatriceG qui étant donné l calculant une matrice de parité et génératrice du code de Hamming pour l
# Une fonction Encodage d'une bloc de taille 2^l-l-1
# Une fonction Bruitage qui altère un bit parmi 2^l-1
# Une fonction Décodage qui décode un mot de taille 2^l-1
# Une fonction Hachage qui découpe un bloc quelconque en sous blocs de taille 2^l-l-1
# Bonus : Pour n, k implémenter la fonction qui calcule le nombre max d'erreurs corrigibles qui provient de l'empilement des sphères

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

def matmul(mot, mat):
    """ Multiplie un mot par une matrice """
    tmp = [0] * (len(mat[0]))
    for i in range(len(mot)):
        for j in range(len(mat[0])):
            tmp[j] = (tmp[j] + (mot[i] * mat[i][j])) % 2
    return tmp



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
        return matmul(mot, matGen)



if __name__ == '__main__':
    hamming = Hamming(3)
    h = hamming.matriceH()
    print(h)
    print('\n')
    g = hamming.matriceG(h)
    print(g)
    m = [1, 1, 0, 0]
    md = hamming.encodage(m, g)
    print(md)