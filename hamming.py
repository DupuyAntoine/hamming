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
        return matriceH

    def matriceG(self, matriceH):
        """ Génère une matrice G avec une matrice H donnée """
        matriceG = buildIdentite(self.k)
        temp = []
        for elt in matriceH:
            if sum(elt) != 1:
                temp.append(elt)
        transposeTemp = transpose(temp)
        for elt in transposeTemp:
            matriceG.append(elt)
        return matriceG


if __name__ == '__main__':
    hamming = Hamming(3)
    h = hamming.matriceH()
    print(h)
    print('\n')
    g = hamming.matriceG(h)
    print(g)